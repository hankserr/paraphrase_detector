import re
from date_data import generate_date_variations
from validity_check import get_date, check_date, print_bad_dates
from datetime import datetime, timedelta
import random
import spacy
import pdb

nlp = spacy.load("en_core_web_sm")

def remove_duplicates_preserve_order(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Mask the dates
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

# Function to get random date
def get_random_date(start_date="1999-01-01", end_date="2099-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    random_days = random.randint(0, (end - start).days)
    random_date = start + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")

# Function to populate a test list
# Shift is used to mix up the variation sentence pairs
def populate_test_list(shift=0, opt_array=None):
    global dates_
    # dates_ = [get_random_date() for _ in range(3)]
    dates_ = ["2021-01-01", "2021-01-02", "2021-01-03"]
    # Create array of sentences from reading test_set.csv
    test_list = []
    with open("test_set.csv", "r") as file:
        for line in file:
            test_list.append(line.strip())
    variations = [generate_date_variations(dates_[i]) for i in range(3)]
    # if opt_array is not None: use opt_array instead of variations
    if opt_array is not None:
        variations = opt_array
    pdb.set_trace()
    for index in range(len(test_list)):
        # locate the <date> tag and replace it with a random variation from variations
        test_list[index] = test_list[index].replace("<date_1>", variations[0][(index + shift) % len(variations[0])])
        test_list[index] = test_list[index].replace("<date_2>", variations[1][(index + shift + 1) % len(variations[1])])
        test_list[index] = test_list[index].replace("<date_3>", variations[2][(index + shift + 2) % len(variations[2])])

    return test_list


# Given a list of strings, check if dates are in the strings and dates are correct
# Output is a list of strings containing bad dates
def check_dates_in_strings(input_list, print_output=True):
    bad_dates = []
    good_dates = []
    # correct_date = get_date(date_)
    count = 0
    for item in input_list:
        count += 1
        item_ = "temp " + item
        dates = find_dates(item_)
        if len(dates) > 3 and any(dates[i] in dates_ for i in range(len(dates))): # check if dates are in the list
            good_dates.append({"sentence": item, "date found": "Partial", "date": dates, "Flagged": "Yes"})
        elif all(dates[i] == dates_[i] for i in range(len(dates))): # check if dates are correct
            good_dates.append({"sentence": item, "date found": "Yes", "date": dates, "Flagged": "No"})
        else:
            bad_dates.append({"sentence": item, "date found": "No", "date": dates, "Flagged": "No"})
    if print_output:
        print_bad_dates(bad_dates)
    else:
        return bad_dates, good_dates
    return

def test_check_dates_in_strings():
    test_list = populate_test_list()
    # for item in test_list:
    #     print(item)
    bad_dates, good_dates = check_dates_in_strings(test_list, print_output=False)
    if len(bad_dates) > 0:
        print(f"Test failed: {len(bad_dates)} bad dates found ({len(good_dates) / len(test_list) * 100}%)")
        for item in bad_dates:
            print(item)
    if len(bad_dates) == 0:
        print("Test passed: no bad dates found")

# test_check_dates_in_strings()
foo = find_dates("Our annual family reunion is set for 2052-04-19, at the lake house.")
print(foo == ['2052-04-19'])