import random
from datetime import datetime, timedelta
import pandas as pd
import math
import pdb

# Helper function to create date variations
def generate_date_variations(date):
    variations = []
    date_obj = datetime.strptime(date, "%Y-%m-%d") # 2009-02-17

    variations.append(date_obj.strftime("%Y-%m-%d")) # 2009-02-17
    variations.append(date_obj.strftime("%m/%d/%Y")) # 02/17/2009
    variations.append(date_obj.strftime("%m/%d/%y")) # 02/17/09
    variations.append(date_obj.strftime("%d/%m/%Y")) # 17/02/2009
    variations.append(date_obj.strftime("%d/%m/%y")) # 17/02/09
    variations.append(date_obj.strftime("%Y/%m/%d")) # 2009/02/17
    variations.append(date_obj.strftime("%B %d, %Y")) # February 17, 2009
    variations.append(date_obj.strftime("%-m/%-d/%Y")) # 2/17/2009
    variations.append(date_obj.strftime("%-m/%-d/%y")) # 2/17/09
    variations.append(date_obj.strftime("%-d/%-m/%Y")) # 17/2/2009
    variations.append(date_obj.strftime("%-d/%-m/%y")) # 17/2/09
    variations.append(date_obj.strftime("%Y/%-m/%-d")) # 2009/2/17
    variations.append(date_obj.strftime("%Y%m%d")) # 20090217
    variations.append(date_obj.strftime("%b%d%Y")) # Feb172009
    variations.append(date_obj.strftime("%d%b%Y")) # 17Feb2009
    variations.append(date_obj.strftime("%Y%b%d")) # 2009Feb17
    variations.append(date_obj.strftime("%d %B, %Y")) # 17 February, 2009
    variations.append(date_obj.strftime("%Y, %B %d")) # 2009, February 17
    variations.append(date_obj.strftime("%b %d, %Y")) # Feb 17, 2009
    variations.append(date_obj.strftime("%d %b, %Y")) # 17 Feb, 2009
    variations.append(date_obj.strftime("%y, %B %d")) # 09, February 17
    variations.append(date_obj.strftime("%b %d, %y")) # Feb 17, 09
    variations.append(date_obj.strftime("%d %b, %y")) # 17 Feb, 09
    variations.append(date_obj.strftime("%Y, %b %d")) # 2009, Feb 17
    variations.append(date_obj.strftime("%y, %b %d")) # 09, Feb 17
    variations.append(date_obj.strftime("%b %d, %Y")) # Feb 17, 2014
    variations.append(date_obj.strftime("%d %b, %Y")) # 17 Feb, 2014
    variations.append(date_obj.strftime("%Y, %b %d")) # 2014, Feb 17


    return variations

# Function to generate multiple impossible date variations
def generate_impossible_date_variation():
    impossible_dates = []

    # Define valid ranges for days in each month
    days_in_month = {
        "January": 31, "February": 28, "March": 31, "April": 30,
        "May": 31, "June": 30, "July": 31, "August": 31,
        "September": 30, "October": 31, "November": 30, "December": 31
    }

    # Generate random impossible date
    month = random.choice(list(days_in_month.keys()))  # Randomly select a month
    max_day = days_in_month[month]  # Get the maximum valid day for the selected month

    # Generate a random invalid day
    invalid_day = random.randint(max_day + 1, max_day + 10)  # Choose a day outside the valid range
    year = random.randint(2000, 2100)  # Choose a random year within a reasonable range

    # Format the invalid date
    impossible_date = f"{month} {invalid_day}, {year}"

    return impossible_date

# Function to generate bad date variations
def generate_bad_date_variations(date):
    variations = []  # Initialize an empty list to store the bad variations
    date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert the input string into a datetime object

    # Incorrect formats
    variations.append(date_obj.strftime("%Y/%d/%m"))  # Add date in "YYYY/DD/MM" format, which is an incorrect order
    variations.append(date_obj.strftime("%y/%d/%m"))  # Add date in "YY/DD/MM" format, which is an incorrect order
    variations.append(date_obj.strftime("%B %Y %d"))  # Add date in "Month YYYY DD" format, which is illogical

    # Logical errors
    # Generate a random incorrect year
    current_year = date_obj.year
    incorrect_year = current_year + random.randint(-10, 10)  # A year within ±10 years of the current year
    while incorrect_year == current_year:  # Ensure it's actually incorrect
        incorrect_year = current_year + random.randint(-10, 10)
    variations.append(date_obj.strftime("%B %d, %Y").replace(str(current_year), str(incorrect_year)))

    # Generate a random incorrect month
    current_month = date_obj.strftime("%B")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    incorrect_month = random.choice(months)
    while incorrect_month == current_month:  # Ensure it's actually incorrect
        incorrect_month = random.choice(months)
    variations.append(date_obj.strftime("%B %d, %Y").replace(current_month, incorrect_month))

    # Nonsense transformations
    variations.append(generate_impossible_date_variation())  # Create an impossible date (January 32 doesn't exist)
    variations.append("Random date text")  # Add completely irrelevant text

    return variations  # Return the list of bad date variations


# Creates pairs of good paraphrasing examples
def generate_pairs(array1, n, array2=None):
    pairs_with_label = []

    if array2 is None:
        label = '1'
        # Single array case: form pairs within array1
        if len(array1) < 2:
            raise ValueError("The array must contain at least two elements to form pairs.")

        for _ in range(n):
            pair = random.sample(array1, 2)  # Select 2 unique values from the same array
            pairs_with_label.append([pair[0], pair[1], label])
    else:
        label = '0'
        # Two array case: form pairs between array1 and array2
        if len(array1) == 0 or len(array2) == 0:
            raise ValueError("Both arrays must contain at least one element to form pairs.")

        for _ in range(n):
            value1 = random.choice(array1)  # Select 1 value from array1
            value2 = random.choice(array2)  # Select 1 value from array2
            pairs_with_label.append([value1, value2, label])

    return pairs_with_label

# Generate the dataset with both good examples and bad examples
def generate_dataset_with_bad_examples(n):
    dataset = []

    # Generating date examples
    base_date = datetime.now()
    for _ in range(n):  # 50 good examples
        random_date = base_date + timedelta(days=random.randint(0, 365))
        base_format = random_date.strftime("%Y-%m-%d")
        good_variations = generate_date_variations(base_format)

        # Must keep good_variation_pairs & bad_variation_pairs lengths at a 5:3 ratio.
        # Splicing is temporarily hardcoded.
        good_variation_pairs = generate_pairs(good_variations, 125)
        bad_variation_pairs = generate_pairs(good_variations, 75, generate_bad_date_variations(base_format))

        # Splice dataset
        x, y = 0, 0
        for _ in range(int(len(good_variation_pairs) / 5)):
            dataset.append(good_variation_pairs[x])
            dataset.append(good_variation_pairs[x+1])
            dataset.append(bad_variation_pairs[y])
            dataset.append(good_variation_pairs[x+2])
            dataset.append(bad_variation_pairs[y+1])
            dataset.append(good_variation_pairs[x+3])
            dataset.append(good_variation_pairs[x+4])
            dataset.append(bad_variation_pairs[y+2])
            x += 5
            y += 3

    return dataset

# function to even balance of examples
def even_dataset(df):
    tot_rows = len(df)
    num_type_1 = len(df[df['label'] == '1'])
    percentage = (num_type_1 / tot_rows)
    num_needed = math.ceil((len(df) * (0.50 * percentage)) / 2)

    # Dataset leans towards bad examples
    new_data = []
    for x in range(int(num_needed / 10)):
        base_date = datetime.now()
        random_date = base_date + timedelta(days=random.randint(0, 365))
        base_format = random_date.strftime("%Y-%m-%d")
        good_variations = generate_date_variations(base_format)
        for variation in good_variations :
            new_data.append({"sentence1": variation[0], "sentence2": variation[1], "label": '1'})

    new_data = reverse_examples(new_data)
    df = pd.concat([df, new_data], ignore_index = True)

    return df

# Reverse the examples to generate a larger dataset
def reverse_examples(dataset):
    flip = lambda x: [x[1], x[0], x[2]]
    size = len(dataset)
    for x in range(size):
        dataset.append(flip(dataset[x]))


def main():
    print("\nStarting dataset with bad examples...\n")
    dataset = generate_dataset_with_bad_examples(50)
    reverse_examples(dataset)
    df = pd.DataFrame(dataset, columns=["sentence1", "sentence2", "label"])
    # even_dataset(df)
    df.to_csv('paraphrase_dataset_dates.csv', index=False)

    # Verification
    print("Printing first 5 positive and negative examples...\n")
    print(df[df['label'] == '1'].head(), "\n")
    print(df[df['label'] == '0'].head(), "\n")


    # Print percentage of 1's
    tot_rows = len(df)
    num_type_1 = len(df[df['label'] == '1'])
    percentage = (num_type_1 / tot_rows) * 100
    print(f"Total size of dataset: {len(dataset)}\nPercentage of good examples in the dataset: {percentage:.2f}%\n")


if __name__ == "__main__":
    main()




#### Old code ####
'''
variations.append(date_obj.strftime("%B %d, %Y"))  # June 1, 2024
    variations.append(date_obj.strftime("%d-%m-%Y"))  # 01-06-2024
    variations.append(date_obj.strftime("%d %B %Y"))  # 1 June 2024
    variations.append(date_obj.strftime("%Y/%m/%d"))  # 2024/06/01
    variations.append(date_obj.strftime("%d/%B/%Y"))  # 01/June/2024 - Using "/" instead of "-"
'''