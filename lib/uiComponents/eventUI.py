import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from lib.constants import *

class EventUI:

    def __init__(self, event, manager):
        self.showed_event = event
        self.manager = manager

    def draw(self):
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

        self.showed_event.draw()
        self.eventImage = UIImage(
            eventImageRect,
            self.showed_event.surface,
            container=self.eventUi,
            manager=self.manager,
        )

    def close_ui(self):
        self.eventUi.kill()
