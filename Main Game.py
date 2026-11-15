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
    #produce values
    "bananas": {"name": "Organic Bananas", "price": 1.49, "weight": 1.5, "category": "produce", "code": "1451", "is_produce": True, "fragile": False},

    "avocados": {"name": "Avocados (3ct)", "price": 2.79, "weight" : 1.3, "category": "produce", "code": "1542", "is_produce": True, "fragile": True},

    "apples" : {"name": "Honeycrisp Apples", "price": 3.99, "weight": 1.7, "category": "produce", "code": "1323", "is_produce": True, "fragile": False},

    "onions" : {"name": "Red Onions", "price": 4.50, "weight": 3.2, "category": "produce", "code": "1234", "is_produce": True, "fragile": False},

    "carrots" : {"name": "Carrots", "price": 2.00, "weight": 0.7, "category": "produce", "code": "1765", "is_produce": True, "fragile": False},

    "potatoes" : {"name": "Russet Potatoes", "price": 7.99, "weight": 5.6, "category": "produce", "code": "1466", "is_produce": True, "fragile": False},

    "garlic" : {"name": "Garlic", "price": 4.99, "weight": 1.2, "category": "produce", "code": "1457", "is_produce": True, "fragile": False},

    "brocoli" : {"name": "Garlic", "price": 2.99, "weight": 0.5, "category": "produce", "code": "1858", "is_produce": True, "fragile": False},

    "strawberries" : {"name": "Strawberries", "price": 5.67, "weight": 1.1, "category": "produce", "code": "1469", "is_produce": True, "fragile": True},

    "bellpeppers" : {"name": "Bell Peppers", "price": 9.79, "weight": 1.4, "category": "produce", "code": "1460", "is_produce": True, "fragile": True},

    # dairy + fridge values

    "milk" : {"name": "Organic Milk", "price": 5.99, "weight": 3.3, "category": "dairy", "code": "2341", "": True, "fragile": False},

    "cheddarcheese": {"name": "Cheddar Cheese (pre-shredded)", "weight" : 2.3, "price": 6.79, "category": "dairy", "code": "2992", "is_dairy": True, "fragile": False},

    "goatmilk" : {"name": "Organic Goat Milk", "price": 8.99, "weight": 1.7, "category": "dairy", "code": "2866", "is_dairy": True, "fragile": False},

    "almondmilk": {"name": "Organic Almond Milk", "price": 3.99, "weight": 1.6, "category": "dairy", "code": "2456", "is_dairy": True, "fragile": False},

    "eggs" : {"name": "Egg carton (12 ct)", "price": 12.99, "weight": 6.6, "category": "refrigerated", "code": "2365", "is_dairy": True, "fragile": True },

    "butter" : {"name": "Butter container", "price": 8.79, "weight": 4.5, "category": "dairy", "code": "2785", "is_dairy": True, "fragile": False},

    "greekyogurt" : {"name": "Greek Yogurt Tub", "price": 6.99, "weight": 5.0, "category": "dairy", "code": "2223", "is_dairy": True, "fragile": False},

    "creamcheese" : {"name": "Cream Cheese Brick", "price": 4.95, "weight" : 1.2, "category": "dairy", "code": "2371", "is_dairy": True, "fragile": True},

    "sourcream" : {"name": "Sour Cream Tub", "price": 4.7, "weight": 2.4, "category": "dairy", "code": "2322", "is_dairy": True, "fragile": False},

    "orangejuice" : {"name": "Freshly Squeezed Organic Orange Juice", "price": 7.89, "weight": 5.6, "category": "refrigerated", "code": "2551", "is_dairy": True, "fragile": False},

    "hummus" : {"name": "Organic Sourced Hummus", "price": 8.99, "weight": 5.9, "category" : "refrigerated","code": "2443", "is_dairy": True, "fragile": False},

    #bakery items

    "whitebread" : {"name": "Wonderful White Bread (24ct)", "price": 3.45, "weight": 1.1, "category": "bakery","code": "3423", "is_bakery": True, "fragile": True},

    "croissants" : {"name": "Croissants (6ct)", "price": 4.35, "weight": 0.8, "category": "bakery", "code": "3373", "is_bakery": True, "fragile": True},

    "burgerbuns" : {"name": "Hamburger Buns (10ct)", "price": 5.69, "weight": 0.9, "category": "bakery", "code": "3987", "is_bakery": True, "fragile": True},

    "muffins" : {"name": "Chocolate Chip Muffins (10ct)", "price": 11.99, "weight": 3.6, "category": "bakery", "code": "3221", "is_bakery": True, "fragile": False},

    "tortillas" : {"name": "Flour Tortillas (12ct)", "price": 3.45, "weight": 2.3, "category": "bakery", "code": "3993", "is_bakery": True, "fragile": False},

    "baguette" : {"name": "French Baguettes (3ct)", "price": 4.55, "weight": 4.5, "category": "bakery", "code": " 3421", "is_bakery": True, "fragile": True},

    "bagels" : {"name": "Everything Bagels", "price": 7.99, "weight": 3.4, "category": "bakery", "code": "3219", "is_bakery": True, "fragile": False},

    "sourdough" : {"name": "Sourdough Bread", "price": 5.67, "weight": 1.2, "category": "bakery", "code": "3110", "is_bakery": True, "fragile": False},

    "chocolatechipcookies" : {"name": "Chocolate Chip Cookies", "price": 14.59, "weight": 7.0, "category": "bakery", "code": "3021", "is_bakery": True, "fragile": False},

    "cinnamonbuns" : {"name": "Cinnamon Buns", "price": 6.99,"weight": 4.6, "category": "bakery", "code": "3481", "is_bakery": True, "fragile": False},

    #raw meat / seafood

    "chicken" : {"name": "Chicken Breast", "price": 9.79, "weight": 7.8, "category": "rawmeat", "code": "4499", "is_rawmeat": True, "fragile": False},

    "steak" : {"name": "Ribeye Steak", "price": 47.99, "weight": 11.0, "category": "rawmeat", "code": "4567", "is_rawmeat": True, "fragile": False},

    "shrimp" : {"name": "Tiger Shrimp", "price": 13.99, "weight": 7.8, "category": "rawmeat", "code": "4659", "is_rawmeat": True, "fragile": False},

    "groundbeef": {"name": "(97-3) Lean Ground Beef", "price": 8.99, "weight": 3.4, "category": "rawmeat", "code": "4109", "is_rawmeat": True, "fragile": False},

    "turkey": {"name": "Full Turkey Bird", "price": 52.99, "weight": 23, "category": "rawmeat", "code": "4416", "is_rawmeat": True, "fragile": False },

    "salmon": {"name": "Fresh Alaskan Salmon", "price": 12.99, "weight": 5.6, "category": "rawmeat", "code": "4417", "is_rawmeat": True, "fragile": False },

    "pork": {"name": "Pork Chops", "price": 9.99, "weight": 3.4, "category": "rawmeat", "code": "4198", "is_rawmeat": True, "fragile": False },

    "bacon": {"name": "Thick Cut Bacon", "price": 7.99, "weight": 1.9, "category": "rawmeat", "code": "4561", "is_rawmeat": True, "fragile": False },

    "lobster": {"name": "Fresh Maine Lobster", "price": 43.79, "weight": 3.4, "category": "rawmeat", "code": "4333", "is_rawmeat": True, "fragile": False },

    "crab": {"name": "Crab Legs", "price": 27.99, "weight": 12.0, "category": "rawmeat", "code": "4999", "is_rawmeat": True, "fragile": False },

    # frozen foods

    "icecream": {"name": "Vanilla Ice Cream", "price": 7.89, "weight": 1.2, "category": "frozen", "code": "5412", "is_frozen": True, "fragile": False },

    "frozenpeas" : {"name": "Farm Fresh Frozen Peas", "price": 5.99, "weight": 2.2, "category": "frozen", "code": "5621", "is_frozen": True, "fragile": False },

    "frozencorn" : {"name": "Farm Fresh Frozen Corn", "price": 4.99, "weight": 2.1, "category": "frozen", "code": "5269", "is_frozen": True, "fragile": False },

    "frozenpizza" : {"name": "Frozen Pepperoni Pizza", "price": 7.99, "weight": 1.2, "category": "frozen", "code": "5111", "is_frozen": True, "fragile": False },

    "chickennuggets" : {"name": "Lightly Seasoned and Breaded Chicken Nuggets", "price": 12.99, "weight": 4.5, "category": "frozen" ,"code" : "5848", "is_frozen": True, "fragile": False },

    "frozenberries" : {"name": "Frozen Mixed Berries", "price": 5.99, "weight": 0.9, "category": "frozen", "code": "5673", "is_frozen": True, "fragile": False },

    "waffles": {"name": "Frozen Chocolate Chip Waffles", "price": 8.99, "weight": 1.3, "category": "frozen", "code": "5000", "is_frozen": True, "fragile": False },

    "fries": {"name": "Frozen Crinkle Cut Fries", "price": 12.99, "weight": 2.4, "category": "frozen", "code": "5101", "is_frozen": True, "fragile": False },

    "burritos": {"name": "Frozen Breakfast Burritos", "price": 4.99, "weight": 1.2, "category": "frozen", "code": "5902", "is_frozen": True, "fragile": False },

    "popsicles": {"name": "Red White and Blue Popsicles", "price": 2.79, "weight": 3.1, "category": "frozen", "code": "5491", "is_frozen": True, "fragile": False },






}



