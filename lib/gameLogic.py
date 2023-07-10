import random

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

def enableBuyButton(cells, player, ui, board):
    curr_pos = player.position
    if(board.checkIfStockCell(player) or len(cells[curr_pos].stocks)  == 0):
        ui.buyButton.disable()
    else:
        if player.balance >= cells[curr_pos].stocks[0].stock_value:
            ui.buyButton.enable()
        else:
            ui.buyButton.disable()

def checkForPenality(cells, players, player_number): # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.position]
    own_by_the_player = False
    if cell in current_player.stocks:
        own_by_the_player = True
    if not own_by_the_player:
        for player in players:
            if player != current_player:
                if cell in player.stocks:
                    print("penality")
                    penality = cell.penality
                    current_player.changeBalance(-penality)
                    player.changeBalance(penality)