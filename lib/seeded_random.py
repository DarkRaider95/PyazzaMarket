"""
Sistema di randomizzazione seeded per garantire riproducibilità.
Permette di rigiocare esattamente la stessa partita usando lo stesso seed.
"""

import random
from typing import Tuple, List, Any
from collections import deque


class SeededRandom:
    """Generatore di numeri casuali con seed per riproducibilità."""

    def __init__(self, seed: int = None):
        """
        Inizializza il generatore con un seed.

        Args:
            seed: Seed per il generatore. Se None, usa il timestamp corrente.
        """
        if seed is None:
            import time
            seed = int(time.time() * 1000) % (2**32)

        self.seed = seed
        self.rng = random.Random(seed)
        self.roll_count = 0
        self.shuffle_count = 0

    def get_seed(self) -> int:
        """Ritorna il seed corrente."""
        return self.seed

    def roll_dice(self) -> Tuple[int, int]:
        """
        Simula il lancio di due dadi a 6 facce.

        Returns:
            Tupla con i valori dei due dadi
        """
        self.roll_count += 1
        dice1 = self.rng.randint(1, 6)
        dice2 = self.rng.randint(1, 6)
        return (dice1, dice2)

    def shuffle_list(self, items: List[Any]) -> List[Any]:
        """
        Mescola una lista in maniera deterministica.

        Args:
            items: Lista da mescolare

        Returns:
            Lista mescolata (copia dell'originale)
        """
        self.shuffle_count += 1
        shuffled = items.copy()
        self.rng.shuffle(shuffled)
        return shuffled

    def shuffle_deque(self, items: deque) -> deque:
        """
        Mescola una deque in maniera deterministica.

        Args:
            items: Deque da mescolare

        Returns:
            Nuova deque mescolata
        """
        self.shuffle_count += 1
        temp_list = list(items)
        self.rng.shuffle(temp_list)
        return deque(temp_list)

    def choice(self, items: List[Any]) -> Any:
        """
        Sceglie un elemento casuale da una lista.

        Args:
            items: Lista da cui scegliere

        Returns:
            Elemento scelto casualmente
        """
        return self.rng.choice(items)

    def randint(self, a: int, b: int) -> int:
        """
        Genera un intero casuale tra a e b (inclusi).

        Args:
            a: Minimo
            b: Massimo

        Returns:
            Intero casuale
        """
        return self.rng.randint(a, b)

    def get_stats(self) -> dict:
        """Ritorna statistiche sull'uso del generatore."""
        return {
            "seed": self.seed,
            "roll_count": self.roll_count,
            "shuffle_count": self.shuffle_count
        }


class DiceController:
    """Controller per gestire i lanci di dadi in modo controllato."""

    def __init__(self, seeded_random: SeededRandom = None, recorded_rolls: List[Tuple[int, int]] = None):
        """
        Inizializza il controller dei dadi.

        Args:
            seeded_random: Generatore seeded per nuovi lanci
            recorded_rolls: Lista di lanci pre-registrati da usare in sequenza (per replay)
        """
        self.seeded_random = seeded_random or SeededRandom()
        self.recorded_rolls = recorded_rolls or []
        self.replay_mode = len(self.recorded_rolls) > 0
        self.current_roll_index = 0
        self.all_rolls = []

    def roll(self) -> Tuple[int, int]:
        """
        Esegue un lancio di dadi.

        Returns:
            Tupla con i valori dei due dadi
        """
        if self.replay_mode and self.current_roll_index < len(self.recorded_rolls):
            # Modalità replay: usa lanci registrati
            roll = self.recorded_rolls[self.current_roll_index]
            self.current_roll_index += 1
        else:
            # Modalità normale: genera nuovo lancio
            roll = self.seeded_random.roll_dice()

        self.all_rolls.append(roll)
        return roll

    def get_all_rolls(self) -> List[Tuple[int, int]]:
        """Ritorna tutti i lanci effettuati."""
        return self.all_rolls.copy()

    def is_replay_finished(self) -> bool:
        """Verifica se il replay è finito."""
        if not self.replay_mode:
            return False
        return self.current_roll_index >= len(self.recorded_rolls)

    def get_stats(self) -> dict:
        """Ritorna statistiche sui lanci."""
        doubles = sum(1 for roll in self.all_rolls if roll[0] == roll[1])
        return {
            "total_rolls": len(self.all_rolls),
            "doubles": doubles,
            "doubles_percentage": (doubles / len(self.all_rolls) * 100) if self.all_rolls else 0,
            "replay_mode": self.replay_mode,
            "current_roll_index": self.current_roll_index
        }


class EventController:
    """Controller per gestire gli eventi in modo controllato."""

    def __init__(self, seeded_random: SeededRandom = None):
        """
        Inizializza il controller degli eventi.

        Args:
            seeded_random: Generatore seeded per shuffling
        """
        self.seeded_random = seeded_random or SeededRandom()
        self.shuffle_history = []

    def shuffle_events(self, events: deque) -> deque:
        """
        Mescola gli eventi in maniera deterministica.

        Args:
            events: Deque di eventi da mescolare

        Returns:
            Nuova deque con eventi mescolati
        """
        shuffled = self.seeded_random.shuffle_deque(events)
        # Non salviamo la storia perché gli eventi non hanno un title
        self.shuffle_history.append({
            "shuffle_count": len(shuffled)
        })
        return shuffled

    def get_shuffle_history(self) -> List[dict]:
        """Ritorna la storia degli shuffle effettuati."""
        return self.shuffle_history.copy()
