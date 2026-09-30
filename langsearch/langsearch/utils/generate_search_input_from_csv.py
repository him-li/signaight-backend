import csv

with open(r'C:\Users\zmumi\Downloads\us_good_loans_for_parse.csv', 'r', newline='\n') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        print (row)

fieldnames = ["firstname",	"lastname"	,"address"	,"city"	,"state"	,"zip"	,"dob"	,"homephone"	,"cellphone"	,"email"]




def csv_to_json_exclude_columns(csv_filepath,  columns_to_exclude):
    with open(csv_filepath, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)


        for row in reader:
            filtered_row = {key: value for key, value in row.items() if key in columns_to_exclude}
            print (filtered_row)


csv_to_json_exclude_columns(r'C:\Users\zmumi\Downloads\us_good_loans_for_parse.csv',fieldnames)
