import os
from .constants import *
import pygame

class Event:    
    def __init__(self, image, effect):
        self.image = image
        self.effect = effect
    
    def initialize_events():
        events = []
        # Get the list of all files in the current directory
        files = os.listdir(EVENTS_DIR)

        # Print the list of files
        for fileName in files:
            filePath = EVENTS_DIR+fileName
            image = pygame.image.load(filePath)
            image = pygame.transform.scale(image, (DICE_WIDTH, DICE_HEIGHT))
            effect = Event.parse_name(fileName)
            events.append(Event(image, effect))

        return events
            
    def parse_name(eventName):
        eventName = eventName[:-4]
        actionsAndValues = eventName.split('_')        
        effect = None

        if 'color' in actionsAndValues:
            effect = Effect(COLOR_EVENT, {'amount':int(actionsAndValues[2])})
        elif eventName == 'buy_what_you_want':
            effect = Effect(BUY_ANTHING_EVENT, None)
        elif eventName == 'stop_1':
            effect = Effect(STOP_1, None)
        elif eventName == 'free_penalty':
            effect = Effect(FREE_PENALTY, None)
        elif eventName == 'free_penalty_martini':
            effect = Effect(FREE_PENALTY_MARTINI, None)
        elif eventName == 'every_50_per_point':
            effect = Effect(EVERYONE_FIFTY_EVENT, None)
        elif eventName == 'player-1_go_39_get_penalty':
            effect = Effect(PREVIOUS_PLAYER_GALUP, None)
        elif eventName == 'player+1_pay_200':
            effect = Effect(NEXT_PLAYER_PAY, None)
        elif 'gift' in actionsAndValues:
            getIndex = actionsAndValues.index('get')
            value = actionsAndValues[getIndex+1]
            effect = Effect(GIFT_EVENT, {'stockIndex':int(actionsAndValues[1]), 'amount':int(value)})
        elif actionsAndValues[0] == 'get':
            getObject = None
            if 'from' in actionsAndValues:
                fromIndex = actionsAndValues.index('from')
                fromValue = actionsAndValues[fromIndex+1]
                getObject = {'amount':int(actionsAndValues[1]), 'from':fromValue}
            else:
                getObject = {'amount':int(actionsAndValues[1])}
            effect = Effect(GET_EVENT, getObject)
        elif actionsAndValues[0] == 'go':            
            goValue = int(actionsAndValues[1])
            startCheck = False
            someone = False
            buy = False
            getValue = None
            passValue = None

            if 'get' in actionsAndValues:
                getIndex = actionsAndValues.index('get')
                getValue = int(actionsAndValues[getIndex+1])

            if 'pass' in actionsAndValues:
                passIndex = actionsAndValues.index('pass')
                passValue = int(actionsAndValues[passIndex+1])

            if 'ifstart' in actionsAndValues:
                startCheck = True

            if 'someone' in actionsAndValues:
                someone = True

            if 'buy' in actionsAndValues:
                buy = True

            effect = Effect(GO_EVENT, {'destination':goValue, 'get':getValue, 'pass':passValue, 'startCheck':startCheck, 'someone': someone, 'buy': buy})
        elif actionsAndValues[0] == 'pay':
            payObject = None
            if 'to' in actionsAndValues:
                toIndex = actionsAndValues.index('to')
                toValue = actionsAndValues[toIndex+1]
                payObject = {'amount':int(actionsAndValues[1]), 'from':toValue}
            else:
                payObject = {'amount':int(actionsAndValues[1])}
            effect = Effect(PAY_EVENT, payObject)            
        elif actionsAndValues[0] == 'own':
            name = actionsAndValues[1]
            each = False
            payValue = None
            
            if 'get' in actionsAndValues:
                getIndex = actionsAndValues.index('get')
                getValue = int(actionsAndValues[getIndex+1])

            if 'each' in actionsAndValues:
                each = True

            if 'others' in actionsAndValues:
                payIndex = actionsAndValues.index('pay')
                payValue = int(actionsAndValues[payIndex+1])
            
            effect = Effect(OWN_EVENT, {'stockName':name, 'getAmount':getValue, 'each': each, 'othersPayValue':payValue})
        elif actionsAndValues[0] == 'buy':
            negotiate = False
            
            if 'negotiate' in actionsAndValues:
                negotiate = True
            
            effect = Effect(BUY_EVENT, {'stockIndex':int(actionsAndValues[1]), 'negotiate':negotiate})
        
        return effect

class Effect:
    def __init__(self, type, effectData):
        self.type = type
        self.data = effectData
