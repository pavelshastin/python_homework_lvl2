import lxml.html as html
import urllib.request
from bs4 import BeautifulSoup as bs
import random
import json
import time

# doc = html.parse("records.html").getroot()
# sports = []
#
# for row in doc.cssselect("tr"):
#     record = {"name": row[0].text_content().strip(),
#      "record": row[1].text_content().strip(),
#      "date": row[6].text_content().strip()
#      }
#
#     sports.append(record)
#
# with open("records.json", "w", encoding="UTF-8") as f:
#     f.write(json.dumps(sports, indent=4))



# with urllib.request.urlopen("https://en.wikipedia.org/wiki/2018_Athletics_World_Cup") as url:
#     wiki_athlet_2018 = url.read()
#
#
# wiki_athlet_2018 = bs(wiki_athlet_2018, "html.parser")
# # print(wiki_athlet_2018.prettify())
#
#
# sports = wiki_athlet_2018.find_all("h4")
#
# sportsmen = []
#
# for s in sports:
#
#     sport_name = s.find("span", class_="mw-headline").get_text()
#     res_table = s.find_next_sibling("table")
#
#     rows = res_table.find_all("tr")
#     head_row = rows[0]
#     data_rows = rows[1:]
#
#     idx = 0
#     rec_idx = 0
#     name_idx = 0
#     c_idx = 0
#     type = ""
#     for h in head_row.find_all("th"):
#         t =  h.get_text()
#         if t == "Time":
#             type = "time"
#             rec_idx = idx
#
#         elif t == "Mark":
#             rec_idx = idx
#             type = "meter"
#
#         elif t == "Nationality":
#             c_idx = idx
#
#         elif t == "Name" or t == "Names":
#             name_idx = idx
#
#         idx += 1
#
#     print(sport_name, name_idx, rec_idx, name_idx, type)
#
#     birth_range = range(1985, 1997, 1)
#
#     for d_row in data_rows:
#         data = d_row.find_all("td")
#
#         name = data[name_idx].find("a").get_text()
#         year = random.choice(birth_range)
#         country = data[c_idx].get_text().strip()
#         record = data[rec_idx].get_text()
#         rank = random.choice(("candidate", "master", "master_int"))
#
#         dic = {"name": name, "year": year, "country": country, "record": record,
#                "rank": rank, "sport": sport_name, "type": type}
#         sportsmen.append(dic)
#
#
#
# print(sportsmen)
#
# with open("sportsmen.json", "w", encoding="UTF-8") as f:
#     f.write(json.dumps(sportsmen, indent=4))


with open("sportsmen.json", "r", encoding="UTF-8") as f:
    sportsmen = json.loads(f.read())


dates = ["15-15-2010", "12-05-2010", "18-06-2011", "21-07-2012", "22-08-2013", "05-09-2014", "03-05-2009"]
cities = ["London", "Moscow", "Tol'yatti", "Dresden", "Berlin", "Paris", "New York", "Atlanta", "Rome", "Vienna"]


print(len(sportsmen))

for s in sportsmen:
    print(s["name"], s["record"], s["type"])