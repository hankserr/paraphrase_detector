"""
0.1.0
Program to take in a sentence and return true if it contains the correct date variations
and false if it doesn't.
"""

# A function to isolate the dates in a sentence using regex
def isolate_dates(sentence):
    # Regex patterns for dates in date_patterns array
    date_patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{4}/\d{2}/\d{2}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{4}/\d{2}/\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{4}\d{2}\d{2}",
        r"\d{2}\d{2}\d{2}",
        r"\d{2}\d{2}\d{4}",
        r"\d{4}\d{2}\d{2}",
        r"\d{2}\d{2}\d{4}",
        r"\d{4}, \d{2}",
        r"\d{4}, \d{2}",
        r"\d{2}, \d{4}",
        r"\d{4}, \d{2}",
        r"\d{2}, \d{4}",
        r"\d{4}, \d{2}",
        r"\d{2}, \d{4}",
        r"\d{4}, \d{2}",
        r"\d{2}, \d{4}",
        r"\d{2}, \d{4}",
        r"\d{4}, \d{2}",
        r"\d{2}, \d{4}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{2}/\d{2}/\d{2}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{4}/\d{2}/\d{2}"
    ]

    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, sentence)
        for match in matches:
            # Convert tuple matches to string by joining with space
            if isinstance(match, tuple):
                dates.append(''.join(match))
            else:
                dates.append(match)

    return dates


from dateutil import parser
# A function that uses parser from dateutil to return a date from a string
def get_date(date_string):
    try:
        date_obj = parser.parse(date_string, fuzzy=True)
        return date_obj
    except ValueError:
        return None

# main: test get_date function
def main():
    test_strings = [
        "The company is going to struggle on 01/12/25 this year, but we'll come out of it.",
        "The company is going to struggle on 20250112 this year, but we'll come out of it.",
        "The company is going to struggle on 2025-01-12 this year, but we'll come out of it.",
        "The company is going to struggle on February 17, 2025 this year, but we'll come out of it.",
        "The company is going to struggle on 17 February, 2025 this year, but we'll come out of it.",
        "The company is going to struggle on 17/02/2025 this year, but we'll come out of it.",
        "The company is going to struggle on 17/02/25 this year, but we'll come out of it.",
        "The company is going to struggle on 17th Feb, 2009 this year, but we'll come out of it.",
        "The company is going to struggle on 09, Feb 17 this year, but we'll come out of it.",
        "The company is going to struggle on 17 Feb, 09 this year, but we'll come out of it.",
        "The company is going to struggle on 17.2.2009 this year, but we'll come out of it.",
    ]
    for string in test_strings:
        print(str(get_date(string))[:10], "\n")

if __name__ == "__main__":
    main()
