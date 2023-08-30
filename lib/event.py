import os
from .constants import *
import pygame

class Event:    
    def __init__(self, image, eventType, effectData):
        self.image = image
        self.evenType = eventType
        self.effectData = effectData
        self.surface = pygame.Surface((EVENT_WIDTH, EVENT_HEIGHT))
    
    def draw(self):
        self.surface.blit(self.image, (0, 0))

    @staticmethod
    def initialize_events():
        events = []
        # Get the list of all files in the events directory
        files = os.listdir(EVENTS_DIR)

        # create events
        for fileName in files:
            filePath = EVENTS_DIR+fileName
            image = pygame.image.load(filePath)
            image = pygame.transform.scale(image, (EVENT_WIDTH, EVENT_HEIGHT))
            eventType, effectData = Event.parse_name(fileName)
            events.append(Event(image, eventType, effectData))

        return events
    
    @staticmethod
    def parse_name(eventName):
        eventName = eventName[:-4]
        actionsAndValues = eventName.split('_')
        eventType = None
        effectData = None

        if 'color' in actionsAndValues:
            eventType = COLOR_EVENT
            effectData = {'amount':int(actionsAndValues[2])}
        elif eventName == 'buy_what_you_want':
            eventType = BUY_ANTHING_EVENT            
        elif eventName == 'stop_1':
            eventType = STOP_1            
        elif eventName == 'free_penalty':
            eventType = FREE_PENALTY                                    
        elif eventName == 'free_penalty_martini':
            eventType = FREE_PENALTY_MARTINI
        elif eventName == 'every_50_per_point': # add dice lunch
            eventType = EVERYONE_FIFTY_EVENT
        elif eventName == 'player-1_go_39_get_penalty':
            eventType = PREVIOUS_PLAYER_GALUP
        elif eventName == 'player+1_pay_200':
            eventType = NEXT_PLAYER_PAY
        elif 'gift' in actionsAndValues:            
            get_index = actionsAndValues.index('get')
            value = actionsAndValues[get_index+1]
            eventType = GIFT_EVENT
            effectData = {'stockIndex':int(actionsAndValues[1]), 'amount':int(value)}
        elif actionsAndValues[0] == 'get':
            
            getObject = None
            if 'from' in actionsAndValues:
                fromIndex = actionsAndValues.index('from')
                fromValue = actionsAndValues[fromIndex+1]
                getObject = {'amount':int(actionsAndValues[1]), 'from':fromValue}
            else:
                getObject = {'amount':int(actionsAndValues[1])}

            eventType = GET_EVENT
            effectData = getObject
        elif actionsAndValues[0] == 'go':            
            goValue = int(actionsAndValues[1])
            startCheck = False
            someone = False
            buy = False
            getValue = None
            passValue = None

            if 'get' in actionsAndValues:
                get_index = actionsAndValues.index('get')
                getValue = int(actionsAndValues[get_index+1])

            if 'pass' in actionsAndValues:
                passIndex = actionsAndValues.index('pass')
                passValue = int(actionsAndValues[passIndex+1])

            if 'ifstart' in actionsAndValues:
                startCheck = True

            if 'someone' in actionsAndValues:
                someone = True

            if 'buy' in actionsAndValues:
                buy = True

            eventType = GO_EVENT
            effectData = {'destination':goValue, 'get':getValue, 'pass':passValue, 'startCheck':startCheck, 'someone': someone, 'buy': buy}
        elif actionsAndValues[0] == 'pay':
            payObject = None
            if 'to' in actionsAndValues:
                toIndex = actionsAndValues.index('to')
                toValue = actionsAndValues[toIndex+1]
                payObject = {'amount':int(actionsAndValues[1]), 'to':toValue}
            else:
                payObject = {'amount':int(actionsAndValues[1])}
            
            eventType = PAY_EVENT
            effectData = payObject
        elif actionsAndValues[0] == 'own':
            name = actionsAndValues[1]
            each = False
            payValue = None
            getValue = None

            if 'get' in actionsAndValues:
                get_index = actionsAndValues.index('get')
                getValue = int(actionsAndValues[get_index+1])

            if 'each' in actionsAndValues:
                each = True

            if 'others' in actionsAndValues:
                payIndex = actionsAndValues.index('pay')
                payValue = int(actionsAndValues[payIndex+1])
            
            eventType = OWN_EVENT
            effectData = {'stockName':name, 'getAmount':getValue, 'each': each, 'othersPayValue':payValue}
        elif actionsAndValues[0] == 'buy':
            negotiate = False
            
            if 'negotiate' in actionsAndValues:
                negotiate = True
            
            eventType = BUY_EVENT
            effectData = {'stockIndex':int(actionsAndValues[1]), 'negotiate':negotiate}
        
        return eventType, effectData