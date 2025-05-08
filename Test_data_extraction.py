from bs4 import BeautifulSoup
import csv
import glob

# Define the keywords to search for
keywords = [
    "Overall number of test cases",
    "Executed test cases",
    "Not executed test cases",
    "Test cases passed",
    "Test cases failed"
]

# Define the keywords to search Test begin and Test end
Test_keywords = ["Test begin","Test end"]

# Collect all HTML files in the current directory
file_names = glob.glob("*.html")

# List to hold all data rows
all_data = []

# Process each HTML file
for filename in file_names:
    with open(filename, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    tables = soup.find_all('table')
    target_table = None
    test_target_table = None

    for table in tables:
        if any(keyword in table.get_text() for keyword in keywords):
            target_table = table
            break

    for table in tables:
        if any(keyword in table.get_text() for keyword in Test_keywords):
            test_target_table = table
            break

    # Initialize values
    no_of_testcases = executed_testcases = not_executed_testcases = passed = failed = ''
    Test_begin = Test_end = ''

    if target_table:
        rows = target_table.find_all('tr')
        try:
            no_of_testcases = rows[0].find_all(['td', 'th'])[1].get_text(strip=True)
            executed_testcases = rows[1].find_all(['td', 'th'])[1].get_text(strip=True)
            not_executed_testcases = rows[2].find_all(['td', 'th'])[1].get_text(strip=True)
            passed = rows[3].find_all(['td', 'th'])[1].get_text(strip=True)
            failed = rows[4].find_all(['td', 'th'])[1].get_text(strip=True)
        except IndexError:
            print(f"Error: Table in {filename} doesn't have the expected format.")

    if test_target_table:
        rows = test_target_table.find_all('tr')
        try:
            Test_begin = rows[0].find_all(['td', 'th'])[1].get_text(strip=True)
            Test_end = rows[1].find_all(['td', 'th'])[1].get_text(strip=True)
        except IndexError:
            print(f"Error: Test time table in {filename} doesn't have the expected format.")

    # Only append if at least one of the tables was found
    if target_table and test_target_table:
        all_data.append([
            no_of_testcases,
            executed_testcases,
            not_executed_testcases,
            passed,
            failed,
            filename,
            Test_begin,
            Test_end
        ])
        print(f"Processed {filename}")
    else:
        print(f"Error: No required tables found in {filename}")

# Write all data to a CSV file
if all_data:
    with open('test_statistics.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'No_of_Testcases',
            'Executed_Testcases',
            'Not_executed_testcases',
            'Pass',
            'Fail',
            'Test_module',
            'Test_begin',
            'Test_end',
        ])
        writer.writerows(all_data)
    print("CSV file 'test_statistics.csv' created successfully.")
else:
    print("No valid test data found in any HTML file.")
