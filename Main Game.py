import time
import random

#- Pregame defined variables. (total - 149) (80 items of produce) (25 coupons) (20 Customers) (8 register events) (6 upgrades)

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

hazard_categories = ["chemical", "raw_meat", "rawmeat", "household"]
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

    "broccoli" : {"name": "Broccoli", "price": 2.99, "weight": 0.5, "category": "produce", "code": "1858", "is_produce": True, "fragile": False},

    "strawberries" : {"name": "Strawberries", "price": 5.67, "weight": 1.1, "category": "produce", "code": "1469", "is_produce": True, "fragile": True},

    "bellpeppers" : {"name": "Bell Peppers", "price": 9.79, "weight": 1.4, "category": "produce", "code": "1460", "is_produce": True, "fragile": True},

    "mango" : {"name": "Organic Mangoes", "price":  8.79, "weight": 3.0, "category": "produce", "code": "1231", "is_produce": True, "fragile": False},

    "plums": {"name": "Black Plums", "price": 7.79, "weight": 4.5, "category": "produce", "code": "1253", "is_produce": True, "fragile": False},

    "lettuce": {"name": "Romaine Lettuce", "price": 4.59, "weight": 1.2, "category": "produce", "code": "1000", "is_produce": True, "fragile": True},

    "limes": {"name": "Key Limes", "price": 2.99, "weight": 1.2, "category": "produce", "code": "1423", "is_produce": True, "fragile": False} ,

    "raspberries": {"name": "Red raspberries", "price": 3.49, "weight": 0.9,"category": "produce", "code": "1111", "is_produce": True, "fragile": False},

    "lemons": {"name": "Lemons (bag)", "price": 3.49, "weight": 1.2,"category": "produce", "code": "1200", "is_produce": True, "fragile": False},

    "cucumbers": {"name": "English Cucumbers", "price": 1.79, "weight": 0.7, "category": "produce", "code": "1345", "is_produce": True, "fragile": True},

    "zucchini": {"name": "Green Zucchini", "price": 2.29, "weight": 0.2, "category": "produce", "code": "1001", "is_produce": True, "fragile": True},

    "spinach": {"name": "Baby Spinach", "price": 3.99, "category": "produce", "code": "1111", "is_produce": True, "fragile": True},


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

    "baguette" : {"name": "French Baguettes (3ct)", "price": 4.55, "weight": 4.5, "category": "bakery", "code": "3421", "is_bakery": True, "fragile": True},

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

    #canned items

    "peanutbutter": {"name": "Organic Peanut Butter", "price": 4.99, "weight": 1.1, "category": "canned", "code": "6111", "is_canned": True, "fragile": False },

    "soup": {"name": "Tomato Soup (6ct)", "price":6.99, "weight": 1.2, "category": "canned", "code": "6732", "is_canned": True, "fragile": False },

    "pasta": {"name": "Pasta", "price": 8.99, "weight": 1.2, "category": "canned", "code": "6000", "is_canned": True, "fragile": False },

    "marinara" : {"name": "Herby Marinara Sauce", "price": 7.99, "weight": 3.4, "category": "canned", "code": "6465", "is_canned": True, "fragile": False },

    "oliveoil": {"name": "Organic Olive Oil", "price": 19.99, "weight": 7.0, "category": "canned", "code": "6666", "is_canned": True, "fragile": True },

    "rice": {"name": "White Rice", "price": 4.99, "weight": 3.0, "category": "canned", "code": "6001", "is_canned": True, "fragile": False },

    "blackbeans": {"name": "Mexican Style Black Beans", "price": 5.79, "weight": 2.0, "category": "canned", "code": "6200", "is_canned": True, "fragile": False },

    "flour" : {"name": "Whole Wheat Flour", "price": 23.99, "weight": 4.6, "category": "canned", "code": "6232", "is_canned": True, "fragile": False },

    "coffee": {"name": "Dark Roast Coffee", "price": 7.89, "weight": 2.3, "category": "canned", "code": "6772", "is_canned": True, "fragile": False },

    "cereal": {"name": "Honey Oat Cereal", "price": 12.99, "weight": 1.2, "category": "canned", "code": "6121", "is_canned": True, "fragile": False },

    #Snacks

    "chips": {"name": "Potato Chips", "price": 5.89, "weight": 0.7, "category": "snack", "code": "7100", "is_snack": True, "fragile": True },

    "sodapack": {"name": "Soda Pack (12ct)", "price": 12.79, "weight": 7.9, "category": "snack", "code": "7001", "is_snack": True, "fragile": False },

    "salsa" : {"name": "Mexican Medium Salsa", "price": 4.59, "weight": 1.2, "category": "canned", "code": "7821", "is_snack": True, "fragile": False },

    "energydrink" : {"name": "Energy Drink", "price": 1.99, "weight": 0.5, "category": "canned", "code": "7122", "is_snack": True, "fragile": False },

    "trailmix" : {"name": "Assorted Trail Mix", "price": 3.29, "weight": 0.3, "category":"canned", "code":"7899", "is_snack": True, "fragile": False },

    "chocolate" : {"name": "Dark Chocolate", "price": 1.29, "weight": 0.1, "category": "canned", "code": "7991", "is_snack": True },

    "tortillachips": {"name": "Tortilla Chips", "price": 5.79, "weight": 0.3, "category": "canned", "code": "7182", "is_snack": True, "fragile": False },

    "granola": {"name": "Mixed Granola", "price": 3.99, "weight": 0.9, "category": "canned", "code": "7000", "is_snack": True, "fragile": False },

    "proteinshake" : {"name": "Chocolate Protein Shake", "price": 2.29, "weight": 0.3, "category": "snack", "code": "7110", "is_snack": True, "fragile": False },

    "crackers" : {"name": "Honey Crackers", "price": 4.59, "weight": 1.1, "category": "snack", "code": "7129", "is_snack": True, "fragile": False },

    #household chemicals/items

    "bleach" : {"name": "Bleach", "price": 6.89, "weight": 1.4, "category": "household", "code": "8201", "is_house": True, "fragile": False },

    "disinfectant" : {"name": "Household Disinfectant", "price": 11.85, "weight": 0.3, "category": "household", "code": "8100", "is_house": True, "fragile": False },

    "wipes" : {"name": "Lemon Lime Wipes", "price": 14.59, "weight": 0.8, "category": "household", "code": "8110", "is_house": True, "fragile": False },

    "hydroperoxide" : {"name": "Household Hydroperoxide", "price": 14.29, "weight": 1.0, "category": "household", "code": "8001", "is_house": True, "fragile": False },

    "tissues" : {"name": "Kitchen Tissues", "price": 10.19, "weight": 0.9, "category": "household", "code": "8017", "is_house": True, "fragile": False },

    "toiletpaper" : {"name": "2-ply Toilet Paper", "price": 9.89, "weight": 1.0, "category": "household", "code": "8921", "is_house": True, "fragile": False },

    "floorcleaner" : {"name": "Flower Floor Cleaner", "price": 7.90, "weight": 1.2, "category": "household", "code": "8012", "is_house": True, "fragile": False },

    "cleaningspray" : {"name": "Lime Clean Spray", "price": 12.95, "weight": 1.9, "category": "household", "code": "8000", "is_house": True, "fragile": False },

    "laundrydetergent" : {"name": "Laundry Detergent", "price": 8.90, "weight": 3.1, "category": "household", "code": "8123", "is_house": True, "fragile": False },

    "water" : {"name": "Spring Water", "price": 4.19, "weight": 6.8, "category": "household", "code": "8233", "is_house": True, "fragile": False },

}


coupons = [
    {"text": "Save $1.00 on Organic Milk (Expires Shift 5)", "item": "milk", "discount": 1.00, "min_qty": 1, "max_shift": 5},

    {"text": "Save $0.75 on Honeycrisp Apples (Expires Shift 7)", "item": "apples", "discount": 0.75, "min_qty": 1, "max_shift": 7},

    {"text": "Save $1.50 on Spring Water (Expires Shift 5)", "item": "water", "discount": 1.50, "min_qty": 1, "max_shift": 5},

    {"text": "Save $3.50 On 2-ply Toilet Paper (Expires Shift 14)", "item": "toiletpaper", "discount": 3.50, "min_qty": 1, "max_shift": 14},

    {"text": "Save $1.00 on Flower Floor Cleaner (Expires Shift 11)", "item": "floorcleaner", "discount": 1.00, "min_qty": 2, "max_shift": 11},

    {"text": "Save $9.50 on Steak (Expires Shift 8)", "item": "steak", "discount": 9.50, "min_qty": 3, "max_shift": 8},

    {"text": "Save $1.25 on Laundry Detergent (Expires Shift 0)","item": "laundrydetergent", "discount": 1.25, "min_qty": 1, "max_shift": 0},

    {"text": "Save $1.00 on Chicken Breast (Expires Shift 9)", "item": "chicken", "discount": 1.00, "min_qty": 1, "max_shift": 9},

    {"text": "Save $1.50 on Tiger Shrimp (Expires Shift 0)", "item": "shrimp", "discount": 1.5, "min_qty": 1, "max_shift": 0},

    {"text": "Save $2.30 on Whole Wheat Flour (Expires Shift 1)", "item": "flour", "discount": 2.30, "min_qty": 1, "max_shift": 1},

    {"text": "Save $2.90 on Tortilla Chips (Expires Shift 10)", "item": "tortillachips", "discount": 2.90, "min_qty": 1, "max_shift": 10},

    {"text": "Save $5.00 on Herby Marinara Sauce (Expires Shift 3)", "item": "marinara", "discount": 5.00, "min_qty": 1, "max_shift": 3},

    {"text": "Save $3.40 on Lemon Lime Wipes (Expires Shift 2)", "item": "cleaningwipes", "discount": 3.40, "min_qty": 1, "max_shift": 2},

    {"text": "Save $ 0.50 on Avocados (Expires Shift 1)", "item": "avocados", "discount": 0.50, "min_qty": 1, "max_shift": 1},

    {"text": "Save $1.50 on Mexican Style Black Beans (Expires Shift 16)", "item": "blackbeans", "discount": 1.50, "min_qty": 1, "max_shift": 16},

    {"text": "Save $2.99 on Thick Cut Bacon (Expires Shift 12)", "item": "blackbeans", "discount": 2.99, "min_qty": 1, "max_shift": 12},

    {"text": "Save $10.00 on Chocolate Chip Cookies (Expires Shift 9)", "item": "chocolatechipcookies", "discount": 10.00, "min_qty": 1, "max_shift": 9},

    {"text": "Save $12.99 on Fresh Maine Lobster (Expires Shift 12)", "item": "lobster", "discount": 12.99, "min_qty": 1, "max_shift": 12},

    {"text": "Save $2.50 on Bleach (Expires Shift 1)","item": "bleach","discount":2.50, "min_qty": 1, "max_shift": 1},

    {"text": "Save $0.75 on Chocolate Protein Shake (Expires Shift 4)", "item": "proteinshake", "discount": 0.75, "min_qty": 1, "max_shift": 4},

    {"text": "Save $2.59 on Tomato Soup (6ct) (Expires Shift 1)", "item": "soup", "discount": 2.59, "min_qty": 1, "max_shift": 1},

    {"text": "Save $2.00 on Garlic (Expires Shift 5)", "item": "garlic", "discount": 2.00, "min_qty": 1, "max_shift": 1},

    {"text": "Save $2.50 on 2 Tubs of Greek Yogurt (Expires Shift 6)", "item": "greekyogurt", "discount": 2.50, "min_qty": 1, "max_shift": 6},

    {"text": "Save $12.00 on 2 Cuts on Ribeye Steak (Expires Shift 9)", "item": "steak", "discount": 12.00, "min_qty": 1, "max_shift": 9},

    {"text": "Save $1.50 on Organic Almond Milk (Expires Shift 4)", "item": "almondmilk", "discount": 1.50, "min_qty": 1, "max_shift": 1},

    {"text": "Save $3.40 on Chocolate Chip Muffins (10ct)", "item": "muffins", "discount": 3.40, "min_qty": 1, "max_shift": 10},

]


customers = [
    {
        "name": "Tim",
        "greeting": "Hi, How are you doing?. Please Keep my meat separate",
        "happy_outro": "Everything looks in order.",
        "angry_outro": "Oh No, Im Going to have to re-bag this",
        "preferred_items": ["chicken","rice","blackbeans","oliveoil","eggs","flour"],
        "tipmult": 1.2,
    },

    {
        "name": "Bill",
        "greeting": "Hi, how are you doing Today?. Please put my Frozen Items with my produce",
        "happy_outro": "Thank You. Keep The Change",
        "angry_outro": "You Crushed My Avocados",
        "preferred_items": ["avocados", "steak", "rice","coffee","flour"],
        "tipmult": 1.1,
    },

    {
        "name": "Connor",
        "greeting": "Hi, Multiple Coupons Today, Be Ready!",
        "happy_outro": "Thank You For Your Time. Keep The Change",
        "angry_outro": "You Crushed My Tortilla Chips",
        "preferred_items" : ["tortillachips", "avocados","blackbeans", "salsa","soup","bellpeppers"],
        "tipmult": 0.95,
    },

    {
        "name": "College Kid",
        "greeting": "On 2 Hours of Sleep, Need Some Caffeine",
        "happy_outro": "Yo, You Got Me Good With the Energy!",
        "angry_outro": "Bro, Where is My Energy Drink?",
        "preferred_items": ["energydrink", "peanutbutter","eggs", "whitebread", "chips"],
        "tipmult": 2.1,
    },

    {
        "name": "Weekend Baker",
        "greeting": "Hey, Here to Bake, Please Don't Crush My Muffins",
        "happy_outro": "You fit my Things Perfectly",
        "angry_outro": "You Put Bleach on Top on my muffins",
        "preferred_items": ["muffin", "coffee", "croissants", "flour", "butter", "whitebread"],
        "tipmult": 1.4,
    },

    {
        "name": "Deep Cleaner Cory",
        "greeting": "Hey, Cleaning Heavily Today, Don't Put my cleaning supplies with my Produce",
        "happy_outro": "Hey, You Separated my bags to accommodate my request Thank You.",
        "angry_outro": "Why Did you put my bleach with my apples?",
        "preferred_items": ["bleach", "cleaningwipes","disinfectant", "apples","banana"],
        "tipmult": 3.2
    },

    {
        "name": "Taco Host",
        "greeting": "Hey, Hosting 12 today for Tacos",
        "happy_outro": "Thank, You For Packing my Items",
        "angry_outro": "Hey, You crushed my beans!",
        "preferred_items": ["blackbeans", "salsa", "rice", "chicken","flour","onions"],
        "tipmult": 2.1,
    },

    {
        "name": "Early Commuter",
        "greeting": "In a rush Today",
        "happy_outro": "Thank You",
        "angry_outro": "You wasted my time!",
        "preferred_items": ["coffee", "bagels","creamcheese"],
        "tipmult": 0.9,
    },

    {
        "name": "Bobby",
        "greeting": "Today is Rainy, Well Hows Your Day",
        "happy_outro": "Thank You For packing my bag",
        "angry_outro": "You Contaminated My bell pepper with my Steak!",
        "preferred_items": ["steak", "bellpepper", "salsa", "soup", "chicken","rice","coffee","flour","onions"],
        "tipmult": 1.6,
    },

    {
        "name": "BBQ Master",
        "greeting": "Hey, Got Some Meat For me?",
        "happy_outro": "Thanks For packing my bag perfectly!",
        "angry_outro": "You Cross contaminated my onions with my shrimp",
        "preferred_items": ["shrimp", "steak", "chicken","coffee"],
        "tipmult": 2.2,
    },

    {
        "name": "Fit BodyBuilder",
        "greeting": "Hey, Need some for my muscles",
        "happy_outro": "My muscles are happy Because of You Thanks!",
        "angry_outro": "Bro, My muscles aren't recovering from This",
        "preferred_items": ["chicken", "steak", "shrimp", "bacon", "porkchops"],
        "tipmult": 3.9,
    },

    {
        "name": "Carlos",
        "greeting": "Hey, Hosting a bbq for 25",
        "happy_outro": "And that is 25 people happy because of you!",
        "angry_outro": "And that is 25 sad because of you!",
        "preferred_items": ["chicken", "steak", "porkchops", "shrimp", "flour", "onions", "bellpeppers", "whitebread", "burgerbuns", "chips"],
        "tipmult": 1.6,
    },

    {
        "name": "Fancy Dinner Date",
        "greeting": "Hey, Give me your Most expensive Cuts of meat",
        "happy_outro": "My Date will appreciate this!",
        "angry_outro": "You Made me Lose my Only Date!",
        "preferred_items": ["steak","bread", "chips","lobster", "energydrink"],
        "tipmult": 0.7,
    },

    {
        "name": "The Lunchbox Parent",
        "greeting": "Hey, in a rush. My kids Bus Leaves in 20mins!",
        "happy_outro": "You saved me, I didnt miss the bus",
        "angry_outro": "You Made me miss my Kid's Bus",
        "preferred_items": ["chicken", "flour", "tortillas", "torillachips"],
        "tipmult": 3.7,
    },

    {
        "name": "Freezer Man",
        "greeting": "Yo, Need Freezer Meals for the week",
        "happy_outro": "Thanks man. There goes another week without cooking!",
        "angry_outro": "Bro. I said All freezer meals",
        "preferred_items": ["icecream", "waffles", "burritos", "fries"],
        "tipmult": 1.4,
    },

    {
        "name": "Generous Tipper",
        "greeting": "Hey, Hows Your Day Been?",
        "happy_outro": "Have A Good one, See you later",
        "angry_outro": "You messed Up My order",
        "preferred_items": ["burgerbuns", "whitebread", "rice", "blackbeans", "tortillachips"],
        "tipmult": 7.2,
    },

    {
        "name": "Seafood Lover",
        "greeting": "Hey, Are Your Fish Fishing Today?",
        "happy_outro": "Yo, The fish are fishing!",
        "angry_outro": "Bro. these fish aren't fishing",
        "preferred_items": ["lobster", "shrimp", "crab", "butter", "garlic"],
        "tipmult": 1.98,
    },

    {
        "name": "Picky Pablo",
        "greeting": "Have Any Chicken Nuggets?",
        "happy_outro": "Yo, Your Chicken Nuggets Are fire",
        "angry_outro": "Bro, These are Bad Your Nuggets are still chickening",
        "preferred_items": ["chickennuggets", "rice", "chicken"],
        "tipmult": 2.9,
    },

    {
        "name": "Soup Maker",
        "greeting": "Hey, What is in store today?",
        "happy_outro": "Your soup is fire",
        "angry_outro": "Your soup is cold and sad",
        "preferred_items": ["soup", "marinara", "carrots", "onions"],
        "tipmult": 1.4,
    },

    {
        "name": "Rordan Gamsey",
        "greeting": "What Are You",
        "happy_outro": "You are not an Idiot Sandwich",
        "angry_outro": "Nah, You are an Idiot Sandwich",
        "preferred_items": ["steak", "whitebread", "burgerbuns"],
        "tipmult": 0.9,
    }
]

upgrades_catalog = {
    "sticky_note": {
        "name": "Plu Sticky Note",
        "cost": 25.00,
        "description": "Displays the 5 most common codes on your screen"
    },
    "heavy_bags": {
        "name": "Heavy Bags",
        "cost": 40.00,
        "description": "Increases Max Bag Weight Capacity From 15.0lbs to 22.0lbs"
    },
    "laser_scanner": {
        "name": "Dual Laser Barcode Scanner",
        "cost": 55.00,
        "description": "Eliminates the random chance of a laser jam happening"
    },
    "auto_calc": {
        "name": "Automatic Change Dispenser",
        "cost": 70.00,
        "description": "Automatically calculates Changes and gives it to the customer"
    },
    "insulated_bags": {
        "name": "Thermal Freezer Bags",
        "cost": 85.00,
        "description": "Doubles the Bonus Tip earned when bagging frozen items"
    },
    "express_belt": {
        "name": "Turbo Conveyor belt",
        "cost": 100.00,
        "description": "Reduces Total Shift time by 15 seconds each Shift"
    }
}

register_events = [
    {"type": "jam", "message": "Scanner Jam Type 'clear' to reset the laser", "penalty_seconds": 3, "action": "clear"},

    {"type": "price_check","message": "Missing Tag! Type 'call' to ask a manger for a price check.", "penalty_seconds":5, "action": "call" },

    {"type": "recipt_paper", "message": "Out of Receipt Paper Type 'reload' to swap the roll", "penalty_seconds":4, "action": "reload"},

    {"type": "bag_tangle", "message": "Bags Stuck Together Type 'Pull; to separate them", "penalty_seconds":2, "action": "pull"},

    {"type": "scale_reset", "message":"Product Scale off zero Type 'reset' to calibrate", "penalty_seconds":3, "action": "reset"},

    {"type": "spill", "message": "Sticky conveyor belt Type 'wipe' to clean the belt up ", "penalty_seconds":4, "action": "wipe"},

    {"type": "coupon_crinkle", "message": "Crumples Coupon Type 'smooth' to uncrinkle the coupon", "penalty_seconds":2, "action": "smooth"},

    {"type": "card_chip", "message": "Chip Reader Error Type 'swipe' to use the magnetic strip", "penalty_seconds":3, "action": "swipe"},
]

from functions import *