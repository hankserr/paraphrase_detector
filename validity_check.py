"""
0.2.7
Program to take in a sentence and return true if it contains the correct date variations
and false if it doesn't.
"""

import pdb
from dateutil import parser
from date_data import generate_date_variations
import sys
from datetime import datetime
import pandas as pd
import re


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

def check_date(sentence, correct_date):

    # Regular expression to match dates in the format MonthDDYYYY or YYYYMonthDD
    pattern = r'\b(?:\d{4}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\d{2}\d{4})\b'

    # Search for the date in the sentence
    match = re.search(pattern, sentence)

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
        return found_date_formatted == correct_date
    else:
        # If no date found, return False
        return False

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

# Function to populate a test list
# Shift is used to mix up the variation sentence pairs
def populate_test_list(date_="2021-01-01", shift=0, opt_array=None):
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
    # if opt_array is not None: use opt_array instead of variations
    if opt_array is not None:
        variations = opt_array
    for index in range(len(test_list)):
        # locate the <date> tag and replace it with a random variation from variations
        test_list[index] = test_list[index].replace("<date>", variations[(index + shift) % len(variations)])
    return test_list



# Given a list of strings, check if dates are in the strings and dates are correct
# Output is a list of strings containing bad dates
def check_dates_in_strings(input_list, print_output=True, date_="2021-01-01"):
    bad_dates = []
    good_dates = []
    correct_date = get_date(date_)
    for item in input_list:
        date = get_date(item)
        if check_date(item, correct_date):
            good_dates.append({"sentence": item, "date found": "Yes", "date": date})
        elif date is None :
            bad_dates.append({"sentence": item, "date found": "No", "date": "None"})
        elif date != correct_date:
            bad_dates.append({"sentence": item, "date found": "Yes", "date": date})
        else :
            good_dates.append({"sentence": item, "date found": "Yes", "date": date})
    if print_output:
        print_bad_dates(bad_dates)
    else:
        return bad_dates, good_dates
    return

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
    else:
        print("Usage: python3 validity_check.py -test")
        print("Usage: python3 validity_check.py -list")

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


################### Colab Code ###################
"""
os.chdir('/content/drive/MyDrive/Colab Notebooks')

from validity_check import populate_test_list, check_dates_in_strings

good_dates = []

with open('output', 'w') as file:
  test_list = populate_test_list()
  for sentence in test_list:
    file.write('\n\n' + sentence + '\n')
    input = generate_paraphrase(sentence)
    output, good_output = check_dates_in_strings(input, False)
    for item in good_output:
      good_dates.append([sentence, item["sentence"]])
    for item in output:
      given_date = item["date"]
      if not given_date:
        given_date = "none"
      file.write(str(item["sentence"] + '\t\t' + item["date found"] + '\t' + given_date + '\n'))


def good_dates_dataset(good_dates):
  i = 0
  new_pairs = []
  last = good_dates[0][1]
  while i < len(good_dates) - 1:
    if good_dates[i][0] == good_dates[i+1][0]:
      new_pairs.append([good_dates[i][1], good_dates[i+1][1]])
      last = good_dates[i+1][1]
      i += 1
    elif good_dates[i][1] != last:
      new_pairs.append([last, good_dates[i][1]])
      last = good_dates[i+1][1]
    i += 1
  return new_pairs

good_pairs = good_dates_dataset(good_dates)


print(len(good_pairs))
# double pairs dataset by flipping pairs
for i in range(len(good_pairs)):
  good_pairs.append(["paraphrase: " + good_pairs[i][1], good_pairs[i][0]])
  good_pairs[i][0] = "paraphrase: " + good_pairs[i][0]
print(len(good_pairs))


 # make a csv dataset & splice into big csv dataset. Save as one large csv dataset
dates = pd.DataFrame(good_pairs, columns=["prompt", "label"])
dates.to_csv('good_pairs.csv', ignore_index = True)
dates.head()

# insert the entirity of the dates dataframe at the halfway point of the df dataframe
def insert_at_halfway(df, dates):
    half = int(len(df) / 2)
    print(half)
    df1 = df.iloc[:half]
    df2 = df.iloc[half:]
    df = pd.concat([df1, dates, df2], ignore_index=True)
    return df

new_df = insert_at_halfway(df, dates)
new_df.to_csv('dateset_with_dates.csv')
"""