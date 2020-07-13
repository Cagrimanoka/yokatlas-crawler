import pickle
import time
import os
import traceback

import pandas
import requests
from bs4 import BeautifulSoup



try:
    # years have difference, class should treat them differently but put em under the same id

    # ly = last_year, oy = other_year

    def progress_bar_msg(progress, total, custom_msg):
        percentage = (progress / total) * 100
        line_count = int((percentage / 2) // 1)
        return f"{custom_msg} - [{'|' * line_count}{'-' * (50 - line_count)}] %{round(percentage, 2)} - ({progress}/{total})"


    year_range = (2016, 2019)

    base_url = "https://yokatlas.yok.gov.tr"

    urls = {"ly_genel_bilgiler": "/content/lisans-dynamic/1000_1.php?y=",
            "oy_genel_bilgiler": "/%y/content/lisans-dynamic/1000_1.php?y="}


    dept_ids = []

    with open("bachelor_ids", "r+") as f:
        for dept_id in f.readlines():
            dept_ids.append(dept_id.replace("\n", ""))

    dept_ids = list(set(dept_ids))

    data = {}

    tables = []

    uni_data_template = {"kod": 0, "uni_adi": "", "uni_tur": "", "bolumler": {}}

    dept_data_template = {"kod": 0, "bolum_adi": "", "fakulte_adi": "", "yil_verileri": {}}

    dept_year_data_template = {"yil": 0, "puan_turu": "", "burs": "", "g_kontenjan": 0, "ob_kontenjan": 0, "t_kontenjan": 0,
                               "g_kontenjan_y": 0, "ob_kontenjan_y": 0, "t_kontenjan_y": 0, "b_kontenjan": 0,
                               "ilk_y_oran": 0, "y_kayitsiz": 0, "ek_y": 0, "taban_sira_012": 0, "taban_sira_012_006": 0,
                               "tavan_puan": 0, "tavan_sira": 0, "obp_kirik_sayi": 0, "ortalama_obp": 0,
                               "ortalama_dip_not": 0}

    uni_data_storage = {}

    dept_data_storage = {}

    total = len(dept_ids)
    i = 1

    for dept_id in dept_ids:
        os.system("cls" if os.name == "nt" else "clear")
        print(progress_bar_msg(i, total, "YÖK'ten veriler alınıyor."))
        dept_id_data = {}
        for yr in range(year_range[0], year_range[1]):
            t_o = False
            while not t_o:
                try:
                    dept_id_data[yr] = BeautifulSoup(
                        requests.get(base_url + urls["oy_genel_bilgiler"].replace("%y", str(yr)) + dept_id).content,
                        "html.parser").prettify()
                    t_o = True
                except:
                    traceback.print_exc(file=open(f"last_err-{dept_id}-{yr}.txt", "w+"))
                    time.sleep(5)
            time.sleep(0.3)
        t_o = False
        while not t_o:
            try:
                dept_id_data[year_range[1]] = BeautifulSoup(requests.get(base_url + urls["ly_genel_bilgiler"] + dept_id).content, "html.parser").prettify()
                t_o = True
            except:
                traceback.print_exc(file=open(f"last_err-{dept_id}-{year_range[1]}.txt", "w+"))
                time.sleep(5)
        time.sleep(0.3)
        tables.append((dept_id, dept_id_data))
        i += 1

    depts = {}

    total = len(tables)
    i = 1

    for dept in tables:
        os.system("cls" if os.name == "nt" else "clear")
        print(progress_bar_msg(i, total, "Bölüm verileri işleniyor."))
        pandas_list = []
        years = []
        for yr in range(year_range[0], year_range[1]):
            try:
                pandas_list.append(pandas.read_html(dept[1][yr], decimal=",", thousands="."))
                years.append(yr)
            except:
                pass
        years.append(year_range[1])
        years = years[::-1]
        pandas_list.append(pandas.read_html(dept[1][year_range[1]], decimal=",", thousands="."))
        uni_id = dept[0][:4]
        dept_id = dept[0]
        second_dict_name = list(pandas_list[::-1][0][0].to_dict())[0] + ".1"
        if uni_id not in uni_data_storage:
            uni_data_storage[uni_id] = (pandas_list[::-1][0][0].to_dict()[second_dict_name][2], pandas_list[::-1][0][0].to_dict()[second_dict_name][1])
        dept_data_form = dict(dept_data_template)
        dept_data_form["kod"] = dept_id
        dept_data_form["bolum_adi"] = list(pandas_list[::-1][0][0].to_dict())[0]
        dept_data_form["fakulte_adi"] = pandas_list[::-1][0][0].to_dict()[second_dict_name][3]
        dept_data_form["yil_verileri"] = {}
        depts[dept_id] = dept_data_form
        for panda in pandas_list[::-1]:
            dept_year_data_form = dict(dept_year_data_template)
            dept_year_data_form["yil"] = years[0]
            yr = years[0]
            del years[0]
            second_dict_name = list(panda[0].to_dict())[0] + ".1"
            part0 = panda[0].to_dict()[second_dict_name]
            dept_year_data_form["puan_turu"] = part0[4]
            dept_year_data_form["burs"] = part0[5]
            part1 = panda[1].to_dict()[1]
            dept_year_data_form["g_kontenjan"] = part1[0]
            dept_year_data_form["ob_kontenjan"] = part1[1]
            dept_year_data_form["t_kontenjan"] = part1[2]
            dept_year_data_form["g_kontenjan_y"] = part1[3]
            dept_year_data_form["ob_kontenjan_y"] = part1[4]
            dept_year_data_form["t_kontenjan_y"] = part1[5]
            dept_year_data_form["b_kontenjan"] = part1[6]
            dept_year_data_form["ilk_y_oran"] = part1[7]
            dept_year_data_form["y_kayitsiz"] = part1[8]
            dept_year_data_form["ek_y"] = part1[9]
            if dept_year_data_form["yil"] > 2017:
                part2 = panda[2].to_dict()[1]
                dept_year_data_form["taban_puan_012"] = part2[0]
                dept_year_data_form["taban_puan_012_006"] = part2[1]
                dept_year_data_form["taban_sira_012"] = part2[2]
                dept_year_data_form["taban_sira_012_006"] = part2[3]
                dept_year_data_form["tavan_puan"] = part2[4]
                dept_year_data_form["tavan_sira"] = part2[5]
                dept_year_data_form["obp_kirik_sayi"] = part2[6]
                dept_year_data_form["ortalama_obp"] = part2[7]
                dept_year_data_form["ortalama_dip_not"] = part2[8]
            else:
                part2 = panda[2].to_dict()[1]
                dept_year_data_form["taban_puan"] = part2[0]
                dept_year_data_form["tavan_puan"] = part2[1]
                dept_year_data_form["taban_sira_012"] = part2[2]
                dept_year_data_form["taban_sira_012_006"] = part2[3]
                dept_year_data_form["tavan_sira"] = part2[4]
                dept_year_data_form["obp_kirik_sayi"] = part2[5]
                dept_year_data_form["ortalama_obp"] = part2[6]
                dept_year_data_form["ortalama_dip_not"] = part2[7]
            depts[dept_id]["yil_verileri"][yr] = dept_year_data_form
        i += 1

    # uni-dept matching

    total = len(uni_data_storage)
    i = 1

    for uni in uni_data_storage:
        os.system("cls" if os.name == "nt" else "clear")
        print(progress_bar_msg(i, total, "Üniversite verileri işleniyor."))
        uni_id = uni
        uni_data = dict(uni_data_template)
        uni_data["kod"] = uni_id
        uni_data["uni_adi"] = uni_data_storage[uni_id][0]
        uni_data["uni_tur"] = uni_data_storage[uni_id][1]
        uni_data["bolumler"] = {}
        for dept in depts:
            if dept.startswith(uni_id):
                uni_data["bolumler"][dept] = depts[dept]
        data[uni_id] = uni_data
        i += 1


    with open("bachelor_data_pickle", "wb") as f:
        pickle.dump(data, f, protocol=4)

    input("Veriler başarıyla işlendi. \"bachelor_data_pickle\" bu verilere ulaşabilirsiniz. Çıkmak için Enter'a basın.")
except:
    traceback.print_exc(file=open("bachelor_err.txt", "w+"))