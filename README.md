# RekoBuk

## **Daftar Isi**

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## **About** <a name = "about"></a>

RekoBuk merupakan sebuah sistem rekomendasi buku menggunakan teknik Content Based dan Item Based Filtering. Sistem ini dibuat untuk membantu user menemukan sebuah buku berdasarkan rekomendasi dari rating yang diberikan oleh user lainnya. Data yang digunakan berisi berbagai macam buku yang dapat digunakan oleh berbagai kalangan user.

## **Getting Started** <a name = "getting_started"></a>

Intruksi ini akan membuat sebuah salinan dari project ini dan dijalankan di local machine untuk keperluan development dan testing. Intruksi ini dibuat dengan menggunakan Python versi 3.10.6, untuk versi lain mungkin akan berbeda.

### **Prerequisites**
Sebelum memulai, kita perlu membuat sebuah [virtual environment](https://docs.python.org/3/library/venv.html) baru (opsional, jika tanpa virtual environment [langkah selanjutnya](#skip)), menginstall module [Flask](https://flask.palletsprojects.com/), [Pandas](https://pandas.pydata.org/), dan [Scikit-Learn](https://scikit-learn.org/)

* Membuat Virtual Environment Baru

```
$ mkdir book-venv
$ python -m venv /book-venv
```

* Aktifkan Virtual Environment

```
$ cd /book-venv
$ Scripts/activate
```

* Install Module yang Dibutuhkan <a name = "skip"></a>

```
(book-venv) $ pip install flask pandas scikit-learn
```

### **Local Installation**

1. Clone repository ini, dan extract di dalam folder book-venv. Atau gunakan git dengan command dibawah ini.

```
(book-venv) $ git clone https://github.com/Wintec-Yuda/Project-akhir-MSIB.git
```

2. Jalankan script app.py

```
(book-venv) $ python app.py
```

3. Log dibawah ini menandakan bahwa instalasi sukses, website dapat diakses pada link yang tercantum di **Running on**.

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://localhost:5000
Press CTRL+C to quit
 * Restarting with stat
```

## **Usage** <a name = "usage"></a>

Berikut ini adalah tampilan dari website RekoBuk.

![Usage-Gif](https://i.postimg.cc/Fsv8Ss49/web.gif)

Untuk menggunakan website ini, masukkan judul buku pada search bar, lalu pilih jenis rekomendasi (Content-Based/Item-Based), setelah itu klik pada tombol search untuk mencari buku rekomendasi.