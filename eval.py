import pdb
import requests
import json
from validity_check import find_dates, populate_test_list
from date_data import generate_date_variations
import os
import pandas as pd

def make_post_request(text, variant_count):
    url = 'http://localhost:8080/api/internal/variants'
    headers = {'Content-Type': 'application/json'}
    data = {
        'text': text,
        'variantCount': variant_count
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def process_responses(texts, variant_count):
    # pdb.set_trace()
    print("Running...")
    with open("bad_output.txt", "a") as file:
        file.write("###############################################################\n")
        tot_variants = 0
        for text in texts:
            response = make_post_request(text, variant_count)
            variants_given = 0
            bad_variants = []
            try:
                for variant in response[0]['variants']:
                    variants_given += 1
                    if "2021-01-01" not in find_dates(variant):
                        bad_variants.append(variant)
                file.write(f"{text}\t{len(bad_variants)}:{variants_given}\n")
                if(len(bad_variants) > 0):
                    # write to bad_output file
                    for variant in bad_variants:
                        file.write(f"{variant}\n")
                file.write("\n\n")
            except:
                print(f"Bad Reponse: {response}\nFrom: {text}\n\n")
            tot_variants += variants_given
        file.write(f"Total Responses given: {tot_variants}\n\n")

    print("Done.")
    os.system("open bad_output.txt")

def read_tester_mester():
    df = pd.read_csv("tester_mester.csv")
    return df.iloc[:, 0].tolist()


if __name__ == "__main__":
    # test_check_dates_in_strings()
    sentences = ["When it comes to baby-sized burritos, it's [all](https://baby.burrito) about the modest ingredients coming together in an adorable package. A humble tortilla, just large enough to swaddle the tiniest of beans, wraps up in what could only be described as a culinary hug."]
    variant_count = 9
    process_responses(sentences, variant_count)
    _ = input("Enter any key to close")
    os.system('killall TextEdit')
    os.system('rm -f bad_output.txt')
