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

def checkForPenality(cells, players, player_number, ui): # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.position]
    if cell.cellImage == None: # first we check if it is a stock cell or not
        own_by_the_player = False # then we check if the player own the stock
        for stock in current_player.stocks:
            if cell.position == stock.position:
                own_by_the_player = True
        if not own_by_the_player: # if it is not owned by the player we check if it is owned by another player
            for player in players:
                if player != current_player:
                    for stock in player.stocks:
                        if cell.position == stock.position:
                            penality = player.computePenality(stock)
                            current_player.changeBalance(-penality)
                            player.changeBalance(penality)
                            ui.updateLabel(current_player)
                            ui.updateLabel(player)
                            break # we break in order to pay only once the fee if the player have more than one card in the same cell