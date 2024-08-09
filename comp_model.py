import pdb
import requests
import json
from validity_check import find_dates, populate_test_list
from date_data import generate_date_variations
import os
import pandas as pd

def make_post_request(text, variant_count):
    responses = []
    urls = ['http://localhost:8080/api/internal/variants',
            'sandbox.em-staging.com/api/internal/variants',
            ]
    # url = 'http://localhost:8080/api/internal/variants'
    url = 'https://sandbox.em-staging.com/api/internal/variants'
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
            pdb.set_trace()
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
    # sentences = read_tester_mester()
    sentences = ["this is a super long test string for testing"]
    variant_count = 9
    process_responses(sentences, variant_count)
    _ = input("Enter any key to close")
    os.system('killall TextEdit')
    os.system('rm -f bad_output.txt')
