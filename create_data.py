import pdb
import random
from datetime import datetime, timedelta
from num2words import num2words
import pandas as pd
import math
import csv

# Helper function to create date variations
def generate_date_variations(date):
    variations = []
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    variations.append(date_obj.strftime("%B %d, %Y"))  # June 1, 2024
    variations.append(date_obj.strftime("%d-%m-%Y"))  # 01-06-2024
    variations.append(date_obj.strftime("%d %B %Y"))  # 1 June 2024
    variations.append(date_obj.strftime("%Y/%m/%d"))  # 2024/06/01
    variations.append(date_obj.strftime("%d/%B/%Y"))  # 01/June/2024 - Using "/" instead of "-"

    return variations

# Helper function to create number variations
def generate_number_variations(number):
    num_str = str(number)
    variations = []
    variations.append("{:,}".format(number))  # 12,345
    # Convert number to words (simple approach for demonstration)
    variations.append(num2words(number))  # twelve thousand three hundred forty-five
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

# Function to generate bad number variations
def generate_bad_number_variations(number):
    variations = []
    
    # Incorrect formats
    variations.append(f"{number:,}a")  # 12,345a - Adding random letter
    variations.append(f"{number}-")  # 12345- - Incomplete transformation
    
    # Logical errors
    if number > 1:
        variations.append(str(number + 1))  # Adding 1 to the number
    if number < 100000:
        variations.append(str(number - 1))  # Subtracting 1 from the number

    # Nonsense transformations
    variations.append("random text")  # Completely irrelevant
    variations.append(num2words(number).replace(" ", ""))  # Removing spaces in words
    
    return variations

def generate_dataset_with_bad_examples():
    dataset = []

    # Generating date examples
    base_date = datetime.now()
    for _ in range(100):  # 50 good examples
        random_date = base_date + timedelta(days=random.randint(0, 365))
        base_format = random_date.strftime("%Y-%m-%d")
        good_variations = generate_date_variations(base_format)
        bad_variations = generate_bad_date_variations(base_format)
        
        for variation in good_variations:
            dataset.append((base_format, variation, '1'))
        
        for variation in bad_variations:
            dataset.append((base_format, variation, '0'))

    # Generating number examples
    for _ in range(100):  # 50 good examples
        random_number = random.randint(1, 100000)
        base_format = str(random_number)
        good_variations = generate_number_variations(random_number)
        bad_variations = generate_bad_number_variations(random_number)
        
        for variation in good_variations:
            dataset.append((base_format, variation, '1'))
        
        for variation in bad_variations:
            dataset.append((base_format, variation, '0'))

    return dataset

# function to even balance of examples
def even_dataset(df):
    tot_rows = len(df)
    num_type_1 = len(df[df['Type'] == '1'])
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
            new_data.append({"Input": variation[0], "Paraphrase": variation[1], "Type": '1'})
    
    for x in range(int(num_needed / 4)):
        random_number = random.randint(1, 100000)
        base_format = str(random_number)
        good_variations = generate_number_variations(random_number)
        for variation in good_variations :
            new_data.append({"Input": variation[0], "Paraphrase": variation[1], "Type": '1'})
        
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
    print("Starting ... Dataset with bad examples")
    dataset = generate_dataset_with_bad_examples()
    reverse_examples(dataset)
    df = pd.DataFrame(dataset, columns=["Input", "Paraphrase", "Type"])
    # even_dataset(df)
    df.to_csv('paraphrase_dataset.csv', index=False)
    
    # Verification
    print(df.head())
    print(df[df['Type'] == '0'].head())


    # Print percentage of 1's
    tot_rows = len(df)
    num_type_1 = len(df[df['Type'] == '1'])
    percentage = (num_type_1 / tot_rows) * 100
    print(f"Percentage of good examples in the dataset: {percentage:.2f}%")


if __name__ == "__main__":
    main()