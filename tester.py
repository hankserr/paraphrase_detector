import pdb
from dateutil import parser
import spacy

nlp = spacy.load("en_core_web_sm")

# A function that uses parser from dateutil to return a date from a string
def get_date(date_string):
    try:
        date_obj = parser.parse(date_string, fuzzy=True)
        return str(date_obj)[:10]
    except ValueError:
        return None


def mask_dates(text):
  doc = nlp(text)
  output = []
  print(doc)
  print(doc.ents)
  for ent in doc.ents:
    if ent.label_ == "DATE":
      output.append(ent.text)
  return output

s1 = "Jan012021 marks the first day of the annual technology conference."
s2 = "The new product launch is scheduled for 2021Jan01, with a press event."

# print(get_date(s1))
# print(get_date(s2))
# print(mask_dates(s1))
# print(mask_dates(s2))

import re

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

# Example usage
sentence = "May052035 is when the new semester begins for most universities."
correct_date = "2035-05-05"

output = check_date(sentence, correct_date)
print(output)  # Should print: True
# pdb.set_trace()
print(check_date(s2, "2021-01-01"))