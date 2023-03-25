import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

headers = {"User-Agent": ua.chrome}

url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2"

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

data = soup.find("tbody").find_all("span", class_="flagicon")
country_list = []
names = []

for i in data:
    url_img = i.find("img").get("src")
    fullname = i.find_next("td").find_next("td").text
    name = i.find_next("td").text
    names.append(name)
    country_list.append({"country": name.strip(),
                         "full_country_name": fullname.strip(),
                         "flag_url": url_img,
                         "full_country_name_words_count": fullname.count(" ") + 1})

count_same_letter = 0
for i in range(len(names)):
    for j in range(len(names)):
        if names[i][0] == names[j][0]:
            count_same_letter += 1

    country_list[i]["same_letter_count"] = count_same_letter
    count_same_letter = 0


def print_info(short_name, args):
    for el in args:
        if short_name in el.values():
            print(el)


search_name = input("Введите название страны:\n")
print_info(search_name, country_list)
