import pickle
import time
import os
import traceback

import pandas
import numpy
import requests

with open("assoc_data_pickle", "rb") as f:
    prev_cache = pickle.load(f)

try:
    # years have difference, class should treat them differently but put em under the same id

    # ly = last_year, oy = other_year

    def progress_bar_msg(progress, total, custom_msg):
        percentage = (progress / total) * 100
        line_count = int((percentage / 2) // 1)
        return f"{custom_msg} - [{'|' * line_count}{'-' * (50 - line_count)}] %{round(percentage, 2)} - ({progress}/{total})"


    year_range = (2020, 2020)

    base_url = "https://yokatlas.yok.gov.tr"

    urls = {"ly_genel_bilgiler": "/content/onlisans-dynamic/3000_1.php?y=",
            "oy_genel_bilgiler": "/%y/content/onlisans-dynamic/3000_1.php?y="}


    dept_ids = []

    with open("assoc_ids", "r+") as f:
        for dept_id in f.readlines():
            dept_ids.append(dept_id.replace("\n", ""))

    dept_ids = list(set(dept_ids))

    data = {}

    tables = []

    uni_data_template = {"kod": 0, "uni_adi": "", "uni_tur": "", "bolumler": {}}

    dept_data_template = {"kod": 0, "bolum_adi": "", "myo": "", "yil_verileri": {}}

    dept_year_data_template = {"yil": 0, "puan_turu": "", "burs": "", "g_kontenjan": 0, "ob_kontenjan": 0, "t_kontenjan": 0,
                               "sinavsiz_kontenjan": 0, "sinavsiz_kontenjan_y": 0, "sinavsiz_g_y": 0, "sinavli_y": 0,
                               "g_kontenjan_y": 0, "ob_kontenjan_y": 0, "t_kontenjan_y": 0, "b_kontenjan": 0,
                               "ilk_y_oran": 0, "y_kayitsiz": 0, "ek_y": 0,
                               "sinavsiz_giren_son": {"oncelikler": "", "obp": 0}}

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
                    dept_id_data[yr] = requests.get(base_url + urls["oy_genel_bilgiler"].replace("%y", str(yr)) + dept_id).content.decode(encoding="utf8").replace("-->", "").replace("<!--", "")
                    t_o = True
                except:
                    traceback.print_exc(file=open(f"last_err-{dept_id}-{yr}.txt", "w+"))
                    time.sleep(5)
            time.sleep(0.3)
        t_o = False
        while not t_o:
            try:
                dept_id_data[year_range[1]] = requests.get(base_url + urls["ly_genel_bilgiler"] + dept_id).content.decode(encoding="utf8").replace("-->", "").replace("<!--", "")
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
            uni_data_storage[uni_id] = (
            pandas_list[::-1][0][0].to_dict()[second_dict_name][2], pandas_list[::-1][0][0].to_dict()[second_dict_name][1])
        newlist = True
        if str(dept_id)[:4] in prev_cache:
            if str(dept_id) in prev_cache[str(dept_id)[:4]]["bolumler"]:
                dept_data_form = prev_cache[str(dept_id)[:4]]["bolumler"][str(dept_id)]
                newlist = False
        if newlist:
            dept_data_form = dept_data_template.copy()
            dept_data_form["kod"] = dept_id
            dept_data_form["bolum_adi"] = list(pandas_list[::-1][0][0].to_dict())[0]
            dept_data_form["myo"] = pandas_list[::-1][0][0].to_dict()[second_dict_name][3]
            dept_data_form["yil_verileri"] = {}
        depts[dept_id] = dept_data_form
        for panda in pandas_list[::-1]:
            panda = [p.replace(numpy.nan, "---", regex=True) for p in panda]
            dept_year_data_form = dept_year_data_template.copy()
            dept_year_data_form["yil"] = years[0]
            yr = years[0]
            del years[0]
            second_dict_name = list(panda[0].to_dict())[0] + ".1"
            part0 = panda[0].to_dict()[second_dict_name]
            dept_year_data_form["puan_turu"] = part0[4]
            dept_year_data_form["burs"] = part0[5]
            part1 = panda[1].to_dict()[1]
            dept_year_data_form["sinavsiz_kontenjan"] = part1[0]
            dept_year_data_form["g_kontenjan"] = part1[1]
            dept_year_data_form["ob_kontenjan"] = part1[2]
            dept_year_data_form["t_kontenjan"] = part1[3]
            dept_year_data_form["sinavsiz_kontenjan_y"] = part1[4]
            dept_year_data_form["g_kontenjan_y"] = part1[5]
            dept_year_data_form["ob_kontenjan_y"] = part1[6]
            dept_year_data_form["t_kontenjan_y"] = part1[7]
            if int(dept_year_data_form["yil"]) > 2016:
                part2 = panda[2].to_dict()[1]
                dept_year_data_form["sinavsiz_g_y"] = part2[0]
                dept_year_data_form["sinavli_y"] = part2[1]
                dept_year_data_form["b_kontenjan"] = part2[2]
                dept_year_data_form["ilk_y_oran"] = part2[3]
                dept_year_data_form["y_kayitsiz"] = part2[4]
                dept_year_data_form["ek_y"] = part2[5]
                part3 = panda[3].to_dict()
                part3 = part3[list(part3)[0] + ".1"]
                dept_year_data_form["sinavsiz_giren_son"]["oncelikler"] = part3[0]
                dept_year_data_form["sinavsiz_giren_son"]["obp"] = part3[1]
                part4 = panda[4].to_dict()
                part4 = part4[list(part4)[0] + ".1"]
                if int(dept_year_data_form["yil"]) > 2017:
                    dept_year_data_form["son_kisi_puan_012"] = part4[0]
                    dept_year_data_form["son_kisi_puan_018"] = part4[1]
                    dept_year_data_form["son_kisi_sira_012"] = part4[2]
                    dept_year_data_form["son_kisi_sira_018"] = part4[3]
                else:
                    dept_year_data_form["son_kisi_puan"] = part4[0]
                    dept_year_data_form["son_kisi_sira"] = part4[1]
            else:
                part2 = panda[2].to_dict()[1]
                dept_year_data_form["sinavsiz_g_y"] = part2[0]
                dept_year_data_form["sinavli_y"] = part2[1]
                part3 = panda[3].to_dict()[1]
                dept_year_data_form["b_kontenjan"] = part3[0]
                dept_year_data_form["ilk_y_oran"] = part3[1]
                dept_year_data_form["y_kayitsiz"] = part3[2]
                dept_year_data_form["ek_y"] = part3[3]
                part4 = panda[4].to_dict()
                part4 = part4[list(part4)[0] + ".1"]
                dept_year_data_form["sinavsiz_giren_son"]["oncelikler"] = part4[0]
                dept_year_data_form["sinavsiz_giren_son"]["obp"] = part4[1]
                part5 = panda[5].to_dict()
                part5 = part5[list(part5)[0] + ".1"]
                dept_year_data_form["son_kisi_puan"] = part5[0]
                dept_year_data_form["son_kisi_sira"] = part5[1]
            dept_data_form["yil_verileri"][dept_year_data_form["yil"]] = dept_year_data_form
        depts[dept_id]["yil_verileri"][yr] = dept_year_data_form
        i += 1

    # uni-dept matching

    total = len(uni_data_storage)
    i = 1

    for uni in uni_data_storage:
        os.system("cls" if os.name == "nt" else "clear")
        print(progress_bar_msg(i, total, "Üniversite verileri işleniyor."))
        uni_id = uni
        uni_data = uni_data_template.copy()
        uni_data["kod"] = uni_id
        uni_data["uni_adi"] = uni_data_storage[uni_id][0]
        uni_data["uni_tur"] = uni_data_storage[uni_id][1]
        uni_data["bolumler"] = {}
        for dept in depts:
            if dept.startswith(uni_id):
                uni_data["bolumler"][dept] = depts[dept]
        data[uni_id] = uni_data
        i += 1

    with open("assoc_data_pickle_new", "wb") as f:
        pickle.dump(data, f, protocol=4)

    input("Veriler başarıyla işlendi. \"assoc_data_pickle_new\" bu verilere ulaşabilirsiniz. Çıkmak için Enter'a basın.")
except:
    traceback.print_exc(file=open("assoc_err.txt", "w+"))