import random
import time
import os
import sys
from game_data import *

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