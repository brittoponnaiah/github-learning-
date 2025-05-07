from bs4 import BeautifulSoup
import csv

# Define the keywords to search for
keywords = [
    "Overall number of test cases",
    "Executed test cases",
    "Not executed test cases",
    "Test cases passed",
    "Test cases failed"
]

# Read the HTML file
with open("D:\\Pythonautomation\\Grafana_POC\\TM_SST_DebugEth_report.html", 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all tables
tables = soup.find_all('table')

# Search for the table containing the statistics
target_table = None
for table in tables:
    if any(keyword in table.get_text() for keyword in keywords):
        target_table = table
        break

# Proceed if the table is found
if target_table:
    rows = target_table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all(['td', 'th'])
        if cols:
            label = cols[0].get_text(strip=True)
            count = cols[1].get_text(strip=True) if len(cols) > 1 else ''
            percentage = cols[2].get_text(strip=True) if len(cols) > 2 else ''
            data.append([label, count, percentage])

    # Write to CSV
    with open('test_statistics.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metric', 'Count', 'Percentage'])
        writer.writerows(data)

    print("CSV file 'test_statistics.csv' created successfully.")
else:
    print("Error: Could not find a table containing test statistics.")
