# yokatlas-crawler
YÖK Atlas genel verilerini (ön lisans ve lisans genel bilgileri) çekmek için yazdığım python 3.7 scripti ve 2016-2020 arası verileri (json ve pickle formatında)

* Bazı rakamlar Python kaynaklı bir hatadan ötürü çok uzun gözükebilir (örn. 241.89637 -> 241.89637000000002 veya 248.07909 -> 248.07908999999998). Bu sorun verileri işlerken `round(num, basamak_sayisi)` fonksiyonuyla çözülebilir.
