# paraphrase_detector
Model trained on PAWs dataset for paraphrase detection.
Varying models were trained, deberta was found to be the most successful.

Additional goal:
Train model to paraphrase numbers and dates.
File create_data.py generates a simple database of good and bad examples of number and date paraphrases.
The split of the file is ~34% good examples.

# Date Rules
This section defines the acceptable date variants. The scope of the dataset is currently American formatting.
| Format  |  Date Order  |  Description  |
|---------|--------------|---------------|
| 1       |  MM/DD/YY    |  Month-Day-Year wtih leading zeros (02/17/2009)  |
| 2       |  DD/MM/YY    |  Day-Month-Year with leading zeros (17/02/2009)  |
| 3       |  YY/MM/DD    |  Year-Month-Day with leading zeros (2009/02/17)  |
| 4       |  Month D, Yr |  Month name-Day-Year with no leading zeros (February 17, 2009)  |
| 5       |  M/D/YY      |  Month-Day-Year with no leading zeros (2/17/2009)  |
| 6       |  D/M/YY      |  Day-Month-Year with no leading zeros (17/2/2009)  |
| 7       |  YY/M/D      |  Year-Month-Day with no leading zeros (2009/2/17)  |
| 8       |  bM/bD/YY    |  Month-Day-Year wiht spaces instead of leading zeros ( 2/17/2009)  |
| 9       |  bD/bM/YY    |  Day-Month-Year with spaces instead of leading zeros (17/ 2/2009)  |
| A       |  YY/bM/bD    |  Year-Month-Day wiht spaces instead of leading zeros (2009/ 2/17)  |
| B       |  MMDDYY      |  Month-Day-year with no separators (17022009)  |
| C       |  DDMMYY      |  Day-Month-Year with no separators (02172009)  |
| D       |  YYMMDD      |  Year-Month-Day with no separators (20090217)  |
| E       |  MonDDYY     |  Month abbreviation-Day-Year with no leading zeros (Feb172009)  |
| F       |  DDMonYY     |  Day-Month abbreviation-Year with laeding zeros (17Feb2009)       |
| G       |  YYMonDD     |  Year-Month abbreviation-Day with leading zeros (2009Feb17)       |
| H       |  D Month, Yr |  Day-Month name-Year (17 Feburary, 2009)                          |
| I       |  Yr, Month D |  Year-Month name-Day (2009, February 17)                          |
| J*      |  Mon-DD-YYYY |  Month abbreviation, Day wiht leading zeros, Year (Feb 17, 2009)  |
| K*      |  DD-Mon-YYYY |  Day with leading zeros, Month abbreviation, Year 17 Feb, 2009    |
| L*      |  YYYY-Mon-DD |  Year, Month abbreviation, Day with leading zeros (2009, Feb 17)  |
| M       |  Mon DD, YYYY|  Month abbreviation, Day with leading zeros, Year (Feb 17, 2014)  |
| N       |  DD Mon, YYYY|  Day with leading zeros, Month abbreviation, Year (17 Feb, 2014)  |
| O       |  YYYY, Mon DD|  Year, Month abbreviation, Day with leading zeros (2014, Feb 17)  |
\* This format defaults to a two-digit year, but can be overridden to have four digits
