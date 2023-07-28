import random
from .constants import *

def roll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return (dice1, dice2)

def is_double(dice):
    return dice[0] == dice[1]

def buy_stock(cells, player):
    curr_pos = player.position
    stock_value = cells[curr_pos].get_stocks()[0].get_stock_value()
    if(len(cells[curr_pos].get_stocks()) > 0):
        if player.get_balance() >= stock_value:
            stock = cells[curr_pos].sellStock()
            player.change_balance(-stock_value)
            player.addStock(stock)

def check_if_can_buy_stock(cell, player):
        if(cell.cellType != STOCKS_TYPE or len(cell.get_stocks())  == 0):
            return False
        else:
            if player.get_balance() >= cell.get_stocks()[0].get_stock_value():
                return True
            else:
                return False

def check_for_penalty(cells, players, player_number): # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.position]
    players = players.copy() # we copy the list in order to not modify the original one
    players.pop(player_number) # we drop the current player in order to not check him self in the for loops
    own_by_the_player = False # then we check if the player own the stock
    for stock in current_player.get_stocks():
        if cell.position == stock.position:
            own_by_the_player = True
    if not own_by_the_player: # if it is not owned by the player we check if it is owned by another player
        for player in players:
            for stock in player.get_stocks():
                if cell.position == stock.position:
                    penality = player.computePenalty(stock)
                    current_player.change_balance(-penality)
                    player.change_balance(penality)
                    break # we break in order to pay only once the fee if the player have more than one card in the same cell

def check_crash(players, player_number): # since current_player is the one that have done the last move it will be the one that will pay for the crash
    current_player = players[player_number]
    players = players.copy() # we copy the list in order to not modify the original one
    players.pop(player_number)
    crash = 0
    for player in players:
        if player.position == current_player.position:
            current_player.change_balance(-CRASH_FEE)
            player.change_balance(CRASH_FEE)
            crash = 1
    return crash

def check_turn(player):
    if player.old_position > player.position:
        player.change_balance(TURN_FEE)

def stock_prize_logic(player):
    player.change_balance(len(player.get_stocks()) * 100)

def quotation_logic(players, board, quotation, game):
    new_quotation = quotation[0]
    for player in players:
        for stock in player.get_stocks():
            difference = stock.updateValue(new_quotation[stock.get_index()])
            player.change_balance(difference)
            game.set_square_balance(difference)
    for cell in board.get_cells():
        if cell.get_stocks() is not None:                                                                          
            cell.updateCellValue(new_quotation[cell.get_index()])
            for stock in cell.get_stocks():
                _ = stock.updateValue(new_quotation[stock.get_index()])
                
    quotation.rotate(-1)

def chanceLogic(player, squareBalance):
    score = roll()
    if (score[0] + score[1]) > 3:
        amount = squareBalance//3
        player.change_balance(amount)        
    else:
        amount = -squareBalance//2
        player.change_balance(amount)

    return score, amount

def sixHundredLogic(player):
    player.change_balance(600)

def startLogic(player):
    player.change_balance(TURN_FEE * 2)

def everyOneFifty(players):
    for player in players:
        player.change_balance(50)

def whoOwnsStock(players, stockPos):
    owners = []
    for player in players:
        for stock in player.get_stocks():
            if stockPos == stock.position:
                owners.append(player)
    
    return owners

def whoOwnsStockByName(players, stockName):
    owners = []
    for player in players:
        for stock in player.get_stocks():
            if stockName == stock.name:
                owners.append(player)
    
    return owners

def transferStock(board, current_player, chosenStock):

    if chosenStock.owner is not None:
        chosenStock.owner.removeStock(chosenStock)    
    else:
        board.removeStock(chosenStock)
        
    chosenStock.owner = current_player
    current_player.addStock(chosenStock)

            
def getMoneyFromOthers(players, player_number, amount):
    current_player = players[player_number]
    players.pop(player_number)
    
    for player in players:
        player.change_balance(-amount)
    
    current_player.change_balance(len(players) * amount)

def checkStartPass(player, destination):
    if player.position <= 39 and destination > 0:
        return True
    else:
        return False
    
def computePassAmount(players, curr_player_pos, player_number, passAmount, destination):
    players.pop(player_number)

    totPassAmount = 0

    for player in players:
        if (            
            (
                curr_player_pos < player.position and
                destination > player.position
            ) 
            or 
            (
                destination < curr_player_pos and 
                (
                    curr_player_pos < player.position or
                    player.position < destination
                )
            )
        ):
            totPassAmount += passAmount

    return totPassAmount

def payMoneyToOthers(players, player_number, amount):
    current_player = players[player_number]
    players.pop(player_number)
    
    for player in players:
        player.change_balance(+amount)
    
    current_player.change_balance(len(players) * (-amount))

#this method is executed when an event with own some stock occurs
def update_owner_balance(owner, stockName, amount, each):
    for stock in owner.get_stocks():
        if stock.name == stockName:
            owner.change_balance(amount)
            if each == False:
                break

#this method is executed when an event with own some stock occurs
#there is an event where the ones that aren't owners pay some money
def update_others_balance(players, owners, amount):
    for player in players:
        if player not in owners:
            player.change_balance(-amount)