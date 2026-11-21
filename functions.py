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
        upgrades
):
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
                    
