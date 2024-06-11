import random
from num2words import num2words
import pandas as pd
import math

# Helper function to create number variations
def generate_number_variations(number):
    num_str = str(number)
    variations = []
    variations.append("{:,}".format(number))  # 12,345
    # Convert number to words (simple approach for demonstration)
    variations.append(num2words(number))  # twelve thousand three hundred forty-five
    return variations

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
    df.to_csv('paraphrase_dataset_numbers.csv', index=False)
    
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