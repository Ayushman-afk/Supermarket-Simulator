import time
import random

#- Pregame defined variables. (total - 115) (80 items of produce) (25 coupons defined.)

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
heavy_item_limit = 4.0 #(lbs) items above this crush items fragile = True
max_bags_per_order = 6
frozen_bonus = 1.5 #($1.50 tip per bag with 2+ frozen category item)
upgraded_frozen_bonus = 3.0 #($3 tip bonus when insulated bag upgrade is bought