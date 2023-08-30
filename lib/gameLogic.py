import random
from .constants import *


def roll(test=False, dice=(0, 0)):
    if test:
        dice1 = dice[0]
        dice2 = dice[1]
    else:
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)

    return (dice1, dice2)


def is_double(dice):
    return dice[0] == dice[1]


def buy_stock_from_cell(cells, player):
    curr_pos = player.get_position()
    stock_value = cells[curr_pos].get_stocks()[0].get_stock_value()
    if len(cells[curr_pos].get_stocks()) > 0:
        if player.get_balance() >= stock_value:
            stock = cells[curr_pos].sell_stock()
            stock.set_owner(player)
            player.change_balance(-stock_value)
            player.add_stock(stock)

def check_if_can_buy_stock(cell, player):
    if cell.cellType != STOCKS_TYPE or len(cell.get_stocks()) == 0:
        return False
    else:
        if player.get_balance() >= cell.get_stocks()[0].get_stock_value():
            return True
        else:
            return False


def check_for_penalty(cells, players, player_number):  # testare per vedere se riconosce quando le celle sono uguali
    current_player = players[player_number]
    cell = cells[current_player.get_position()]
    players = players.copy()  # we copy the list in order to not modify the original one
    players.pop(player_number)  # we drop the current player in order to not check him self in the for loops
    own_by_the_player = False  # then we check if the player own the stock
    for stock in current_player.get_stocks():
        if cell.position == stock.get_position():
            own_by_the_player = True
    if not own_by_the_player:  # if it is not owned by the player we check if it is owned by another player
        for player in players:
            for stock in player.get_stocks():
                if cell.position == stock.get_position():
                    penality = player.compute_penalty(stock)
                    #if current_player doesn't have enough money he will be put in debt
                    if current_player.get_balance() < penality:
                        current_player.set_in_debt_with(player)
                        current_player.add_debt(penality)
                    else:                        
                        current_player.change_balance(-penality)
                        player.change_balance(penality)
                    break  # we break in order to pay only once the fee if the player have more than one card in the same cell

#function to solve the debt
def solve_bankrupt(debtor, game):
    
    for creditor, debt in zip(debtor.get_in_debt_with(), debtor.get_debts()):

        if creditor == "BANK":
            debtor.change_balance(-debt)
        elif creditor == "SQUARE":
            debtor.change_balance(-debt)
            game.set_square_balance(debt)
        else:
            debtor.change_balance(-debt)
            creditor.change_balance(debt)
    
    debtor.erase_debts()

#function to sort the debts and solve the larger ones if possible
def solve_larger_debts(debtor, game):
    # Zip the two lists together
    zipped_lists = zip(debtor.get_in_debt_with(), debtor.get_debts())

    # Sort the zipped list using the debts
    sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[1], reverse=True)

    #with this for we solve all the possible debts starting from the biggest one
    #if it can't solve some of them it tries to solve the smaller ones
    for creditor, debt in sorted_zipped_lists:
        if debtor.get_balance() > debt:
            if creditor == "BANK":
                debtor.change_balance(-debt)
            elif creditor == "SQUARE":
                debtor.change_balance(-debt)
                game.set_square_balance(debt)
            else:
                debtor.change_balance(-debt)
                creditor.change_balance(debt)
            
            debt = 0

    #after an entire cycle if there is still balance it gives the rest of the money to the bigger debt
    remaining_balance = debtor.get_balance()
    if remaining_balance > 0:
        for creditor, debt in sorted_zipped_lists:
            if debt > 0 and debt > remaining_balance:
                if creditor == "BANK":
                    debtor.change_balance(-remaining_balance)
                elif creditor == "SQUARE":
                    debtor.change_balance(-remaining_balance)
                    game.set_square_balance(remaining_balance)
                else:
                    debtor.change_balance(-remaining_balance)
                    creditor.change_balance(remaining_balance)
                break   #after giving the remaining balance it makes no sense to keep looping

def check_crash(
    players, player_number
):  # since current_player is the one that have done the last move it will be the one that will pay for the crash
    current_player = players[player_number]
    players = players.copy()  # we copy the list in order to not modify the original one
    players.pop(player_number)
    crash = 0
    for player in players:
        if player.get_position() == current_player.get_position():
            #if current_player doesn't have enough money he will be put in debt
            if current_player.get_balance() < CRASH_FEE:
                current_player.set_in_debt_with(player)
                current_player.add_debt(CRASH_FEE)
            else:                        
                current_player.change_balance(-CRASH_FEE)
                player.change_balance(CRASH_FEE)
            crash = 1
    return crash


def check_turn(player):
    if player.get_old_position() > player.get_position():
        player.change_balance(TURN_FEE)


def stock_prize_logic(player):
    player.change_balance(len(player.get_stocks()) * 100)


def quotation_logic(players, board, quotation, game):
    new_quotation = quotation[0]
    for player in players:
        for stock in player.get_stocks():
            difference = stock.update_value(new_quotation[stock.get_index()])

            #handling bankrupt saving debts if the difference is negative and the player doesn't have enough money
            #he is in bankrupt
            if difference < 0 and player.get_balance() < -difference: 
                player.set_in_debt_with("SQUARE")
                player.add_debt(-difference)
            else:
                player.change_balance(difference)
                game.set_square_balance(difference)
    for cell in board.get_cells():
        if cell.get_stocks() is not None:
            cell.updateCellValue(new_quotation[cell.get_index()])
            for stock in cell.get_stocks():
                _ = stock.update_value(new_quotation[stock.get_index()])

    quotation.rotate(-1)


def chance_logic(player, squareBalance):
    score = roll()
    if score[0] > 3:
        amount = squareBalance // 3
        player.change_balance(amount)
    else:
        amount = -squareBalance // 2
        if player.get_balance() < -amount:
            player.set_in_debt_with("SQUARE")
            player.add_debt(-amount)
        else:
            player.change_balance(amount)

    return score, amount


def six_hundred_logic(player):
    player.change_balance(600)


def start_logic(player):
    player.change_balance(TURN_FEE * 2)


def every_one_fifty(players):
    for player in players:
        player.change_balance(50)


def who_owns_stock(players, stock_pos):
    owners = []
    for player in players:
        for stock in player.get_stocks():
            if stock_pos == stock.get_position():
                owners.append(player)

    return owners


def who_owns_stock_by_name(players, stock_name):
    owners = []
    for player in players:
        for stock in player.get_stocks():
            if stock_name == stock.get_name():
                owners.append(player)

    return owners


def transfer_stock(board, current_player, chosen_stock, withMoney = False):
    if chosen_stock.get_owner() is not None:
        chosen_stock.get_owner().remove_stock(chosen_stock)
        if withMoney:
            stockValue = chosen_stock.get_new_value()
            chosen_stock.get_owner().change_balance(stockValue)
            current_player.change_balance(-stockValue)
    else:
        board.remove_stock(chosen_stock)
        if withMoney:
            stockValue = chosen_stock.get_new_value()
            current_player.change_balance(-stockValue)         

    chosen_stock.set_owner(current_player)
    current_player.add_stock(chosen_stock)

def sell_stock_to_bank(board, chosen_stock):
    if chosen_stock.get_owner() is not None:
        chosen_stock.get_owner().remove_stock(chosen_stock)
        chosen_stock.get_owner().change_balance(chosen_stock.get_new_value())
        cell = board.get_cell(chosen_stock.get_position())
        cell.add_stock(chosen_stock)
        chosen_stock.set_owner(None)

def get_money_from_others(players, player_number, amount):
    current_player = players[player_number]
    players = players.copy()
    players.pop(player_number)

    players_not_in_debt = len(players)
    for player in players:
        if player.get_balance() < amount:
            player.set_in_debt_with(current_player)
            player.add_debt(amount)
            players_not_in_debt -= 1
        else:
            player.change_balance(-amount)

    current_player.change_balance(players_not_in_debt * amount)


def check_start_pass(player, destination):
    if player.get_position() > destination:
        return True
    else:
        return False


def compute_pass_amount(players, player_number, passAmount, destination):
    players = players.copy()
    curr_player_pos = players[player_number].get_position()
    players.pop(player_number)

    totPassAmount = 0

    for player in players:
        if (curr_player_pos < player.get_position() and destination > player.get_position()) or (
            destination < curr_player_pos
            and (curr_player_pos < player.get_position() or player.get_position() < destination)
        ):
            totPassAmount += passAmount

    return totPassAmount


def pay_money_to_others(players, player_number, amount):
    current_player = players[player_number]
    players = players.copy()
    players.pop(player_number)

    for player in players:
        if current_player.get_balance() < amount:
            current_player.set_in_debt_with(player)
            current_player.add_debt(amount)
        else:
            player.change_balance(amount)
            current_player.change_balance(-amount)

# this method is executed when an event with own some stock occurs
def update_owner_balance(owner, stock_name, amount, each):
    for stock in owner.get_stocks():
        if stock.get_name() == stock_name:
            owner.change_balance(amount)
            if each == False:
                break


# this method is executed when an event with own some stock occurs
# there is an event where the ones that aren't owners pay some money
# to the bank
def update_others_balance(players, owners, amount):
    for player in players:
        if player not in owners:
            if player.get_balance() < amount:
                player.set_in_debt_with("BANK")
                player.add_debt(amount)
            else:
                player.change_balance(-amount)

# transfer stock from player1 to player2 with amount of money
def transfer_stock_between_players(player1, player2, amount, stock):
    player1.change_balance(amount)
    player2.change_balance(-amount)
    player1.remove_stock(stock)
    player2.add_stock(stock)
    stock.set_owner(player2)

def finished_auction_logic(board, auction):
    winner =  auction.get_winner() 
    owner = auction.get_owner()
    stock = auction.get_stock()

    if auction.get_winner() is not None:
        winner_bid = auction.get_winner_bid()
        transfer_stock_between_players(owner, winner, winner_bid, stock)
    else:
        sell_stock_to_bank(board, stock)