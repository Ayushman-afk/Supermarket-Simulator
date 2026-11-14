import time
import random

#- Pregame defined variables. (total - 115) (80 items of produce) (25 coupons)

save_file_name = "SuperSimSave.txt"
shift_num = 1
bank_balance = 0.00
upgrades = []
total_customers_served = 0
total_mistakes = 0
best_shift_time = 999.9
alltime_tips_earned = 0.00

# difficulty values/ Scaling
# shift 1 = 3 customers per shift 4 minimum items in cart, 6 max in cart, 1 coupon per customer rand event chance = 0.10 (10%)
# shift 2 = 4, 4, 7, 1, 0.15 (15%)
#shift 3 = 4, 5, 8, 2, 0.20 (20%)
#shift 4 = 5, 6, 9, 2, 0.25 (25%)
#shift 5+ = 6, 7, 11, 3, 0.30 (30%)

hazard_categories = ["chemical", "raw_meat"]
fresh_categories = ["produce", "bakery"]
cold_categories = ["frozen", "dairy"]
standard_max_bag_weight = 15 #(lbs)
upgraded_max_bag_weight = 22 #(lbs) only works when the upgrade is bought
heavy_item_limit = 4.0 #(lbs) items above this weight crush items (fragile = True)
max_bags_per_order = 6
frozen_bonus = 1.5 #($1.50 tip per bag with 2+ frozen category item)
upgraded_frozen_bonus = 3.0 #($3 tip bonus when insulated bag upgrade is bought

#shift grades
# S rank = 0 mistakes time per shift <= 60.0 seconds +10$ tip bonus
# A rank = 0 mistakes time per shift > 60.0 seconds +5$ tip bonus
# B rank = 1-2 mistakes anytime  +2$ tip bonus
# C rank = 3-4 mistakes anytime +0$ tip bonus
# F rank = 5 or more mistakes anytime -5.0$ tip bonus (max at 0.00)

base_shift_tip = 15.00
mistake_deduction = 2.50 #(per mistake)
plu_time_penalty = 5 # (seconds)
express_time_belt_reduction = 15.0 #(Seconds subtracted from total shift time when "express belt" upgrade is unlocked)

bill_denominations = [1,5,10,20,50,100]
keep_change_limit = 0.25 #( if this much change is owed or is under this customer lets the cashier keep it)
store_name = "Super Mart"
store_tagline = "Quality groceries at an affordable price!"
recipt_width = 36 #(characters wide)
main_menu = {"1.": "Start Shift", "2.": "Upgrade Shop", "3.": "PlU Master Key", "4.": "Career Stats", "5.": "Reset Save", "6.": "Quit"}
valid_scan_commands = ["book"]
valid_coupon_commands = ["accept", "reject"]
valid_bag_commands = ["new", "inspect"]

store_items = {
    "bananas": {"name": "Organic Bananas", "price": 1.49, "weight": 1.5, "category": "produce", "code": "1001", "is_produce": True, "fragile": False},

    "avocados": {"name": "Avocados (3ct)", "price": 2.79, "weight" : 1.3, "category": "produce", "code": "1002", "is_produce": True, "fragile": True},

    "apples" : {"name": "Honeycrisp Apples", "price": 3.99, "weight": 1.7, "category": "produce", "code": "1003", "is_produce": True, "fragile": False},

    "onions" : {"name": "Red Onions", "price": 4.50, "weight": 3.2, "category": "produce", "code": "1004", "is_produce": True, "fragile": False},

    "carrots" : {"name": "Carrots", "price": 2.00, "weight": 0.7, "category": "produce", "code": "1005", "is_produce": True, "fragile": False},

    "potatoes" : {"name": "Russet Potatoes", "price": 7.99, "weight": 5.6, "category": "produce", "code": "1006", "is_produce": True, "fragile": False},

    "garlic" : {"name": "Garlic", "price": 4.99, "weight": 1.2, "category": "produce", "code": "1007", "is_produce": True, "fragile": False},

    "brocoli" : {"name": "Garlic", "price": 2.99, "weight": 0.5, "category": "produce", "code": "1008", "is_produce": True, "fragile": False},

    
}



