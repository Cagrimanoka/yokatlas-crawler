import pickle
import time
import os
import traceback

import pandas
import requests
from bs4 import BeautifulSoup

with open("bachelor_data_pickle", "rb") as f:
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

    urls = {"ly_genel_bilgiler": "/content/lisans-dynamic/1000_1.php?y=",
            "oy_genel_bilgiler": "/%y/content/lisans-dynamic/1000_1.php?y="}

    """
    main_urls = {"ly_main_url": "/lisans.php?y=", "oy_main_url": "/%y/lisans.php?y="}
    
    additional_urls = {"ly_yerlesen": "/content/lisans-dynamic/1000_2.php?y=",
                    "oy_yerlesen": "/%y/content/lisans-dynamic/1000_2.php?y=",
                    "ly_cinsiyet": "/content/lisans-dynamic/1010.php?y=",
                    "oy_cinsiyet": "/%y/content/lisans-dynamic/1010.php?y=",
                    "ly_cografi_bolgeler": "/content/lisans-dynamic/1020ab.php?y=",
                    "oy_cografi_bolgeler": "/%y/content/lisans-dynamic/1020ab.php?y=",
                    "ly_iller": "/content/lisans-dynamic/1020c.php?y=",
                    "oy_iller": "/%y/content/lisans-dynamic/1020c.php?y=",
                    "ly_ogrenim_durumu": "/content/lisans-dynamic/1030a.php?y=",
                    "oy_ogrenim_durumu": "/%y/content/lisans-dynamic/1030a.php?y=",
                    "ly_lise_mezuniyet_yili": "/content/lisans-dynamic/1030b.php?y=",
                    "oy_lise_mezuniyet_yili": "/%y/content/lisans-dynamic/1030b.php?y=",
                    "ly_lise_alani": "/content/lisans-dynamic/1050b.php?y=",
                    "oy_lise_alani": "/%y/content/lisans-dynamic/1050b.php?y=",
                    "ly_lise_grubu": "/content/lisans-dynamic/1050a.php?y=",
                    "oy_lise_grubu": "/%y/content/lisans-dynamic/1050a.php?y=",
                    "ly_lise": "/content/lisans-dynamic/1060.php?y=",
                    "oy_lise": "/%y/content/lisans-dynamic/1060.php?y=",
                    "ly_okul_birincileri": "/content/lisans-dynamic/1030c.php?y=",
                    "oy_okul_birincileri": "/%y/content/lisans-dynamic/1030c.php?y=",
                    "ly_taban_puan_sira": "/content/lisans-dynamic/1000_3.php?y=",
                    "oy_taban_puan_sira": "/%y/content/lisans-dynamic/1000_3.php?y=",
                    "ly_son_profil": "/content/lisans-dynamic/1070.php?y=",
                    "oy_son_profil": "/%y/content/lisans-dynamic/1070.php?y=",
                    "ly_osys_net_ortalama": "/content/lisans-dynamic/1210a.php?y=",
                    "oy_osys_net_ortalama": "/%y/content/lisans-dynamic/1210a.php?y=",
                    "ly_osys_puanlar": "/content/lisans-dynamic/1220.php?y=",
                    "oy_osys_puanlar": "/%y/content/lisans-dynamic/1220.php?y=",
                    "ly_osys_siralamalar": "/content/lisans-dynamic/1230.php?y=",
                    "oy_osys_siralamalar": "/%y/content/lisans-dynamic/1230.php?y=",
                    "ly_tercih_istatistikleri": "/content/lisans-dynamic/1080.php?y=",
                    "oy_tercih_istatistikleri": "/%y/content/lisans-dynamic/1080.php?y=",
                    "ly_yerlesilen_tercih_sirasi": "/content/lisans-dynamic/1040.php?y=",
                    "oy_yerlesilen_tercih_sirasi": "/%y/content/lisans-dynamic/1040.php?y=",
                    "ly_tercih_egilim_genel": "/content/lisans-dynamic/1300.php?y=",
                    "oy_tercih_egilim_genel": "/%y/content/lisans-dynamic/1300.php?y=",
                    "ly_tercih_egilim_tur": "/content/lisans-dynamic/1310.php?y=",
                    "oy_tercih_egilim_tur": "/%y/content/lisans-dynamic/1310.php?y=",
                    "ly_tercih_egilim_uni": "/content/lisans-dynamic/1320.php?y=",
                    "oy_tercih_egilim_uni": "/%y/content/lisans-dynamic/1320.php?y=",
                    "ly_tercih_egilim_il": "/content/lisans-dynamic/1330.php?y=",
                    "oy_tercih_egilim_il": "/%y/content/lisans-dynamic/1330.php?y=",
                    "ly_tercih_egilim_program": "/content/lisans-dynamic/1340a.php?y=",
                    "oy_tercih_egilim_program": "/%y/content/lisans-dynamic/1340a.php?y=",
                    "ly_tercih_egilim_meslek": "/content/lisans-dynamic/1340b.php?y=",
                    "oy_tercih_egilim_meslek": "/%y/content/lisans-dynamic/1340b.php?y=",
                    "ly_yerlesme_kosullar": "/content/lisans-dynamic/1110.php?y=",
                    "oy_yerlesme_kosullar": "/%y/content/lisans-dynamic/1110.php?y=",
                    "ly_ogretim_uyesi": "/content/lisans-dynamic/2050.php?y=",
                    "oy_ogretim_uyesi": "/%y/content/lisans-dynamic/2050.php?y=",
                    "ly_kayitli_ogrenci_sayisi": "/content/lisans-dynamic/2010.php?y=",
                    "oy_kayitli_ogrenci_sayisi": "/%y/content/lisans-dynamic/2010.php?y=",
                    "ly_mezun_ogrenci_sayisi": "/content/lisans-dynamic/2030.php?y=",
                    "oy_mezun_ogrenci_sayisi": "/%y/content/lisans-dynamic/2030.php?y=",
                    "ly_degisim_programi_sayi": "/content/lisans-dynamic/2040.php?y=",
                    "oy_degisim_programi_sayi": "/%y/content/lisans-dynamic/2040.php?y=",
                    "ly_yatay_gecis_sayi": "/content/lisans-dynamic/2060.php?y=",
                    "oy_yatay_gecis_sayi": "/%y/content/lisans-dynamic/2060.php?y="}
    """

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
        newlist = True
        if str(dept_id)[:4] in prev_cache:
            if str(dept_id) in prev_cache[str(dept_id)[:4]]["bolumler"]:
                dept_data_form = prev_cache[str(dept_id)[:4]]["bolumler"][str(dept_id)]
                newlist = False
        if newlist:
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


    with open("bachelor_data_pickle_new", "wb") as f:
        pickle.dump(data, f, protocol=4)

    input("Veriler başarıyla işlendi. \"bachelor_data_pickle_new\" bu verilere ulaşabilirsiniz. Çıkmak için Enter'a basın.")
except:
    traceback.print_exc(file=open("bachelor_err.txt", "w+"))