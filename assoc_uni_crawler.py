import os
import time

import requests
from bs4 import BeautifulSoup


def progress_bar_msg(progress, total):
    percentage = (progress / total) * 100
    line_count = int((percentage / 2) // 1)
    return f"[{'|' * line_count}{'-' * (50 - line_count)}] %{round(percentage, 2)} - ({progress}/{total})"


assoc_url = "https://yokatlas.yok.gov.tr/onlisans-univ.php?u="
assoc_prefix = "onlisans.php?y="
cooldown = 0.5

uni_range = (1000, 4000)

ids = []

for i in range(uni_range[0], uni_range[1]):
    os.system("cls" if os.name == "nt" else "clear")
    print(progress_bar_msg(i - uni_range[0] + 1, uni_range[1] - uni_range[0]))
    response = requests.get(assoc_url + str(i))
    soup = BeautifulSoup(response.content, 'html.parser')
    for a in soup.find_all('a', attrs={"data-parent": "#"}):
        dep_id = a['href'].replace(assoc_prefix, "")
        ids.append(dep_id)
    time.sleep(cooldown)

ids = sorted(list(set(ids)))

with open("assoc_ids", "w+") as f:
    f.write("\n".join(ids))

input(
    f"{len(ids)} önlisans bölümü IDsi bulundu ve assoc_ids dosyasına kaydedildi. \"assoc_dept_crawler.py\" dosyasıyla bölümlerin bilgilerini alabilirsiniz. Enter'a basarak bu pencereyi kapayabilirsiniz.")
