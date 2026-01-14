# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyazzaMarket is a Python implementation of "Piazza Mercato," an Italian Monopoly-like board game from the 1990s. Built with Pygame and pygame_gui, it features a single-computer multiplayer mode with plans for AI players and network capabilities.

**Current Status**: Beta - GUI and rules are in Italian, code comments are in English.

## Setup and Installation

### Dependencies
```bash
pip install -r requirements.txt
```

**Important**: Must use pygame-ce (not pygame). If pygame is installed, uninstall it first before installing pygame-ce and pygame_gui.

### Running the Game
```bash
python main.py              # Normal mode
python main.py --test       # Test mode (manual dice control)
```

## Testing

### Unit Tests
```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest lib/tests/test_game_logic.py

# Run with verbose output
pytest -v
```

### Stress Testing
The project includes a comprehensive stress test system for automated game simulation:

```bash
# Quick tests (recommended for development)
python test_runner.py quick              # 10 games
python test_runner.py quick -j 4         # 10 games, 4 parallel processes

# Medium/intensive tests
python test_runner.py medium             # 50 games
python test_runner.py intensive          # 100 games
python test_runner.py intensive -j 8     # 100 games, 8 parallel

# Test with specific seed (for reproducibility)
python test_runner.py seed 12345

# Adjust performance
python test_runner.py quick --fps 240 --max-turns 1000

# Find errors in previous test runs
python test_runner.py find-errors

# Replay a specific game
python test_runner.py replay stress_test_logs/stress_test_XXXX.json

# Show test statistics
python test_runner.py stats
```

**Stress test logs** are saved to `stress_test_logs/` directory with detailed JSON logs for each game.

## Architecture Overview

### Core Architecture Pattern

PyazzaMarket uses an **event-driven architecture** with a centralized panel queue system:

1. **Centralized Event Management**: All pygame events flow through `Game.manage_events()` which delegates to UI components
2. **Panel Queue System**: Two separate queues (`panels_to_show` and `alert_messages`) manage sequential window display
3. **State Management**: `ActionsStatus` class controls button enable/disable states
4. **Separation of Concerns**: UI components (`lib/uiComponents/`) are separate from game logic (`lib/gameLogic.py`)

### Directory Structure

```
lib/
├── game.py              # Main game class, event loop, panel management
├── gameLogic.py         # Core game logic (turns, penalties, bankruptcy)
├── player.py            # Player class with balance, stocks, debts
├── board.py             # Board construction (40 cells in clockwise order)
├── stock.py             # Stock/property cards (cedole)
├── auction.py           # Auction system
├── event.py             # Random event cards (70+ events)
├── cell.py              # Board cell types
├── constants.py         # Game constants (colors, cell definitions, quotations)
├── menu.py              # Start menu and player setup
├── save_manager.py      # Save/load game state
├── state_manager/
│   └── actions_status.py # Button state management
└── uiComponents/
    ├── gameUI.py        # Main UI (dice, buttons, leaderboard, stockboard)
    ├── eventUI.py       # Event card display panel
    ├── bargainUI.py     # Player negotiation/trading interface
    ├── showStockUI.py   # Multi-purpose stock display panel
    ├── diceOverlayUI.py # Dice rolling overlay (turn order, color events)
    └── auction.py       # Auction UI panel
```

### Key Architecture Concepts

#### 1. Board Construction
- **40 cells** arranged clockwise starting from bottom-right corner
- 4 corners (special cells) + 4 sides of 9 cells each
- Each side follows pattern: 3 stocks (color 1), event, stock, special cell, stock, event, 2 stocks (color 2)
- Built by `Board.__init__()` and `Board.create_side()`

#### 2. Event Asset Loading
Events are loaded **dynamically from filenames** using a structured naming convention:
- `color_{color}_{amount}.png` - Color events (pay/receive based on stocks owned)
- `get_{amount}[_from_{source}].png` - Receive money
- `pay_{amount}[_to_{target}].png` - Pay money
- `go_{position}[_options].png` - Move to position (with optional buy/pass/someone)
- `own_{stock}[_get_{amount}][_each][_others_pay_{amount}].png` - Own-based events
- `gift_{position}_or_get_{amount}.png` - Gift events

**Parsing**: `Event.parse_name()` extracts event type and parameters from filename, enabling easy expansion by adding new PNG files.

#### 3. Panel Queue System
```python
# Two queues for sequential display
self.__alert_messages = []      # Priority: alert messages
self.panels_to_show = []        # Secondary: UI panels
self.current_panel = None       # Currently displayed panel

# Flow: draw_window() → pops from queue → displays panel → user interacts → panel.close_ui() → next panel
```

**Lifecycle**: Create panel → append to queue → `draw_window()` displays → user interaction via `manage_events()` → `close_ui()` → next panel

#### 4. Event Delegation Pattern
```
pygame.event.get()
  ↓
Game.manage_events(event)
  ↓
Check if event matches main UI buttons (dice, buy, pass)
  ↓ (if not matched)
Delegate to current_panel.manage_events(event, players, curr_player)
```

#### 5. Stock/Property System
- Each stock cell creates **2 identical stocks** (cedole)
- Stocks have: base value, current value (modified by quotation), 6-tier penalty array, owner
- **Quotation events** change stock values and trigger auctions (one stock per player)
- **Penalty calculation** depends on how many stocks of same color the owner has

#### 6. Bankruptcy System
When a player cannot pay:
1. Player marked as in debt with creditor (another player, "BANK", or "SQUARE")
2. Debt amount stored in `__debts` list
3. `ShowStockUI` panel shown with "BANKRUPT_STOCK" type
4. Player must sell stocks (to bank at 50% value) or auction them
5. After each stock sale, `is_debt_solved()` checks if debt is cleared
6. If still in debt with no stocks left, player is eliminated via `kill_player()`

#### 7. Turn Flow
```
Click "Lancia Dadi" → turn()
  ↓
Roll dice → move player → check_turn() (accidents)
  ↓
check_crash() (other players on same cell)
  ↓
special_cell_logic() (based on cell type)
  ├─ STOCKS_TYPE → enable buy button + check for penalty
  ├─ EVENTS_TYPE → show EventUI panel
  ├─ QUOTATION_TYPE → update values + trigger auctions
  ├─ CHOOSE_STOCK_TYPE → show stock selection
  ├─ FREE_STOP_TYPE → buy available stock + enable bargain
  ├─ CHANCE_TYPE → dice overlay for money win/loss
  └─ Others...
  ↓
Check if in debt → ShowStockUI (BANKRUPT_STOCK)
  ↓
Click "Passa Turno" → next player
```

### Important Implementation Details

#### Stock Penalty Calculation
Penalty array has 6 elements:
1. 1 stock of same color
2. 2 stocks of same company (same logo)
3. 3 stocks of same color
4. 4 stocks of same color
5. 5 stocks of same color
6. 6 stocks of same color

When quotation changes stock value, penalties are recalculated proportionally: `(penalty / original_value) * new_value`

#### Multiple Auctions
When QUOTATION cell is triggered:
1. All players with stocks choose one to auction
2. All auctions added to `__auctions` queue
3. `start_first_auction()` processes queue one by one
4. Each auction ends with `open_next_if_present()` to continue or finish

#### Test Mode
When running with `--test` flag:
- Press 0-9 to set dice values
- Press ENTER to roll
- Press SPACE to reset
- Useful for testing specific game scenarios

## Code Style and Patterns

### Common Patterns

**1. Money Transfers**
```python
# Always use change_balance(), never modify __balance directly
player.change_balance(amount)   # Positive to receive, negative to pay
```

**2. Stock Transfers**
```python
# Use transfer_stock() from gameLogic
from lib.gameLogic import transfer_stock
transfer_stock(board, new_owner, stock, enable_buy_button)
```

**3. Adding New Panels**
```python
# Step 1: Create panel class in lib/uiComponents/
# Step 2: Add to queue in game logic
self.panels_to_show.append(MyNewPanel(...))
self.disable_actions()  # Disable main UI while panel is open
# Step 3: Panel handles events via manage_events()
# Step 4: Panel calls close_ui() and game.renable_actions()
```

**4. Updating UI After Changes**
```python
# After modifying player balances/stocks
self.__gameUI.updateAllPlayerLables(self.get_players())

# After stock changes
Player.last_stock_update = time.time()
# update_graphic() will refresh stockboard automatically
```

### Naming Conventions
- **Italian terms** in UI and game rules: "cedole" (stocks), "scudi" (currency), "piazza" (square)
- **English** in code comments and variable names
- Private methods/attributes use double underscore: `__private_method()`
- UI components typically have `draw()`, `manage_events()`, and `close_ui()` methods

## Important Files Reference

### Key Configuration Files
- [lib/constants.py](lib/constants.py) - All game constants including `CELLS_DEF` (cell definitions), `QUOTATION` (stock value changes), colors, dimensions
- [lib/event.py](lib/event.py) - Event parsing logic (`parse_name()` method)
- [state_manager/actions_status.py](state_manager/actions_status.py) - Button state management

### Core Game Logic
- [lib/game.py](lib/game.py) - Main game class, see `manage_events()` at line 273 and `turn()` for turn flow
- [lib/gameLogic.py](lib/gameLogic.py) - Shared game logic functions: `check_for_penalty()`, `buy_stock_from_cell()`, `transfer_stock()`, `quotation_logic()`, bankruptcy resolution
- [lib/board.py](lib/board.py) - Board construction starting at `__init__()`

### Documentation
- [ARCHITETTURA_GIOCO.md](ARCHITETTURA_GIOCO.md) - Comprehensive Italian architecture documentation with detailed diagrams and examples (2000+ lines)
- [README.md](README.md) - Game overview and rules with images
- [INSTALL.md](INSTALL.md) - Installation instructions

## Testing Best Practices

1. **Before committing**: Run `pytest` to ensure all unit tests pass
2. **After major changes**: Run `python test_runner.py quick` (10 automated games) to catch edge cases
3. **For debugging**: Use `python test_runner.py seed <specific_seed>` to reproduce specific game scenarios
4. **Finding regressions**: Use `python test_runner.py find-errors` after running intensive tests
5. **Performance testing**: Use `--fps 240` and `-j` (parallel processes) flags for faster test execution

## Common Development Tasks

### Adding a New Event Type
1. Create PNG file with appropriate naming pattern in `assets/events/`
2. Update `Event.parse_name()` if new pattern is needed
3. Add event handling logic in `Game.events_logic()` method
4. Test with stress test system

### Adding a New Cell Type
1. Add constant in [lib/constants.py](lib/constants.py)
2. Update `Board.create_side()` or corner creation in `Board.__init__()`
3. Add case in `Game.special_cell_logic()`
4. Test turn flow with new cell type

### Modifying UI Components
1. UI components are in [lib/uiComponents/](lib/uiComponents/)
2. Always disable main actions when panel is shown: `game.disable_actions()`
3. Re-enable when closing: `game.renable_actions()`
4. Update player labels after any balance/stock changes

### Debugging Game State
1. Use test mode: `python main.py --test`
2. Check stress test logs in `stress_test_logs/` directory
3. Replay specific games: `python test_runner.py replay <log_file>`
4. Use `--analyze-only` flag for quick log inspection without GUI
