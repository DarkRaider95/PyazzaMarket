import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from lib.constants import *
import time

# Inizializzazione della finestra di gioco
pygame.display.set_caption("Menu di Gioco")

class GameUI:
    def __init__(
        self, screen, clock, actions_status
    ):  # each player initialised with its data
        self.screen = screen
        self.running = True  # Used to shutdown the game
        self.clock = clock
        # Create something similar to pygame.display.set_mode((WIDTH, HEIGHT))
        self.manager = UIManager((WIDTH, HEIGHT))
        self.playerLabels = []
        self.stockboardLabels = []
        self.actions = []
        self.image_dice_1 = pygame.image.load(DICE_1)
        self.image_dice_1 = pygame.transform.scale(
            self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT)
        )
        self.image_dice_2 = pygame.image.load(DICE_1)
        self.image_dice_2 = pygame.transform.scale(
            self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT)
        )
        # this is used when we update the dice overlay image to know if the
        # overlay have one or two dices
        self.twoDices = True
        self.__actions_status = actions_status

    def draw_actions_ui(self):
        panel_rect = pygame.Rect(
            (30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT)
        )
        actions_UI = UIPanel(panel_rect, manager=self.manager)
        # actionLabel = self.font.render(str('AZIONI'), True, BLACK)
        label_rect = pygame.Rect(
            (ACTIONS_WIDTH // 2 - LABEL_WIDTH // 2, 10), (LABEL_WIDTH, LABEL_HEIGHT)
        )
        UILabel(label_rect, "AZIONI", manager=self.manager, container=actions_UI)
        # self.actions_UI.blit(actionLabel, (ACTIONS_WIDTH // 2 - actionLabel.get_width() // 2, 10))
        self.launchDice = UIButton(
            relative_rect=pygame.Rect(
                ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT
            ),
            text="Lancia i dadi",
            container=actions_UI,
            object_id="LAUNCH_DICE",
            manager=self.manager,
        )

        self.buyButton = UIButton(
            relative_rect=pygame.Rect(
                ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT
            ),
            text="Compra",
            container=actions_UI,
            object_id="BUY",
            manager=self.manager,
        )

        self.showStocks = UIButton(
            relative_rect=pygame.Rect(
                ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT
            ),
            text="Mostra Cedole",
            container=actions_UI,
            object_id="SHOW_STOCKS",
            manager=self.manager,
        )

        self.passButton = UIButton(
            relative_rect=pygame.Rect(
                ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT
            ),
            text="Passa il turno",
            container=actions_UI,
            object_id="PASS",
            manager=self.manager,
        )

        self.buyButton.disable()
        self.passButton.disable()
        self.showStocks.disable()

        self.actions = [
            self.launchDice,
            self.buyButton,
            self.showStocks,
            self.passButton,
        ]

    def draw_leaderboard(self, players, squareBalance, currentPlayer):
        # DRAWING THE BOARD
        position_x = LEADERBOARD_WIDTH // 2 - LEADERBOARD_LABEL_WIDTH // 2
        label_dimension = (LEADERBOARD_LABEL_WIDTH, LABEL_HEIGHT)
        panel_rect = pygame.Rect(
            (30, 30), (LEADERBOARD_WIDTH, LEADERBOARD_HEIGHT)
        )  # x, y, width, height
        leaderboard = UIPanel(panel_rect, manager=self.manager)
        # ADDING THE TITLE LABEL
        title_rect = pygame.Rect((position_x, 10), label_dimension)
        UILabel(title_rect, "LEADERBOARD", manager=self.manager, container=leaderboard)
        # ADDING WHO IS THE TURN
        turn_rect = pygame.Rect((position_x, 30), label_dimension)
        self.turnName = UILabel(
            turn_rect,
            "Turno di " + currentPlayer.get_name(),
            manager=self.manager,
            container=leaderboard
        )
        # ADDING SQUARE BALANCE LABEL
        balance_rect = pygame.Rect((position_x, 50), label_dimension)
        self.squareBalanceLabel = UILabel(
            balance_rect,
            "Riserva di piazza : " + str(squareBalance),
            manager=self.manager,
            container=leaderboard,
        )
        # Head of players table
        player_label_rect = pygame.Rect((position_x, 70), label_dimension)
        UILabel(
            player_label_rect,
            "Giocatore: Scudi | Azioni ",
            manager=self.manager,
            container=leaderboard,
        )
        # ADDING THE PLAYERS LABELS
        for i, player in enumerate(
            players
        ):  # considerare di fare una lable unica e andare a capo per ogni riga
            player_label_rect = pygame.Rect(
                (position_x, 70 + (20 * (i + 1))), label_dimension
            )
            label = UILabel(
                player_label_rect,
                player.get_name()
                + " : "
                + str(player.get_balance())
                + " | "
                + str(player.stock_value()),
                manager=self.manager,
                container=leaderboard,
            )
            self.playerLabels.append(label)

    def updateSquareBalanceLabel(self, squareBalance):
        self.squareBalanceLabel.set_text("Riserva di piazza : " + str(squareBalance))

    def updateTurnLabel(self, currentPlayer):
        self.turnName.set_text("Turno di " + currentPlayer.get_name())

    def draw_stockboard(self, players):
        # DRAWING THE BOARD
        label_dimension = (150, LABEL_HEIGHT)
        sorted_players = sorted(
            players, key=lambda x: len(x.get_stocks()), reverse=True
        )
        max_stock = max(len(sorted_players[0].get_stocks()), 1)
        num_columns = min(3, len(sorted_players))
        self.drawRowStockboard(
            0, num_columns, sorted_players, 20, 0, label_dimension, True
        )
        if len(sorted_players) > 3:
            self.drawRowStockboard(
                3,
                len(sorted_players),
                sorted_players,
                60,
                max_stock,
                label_dimension,
                False,
            )
        self.latestStockUpdate = time.time()
        # since we update the lastestStockUpdate we will not update twice the
        # stockboard if someone sold a stock to another player

    def drawRowStockboard(
        self,
        start_range,
        end_range,
        sorted_player,
        offset,
        max_stock,
        label_dimension,
        first_row,
    ):
        for i in range(start_range, end_range):
            player = sorted_player[i]
            if first_row:
                position_x = (
                    WIDTH
                    + 25
                    - CORNER_WIDTH
                    - (CELL_WIDTH * 9)
                    + (STOCKBOARD_WIDTH * i)
                )
            else:
                position_x = (
                    WIDTH
                    + 25
                    - CORNER_WIDTH
                    - (CELL_WIDTH * 9)
                    + (STOCKBOARD_WIDTH * (i - 3))
                )
            # ADDING THE TITLE LABEL
            title_rect = pygame.Rect(
                (position_x, offset + CELL_HEIGHT + (max_stock * 20)), (label_dimension)
            )
            nameLabel = UILabel(title_rect, player.get_name(), manager=self.manager)
            self.stockboardLabels.append(nameLabel)
            if len(player.get_stocks()) == 0:
                player_label_rect = pygame.Rect(
                    (position_x, offset + 20 + CELL_HEIGHT + (max_stock * 20)),
                    label_dimension,
                )
                noStockLabel = UILabel(
                    player_label_rect, "No stock", manager=self.manager
                )
                self.stockboardLabels.append(noStockLabel)
            else:
                count_label = 0
                # setted to -1 because the first stock will always be different
                latest_stock_position = -1
                for (
                    stock
                ) in (
                    player.get_stocks()
                ):  # considerare di fare una lable unica e andare a capo per ogni riga
                    position_y = (
                        offset
                        + 20
                        + CELL_HEIGHT
                        + (20 * count_label)
                        + (max_stock * 20)
                    )
                    if latest_stock_position == stock.get_position():
                        self.stockboardLabels[-1].set_text(stock.get_name() + " 2x")
                    else:
                        player_label_rect = pygame.Rect(
                            (position_x, position_y), label_dimension
                        )
                        stockNameLabel = UILabel(
                            player_label_rect, stock.get_name(), manager=self.manager
                        )
                        count_label += 1
                        latest_stock_position = stock.get_position()
                        self.stockboardLabels.append(stockNameLabel)

    def updateStockboard(self, players, last_stock_update, dice):
        # add a class variable for and update of the stock board as a or on the
        # if cicle
        if last_stock_update > self.latestStockUpdate:
            for label in self.stockboardLabels:
                label.kill()
            self.screen.fill(BLACK)
            dice.draw_dices()
            self.stockboardLabels = []
            self.draw_stockboard(players)

    def updateAllPlayerLables(self, players):
        sorted_players = sorted(
            players, key=lambda x: x.get_balance() + x.stock_value(), reverse=True
        )
        for i, player in enumerate(sorted_players):
            self.playerLabels[i].set_text(
                player.get_name()
                + " : "
                + str(player.get_balance())
                + " | "
                + str(player.stock_value())
            )

    def renable_actions(self):
        """This function get the action status from the status manager and enable or disable the actions accordingly"""
        actions_status = self.__actions_status.get_actions_status()

        for index, action in enumerate(self.actions):
            if actions_status[index]:
                action.enable()
            else:
                action.disable()

    def showEventUi(self, event):
        self.showedEvent = event
        self.drawEventUi()

    def drawEventUi(self):
        panel_rect = pygame.Rect(
            (WIDTH // 2 - EVENT_UI_WIDTH // 2, 20), (EVENT_UI_WIDTH, EVENT_UI_HEIGHT)
        )
        self.eventUi = UIPanel(panel_rect, starting_height=2, manager=self.manager)

        title_rect = pygame.Rect(
            (EVENT_UI_WIDTH // 2 - EVENT_UI_TITLE_WIDTH // 2, 10),
            (EVENT_UI_TITLE_WIDTH, EVENT_UI_TITLE_HEIGHT),
        )
        UILabel(title_rect, "EVENTI", manager=self.manager, container=self.eventUi)

        eventRect = pygame.Rect(
            (
                EVENT_UI_WIDTH - 30 - EVENT_UI_BUT_WIDTH,
                EVENT_UI_HEIGHT // 2 - EVENT_UI_BUT_HEIGHT // 2,
            ),
            (EVENT_UI_BUT_WIDTH, EVENT_UI_BUT_WIDTH),
        )

        self.eventBut = UIButton(
            relative_rect=eventRect,
            text="OK",
            container=self.eventUi,
            object_id="EVENT_OK",
            manager=self.manager,
        )

        eventImageRect = pygame.Rect(
            (EVENT_UI_WIDTH // 2 - EVENT_WIDTH // 2, 60), (EVENT_WIDTH, EVENT_HEIGHT)
        )

        self.showedEvent.draw()
        self.eventImage = UIImage(
            eventImageRect,
            self.showedEvent.surface,
            container=self.eventUi,
            manager=self.manager,
        )

    def closeEventUi(self):
        self.eventUi.kill()

    def drawAlert(self, message):
        surface = pygame.Rect(
            ((WIDTH - ALERT_WIDTH) // 2, (HEIGHT - ALERT_HEIGHT) // 2),
            (ALERT_WIDTH, ALERT_HEIGHT),
        )
        self.alertUi = UIPanel(surface, starting_height=2, manager=self.manager)

        message_rect = pygame.Rect(
            (
                (ALERT_WIDTH - ALERT_MESSAGE_WIDTH) // 2,
                (ALERT_HEIGHT - ALERT_MESSAGE_HEIGHT - 20) // 2,
            ),
            (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT),
        )
        UILabel(message_rect, message, manager=self.manager, container=self.alertUi)

        close_rect = pygame.Rect(
            (
                (ALERT_WIDTH - ALERT_BUT_WIDTH) // 2,
                ALERT_HEIGHT - ALERT_BUT_HEIGHT - 10,
            ),
            (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT),
        )
        self.closeAlertBut = UIButton(
            relative_rect=close_rect,
            text="chiudi",
            container=self.alertUi,
            object_id="CLOSE_ALERT",
            manager=self.manager,
        )

        self.__actions_status.disable_actions()

    def closeAlert(self, players, dice):
        # since screen.fill(BLACK) is already on updateStockboard and
        # dice.draw also we directly call that function
        self.alertUi.kill()
        self.updateStockboard(players, time.time(), dice)
        self.__actions_status.renable_actions()

    def drawDiceOverlay(self, message, title, twoDices=True):
        surface = pygame.Rect(
            ((WIDTH - DICE_OVERLAY_WIDTH) // 2, (HEIGHT - DICE_OVERLAY_HEIGHT) // 2),
            (DICE_OVERLAY_WIDTH, DICE_OVERLAY_HEIGHT),
        )
        self.diceOverlay = UIPanel(surface, starting_height=2, manager=self.manager)

        title_rect = pygame.Rect(
            ((DICE_OVERLAY_WIDTH - ALERT_MESSAGE_WIDTH) // 2, 10),
            (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT),
        )
        UILabel(title_rect, title, manager=self.manager, container=self.diceOverlay)

        message_rect = pygame.Rect(
            ((DICE_OVERLAY_WIDTH - ALERT_MESSAGE_WIDTH) // 2, 30),
            (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT),
        )
        UILabel(message_rect, message, manager=self.manager, container=self.diceOverlay)

        close_rect = pygame.Rect(
            (
                DICE_OVERLAY_WIDTH - ALERT_BUT_WIDTH - 20,
                DICE_OVERLAY_HEIGHT - ALERT_BUT_HEIGHT - 10,
            ),
            (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT),
        )

        if twoDices:
            imgRect = pygame.Rect(
                (DICE_OVERLAY_WIDTH // 2 - DICE_WIDTH, 65),
                (DICE_WIDTH * 2, DICE_HEIGHT),
            )
            diceSurface = self.createDiceSurface(twoDices)
            self.diceOverlayImg = UIImage(
                imgRect, diceSurface, manager=self.manager, container=self.diceOverlay
            )

            self.closeDiceOverlayBut = UIButton(
                relative_rect=close_rect,
                text="Chiudi",
                container=self.diceOverlay,
                object_id="CLOSE_DICE_OVERLAY",
                manager=self.manager,
            )
            self.closeDiceOverlayBut.disable()
        else:
            imgRect = pygame.Rect(
                ((DICE_OVERLAY_WIDTH - DICE_WIDTH) // 2, 65), (DICE_WIDTH, DICE_HEIGHT)
            )
            diceSurface = self.createDiceSurface(twoDices)
            self.diceOverlayImg = UIImage(
                imgRect, diceSurface, manager=self.manager, container=self.diceOverlay
            )
            self.close_die_overlay_but = UIButton(
                relative_rect=close_rect,
                text="Chiudi",
                container=self.diceOverlay,
                object_id="CLOSE_DICE_OVERLAY",
                manager=self.manager,
            )
            self.close_die_overlay_but.disable()


        self.__actions_status.disable_actions()

        throw_rect = pygame.Rect(
            (20, DICE_OVERLAY_HEIGHT - ALERT_BUT_HEIGHT - 10),
            (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT),
        )
        self.launchOverlayDiceBut = UIButton(
            relative_rect=throw_rect,
            text="Lancia",
            container=self.diceOverlay,
            object_id="CLOSE_DICE_OVERLAY",
            manager=self.manager,
        )

        self.twoDices = twoDices

    def createDiceSurface(self, twoDices=True):
        if twoDices:  # guardare se si può aggiornare solo la superficie con blit
            diceSurface = pygame.Surface((DICE_WIDTH * 2, DICE_HEIGHT))
            diceSurface.blit(self.image_dice_1, (0, 0))
            diceSurface.blit(self.image_dice_2, (0 + DICE_WIDTH, 0))
        else:
            diceSurface = pygame.Surface((DICE_WIDTH, DICE_HEIGHT))
            diceSurface.blit(self.image_dice_1, (0, 0))
        return diceSurface

    def updateDiceOverlay(self, score):
        self.update_dice(score)
        self.diceOverlayImg.set_image(self.createDiceSurface(self.twoDices))
        self.launchOverlayDiceBut.disable()
        if hasattr(self, "close_die_overlay_but"):
            self.close_die_overlay_but.enable()
        if hasattr(self, "closeDiceOverlayBut"):
            self.closeDiceOverlayBut.enable()

    def closeDiceOverlay(self, players, dice):
        # since screen.fill(BLACK) is already on updateStockboard and
        # dice.draw also we directly call that function
        self.diceOverlay.kill()
        self.updateStockboard(players, time.time(), dice)
        self.__actions_status.renable_actions()

    def draw_dices(self):
        surface = self.createDiceSurface()
        self.screen.blit(surface, (DICE_SURFACE_X, DICE_SURFACE_Y))

    def update_dice(self, score):  # score is a tuple from roll in gameLogic
        scoreToImage = [
            {"score": 1, "image": DICE_1},
            {"score": 2, "image": DICE_2},
            {"score": 3, "image": DICE_3},
            {"score": 4, "image": DICE_4},
            {"score": 5, "image": DICE_5},
            {"score": 6, "image": DICE_6},
        ]
        for scoreImage in scoreToImage:
            if scoreImage["score"] == score[0]:
                self.image_dice_1 = pygame.image.load(scoreImage["image"])
                self.image_dice_1 = pygame.transform.scale(
                    self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT)
                )
            if scoreImage["score"] == score[1]:
                self.image_dice_2 = pygame.image.load(scoreImage["image"])
                self.image_dice_2 = pygame.transform.scale(
                    self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT)
                )

        self.draw_dices()

    def get_screen(self):
        return self.screen

    def get_manager(self):
        return self.manager
