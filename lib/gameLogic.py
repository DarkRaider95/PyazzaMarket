import random
from .constants import *

actual_stock_price = [200,280,360,440,500,600,700,800]

def roll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return (dice1, dice2)

def is_double(dice):
    return dice[0] == dice[1]

def gain_and_loss(new_stock_price):
    diff = []
    for i in new_stock_price:
        diff.append(new_stock_price[i] - actual_stock_price[i])
    return diff

def update_stock_price(new_stock_price):
    for i in new_stock_price:
        actual_stock_price[i] = new_stock_price[i]

def updated_penality(old_penality, old_stock_price, new_stock_price):
    return (old_penality // (old_stock_price * new_stock_price))

def buyStock(cells, player):
    curr_pos = player.position
    stock_value = cells[curr_pos].stocks[0].stock_value
    if(len(cells[curr_pos].stocks) > 0):
        if player.balance >= stock_value:
            stock = cells[curr_pos].stocks.pop()
            player.changeBalance(-stock_value)
            player.addStock(stock)
    
    return cells

def checkForPenalty(cells, players, player_number): # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.position]
    players.pop(player_number) # we drop the current player in order to not check him self in the for loops
    own_by_the_player = False # then we check if the player own the stock
    for stock in current_player.getStocks():
        if cell.position == stock.position:
            own_by_the_player = True
    if not own_by_the_player: # if it is not owned by the player we check if it is owned by another player
        for player in players:
            for stock in player.getStocks():
                if cell.position == stock.position:
                    penality = player.computePenalty(stock)
                    current_player.changeBalance(-penality)
                    player.changeBalance(penality)
                    break # we break in order to pay only once the fee if the player have more than one card in the same cell

def checkCrash(players, player_number): # since current_player is the one that have done the last move it will be the one that will pay for the crash
    current_player = players[player_number]
    players.pop(player_number)
    for player in players:
        if player.position == current_player.position:
            current_player.changeBalance(-CRASH_FEE)
            player.changeBalance(CRASH_FEE)

def checkTurn(player):
    if player.old_position > player.position:
        player.changeBalance(TURN_FEE)

def stockPrizeLogic(player):
    player.changeBalance(len(player.getStocks()) * 100)

def quotationLogic(player):
    pass

def chanceLogic(player, squareBalance):
    score = roll()
    if (score[0] + score[1]) > 3:
        amount = squareBalance//3
        player.changeBalance(amount)        
    else:
        amount = -squareBalance//2
        player.changeBalance(amount)

    return score, amount

def sixHundredLogic(player):
    player.changeBalance(600)

def startLogic(player):
    player.changeBalance(TURN_FEE * 2)

def everyOneFifty(players):
    for player in players:
        player.changeBalance(50)

def whoOwnsStock(players, stockPos):
    for player in players:
        for stock in player.getStocks():
            if stockPos == stock.position:
                return player
            
def getMoneyFromOthers(players, player_number, amount): # since current_player is the one that have done the last move it will be the one that will pay for the crash
    current_player = players[player_number]
    players.pop(player_number)
    
    for player in players:
        player.changeBalance(-amount)
    
    current_player.changeBalance(len(players) * amount)

def checkStartPass(player, destination):
    if player.position <= 39 and destination > 0:
        return True
    else:
        return False
    
def computePassAmount(players, player_number, passAmount, destination):
    current_player = players[player_number]
    players.pop(player_number)

    totPassAmount = 0

    for player in players:
        if (            
            (
                current_player.position < player.position and 
                destination > current_player.position and 
                destination > player.position
            ) 
            or 
            (
                current_player.position < player.position and 
                destination < current_player.position and 
                destination < player.position
            )
        ):
            totPassAmount += passAmount

    return totPassAmount