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
        save_game(filepath, 0.00, 1, 0, 0.00, 0, 999.99)
        return 0.00, 1, 0, 0.00, 0, 999.99, []

    try:
        file_reader = open(filepath, "r")
        lines = file_reader.readline()
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

    answer = intput("\nType 'yes' to erase everything and reset: ").strip().lower()

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

    if total_customer_served > 0:
        mistakes_per_customer = round(total_mistakes / total_customer_served, 2)
    else:
        mistakes_per_customer = 0.00

    if completed_shits > 0:
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
        print("Owned Upgrades (" + str(len(upgrades)) + " of "+ str(len(upgrade_catalog) + "):"))

        for up_key in upgrade:
            if up_key in upgrade_catalog:
                up_name = upgrade_catalog[up_key]["name"]
                up_desc = upgrade_catalog[up_key]["description"]
                print("  *" + up_name + " - " + up_desc)
            else:
                print("  *" + up_key)
    print("\n")

#function 6 - plu master key

def show_plu_master_key():
    print("Plu Master Key")
    print("Produce Name       | Plu Code | Price | Notes|")

    produce_keys = []

    for key in store_items:
        item = store_items[key]
        if item.get("is_produce") == True:
            produce_keys.append(key)
            padded_name = item["name"].ljust(20)
            clean_code = item["code"].strip().ljust(8)
            price_str = ("$ {:.2f}".format(item["price"])).ljust(6)

            if item.get("fragile") == True:
                note_str = "FRAGILE"
            else:
                noter_str = "Sturdy (" + str(item["weight"]) + " lbs"

            print(padded_name + " | " + clean_code + " | " + price_str + " | " + note_str)


        print("Total Produce Items: " + str(len(produce_keys)))

        if len(produce) > 0:
            practice_choice = input("\nType 'quiz' to practice Plu Codes (or press enter to return): ").strip().lower()
            if practice_choice == "quiz":
                correct_count = 0
                total_question = 3
                for q_num in range(total_questions):
                    random_key = random.choice(produce_keys)
                    random_item = random.choice[random_key]
                    expected_code = random_item["code"].strip()
                    user_guess = input("Question " + str(q_num + 1) + ": Enter Plu Code for "+ random_item["name"] + ": ").strip()
                    if user_guess == expected_code:
                        print("Correct")
                        correct_count += 1
                    else:
                        print("Wrong, The Plu Code for " + random_item["name"] + "is " + expected_code + ".")
                print("Quiz Finished, Score = " + str(correct_count) + "out of " + str(total_question))


# function 7 - open Upgrade Shop

def open_upgrade_shop(bank_balance, upgrades):
    while True:
        print("Super Mart Upgrade Shop")
        print("Available Bank Balance: ${}".format(bank_balance))
        print("Upgrades Owned: "+ str(len(upgrade)) + "/" + str(len(upgrade_keys)))

        index = 0

        while index < len(upgrade_keys):
            key = upgrade_keys[index]
            item_info = upgrade_catalog[key]
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

        if choice.isdigit == True:
            choice_num = int(choice)

            if choice_num == 0:
                print("Leaving Upgrade Shop")
                break

            elif choice_num >= 1 and choice_num <= len(upgrade_keys):
                selected_key = upgrade_keys[choice_num - 1]
                selected_upgrade = upgrade_catalog[selected_key]
                selected_name = selected_upgrade["name"]
                selected_cost = select_upgrade["cost"]

                if selected_key in upgrades:
                    print("Your Already Own: "+ selected_name)
                elif selected_cost > bank_balance:
                    amount_needed = round(selected_cost - bank_balance, 2)
                    print("Not Enough Money, Need: ${:.2f}".format(amount_needed) + "more!")
                else:
                    new_balance = round(bank_balance - selected_cost, 2)
                    print("\nPurchase "+ selected_name + "for ${:.2f}".format(selected_cost))
                    print("Remaining Balance will be: ${:.2f}".format(new_balance))
                    confirm = input("Type 'yes' to confirm purchaseL ").strip().lower()

                    if confirm == "yes":
                         bank_balance = new_balance
                         upgrades.append(selected_key)
                         print("Purchased " + selected_name)
                    else:
                        print("Purchase Cancelled")
            else:
                print("Invalid Number. Please Choose Between 0 and "+ str(len(upgrade_keys) + "."))
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
        return  num_customers, min_item, max_items, coupons_per_customer, event_chance
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
        return num_customer, min_items, max_items, coupons_per_customer, event_chance
    else:
        num_customers = 6
        min_items = 7
        max_items = 11
        coupons_per_customer = 3
        event_chance = 0.3
        return num_customer, min_items, max_items, coupons_per_customer, event_chance


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
                safe-preferred.append(mapped_key)


     count = 0
     while count < cart_size:
         roll = random.random()
         if roll < 0.6 and len(safe_preferred) > 0:
             picked_key  = random.choice(safe_preferred)
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
                    print("Looked Up in the PLU Book (+"+ str(plu_time_penalty) + "s penalty.")
                    print("The PLU Code for" + item_name + "is:" + item_code)
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
                print("(+" + str(event["penalty_seconds"]) + " seconds penalty addded)")
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
        listed_keys.append(x)
        qty = cart.keys.count(x)
        print("  - " + store_items[x]["name"] + " (x" + str(qty) + ")")


    for x in range(total_coupons):
        coupon = random.choice(coupons)
        c_text = coupon["text"]
        c_item = coupon["item"]
        c_min_qty = coupon["min_qty"]
        c_max_shift = coupon["max_shift"]
        c_discount = coupon["discount"]

        print("\nCoupon #" + str(x + 2) + ":" + c_text)

        is_valid = True
        reasons = []

        if c_item not in cart_keys:
            is_valid = False
            reasons.append("Item Not in cart")

        if cart_keys.count(c_item) < c_min_qty:
            is_valid = False
            reasons.append("Cart Only Has " + str(cart_keys.count(c_item)) + ", But coupon requires" + str(c_min_qty) + ".")

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
                stage_mistakes += 1
                print("Mistake, That Coupon Was Not Valid")
                for x in reasons:
                    print("  *" + r)
        else:
            if is_valid == True:
                stage_mistakes += 1
                print("Mistake That Coupon was Valid and Should've Been Accepted")
            else:
                 print("Good Catch, Rejected Valid Coupon")
                 for x in reasons:
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
    print(store.name.center(recipt_width))
    print("-" * recipt_width)

    for key in cart_keys:
        raw_name = store_items["key"]["name"]
        price_str = "${:.2f}".format(store_items["key"]["price"])
        max_name_width = recipt_width - len(price_str) - 1
        trimmed_name = raw_name[:max_name_width]
        left_width = recipt_width - len(price_str)
        print(trimmed_name.ljust(left_width) + price_str)


    print("-" * recipt_width)

    sub_str = "${:.2f}".format(subtotal)
    print("Subtotal".ljust(recipt_width - len(sub_str)) + sub_str)

    disc_str = "-${:.2f}".format(applied_discount)
    print("Coupon Savings".ljust(recipt_width - len(disc-str)) + disc_str)

    tax_str = "${:.2f}".format(tax)
    print("Tax".ljust(recipt_width - len(tax_str)) + tax_str)

    tot_str = "${:.2f}".format(final_total)
    print("Total".ljust(recipt_width - len(tot-str)) + tot_str)
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

    print("Customer Hands you ${:.2f}".format(handed) + "in cash")

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
             return 0.00
         else:
             print("Wrong Change, The Right Amount was ${:.2f}".format(change))
             return 1, 0.0
    except:
        print("Invalid Input The right amount was ${:.2f}".format(change))
        return 1, 0.0

# function 13 - run_bagging_stage




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
    print("Coupons / Customer: "+ str(coupon_count))
    print("Event_Chance : "+ str(event_chance * 100) + "%")


    shift_mistakes = 0
    time_penalties = 0
    shift_tips = 0.0
    start = time.time()

    for x in range(customer_count):
        customer, cart_keys = generate_customer(min_items, max_items)
        print("Customer " + str( x +1 ) + " of "+ str(customer_count) + ": " + customer["name"])

        print("\"" + customer["greeting"] + "\"")

        scan_penalties = run_scanning_stage(cart_keys_upgrades, event_chance)
        time_penalties += scan_penalties

        total_discount, coupon_mistakes = run_coupon_stage(cart_keys, shift_num,coupons_count, customer)
        pay_mistakes, change_tip = run_payment_stage(cart_keys, total_discount, upgrades)
        bag_mistakes, frozen_bonus_earned = run_bagging_stage(cart_keys, upgrades, customer)

        customer_mistakes = coupon_mistakes + pay_mistakes + bag_mistake
        shift_mistakes += customer_mistakes
        total_customers_served += 1

        if customer_mistakes == 0:
            print(customer["name"] + ": \"" + customer["happy_outro"] + "\"")
            customer_tip = round((change_tip + frozen_bonus_earned) * customer["tipmult"], 2)
            shift_tips = round((shift_tips + customer_tip , 2))
            print("Customer Tip Earned ${:.2f}".format(customer_tip))

        else:
            print(customer["name"] + ": \"" + customer["angry_outro"] + "\"")
            print("Customer Mistakes: " + str(customer_mistakes) + "NO Tips Earned")
            if customer["name"] == "Rordan Gamsey":
                shift_mistake += 1
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
    print("Total Shift Pay: ${:.2f".format(pay))
    print("New Bank Balance: ${:.2f}".format(bank_balance))