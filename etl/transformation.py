import simplejson as json
import sys

unique_companies = set()
companies_json = sys.argv[1]

with open(companies_json, 'r', encoding='utf-8') as f:
    for line_number, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            company = data['company']
            unique_companies.add(company)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line {line_number}: {e}")

print(unique_companies)