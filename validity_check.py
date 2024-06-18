"""
0.1.0
Program to take in a sentence and return true if it contains the correct date variations
and false if it doesn't.
"""

import pdb
from dateutil import parser
from date_data import generate_date_variations
import sys
from datetime import datetime

# A function that uses parser from dateutil to return a date from a string
def get_date(date_string):
    try:
        date_obj = parser.parse(date_string, fuzzy=True)
        return str(date_obj)[:10]
    except ValueError:
        return None

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

# Function to populate a test list
# Shift is used to mix up the variation sentence pairs
def populate_test_list(date_="2021-01-01", shift=0):
    test_list = [
        "<date> marks the start of our company's fiscal year.",
        "<date> is when the new semester begins for most universities.",
        "<date> contains the deadline for all submissions to the journal.",
        "On <date>, the committee will meet to discuss the new policy.",
        "By <date>, we need to finalize our travel arrangements.",
        "From <date>, the store will be closed for renovations.",
        "The concert will take place on <date>, in the evening.",
        "The book release is scheduled for <date>, so mark your calendars.",
        "Our vacation begins the day of <date>, so pack your bags.",
        "The project needs to be completed by <date>.",
        "We will celebrate her retirement on <date>.",
        "The software update is scheduled for <date>.",
        "The birthday party is on <date>, please do not be late",
        "<date> is the deadline for all scholarship applications.",
        "<date> marks the first day of the annual technology conference.",
        "On <date>, the board will announce the new executive appointments.",
        "The new product launch is scheduled for <date>, with a press event.",
        "By <date>, all employees must complete the mandatory training.",
        "From <date>, the exhibition will be open to the public.",
        "<date> is when the marathon will take place, starting at dawn.",
        "<date> is the release date for the highly anticipated movie.",
        "Our annual family reunion is set for <date>, at the lake house.",
        "The tax filing deadline is on <date>, so submit your returns by then.",
        "The conference call to discuss the merger has been scheduled for <date> in the afternoon.",
        "Please ensure all documents are submitted by the deadline of <date> to avoid penalties.",
        "Preparations for the festival, happening <date>, should be finalized by the end of this week.",
        "The award ceremony, planned for <date>, will be held at the downtown auditorium.",
        "Make sure to RSVP by <date> to secure your spot at the workshop.",
        "Construction of the new office building is expected to begin around <date>.",
    ]
    date = get_date(date_)
    variations = generate_date_variations(date)
    for index in range(len(test_list)):
        # locate the <date> tag and replace it with a random variation from variations
        test_list[index] = test_list[index].replace("<date>", variations[(index + shift) % len(variations)])
    return test_list

# Given a list of strings, check if dates are in the strings and dates are correct
# Output is a list of strings containing bad dates
def check_dates_in_strings(input_list, date_="2021-01-01", print_output=True):
    bad_dates = []
    correct_date = get_date(date_)
    for item in input_list:
        date = get_date(item)
        if date is None or date != correct_date:
            bad_dates.append(item)
    if print_output:
        print_bad_dates(bad_dates)
    return

# Print bad_dates list
def print_bad_dates(bad_dates):
    if len(bad_dates) == 0:
        print("All dates are correct.")
    else:
        print(len(bad_dates), "bad date(s) found:")
        for bad_date in bad_dates:
            print(bad_date)
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
    elif len(sys.argv) == 2 and sys.argv[1] == "-list":
        test_list = populate_test_list()
        for item in test_list:
            print(item)
    else:
        print("Usage: python3 validity_check.py -test")
        print("Usage: python3 validity_check.py -list")

    return

if __name__ == "__main__":
    main()
