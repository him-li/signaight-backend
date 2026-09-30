import csv
import pandas as pd

# url_dict = {   "https://example.com/data4": "blah blah",
#                 "https://example.com/data5": "blu blu" }
# id="1_farsi"
# person={
#         'f_name': 'محمد حسن',
#         'l_name': 'پور آقا',
#         'cellphone': '+984136307693',
#         'email_address': 'hym.civil.eng@gmail.com',
#         'work': 'شرکت فروزان فام فجر'
#         }

PATH = 'C:\\code\\google_results.csv'

def insert_to_csv_from_url_dict(id, person, url_dict) -> None:
    df = pd.read_csv(PATH)
    filtered_df = df[df['id']  == id]
    previous_urls = set(filtered_df["url"])
    with open(PATH, mode='a', newline='\n', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for url, content in url_dict.items():
            if url not in previous_urls:
                csv_writer.writerow([id, person, url, content])


# insert_to_csv_from_url_dict(id,person,url_dict)
