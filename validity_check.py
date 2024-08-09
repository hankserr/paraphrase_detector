"""
0.2.8
0.2.8
Program to take in a sentence and return true if it contains the correct date variations
and false if it doesn't.
"""

import pdb
import requests
from dateutil import parser
from date_data import generate_date_variations
import sys
from datetime import datetime, timedelta
import pandas as pd
import re
import random

############################## GLOBAL VARIABLES ##############################

# date_ = [get_random_date() for _ in range(3)]
# global dates array used for populating test_list and check_dates_in_strings

def get_dates():
    return dates_

# A function that uses parser from dateutil to return a date from a string
def get_date(date_string):
    try:
        date_obj = parser.parse(date_string, fuzzy=True)
        return str(date_obj)[:10]
    except ValueError:
        return None

def convert_month_to_number(month):
    months = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    return months.get(month, "00")

def check_date(sentence, correct_date = [], check=False):

    # Regular expression to match dates in the format MonthDDYYYY or YYYYMonthDD
    pattern = r'\b(?:\d{4}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}\d{4})\b'

    # Search for the date in the sentence
    match = re.search(pattern, sentence.lower())

    if match:
        found_date = match.group(0)

        # Determine the format of the found date
        if found_date[:4].isdigit():
            found_month = convert_month_to_number(found_date[4:7])
            found_day = found_date[7:9]
            found_year = found_date[:4]
        else:
            found_month = convert_month_to_number(found_date[:3])
            found_day = found_date[3:5]
            found_year = found_date[5:]

        found_date_formatted = f"{found_year}-{found_month}-{found_day}"
        # Compare the found date with the correct date
        if check is True: return found_date_formatted in correct_date
        else: return found_date_formatted
    else:
        # If no date found, return False
        if check is True: return False
        else: return None

# A function to test date_in_string
# It generates variations using date_data.py and checks if date_in_string returns true
# For each variation, checking what variations are missed
def test_date_in_string():
    # pdb.set_trace()
    date = get_date("2021-01-01")
    variations = generate_date_variations(date)
    missed_variations = []
    for variation in variations:
        test_str = str("The birthday party is on " + variation + ", please do not be late")
        if not date == get_date(test_str):
            missed_variations.append(variation)
    return missed_variations

# Function to test check_dates_in_strings
def test_check_dates_in_strings():
    test_list = populate_test_list()
    check_dates_in_strings(test_list)
    return

# Function to get random date
def get_random_date(start_date="1999-01-01", end_date="2099-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    random_days = random.randint(0, (end - start).days)
    random_date = start + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

# Function to populate a test list
# Shift is used to mix up the variation sentence pairs
def populate_test_list(shift=0, opt_array=None, test=False):
    global dates_
    dates_ = [get_random_date() for _ in range(3)]
    # Create array of sentences from reading test_set.csv
    test_list = []
    with open("test_set.csv", "r") as file:
        for line in file:
            test_list.append(line.strip())
    variations = [generate_date_variations(dates_[i]) for i in range(3)]
    # if opt_array is not None: use opt_array instead of variations
    if opt_array is not None:
        variations = opt_array
    for index in range(len(test_list)):
        if not test:
            # locate the <date> tag and replace it with a random variation from variations
            test_list[index] = test_list[index].replace("<date_1>", variations[0][(index + shift) % len(variations)])
            test_list[index] = test_list[index].replace("<date_2>", variations[1][(index + shift + 1) % len(variations)])
            test_list[index] = test_list[index].replace("<date_3>", variations[2][(index + shift + 2) % len(variations)])
        else:
            rand = random.uniform(0, 1)
            if rand < 0.5:
                test_list[index] = test_list[index].replace("<date_1>", variations[0][(index + shift) % len(variations)])
                test_list[index] = test_list[index].replace("<date_2>", variations[1][(index + shift + 1) % len(variations)])
                test_list[index] = test_list[index].replace("<date_3>", variations[2][(index + shift + 2) % len(variations)])
            elif rand < 0.75:
                test_list[index] = test_list[index].replace("<date_1>", variations[1][(index + shift) % len(variations)])
                test_list[index] = test_list[index].replace("<date_2>", variations[2][(index + shift + 1) % len(variations)])
                test_list[index] = test_list[index].replace("<date_3>", variations[0][(index + shift + 2) % len(variations)])
            else:
                test_list[index] = test_list[index].replace("<date_1>", variations[2][(index + shift) % len(variations)])
                test_list[index] = test_list[index].replace("<date_2>", variations[0][(index + shift + 1) % len(variations)])
                test_list[index] = test_list[index].replace("<date_3>", variations[1][(index + shift + 2) % len(variations)])

    return test_list

# Helper function for find_dates()
def remove_duplicates_preserve_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Finds dates in a string
def find_dates(text):
    parts = text.split()
    found_dates = []
    # for each grouping of 3 words, check if it is a date
    for i in range(len(parts) - 2):
        part = " ".join(parts[i:i+3])
        date = check_date(part)
        if date is None:
            date = get_date(part)
        if date is not None:
            found_dates.append(date)

    date = get_date(" ".join(parts[-2:]))
    if date is not None:
        found_dates.append(date)

    return remove_duplicates_preserve_order(found_dates)

# Given a list of strings, check if dates are in the strings and dates are correct
# Output is a list of strings containing bad dates
def check_dates_in_strings(input_list, print_output=True):
    bad_dates = []
    good_dates = []
    flagged_count = 0
    # correct_date = get_date(date_)
    count = 0
    for item in input_list:
        count += 1
        item_ = "temp " + item
        dates = find_dates(item_)
        if len(dates) > 3 and any(dates[i] in dates_ for i in range(len(dates))): # check if dates are in the list
            good_dates.append({"sentence": item, "date found": "Partial", "date": dates, "Flagged": "Yes"})
            flagged_count += 1
        elif all(dates[i] == dates_[i] for i in range(len(dates))): # check if dates are correct
            good_dates.append({"sentence": item, "date found": "Yes", "date": dates, "Flagged": "No"})
        else:
            bad_dates.append({"sentence": item, "date found": "No", "date": dates, "Flagged": "No"})
    if print_output:
        print_bad_dates(bad_dates)
    else:
        return bad_dates, good_dates, flagged_count
    return


# Function to get results from check_dates_in_strings
def run_check_dates_in_strings(test_list = populate_test_list()):
    bad_dates, good_dates, flagged = check_dates_in_strings(test_list, print_output=False)
    passing_threshold = 6
    if len(bad_dates) > passing_threshold:
        print(f"Test failed: {len(bad_dates)} bad dates found ({len(good_dates) / len(test_list) * 100}%)")
        print(f"Passing Theshold: {passing_threshold}")
        print(f"\nFlagged: {flagged}")
        for item in bad_dates:
            print(item)
    else:
        print(f"Test passed: threshold ({passing_threshold}) reached")

# Make post request to localhost
def make_post_request(text, variant_count):
    url = 'http://localhost:8080/api/internal/variants'
    headers = {'Content-Type': 'application/json'}
    data = {
        'text': text,
        'variantCount': variant_count
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# process the model json response
# return list of variant sentences
# input: list of original sentences, variant count
def process_report(texts, variant_count):
    variants = []
    for text in texts:
        response = make_post_request(text, variant_count)
        try:
            for variant in response[0]['variants']:
                variants.append(variant)
        except:
            print(f"Bad Response: {response}\nFrom: {text}\n\n")
    return variants

def test_model(path):
    model_in = populate_test_list()
    model_out = process_report(model_in, 9) # default variant count = 9 per input
    run_check_dates_in_strings(model_out)

# Print bad_dates list
def print_bad_dates(bad_dates):
    # Make bad_dates into pandas dataframe
    bad_dates = pd.DataFrame(bad_dates)
    # pdb.set_trace()
    if len(bad_dates) == 0:
        print("All dates are correct.")
    else:
        print(len(bad_dates), "bad date(s) found:")
        # print bad_dates dataframe
        print(bad_dates)
        bad_dates.to_csv('paraphrase_dataset_dates.csv', index=False)
    return

# main: test get_date function
def main():
    # Check if file ran with -test flag, else check if file ran with -list flag
    if len(sys.argv) == 2 and sys.argv[1] == "-test":
        missed_variations = test_date_in_string()
        if len(missed_variations) == 0:
            print("All variations are found.")
        else:
            print("The following variations are not found:")
            for variation in missed_variations:
                print(variation)
        test_check_dates_in_strings()

    elif len(sys.argv) == 2 and sys.argv[1] == "-list":
        test_list = populate_test_list()
        for item in test_list:
            print(item)


    elif len(sys.argv) == 2 and sys.argv[1] == "-check":
        with open('output', 'w') as file:
            file.write('\n' + "tester" + '\n')
            test_list = populate_test_list()
            output = check_dates_in_strings(test_list, False)
            for item in output:
                file.write(str(item["sentence"] + '\t' + item["date found"] + '\t' + item["date"] + '\n'))
            file.write('\n' + "closing" + '\n')
    elif len(sys.argv) == 3 and sys.argv[1] == "-run":
        test_model(sys.argv[2])
    else:
        print("Usage: python3 validity_check.py -test")
        print("Usage: python3 validity_check.py -list")
        print("Usage: python3 validity_check.py -check")
        print("Usage: python3 validity_check.py -run [path to model]")

    return

# Function: input two pandas dataframes.
# Output: insert the entire second dataframe at the halfway point of the first dataframe
def insert_at_halfway(df, dates):
    half = int(len(df) / 2)
    df1 = df.iloc[:half]
    df2 = df.iloc[half:]
    df = pd.concat([df1, dates, df2], ignore_index=True)
    return df

if __name__ == "__main__":
    main()
