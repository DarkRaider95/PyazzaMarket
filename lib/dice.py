import random

actual_stock_price = [200,280,360,440,500,600,700,800]

def roll():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return [dice1, dice2]

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
