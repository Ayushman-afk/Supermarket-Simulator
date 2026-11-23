import time
import random

#- Pregame defined variables. (total - 224) (115 items of produce) (40 coupons) (20 Customers) (8 register events) (6 upgrades)

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

    "spinach": {"name": "Baby Spinach", "price": 3.99, "weight": 1.3, "category": "produce", "code": "1111", "is_produce": True, "fragile": True},

    "blueberries": {"name": "Fresh Blueberries", "price": 2.29, "weight": 0.3, "category": "produce", "code": "1099", "is_produce": True, "fragile": False},

    "greengrapes": {"name": "Green Seedless Grapes", "price": 4.79, "weight": 1.3, "category": "produce", "code": "1938", "is_produce": True, "fragile": False},

    "redgrapes": {"name": "Red Seedless Grapes", "price": 4.89, "weight": 2.1, "category": "produce", "code": "1324", "is_produce": True, "fragile": False},

    "watermelon": {"name": "Seedless Watermelon", "price": 8.99, "weight": 11.5, "category": "produce", "code": "1999", "is_produce": True, "fragile": False},

    "pineapple": {"name": "Golden Pineapple", "price": 4.49, "weight": 3.4, "category": "produce", "code": "1222", "is_produce": True, "fragile": False},

    "peaches": {"name": "Yellow Peaches", "price": 4.29, "weight": 4.5, "category": "produce", "code": "1122", "is_produce": True, "fragile": False},

    "pears": {"name": "Bartlett Pears", "price": 3.79, "weight": 1.9, "category": "produce", "code": "1100", "is_produce": True, "fragile": False},

    "celery": {"name": "Celery Stalks", "price": 2.49, "weight": 1.6, "category": "produce", "code": "1900", "is_produce": True, "fragile": False},

    "mushrooms": {"name": "Sliced Mushrooms", "price": 3.29, "weight": 0.7, "category": "produce", "code": "1290", "is_produce": True, "fragile": False},

    "jalapenos": {"name": "Jalapeno Peppers", "price": 1.89, "weight": 0.9, "category": "produce", "code": "1298", "is_produce": True, "fragile": False},

    "ginger": {"name": "Fresh Ginger Root", "price": 2.69, "weight": 0.5, "category": "produce", "code": "1992", "is_produce": True, "fragile": False},

    "sweetpotatoes": {"name": "Sweet Potatoes", "price": 5.49, "weight": 4.5, "category": "produce", "code": "1090", "is_produce": True, "fragile": False},

    "asparagus": {"name": "Green Asparagus", "price": 4.59, "weight": 1.0, "category": "produce", "code": "1911", "is_produce": True, "fragile": False},

    "cauliflower": {"name": "Cauliflower Head", "price": 2.99, "weight": 1.7, "category": "produce", "code": "1005", "is_produce": True, "fragile": False},

    "cabbage": {"name": "Green Cabbage", "price": 2.79 ,"weight": 3.8, "category": "produce", "code": "1004", "is_produce": True, "fragile": False},

    "greenbeans": {"name": "French Green Beans", "price": 3.49, "weight": 1.0, "category": "produce", "code": "1009", "is_produce": True, "fragile": True},

    "cornonthecob": {"name": "Sweet Corn (4ct)", "price": 3.99, "weight": 2.5, "category": "produce", "code": "1010", "is_produce": True, "fragile": False},

    "cherries": {"name": "Dark Sweet Cherries", "price": 6.99, "weight": 1.2, "category": "produce", "code": "1011", "is_produce": True, "fragile": False},

    "kiwis": {"name": "Kiwi Fruit (4ct)", "price": 3.79, "weight": 0.9, "category": "produce", "code": "1012", "is_produce": True, "fragile": False},

    "oranges": {"name": "Navel Oranges", "price": 4.99, "weight": 3.5, "category": "produce", "code": "1013", "is_produce": True, "fragile": False},

    "grapefruit": {"name": "Ruby Red Grapefruit", "price": 2.49, "weight": 1.3, "category": "produce", "code": "1014", "is_produce": True, "fragile": False},

    "cantaloupe" : {"name": "Ripe Cantaloupe", "price": 3.99, "weight": 4.8, "category": "produce", "code": "1015", "is_produce": True, "fragile": False},

    "honeydew" : {"name": "HoneyDew Melon", "price": 4.49, "weight": 5.2, "category": "produce", "code": "1016", "is_produce": True, "fragile": False},

    "cilantro" : {"name": "Fresh Cilantro Bunch", "price": 1.29, "weight": 0.3, "category": "produce", "code": "1017", "is_produce": True, "fragile": True},

    "greenonions" : {"name": "Green Onions", "price": 1.49, "weight": 0.4, "category": "produce", "code": "1018", "is_produce": True, "fragile": True},

    "radishes" : {"name": "Red Radish", "price": 1.99, "weight": 0.8, "category": "produce", "code": "1019", "is_produce": True, "fragile": False},

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

    "mozzarella" : {"name": "Fresh Mozzarella Ball", "price": 5.49, "weight": 1.0, "category": "dairy", "code": "2000", "is_dairy": True, "fragile": False},

    "parmesan" : {"name": "Grated Parmesan Cheese", "price": 4.99, "weight": 0.8, "category": "dairy", "code": "2001", "is_dairy": True, "fragile": False},

    "oatmilk": {"name": "Barista Oat Milk", "price": 4.79, "weight": 2.2, "category": "dairy", "code": "2002", "is_dairy": True, "fragile": False},

    "heavycream" : {"name": "Heavy Whipping Cream", "price": 4.49, "weight": 1.3, "category": "dairy", "code": "2003", "is_dairy": True, "fragile": False},

    "cottagecheese": {"name": "Low Fat Cottage Cheese", "price": 3.99, "weight": 0.9, "category": "dairy", "code": "2004", "is_dairy": True, "fragile": False},

    "swisscheese": {"name": "Sliced Swiss Cheese", "price": 4.59, "weight": 1.3, "category": "dairy", "code": "2005","is_dairy": True, "fragile": False},

    "provolone" : {"name": "Deli Provolone Slices", "price": 4.79, "weight": 0.9, "category": "dairy", "code": "2006", "is_dairy": True, "fragile": False},

    "chocolatemilk" : {"name": "Whole Chocolate Milk", "price": 4.29, "weight": 3.4, "category": "dairy", "code": "2007", "is_dairy": True, "fragile": False},

    "strawberryyogurt" : {"name": "Strawberry Yogurt", "price": 3.89, "weight": 1.3, "category": "dairy", "code": "2008", "is_dairy": True, "fragile": False},

    "ricotta": {"name": "Whole Milk Ricotta", "price": 5.29, "weight": 2.0, "category": "dairy", "code": "2009", "is_dairy": True, "fragile": False},

    "applejuice": {"name": "Cold Pressed Apple Juice", "price": 5.99, "weight": 4.2, "category": "refrigerated", "code": "2010", "is_dairy": True, "fragile": False},

    "icedcoffee" : {"name": "Cold Brew Iced Coffee", "price": 4.99, "weight": 3.1, "category": "dairy", "code": "2011", "is_dairy": True, "fragile": False},

    "guacamole" : {"name": "Fresh Chunky Guacamole", "price": 5.49, "weight": 3.4, "category": "refrigerated", "code": "2012", "is_dairy": True, "fragile": False},

    "pesto" : {"name": "Fresh Basil pesto Tub", "price": 6.29, "weight": 0.4, "category": "dairy", "code": "2013", "is_dairy": True, "fragile": False},

    "biscuitdough": {"name": "Buttermilk Biscuit Dough", "price": 3.49, "weight": 1.2, "category": "refrigerated","code": "2014", "is_dairy": True, "fragile": False},

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

    "englishmuffins" : {"name": "English Muffins (6ct)", "price": 3.79, "weight": 0.7, "category": "bakery", "code": "3001", "is_bakery": True, "fragile": True},

    "hotdogbuns" : {"name": "Hot Dog Buns (8ct)", "price": 3.29, "weight": 0.8, "category": "bakery", "code": "3002", "is_bakery": True, "fragile": True},

    "blueberrymuffins": {"name": "Blueberry Muffins (4ct)", "price": 5.99, "weight": 1.4, "category": "bakery", "code": "3003", "is_bakery": True, "fragile": True},

    "glazeddonuts": {"name": "Glazed Donuts (6ct)", "price": 6.49, "weight": 1.3, "category": "bakery", "code": "3004", "is_bakery": True, "fragile": False},

    "garlicbread": {"name": "Bakery Garlic Bread Loaf", "price": 4.29, "weight": 1.2, "category": "bakery", "code": "3005", "is_bakery": True, "fragile": False},

    "pitabread": {"name": "Whole Wheat Pita Pockets", "price": 3.69, "weight": 1.0, "category": "bakery", "code": "3006", "is_bakery": True, "fragile": True},

    "naan" : {"name": "Garlic Naan", "price": 4.49, "weight": 1.1, "category": "bakery", "code": "3007", "is_bakery": True, "fragile": False},

    "brownies" : {"name": "Fudge Brownie Bites", "price": 6.99, "weight": 1.5, "category": "bakery", "code": "3008", "is_bakery": True, "fragile": False},

    "applepie" : {"name": "Apple Pie", "price": 9.99, "weight": 1.4, "category": "bakery", "code": "3009", "is_bakery": True, "fragile": False},

    "cheesecake" : {"name":"New York Cheesecake", "price": 12.99, "weight": 3.9, "category": "bakery", "code":"3010", "is_bakery": True, "fragile": False},

    "cornbread" : {"name": "Honey Corn Bread", "price": 7.99, "weight": 3.1, "category": "bakery", "code": "3011", "is_bakery": True, "fragile": False},

    "ryebread" : {"name": "Rye Bread", "price": 4.59, "weight": 2.1, "category": "bakery", "code": "3012", "is_bakery": True, "fragile": True},

    "briochebuns" : {"name": "Brioche Burger Buns (4ct)", "price": 4.99, "weight": 0.9, "category": "bakery","code": "3013", "is_bakery": True, "fragile": True},

    "bananabread" : {"name": "Cinnamon Banana Bread", "price": 6.79, "weight": 1.0,"category": "bakery", "code": "3014", "is_bakery": True, "fragile": False},

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

    "chickenthighs" : {"name": "Fresh Organic Chicken Thighs", "price": 8.49, "weight": 3.2, "category": "rawmeat", "code": "4001", "is_rawmeat": True, "fragile": False},

    "chickenwings" : {"name": "Chicken Wings (40pc)", "price": 14.99, "weight": 5.0, "category": "rawmeat", "code": "4002", "is_rawmeat": True, "fragile": False},

    "groundturkey" : {"name": "Lean Ground Turkey", "price": 9.99, "weight": 4.9, "category": "rawmeat", "code":"4003", "is_rawmeat": True, "fragile": False},

    "italiansausage" : {"name": "Chicken Italian Style Sausage", "price": 7.49, "weight": 1.9, "category":"rawmeat", "code": "4004", "is_rawmeat": True, "fragile": False},

    "porktenderloin" : {"name": "Pork Tenderloin Roast","price": 11.49, "weight": 3.5, "category": "rawmeat", "code": "4005", "is_rawmeat": True, "fragile": False},

    "lambchops" : {"name": "Organic Lamb Chops", "price": 19.99, "weight": 2.4, "category": "rawmeat","code": "4006","is_rawmeat": True, "fragile": False},

    "sirloinsteak" : {"name": "Sirloin Steak", "price": 16.49, "weight": 2.8, "category": "rawmeat","code":"4007" ,"is_rawmeat": True,"fragile": False},

    "beefroast" : {"name": "Chuck Pot Roast", "price": 21.99, "weight": 4.8, "category": "rawmeat", "code": "4008","is_rawmeat": True, "fragile": False},

    "codfillets" : {"name" : "Wild Atlantic Caught Cod Fillets", "price": 11.99, "weight": 2.2, "category": "rawmeat","code": "4009", "is_rawmeat": True, "fragile": False},

    "tilapia" : {"name": "Fresh Tilapia Fillets", "price": 9.49, "weight": 2.0, "category": "rawmeat","code": "4010" ,"is_rawmeat":True, "fragile": False},

    "scallops" : {"name": "Jumbo Sea Scallops", "price": 22.49, "weight": 1.8, "category": "rawmeat","code":"4011" ,"is_rawmeat": True, "fragile": False},

    "bratwurst" : {"name": "Bratwurst", "price": 6.79, "weight": 1.7, "category": "rawmeat","code": "4012" ,"is_rawmeat": True, "fragile": False},

    "drumsticks" : {"name": "Chicken Drumsticks", "price": 5.99,"weight": 3.6, "category": "rawmeat","code":"4013" ,"is_rawmeat": True, "fragile": False},

    "babybackribs" : {"name": "Pork barbeque Ribs", "price": 18.99, "weight": 4.4, "category": "rawmeat","code":"4014" ,"is_rawmeat": True, "fragile": False},

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

    "frozenlasagna" : {"name": "Family Size Meat lasagna", "price": 13.49,"weight": 7.9, "category": "frozen", "code": "5001", "is_frzoen": True, "fragile": False},

    "taters" : {"name": "Crispy Frozen Tater Tots", "price": 4.79,"weight": 1.4, "category":"frozen", "code": "5002", "is_frozen" : True, "fragile": False},

    "frozenbroccoli" :{"name": "Steamable Frozen Broccoli Florets", "price": 5.79, "weight": 2.3, "category": "frozen", "code": "5003", "is_frozen": True, "fragile": False},

    "mozzarellasticks" : {"name": "Frozen Garlic Flavoured Mozzarella Sticks", "price": 7.49, "weight": 2.3, "category": "frozen", "code": "5004", "is_froze": True, "fragile": False},

    "pizzarolls" : {"name": "Pepperoni Pizza Rolls", "price": 6.99, "weight": 1.2, "category": "frozen", "code":"5005", "is_frozen": True, "fragile": False},

    "frozendumplings" : {"name": "Chicken and Veggie Dumplings", "price": 7.99, "weight": 3.4, "category": "frozen", "code": "5006", "is_frozen": True,"fragile": False },

    "minticecream" : {"name": "Mint Chocolate Chip Ice Cream", "price": 5.49, "weight": 1.2, "category":"frozen", "code":"5007", "is_frozen": True, "fragile": False},

    "icecreamsandwiches" : {"name": "Chocolate Chip Ice Cream Sandwiches", "price": 4.89, "weight": 2.2, "category": "frozen", "code": "5008", "is_frozen": True, "fragile": True},

    "frozenravioli" : {"name": "Four Cheese Frozen Ravioli", "price": 6.49, "weight": 2.7, "category": "frozen", "code": "5009", "is_frozen": True, "fragile": False},

    "hashbrowns" : {"name": "Shredded Hash Browns", "price": 3.99, "weight": 1.9, "category": "frozen", "code": "5010", "is_frozen": True, "fragile": False},

    "onionrings" : {"name": "Onion Rings", "price": 5.29, "weight": 1.7, "category": "frozen", "code": "5011", "is_frozen": True, "fragile": False},

    "frozenmeatballs" : {"name": "Frozen Meatballs", "price": 9.99, "weight": 0.9, "category": "frozen", "code": "5012", "is_frozen": True, "fragile": False},

    "mangosorbet" : {"name" : "Tropical Mango Sorbet", "price": 4.99, "weight": 0.3, "category": "frozen", "code": "5013", "is_frozen": True, "fragile": False},

    "fishsticks" : {"name" : "Crunchy Fish Sticks", "price": 6.79, "weight": 1.5, "category": "frozen", "code": "5014", "is_frozen": True, "fragile": False},

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

    "chickennoodlesoup" : {"name": "Chicken Noodle Soup", "price": 4.99, "weight": 4.2, "category": "canned", "code": "6001", "is_canned": True, "fragile": False},

    "cannedtuna": {"name": "Canned White Tuna", "price": 2.79, "weight": 0.6, "category": "canned", "code": "6002", "is_canned": True, "fragile": False},

    "chickpeas" : {"name" : "Organic Chickpea Can", "price": 3.99, "weight": 3.7, "category": "canned", "code": "6003", "is_canned": True, "fragile": False},

    "kidneybeans" : {"name" : "Dark Red Kidney Beans", "price": 1.89, "weight": 2.1,"category": "canned", "code": "6004", "is_canned": True, "fragile": False},

    "dicedtomatoes" : {"name": "Roasted Diced Tomatoes", "price" : 2.29, "weight": 1.1,"category": "canned", "code": "6005", "is_canned": True, "fragile": False},

    "chickenbroth" : {"name": "Low Sodium Chicken Broth", "price": 3.49, "weight": 1.2, "category": "canned","code": "6006", "is_canned": True, "fragile": False},

    "coconutmilk" : {"name": "Sweetened Coconut Milk", "price": 3.49, "weight": 3.4, "category": "canned", "code": "6007", "is_canned": True, "fragile": False},

    "cannedcorn" : {"name": "Sweet Kernel Canned Corn", "price": 1.79, "weight": 1.0, "category": "canned", "code": "6008", "is_canned": True, "fragile": False},

    "strawberryjam" : {"name": "Strawberry Fruit Jam", "price": 4.49, "weight": 3.4, "category":"canned", "code": "6009", "is_canned": True, "fragile": False},

    "rawhoney" : {"name" : "Raw Honey", "price": 7.99, "weight": 1.4, "category": "canned", "code": " 6010","is_canned": True, "fragile": True},

    "maplesyrup" : {"name": "Maple Syrup", "price": 9.49, "weight": 1.6, "category": "canned", "code": "6011", "is_canned": True, "fragile": False},

    "ketchup" : {"name": "Tomato Ketchup", "price": 4.59, "weight": 1.4, "category": "canned", "code": "6012", "is_canned": True, "fragile": False},

    "mayo" : {"name": "Mayonnaise", "price": 3.59, "weight": 1.2,"category": "canned", "code": "6013", "is_canned": True, "fragile": False},

    "rolledoats" : {"name": "Rolled Oats", "price": 4.69, "weight": 4.6,"category":"canned", "code": "6014", "is_canned": True, "fragile": False},

    "brownrice" : {"name": "Long Grain Brown Rice", "price": 4.29, "weight": 3.4,"category":"canned", "code": "6015", "is_canned": True, "fragile": False},

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

    "pretzels": {"name": "Salted Pretzels", "price": 3.69, "weight": 4.5, "category": "snack", "code": "7001", "is_snack": True, "fragile": True},

    "popcorn" : {"name": "White Cheddar Popcorn", "price": 4.29, "weight": 1.2, "category": "snack", "code": "7002", "is_snack" : True, "fragile": False},

    "cheesepuffs" : {"name": "Crunchy Cheese Puffs", "price": 3.99, "weight": 3.1, "category": "snack", "code": "7003", "is_snack": True, "fragile": False},

    "beefjerky" : {"name": "Teriyaki Beef Jerky", "price": 2.99, "weight": 4.1, "category": "snack", "code": "7004", "is_snack": True, "fragile": False},

    "roastedalmonds" : {"name": "Sea Salt Roasted Almonds", "price": 2.59, "weight": 3.4, "category": "snack", "code": "7005", "is_snack": True, "fragile": False},

    "cashews" : {"name": "Honey roasted Cashews", "price": 8.49, "weight": 0.5, "category": "snack","code": "7006", "is_snack": True, "fragile": False},

    "oreocookies" : {"name": "Chocolate Sandwich Cookies", "price": 4.79, "weight": 4.3, "category": "snack", "code": "7007", "is_snack": True, "fragile": False},

    "gummybears" : {"name": "Fruity Gummy Bears", "price": 2.99, "weight": 0.7, "category": "snack", "code": "7008", "is_snack": True, "fragile": False},

    "granolabars" : {"name": "Oats & Granola Bars", "price": 4.29, "weight": 0.8, "category": "snack", "code": "7009", "is_snack": True, "fragile": False},

    "fruitsnacks" : {"name": "Assorted Fruit Snacks", "price": 3.49,"weight": 2.3 ,"category": "snack", "code": "7010", "is_snack" : True, "fragile": False},

    "sparklingwater" : {"name": "Lime Sparkling Water", "price": 5.99, "weight": 7.3, "category": "snack", "code": " 7011", "is_snack" : True, "fragile": False},

    "icedtea" : {"name": "Peach Iced Tea", "price": 5.99, "weight": 12.9, "category": "snack", "code": "7012", "is_snack": True, "fragile": False},

    "sportsdrink" : {"name": "Electrolyte Sports Drink", "price": 4.59, "weight": 2.3, "category": "snack", "code": "7013", "is_snack": True, "fragile": False},

    "ricecakes" : {"name": "Caramel Rice Cake", "price": 2.99,"weight": 1.2, "category":"snack","code":"7014","is_snack": True, "fragile": False},

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

    "papertowels" : {"name": "Mega Roll Paper Towels", "price": 13.99, "weight": 1.9, "category": "household","code": "8001", "is_house": True, "fragile": False},

    "dishsoap" : {"name": "Ultra Liquid Dish Soap", "price":3.99, "weight": 1.5, "category": "household", "code": "8002", "is_house": True, "fragile": False},

    "dishwashertab" : {"name": "Dishwasher Detergent Pods", "price":12.49, "weight": 3.4,"category": "household", "code": "8003", "is_house": True, "fragile": False},

    "trashbags" : {"name": "Tall Kitchen Trash Bags", "price": 9.99, "weight": 7.9, "category": "household", "code": "8004", "is_house": True, "fragile": False},

    "aluminumfoil" : {"name": "Heavy Duty Aluminum Foil", "price": 13.49, "weight": 6.4, "category": "household", "code": "8005", "is_house": True, "fragile": False},

    "plasticwrap" : {"name": "Kitchen Plastic Wrap", "price": 12.39, "weight": 3.1, "category": "household", "code": "8006", "is_house": True, "fragile": False},

    "ziplockbags" : {"name": "Gallon Freezer Zip Bags", "price": 7.99, "weight": 3.1, "category": "household","code": "8007", "is_house": True, "fragile": False},

    "sponges" : {"name": "Heavy Duty Scrub Sponges", "price": 5.99, "weight": 0.7, "category": "household", "code": "8008","is_house": True, "fragile": False},

    "glasscleaner" : {"name": "Glass Cleaner", "price": 3.99, "weight": 4.3, "category": "household", "code":"8009", "is_house": True, "fragile": False},

    "dryersheets" : {"name": "Fresh Linen Dryer Sheets", "price": 5.49, "weight": 0.6, "category": "household", "code": "8010", "is_house": True, "fragile": False},

    "handsoap" : {"name": "Lavender Hand Soap", "price": 3.49, "weight": 1.9, "category": "household", "code": "8011", "is_household": True, "fragile": False},

    "paperplates" : {"name" : "Paper Plates", "price": 5.99, "weight": 1.8, "category": "household", "code": "8012", "is_household": True, "fragile": False},

    "plasticcups" : {"name": "Red Party Cups", "price": 3.49, "weight": 2.1, "category": "household","code": "8013","is_household": True, "fragile": False},

    "fabricsoftner" : {"name": "Liquid Fabric Softner", "price": 11.79, "weight": 3.4, "category": "household", "code": "8014", "is_household": True, "fragile": False}

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

    {"text": "Save $3.40 on Lemon Lime Wipes (Expires Shift 2)", "item": "wipes", "discount": 3.40, "min_qty": 1, "max_shift": 2},

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

    {"type": "price_check","message": "Missing Tag! Type 'call' to ask a manager for a price check.", "penalty_seconds": 5, "action": "call" },

    {"type": "recipt_paper", "message": "Out of Receipt Paper Type 'reload' to swap the roll", "penalty_seconds":4, "action": "reload"},

    {"type": "bag_tangle", "message": "Bags Stuck Together Type 'pull' to separate them", "penalty_seconds":2, "action": "pull"},

    {"type": "scale_reset", "message":"Product Scale off zero Type 'reset' to calibrate", "penalty_seconds":3, "action": "reset"},

    {"type": "spill", "message": "Sticky conveyor belt Type 'wipe' to clean the belt up ", "penalty_seconds":4, "action": "wipe"},

    {"type": "coupon_crinkle", "message": "Crumples Coupon Type 'smooth' to uncrinkle the coupon", "penalty_seconds":2, "action": "smooth"},

    {"type": "card_chip", "message": "Chip Reader Error Type 'swipe' to use the magnetic strip", "penalty_seconds":3, "action": "swipe"},
]

import random
import time
import os
import sys
from __main__ import *

#function 1 - finds the folder where main.py or the complied .exe is running so supersimsave.txt always saves right next to the game file

def get_save_path(filename):
    running_as_exe = getattr(sys, "frozen", False)

    if running_as_exe == True:
        exe_location = sys.executable
        folder_path = os.path.dirname(exe_location)
    else:
        script_location = os.path.abspath(__file__)
        folder_path = os.path.dirname(script_location)

    full_path = os.path.join(folder_path, filename)

    return full_path

#function 2 - Formats all 7 player stats and writes then line by line to the save file

def save_game(
        filepath,
        bank_balance,
        shift_num,
        total_customers_served,
        alltime_tips_earned,
        total_mistakes,
        best_shift_time,
        upgrades):

    if len(upgrades) == 0:
        upgrades_text = "No Upgrades"
    else:
        upgrades_text = ",".join(upgrades)

    clean_balance = round(bank_balance, 2)
    clean_shift = int(shift_num)
    clean_customer = int(total_customers_served)
    clean_tips = round(alltime_tips_earned, 2)
    clean_mistakes = int(total_mistakes)
    clean_best_time = round(best_shift_time, 2)


    line_1 = str(clean_balance) + "\n"
    line_2 = str(clean_shift) + "\n"
    line_3 = str(clean_customer) + "\n"
    line_4 = str(clean_tips) + "\n"
    line_5 = str(clean_mistakes) + "\n"
    line_6 = str(clean_best_time) + "\n"
    line_7 = upgrades_text + "\n"

    file_writer = open(filepath, "w")
    file_writer.write(line_1)
    file_writer.write(line_2)
    file_writer.write(line_3)
    file_writer.write(line_4)
    file_writer.write(line_5)
    file_writer.write(line_6)
    file_writer.write(line_7)
    file_writer.close()


# function 3 - reads the 7 stats, If the file is missing or corrupted, creates a fresh save file with default values.

def load_game(filepath):
    file_found = os.path.exists(filepath)

    if file_found == False:
        default_upgrades = []
        save_game(filepath, 0.00, 1, 0, 0.00, 0, 999.99, default_upgrades)
        return 0.00, 1, 0, 0.00, 0, 999.99, []

    try:
        file_reader = open(filepath, "r")
        lines = file_reader.readlines()
        file_reader.close()

        if len(lines) < 7:
            raise ValueError("Save File Is Missing Required Lines")

        text_balance = lines[0].strip()
        text_shift = lines[1].strip()
        text_customers = lines[2].strip()
        text_tips = lines[3].strip()
        text_mistakes = lines[4].strip()
        text_best_time = lines[5].strip()
        text_upgrades = lines[6].strip()

        loaded_balance = round(float(text_balance), 2)
        loaded_shift = int(text_shift)
        loaded_customers = int(text_customers)
        loaded_tips = round(float(text_tips), 2)
        loaded_mistakes = int(text_mistakes)
        loaded_best_time = round(float(text_best_time), 2)


        if loaded_balance < 0:
            loaded_balance = 0.00

        if loaded_shift < 1:
            loaded_shift = 1

        if loaded_customers < 0:
            loaded_customers = 0

        if loaded_tips < 0:
            loaded_tips = 0.00

        if loaded_mistakes < 0:
            loaded_mistakes = 0

        if loaded_best_time < 0:
            loaded_best_time = 999.99


        loaded_upgrades = []
        if text_upgrades != "none" and text_upgrades != "":
            raw_list = text_upgrades.split(",")
            for raw_key in raw_list:
                clean_key = raw_key.strip()
                if clean_key in upgrades_catalog:
                    if clean_key not in loaded_upgrades:
                        loaded_upgrades.append(clean_key)


        return (
            loaded_balance,
            loaded_shift,
            loaded_customers,
            loaded_tips,
            loaded_mistakes,
            loaded_best_time,
            loaded_upgrades,
        )

    except:
        print("Save File is missing Data or corrupted, Creating a new save file.")
        default_upgrades = []
        save_game(filepath, 0.00, 1,0, 0.00, 0, 999.99, default_upgrades)
        return 0.00, 1, 0, 0.00, 0, 999.99, []


#function 4- prompts the player to type yes before wiping all save progress.
def reset_save(filepath):
    print("RESET SAVE DATA WARNING")
    print("This Will permanently erase your bank balance,")
    print("shift progress, career stats, and upgrades.")

    answer = input("\nType 'yes' to erase everything and reset: ").strip().lower()

    if answer == "yes":
        double_check = input("Type 'confirm' to complete the reset: ").strip().lower()
        if double_check == "confirm":
            fresh_upgrades = []
            save_game(filepath, 0,1,0,0.00,0,999.99, fresh_upgrades)
            print("\n Your save file has been completely reset to default")
            return 0.00, 1, 0, 0.00 , 0, 999.99, []
        else:
            print("cancelled")
            return load_game(filepath)
    else:
        print("cancelled")
        return load_game(filepath)


#function 5 - shows career stats

def show_career_stats(
        bank_balance,
        shift_num,
        total_customers_served,
        alltime_tips_earned,
        total_mistakes,
        best_shift_time,
        upgrades
):
    completed_shifts = shift_num - 1

    if completed_shifts == 0:
        rank_title = "Trainee Cashier"
    elif completed_shifts <= 2:
        rank_title = "Junior Checkout Cashier"
    elif completed_shifts <= 4:
        rank_title = "Experienced Cashier"
    elif completed_shifts <= 7:
        rank_title = "Senior Register Operator"
    elif completed_shifts <= 11:
        rank_title = "Front End Shift lead"
    else:
        rank_title = "Super Mart Store Legend"

    if total_customers_served > 0:
        mistakes_per_customer = round(total_mistakes / total_customers_served, 2)
    else:
        mistakes_per_customer = 0.00

    if completed_shifts > 0:
        average_shift_pay = round(alltime_tips_earned / completed_shifts, 2)
    else:
        average_shift_pay = 0.00

    print("Super Mart Career Record")

    print("Cashier Rank: " + rank_title)
    print("Current Bank Balance: ${:.2f}".format(bank_balance))
    print("Next Shift Number: #" + str(shift_num))
    print("Shifts Completed: #" + str(completed_shifts))
    print("Customer Served: "+ str(total_customers_served))
    print("All Time Earnings: ${:.2f}".format(alltime_tips_earned))
    print("Average Pay / Shift: ${:.2f}".format(average_shift_pay))
    print("Total Mistakes Made: "+ str(total_mistakes))
    print("Mistakes / Customer: {:.2f}".format(mistakes_per_customer))

    if best_shift_time == 999.99:
        print("Best Shift Time: No Shifts Yet")
    else:
        print("Best Shift Time: {:.2f}".format(best_shift_time) + "seconds")

    if len(upgrades) == 0:
        print("Owned Upgrades = None")
    else:
        print("Owned Upgrades (" + str(len(upgrades)) + " of "+ str(len(upgrades_catalog)) + "):")

        for up_key in upgrades:
            if up_key in upgrades_catalog:
                up_name = upgrades_catalog[up_key]["name"]
                up_desc = upgrades_catalog[up_key]["description"]
                print("  *" + up_name + " - " + up_desc)
            else:
                print("  *" + up_key)
    print("\n")

#function 6 - plu master key

def show_plu_master_key():
    while True:
        print("\nSuper Mart Catalog & PLU Master Key")
        print("1. Produce (PLU Codes)")
        print("2. Dairy and Refrigerated")
        print("3. Bakery")
        print("4. Raw Meat and refrigerated")
        print("5. Frozen Foods")
        print("6. Canned & Pantry")
        print("7. Snacks & Beverages")
        print("8. Household & Cleaning")
        print("9. All Store Items")
        print("0. Return to Main Menu")

        section_choice = input("\n Choose section to view (0-9): ").strip().lower()

        if section_choice == "0":
            break
        elif section_choice == "1":
            section_title = "Produce (PLU Codes)"
            allowed_categories = ["produce"]
        elif section_choice == "2":
            section_title = "Dairy & Refrigerated"
            allowed_categories = ["dairy", "refrigerated"]
        elif section_choice == "3":
            section_title = "Bakery"
            allowed_categories = ["bakery"]
        elif section_choice == "4":
            section_title = "Raw Meat & Seafood"
            allowed_categories = ["rawmeat"]
        elif section_choice == "5":
            section_title = "Frozen Foods"
            allowed_categories = ["frozen"]
        elif section_choice == "6":
            section_title = "Canned & Pantry"
            allowed_categories = ["canned"]
        elif section_choice == "7":
            section_title = "Snack & Beverage"
            allowed_categories = ["snack"]
        elif section_choice == "8":
            section_title = "Household & Cleaning"
            allowed_categories = ["household"]
        elif section_choice == "9":
            section_title = "All Store Items"
            allowed_categories = "all"
        else:
            print("Invalid Choice. Please Choose from 0 to 9.")
            continue

        print(section_title)
        print("Item name". ljust(32) + " | " + "Code".ljust(6) + " | " + "Price".ljust(7) + " | " + "Category".ljust(12) + " | Notes")
        print("-" * 82)

        shown_count = 0
        produce_keys = []

        for key in store_items:
            item = store_items[key]
            item_cat = item["category"]

            if item.get("is_produce") == True:
                produce_keys.append(key)

            if allowed_categories == "all" or item_cat in allowed_categories:
                shown_count += 1
                padded_name = item["name"][:32].ljust(32)
                clean_code = item["code"].strip().ljust(6)
                price_str = ("${:.2f}".format(item["price"])).ljust(7)
                cat_str = item_cat.ljust(12)

                if item.get("fragile") == True:
                    note_str = "FRAGILE"
                else:
                    note_str = "Sturdy (" + str(item["weight"]) + " lbs)"

                print(padded_name + " | " + clean_code + " | " + price_str + " | " + cat_str + " | " + note_str)

        print("\n Total Items in " + section_title + ": " + str(shown_count))

        if (allowed_categories == "all" or "produce" in allowed_categories) and len(produce_keys) > 0:
            practice_choice = input("\nType 'quiz' to practice PLU Codes (or press enter to go back): ").strip().lower()
            if practice_choice == "quiz":
                correct_count = 0
                total_questions = 3
                for q_num in range(total_questions):
                    random_key = random.choice(produce_keys)
                    random_item = store_items[random_key]
                    expected_code = random_item["code"].strip()
                    user_guess = input("Question " + str(q_num + 1) + ": Enter PLU Code for " + random_item["name"] + ": ").strip()
                    if user_guess == expected_code:
                        print("Correct")
                        correct_count += 1
                    else:
                        print("Wrong. The PLU code for " + random_item["name"] + " is " + expected_code + ".")
                print("Quiz Finished Score = " + str(correct_count) + " out of " + str(total_questions))
        else:
            input("\n Press Enter to pick another section")



# function 7 - open Upgrade Shop

def open_upgrade_shop(bank_balance, upgrades):
    upgrade_keys = list(upgrades_catalog.keys())
    while True:
        print("Super Mart Upgrade Shop")
        print("Available Bank Balance: ${}".format(bank_balance))
        print("Upgrades Owned: "+ str(len(upgrades)) + "/" + str(len(upgrade_keys)))

        index = 0

        while index < len(upgrade_keys):
            key = upgrade_keys[index]
            item_info = upgrades_catalog[key]
            number_label = str(index + 1) + ". "
            padded_name = item_info["name"].ljust(30)
            item_cost = item_info["cost"]

            if key in upgrades:
                status_text = "Owned"
            else:
                status_text = "$ {:.2f}".format(item_cost)

            print(number_label + padded_name + " | " + status_text)
            print("  Effect: " + item_info["description"])
            index += 1

        print("0. Leave Upgrade Shop")
        choice = input("\n Enter Upgrade number to buy (or 0 to leave): ").strip().lower()

        if choice.isdigit():
            choice_num = int(choice)

            if choice_num == 0:
                print("Leaving Upgrade Shop")
                break

            elif choice_num >= 1 and choice_num <= len(upgrade_keys):
                selected_key = upgrade_keys[choice_num - 1]
                selected_upgrade = upgrades_catalog[selected_key]
                selected_name = selected_upgrade["name"]
                selected_cost = selected_upgrade["cost"]

                if selected_key in upgrades:
                    print("Your Already Own: "+ selected_name)
                elif selected_cost > bank_balance:
                    amount_needed = round(selected_cost - bank_balance, 2)
                    print("Not Enough Money, Need: ${:.2f}".format(amount_needed) + "more!")
                else:
                    new_balance = round(bank_balance - selected_cost, 2)
                    print("\nPurchase "+ selected_name + "for ${:.2f}".format(selected_cost))
                    print("Remaining Balance will be: ${:.2f}".format(new_balance))
                    confirm = input("Type 'yes' to confirm purchase: ").strip().lower()

                    if confirm == "yes":
                         bank_balance = new_balance
                         upgrades.append(selected_key)
                         print("Purchased " + selected_name)
                    else:
                        print("Purchase Cancelled")
            else:
                print("Invalid Number. Please Choose Between 0 and "+ str(len(upgrade_keys)) + ".")
        else:
            print("Invalid Input. Please Enter a Number")

    return bank_balance, upgrades

#function 8 - get shift settings

def get_shift_settings(shift_num):
    if shift_num == 1:
        num_customers = 3
        min_items = 4
        max_items = 6
        coupons_per_customer = 1
        event_chance = 0.1
        return num_customers, min_items, max_items, coupons_per_customer,event_chance
    elif shift_num == 2:
        num_customers = 4
        min_items = 4
        max_items = 7
        coupons_per_customer = 1
        event_chance = 0.15
        return  num_customers, min_items, max_items, coupons_per_customer, event_chance
    elif shift_num == 3:
        num_customers = 4
        min_items = 5
        max_items = 8
        coupons_per_customer = 2
        event_chance = 0.2
        return num_customers, min_items, max_items, coupons_per_customer, event_chance
    elif shift_num == 4:
        num_customers = 5
        min_items = 6
        max_items = 9
        coupons_per_customer = 2
        event_chance = 0.25
        return num_customers, min_items, max_items, coupons_per_customer, event_chance
    else:
        num_customers = 6
        min_items = 7
        max_items = 11
        coupons_per_customer = 3
        event_chance = 0.3
        return num_customers, min_items, max_items, coupons_per_customer, event_chance


#function 9 - generate customer(min_items, max_items)

def generate_customer(min_items, max_items):
    customer = random.choice(customers)
    cart_size = random.randint(min_items, max_items)
    all_keys = list(store_items.keys())
    cart_keys = []

    spelling_map = {
        "muffin": "muffins",
        "banana": "bananas",
        "cleaningwipes": "wipes",
        "bellpepper": "bellpeppers",
        "porkchops": "pork",
        "bread": "whitebread",
        "tortillachips": "tortillachips"
    }

    safe_preferred = []
    for raw_key in customer["preferred_items"]:
        if raw_key in store_items:
            safe_preferred.append(raw_key)
        elif raw_key in spelling_map:
            mapped_key = spelling_map[raw_key]
            if mapped_key in store_items:
                safe_preferred.append(mapped_key)

    count = 0
    while count < cart_size:
        roll = random.random()
        if roll < 0.6 and len(safe_preferred) > 0:
            picked_key = random.choice(safe_preferred)
        else:
            picked_key = random.choice(all_keys)

        cart_keys.append(picked_key)
        count += 1

    if customer["name"] == "Bill":
        has_frozen = False
        has_produce = False
        for k in cart_keys:
            if store_items[k]["category"] == "frozen":
                has_frozen = True
            if store_items[k]["category"] == "produce":
                has_produce = True
        if has_frozen == False:
            cart_keys[0] = "icecream"
        if has_produce == False and len(cart_keys) > 1:
            cart_keys[1] = "avocados"

    if customer["name"] == "Freezer Man":
        frozen_total = 0
        for k in cart_keys:
            if store_items[k]["category"] == "frozen":
                frozen_total += 1
        if frozen_total < 2 and len(cart_keys) >= 2:
            cart_keys[0] = "icecream"
            cart_keys[1] = "waffles"

    if customer["name"] == "College Kid":
        if "energydrink" not in cart_keys:
            cart_keys[0] = "energydrink"

    return customer, cart_keys

#function 10 - run_scanning_stage

note_str = ""

def run_scanning_stage(cart_keys, upgrades, event_chance):
    time_penalties = 0
    total_items = len(cart_keys)

    print("Stage 1: Item Scanning")
    print("Items to Scan: "+ str(total_items))

    if "sticky_note" in upgrades:
        print("\n[PLU Stick Note - 5 Main Produce Codes]")
        main = ["bananas", "avocados", "apples", "onions", "carrots"]
        for m_key in main:
            if m_key in store_items:
                m_item = store_items[m_key]
                print("  *" + m_item["name"].ljust(20) + " : " + m_item["code"].strip())

    item_num = 0
    for key in cart_keys:
        item_num += 1
        item = store_items[key]
        item_name = item["name"]
        item_code = item["code"]
        item_price = item["price"]
        item_cat = item["category"]

        print("\n[Item " + str(item_num) + " of " + str(total_items) + "]")

        if item.get("is_produce") != True:
            print("Item      :" + item_name + " (" + item_cat + ")")
            print("Barcode   :" + item_code + " | Price: ${:.2f}".format(item_price))
            input("Press Enter to Scan Item")
            print("beep")

        else:
            print("Produce   : " + item_name + "(${:.2f}".format(item_price) + ")")
            print("Type the 4-digit PLU code (or type 'book' to look it up).")

            while True:
                typed = input("PLU Code > ").strip().lower()

                if typed in valid_scan_commands:
                    time_penalties += plu_time_penalty
                    print("Looked Up in the PLU Book (+"+ str(plu_time_penalty) + "s penalty).")
                    print("The PLU Code for " + item_name + " is: " + item_code)
                elif typed == item_code:
                    print("beep")
                    break
                else:
                    if typed.isdigit() == False:
                        print("wrong code, try again (enter 4 digits or 'book') ")
                    elif len(typed) != 4:
                        print("wrong code, try again (code must be 4 digits ")
                    else:
                        print("wrong code, try again")

        if random.random() < event_chance:
            event = random.choice(register_events)

            if event["type"] == "jam" and "laser_scanner" in upgrades:
                print("\n[Dual Laser Barcode Scanner Prevented a Scanner Jam]")
            else:
                print("Register Event")
                print(event["message"])
                print("(+" + str(event["penalty_seconds"]) + " seconds penalty added)")
                time_penalties += event["penalty_seconds"]

                required_action = event["action"].strip().lower()
                while True:
                    player_action = input("Type Command to fix > ").strip().lower()
                    if player_action == required_action:
                        print("Issue Fixed")
                        break
                    else:
                        print("Wrong Command, Type '" + required_action +"' to fix it")

    print("\n Scanning Finished! Total Scanning penalties: +"+str(time_penalties) + "s")
    return time_penalties

# function 11 - run_coupon_stage

def run_coupon_stage(cart_keys, shift_num, coupons_per_customer,customer = None):
    total_discount = 0.0
    stage_mistakes = 0

    total_coupons = coupons_per_customer
    if customer != None:
        if customer["name"] == "Connor":
            total_coupons = coupons_per_customer + 2

    print("Stage 2: Coupon Check")

    print("Active Shift: #" + str(shift_num) + " | Coupons Given: "+ str(total_coupons))

    print("Cart Summary: ")
    listed_keys = []
    for x in cart_keys:
        if x not in listed_keys:
            listed_keys.append(x)
            qty = cart_keys.count(x)
            print("  - " + store_items[x]["name"] + " (x" + str(qty) + ")")


    for x in range(total_coupons):
        coupon = random.choice(coupons)
        c_text = coupon["text"]
        c_item = coupon["item"]
        c_min_qty = coupon["min_qty"]
        c_max_shift = coupon["max_shift"]
        c_discount = coupon["discount"]

        print("\nCoupon #" + str(x + 1) + ": " + c_text)

        is_valid = True
        reasons = []

        if c_item not in cart_keys:
            is_valid = False
            reasons.append("Item Not in cart")

        if cart_keys.count(c_item) < c_min_qty:
            is_valid = False
            reasons.append("Cart Only Has " + str(cart_keys.count(c_item)) + ", But coupon requires " + str(c_min_qty) + ".")

        if shift_num > c_max_shift:
            is_valid = False
            reasons.append("Coupon Expired at Shift #"  + str(c_max_shift) + " current shift is #" + str(shift_num) + ").")

        while True:
            decision = input("Accept Or Reject? ").strip().lower()
            if decision in valid_coupon_commands:
                break
            else:
                print("Invalid Choice. Please type 'accept' or 'reject'.")

        if decision == "accept":
            if is_valid == True:
                total_discount = round(total_discount + c_discount, 2)
                print("Accepted Valid Coupon, Discount -${:.2f}".format(c_discount))
            else:
                stage_mistakes+= 1
                print("Mistake, That Coupon Was Not Valid")
                for r in reasons:
                    print("  *" + r)
        else:
            if is_valid == True:
                stage_mistakes += 1
                print("Mistake That Coupon was Valid and Should've Been Accepted")
            else:
                 print("Good Catch, Rejected Invalid Coupon")
                 for r in reasons:
                     print("  *" + r)

    return round(total_discount, 2), stage_mistakes

# function 12 - run_payment_stage

def run_payment_stage(cart_keys, total_discount, upgrades):
    print("Stage 3: Receipt And Payment")

    subtotal = 0.0

    for key in cart_keys:
        subtotal = round(subtotal + store_items[key]["price"], 2)

    applied_discount = round(total_discount, 2)
    if applied_discount > subtotal:
        applied_discount = subtotal

    after_coupons = round(subtotal - applied_discount, 2)
    if after_coupons < 0:
        after_coupons = 0.0

    tax_rate = 0.07
    tax = round(after_coupons * tax_rate, 2)

    final_total = round(after_coupons + tax, 2)

    print("")
    print(store_name.center(recipt_width))
    print("-" * recipt_width)

    for key in cart_keys:
        raw_name = store_items[key]["name"]
        price_str = "${:.2f}".format(store_items[key]["price"])
        max_name_width = recipt_width - len(price_str) - 1
        trimmed_name = raw_name[:max_name_width]
        left_width = recipt_width - len(price_str)
        print(trimmed_name.ljust(left_width) + price_str)


    print("-" * recipt_width)

    sub_str = "${:.2f}".format(subtotal)
    print("Subtotal".ljust(recipt_width - len(sub_str)) + sub_str)

    disc_str = "-${:.2f}".format(applied_discount)
    print("Coupon Savings".ljust(recipt_width - len(disc_str)) + disc_str)

    tax_str = "${:.2f}".format(tax)
    print("Tax".ljust(recipt_width - len(tax_str)) + tax_str)

    tot_str = "${:.2f}".format(final_total)
    print("Total".ljust(recipt_width - len(tot_str)) + tot_str)
    print("_" * recipt_width)
    print("")

    method = random.choice(["card", "cash"])
    if method == "card":
        print("Customer Pays by card Approved")
        return 0, 0.00

    handed = 0
    for bill in bill_denominations:
        if bill >= final_total:
            handed = bill
            break

    if handed == 0:
        handed = 100
        while handed < final_total:
            handed = handed + 100

    handed = round(float(handed), 2)
    change = round(handed - final_total, 2)

    print("Customer Hands you ${:.2f}".format(handed) + " in cash")

    if change <= keep_change_limit:
        print("Customer Says Keep the Change")
        return 0, change

    if "auto_calc" in upgrades:
        print("Automatic Change Dispenser Gives Exact Change: ${:.2f}".format(change))
        return 0, 0.00


    print("Total is ${:.2f}".format(final_total) + " | Cash Given is ${:.2f}".format(handed))
    typed = input("Enter exact Change due: $").strip().lower()

    try:
         typed_val = float(typed)
         if round(typed_val, 2) == change:
             print("Exact Change Given")
             return 0,0.00
         else:
             print("Wrong Change, The Right Amount was ${:.2f}".format(change))
             return 1, 0.0
    except:
        print("Invalid Input The right amount was ${:.2f}".format(change))
        return 1, 0.0

# function 13 - run_bagging_stage

def run_bagging_stage(cart_keys, upgrades, customer=None):
    print("Stage 4: Grocery Bagging")

    if "heavy_bags" in upgrades:
         max_weight = upgraded_max_bag_weight
    else:
        max_weight = standard_max_bag_weight

    if "insulated_bags" in upgrades:
        bonus_per_bag = upgraded_frozen_bonus
    else:
        bonus_per_bag = frozen_bonus

    if customer != None:
        print("Customer Note \""+ customer["greeting"]+"\"")

    bags = [[]]
    total_items = len(cart_keys)

    item_num = 0
    for key in cart_keys:
        item_num += 1
        item = store_items[key]
        item_name = item["name"]
        item_weight = item["weight"]
        item_cat = item["category"]

        if item.get("fragile") == True:
            fragile_tag = "FRAGILE"
        else:
            fragile_tag = "sturdy"

        while True:
            print("Item "+ str(item_num)+ "/" + str(total_items) + ":" + item_name)
            print("Weight: "+ str(item_weight) + " lbs | Category: " + item_cat + " | " + fragile_tag)
            print("Current Bags: " + str(len(bags)) + " (Max bags: " + str(max_bags_per_order) + ", Max Weight: " + str(max_weight) + " lbs")
            cmd = input("Enter 'add bag <num>', Bag Number 'new', or 'inspect' > ").strip().lower()

            if cmd.startswith("add bag") or cmd.isdigit():
                num_str = cmd.replace("add bag", "").strip()
                if num_str.isdigit():
                    bag_num = int(num_str)
                    if 1 <= bag_num <= len(bags):
                        bags[bag_num - 1].append(key)
                        print("Placed " + item_name + " into bag " + str(bag_num) + ".")
                        break
                    else:
                        print("Invalid Bag Number. Choose between 1 and " + str(len(bags)) + ".")
                else:
                    print("Invalid Command. Try 'add bag 1', 'new', or 'inspect'.")

            elif cmd == "new":
                if len(bags) < max_bags_per_order:
                    bags.append([key])
                    print("Opened Bag " + str(len(bags)) + " and placed " + item_name + " inside")
                    break
                else:
                    print("Bag Limit reached (" + str(max_bags_per_order) + " bags max)")

            elif cmd == "inspect":
                print("Bag Inspection")
                for b in range(len(bags)):
                    bag_w = 0.0
                    bag_names = []
                    for x in bags[b]:
                        bag_w = round(bag_w + store_items[x]["weight"], 2)
                        bag_names.append(store_items[x]["name"] + " (" + store_items[x]["category"] + ")")
                    if len(bag_names) == 0:
                        print("Bag " + str(b + 1) + "[0.0 / " + str(max_weight) + " lbs]: empty")
                    else:
                        print("Bag " + str(b + 1) + " [" + str(bag_w) + " / " + str(max_weight) + " lbs] " + ", ".join(bag_names))
            else:
                print("Invalid Command. Enter a bag number, 'new' or 'inspect'.")

    print("Bagging Inspection")

    stage_mistakes = 0
    frozen_tip_bonus = 0.0

    for b in range(len(bags)):
        bag = bags[b]
        problems = []

        bag_weight = 0.0
        for k in bag:
            bag_weight = round(bag_weight + store_items[k]["weight"],2)

        if bag_weight > max_weight:
            stage_mistakes += 1
            problems.append("Overweight (" + str(bag_weight) + " lbs > " + str(max_weight) + " lbs)")

        crushed = False
        for x in range(len(bag)):
           for y in range(len(bag)):
               if x == y:
                   continue
               item_x = store_items[bag[x]]
               item_y = store_items[bag[y]]
               if item_x["weight"] > heavy_item_limit and item_y.get("fragile") == True:
                   crushed = True

        if crushed == True:
            stage_mistakes += 1
            problems.append("Heavy Item crushed a Fragile item")

        has_hazard = False
        has_fresh = False
        for k in bag:
            cat = store_items[k]["category"]
            if cat in hazard_categories:
                has_hazard = True
            if cat in fresh_categories:
                has_fresh = True

        if has_hazard == True and has_fresh == True:
            stage_mistakes += 1
            problems.append("Hazard/Raw meat mixed with fresh produce/bakery")

        if customer != None:
            if customer["name"] == "Tim":
                has_meat = False
                has_non_meat = False
                for x in bag:
                    if store_items[x]["category"] == "rawmeat":
                        has_meat = True
                    else:
                        has_non_meat = True
                if has_meat == True and has_non_meat == True:
                    stage_mistakes += 1
                    problems.append("Tim asked to keep his raw meat completely separate")

            if customer["name"] == "Deep Cleaner Cory":
                has_chem = False
                has_prod = False
                for x in bag:
                    if store_items[x]["category"] == "household":
                        has_chem = True
                    if store_items[x]["category"] == "produce":
                        has_prod = True
                if has_chem == True and has_prod == True:
                    stage_mistakes += 1
                    problems.append("Cory Asked Not to Mix His cleaning Supplies with His Produce")

            if customer["name"] == "Weekend Baker":
                has_bakery = False
                has_heavy_for_bakery = False
                for k in bag:
                    if store_items[k]["category"] == "bakery":
                        has_bakery = True
                    if store_items[k]["weight"] > 3.0:
                        has_heavy_for_bakery = True
                if has_bakery == True and has_heavy_for_bakery == True:
                    stage_mistakes += 1
                    problems.append("Weekend Baker's baked goods were packed with heavy items")

        frozen_count = 0
        for x in bag:
            if store_items[x]["category"] == "frozen":
                frozen_count += 1

        if frozen_count >= 2:
            frozen_tip_bonus = round(frozen_tip_bonus + bonus_per_bag, 2)

        if len(problems) == 0:
            print("Bag " + str(b + 1) + " (" + str(bag_weight) + " lbs): Ok")
        else:
            print("Bag " + str(b + 1) + " (" + str(bag_weight) + " lbs): problem")
            for p in problems:
                print("  -->" + p)

    if customer != None and customer["name"] == "Bill":
        paired_properly = False
        for bag in bags:
            found_frozen = False
            found_produce = False
            for k in bag:
                if store_items[k]["category"] == "frozen":
                    found_frozen = True
                if store_items[k]["category"] == "produce":
                    found_produce = True
            if found_frozen == True and found_produce == True:
                 paired_properly = True
        if paired_properly == False:
            stage_mistakes += 1
            print("Special Request Missed: Bill Asked to put his frozen items with his produce (+1 Mistake)")

    if customer != None and customer["name"] == "Freezer Man":
       bags_with_frozen = 0
       for bag in bags:
           has_f = False
           for k in bag:
               if store_items[k]["category"] == "frozen":
                   has_f = True
           if has_f == True:
               bags_with_frozen += 1
       if bags_with_frozen == 1:
           frozen_tip_bonus = round(frozen_tip_bonus + 2.00, 2)
           print("Freezer Man Bonus: All Frozen Meals packed together, (+$2.00 Tip)")

    return stage_mistakes, round(frozen_tip_bonus, 2)

# function 14 - calculate_shift_grade

def calculate_shift_grade(shift_mistakes, elapsed_time):
    if shift_mistakes == 0 and elapsed_time <= 60.0:
        return "S", 10.00
    elif shift_mistakes == 0:
        return "A", 5.00
    elif shift_mistakes <= 2:
        return "B", 2.00
    elif shift_mistakes <= 4:
        return "C", 0.0
    else:
        return "F", 0.00

#Function 15 - play_shift

def play_shift(
        bank_balance ,
        shift_num,
        total_customers_served,
        alltime_tips_earned,
        total_mistakes,
        best_shift_time,
        upgrades
):
    customer_count, min_items,max_items, coupons_count, event_chance = get_shift_settings(shift_num)

    print("Starting Shift #"+ str(shift_num))

    print("Customers Today: " + str(customer_count))
    print("Items per cart: " + str(min_items) + " - " + str(max_items))
    print("Coupons  / Customer: "+ str(coupons_count))
    print("Event_Chance : "+ str(event_chance * 100) + "%")


    shift_mistakes = 0
    time_penalties = 0
    shift_tips = 0.0
    start = time.time()

    for x in range(customer_count):
        customer, cart_keys = generate_customer(min_items, max_items)
        print("Customer " + str( x +1 ) + " of "+ str(customer_count) + ": " + customer["name"])

        print("\"" + customer["greeting"] + "\"")

        scan_penalties = run_scanning_stage(cart_keys,upgrades, event_chance)
        time_penalties += scan_penalties

        total_discount, coupon_mistakes = run_coupon_stage(cart_keys, shift_num,coupons_count, customer)
        pay_mistakes, change_tip = run_payment_stage(cart_keys, total_discount, upgrades)
        bag_mistakes, frozen_bonus_earned = run_bagging_stage(cart_keys, upgrades, customer)

        customer_mistakes = coupon_mistakes + pay_mistakes + bag_mistakes
        shift_mistakes += customer_mistakes
        total_customers_served += 1

        if customer_mistakes == 0:
            print(customer["name"] + ": \"" + customer["happy_outro"] + "\"")
            customer_tip = round((change_tip + frozen_bonus_earned) * customer["tipmult"], 2)
            shift_tips = round(shift_tips + customer_tip , 2)
            print("Customer Tip Earned ${:.2f}".format(customer_tip))

        else:
            print(customer["name"] + ": \"" + customer["angry_outro"] + "\"")
            print("Customer Mistakes: " + str(customer_mistakes) + " NO Tips Earned")
            if customer["name"] == "Rordan Gamsey":
                shift_mistakes += 1
                print("Rordan Ramsey Reported You!, (+1 Extra Mistake)")


    elapsed = round((time.time()-start) + time_penalties,2)
    if "express_belt" in upgrades:
            elapsed = round(elapsed - express_time_belt_reduction, 2)
            if elapsed < 0:
                elapsed = 0.0
    letter, grade_bonus = calculate_shift_grade(shift_mistakes, elapsed)

    pay = round(base_shift_tip - (shift_mistakes * mistake_deduction) + shift_tips + grade_bonus, 2)
    if pay < 0:
       pay = 0.0

    bank_balance = round(bank_balance + pay, 2)
    alltime_tips_earned = round(alltime_tips_earned + pay, 2)
    total_mistakes += shift_mistakes

    if elapsed < best_shift_time:
        best_shift_time = elapsed

    shift_num += 1

    print("Total Shift Time: {:.2f}".format(elapsed)+ "s")
    print("Total Mistakes: " + str(shift_mistakes))
    print("Shift Grade: " + letter + " (Bonus: ${:.2f}".format(grade_bonus) + ")")
    print("Customer Tips: ${:.2f}".format(shift_tips))
    print("Total Shift Pay: ${:.2f}".format(pay))
    print("New Bank Balance: ${:.2f}".format(bank_balance))

    return (
        bank_balance,
        shift_num,
        total_customers_served,
        alltime_tips_earned,
        total_mistakes,
        best_shift_time,
        upgrades,
    )


# function 16 - show_cashier_handbook

def show_cashier_handbook():
    print("SUPER MART CASHIER HANDBOOK")

    print("\n[1] Stage 1: Scanning & Register Events")
    print("   - Regular items show a barcode: press enter to scan.")
    print("   - Produce items have NO barcode: enter their 4 digit Plu Code")
    print("   - Type 'book' during produce scanning to look up the code (+5 seconds penalty)")
    print("   - If a register event pops up, type the exact fix word shown.")

    print("\n[2] Stage 2: Coupon Validation")
    print(" - Only Type 'accept' if all 3 rules passed")
    print(" 1. The required item is actually in the customer's cart.")
    print(" 2. The cart Quantity is at least the coupon's minimum quantity")
    print(" 3. The Current shift number is not above the coupon's expiration shift")

    print("\n[3] Stage 3: Payment and Change")
    print(" - Card Payments process automatically")
    print(" - If cash change is $0.25 or less, the customer lets you keep it as a tip")
    print(" - Otherwise, type the exact change owed")

    print("\n[4] Stage 4: Bagging Rules")
    print(" - Standard Bag limit is 15.0 lbs (22.0 lbs with the Heavy Bag Upgrade)")
    print(" - Never put a heavy item (over 4.0 lbs) with a fragile item")
    print(" - Never Mix raw meat or household chemicals with produce or bakery items")
    print(" - Put 2 or more Frozen items in the same bag for +$1.50 tip bonus")
    print(" - Pay Close attention to each customer's greeting for a special requests")

    print("\n[5] Stage 5: Shift Grading")
    print(" - Grade S: 0 Mistakes and 60.0s or faster (+$10.00 bonus)")
    print(" - Grade A: 0 Mistakes and over 60.0s (+$5.00 bonus)")
    print(" - Grade B: 1-2 Mistakes (+$2.00 bonus")
    print(" - Grade C: 3-4 Mistakes (+$0.00 penalty)")
    print(" - Grade F: 5+ Mistakes (-$5.00 penalty, caps at $0.00)")


main_menu = {
    "1.": "Start Shift",
    "2.": "Upgrade Shop",
    "3.": "Store Catalog & Plu Master Key",
    "4.": "Career Stats",
    "5.": "Cashier Handbook",
    "6.": "Reset Save",
    "7.": "Quit"
}


# stress test
#for test_round in range(500):
    #test_cust, test_cart = generate_customer(4,11)

    #for k in test_cart:
        #item_check = store_items[k]
       # _ = item_check["name"]
        #_ = item_check["price"]
       # _ = item_check["weight"]
       # _ = item_check["category"]
        #_ = item_check["code"].strip()

#for c_info in coupons:
    # _ = store_items[c_info["item"]]
#print("Stress Test Passed All 115, 25 Coupons and, 20 Customers verified")


save_path = save_file_name

load_game(save_path)

while True:
    print("\n Main Menu (Shift #" + str(shift_num) + " | Balance: ${:.2f}".format(bank_balance) + ")")
    for menu_key in main_menu:
        print(menu_key + " " + main_menu[menu_key])

    choice = input("\nChoose an Option(1-7): ").strip().lower()

    if choice == "1":
        (
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        ) = play_shift(
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        )

        save_game(
            save_path,
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        )

    elif choice == "2":
        bank_balance, upgrades = open_upgrade_shop(bank_balance, upgrades)
        save_game(
            save_path,
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        )

    elif choice == "3":
        show_plu_master_key()

    elif choice == "4":
        show_career_stats(
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        )
    elif choice == "5":
        show_cashier_handbook()
    elif choice == "6":
        (
            bank_balance,
            shift_num,
            total_customers_served,
            alltime_tips_earned,
            total_mistakes,
            best_shift_time,
            upgrades
        ) = reset_save(save_path)

    elif choice == "adminpasscash":
        amt_str = input("Enter Test Cash Amount ($): ").strip()
        try:
            bonus = round(float(amt_str), 2)
            bank_balance = round(bank_balance + bonus, 2)
            print("Added ${:.2f}".format(bonus) + " New balance: ${:.2f}".format(bank_balance))
            save_game (
                save_path,
                bank_balance,
                shift_num,
                total_customers_served,
                alltime_tips_earned,
                total_mistakes,
                best_shift_time,
                upgrades
            )
        except ValueError:
            print("Invalid Number")


    elif choice == "7":
        break

    else:
        print("Invalid Choice")

print("\nThanks For playing " + store_name + "! GoodBye.")
input("Press Enter to exit")