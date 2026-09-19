# Cheat sheet cursorbot: 125 perintah

Ketik perintah di **mode shell** (`python cursorbot.py shell`, prompt `bot>`), atau tulis satu-satu di terminal dengan awalan `python cursorbot.py`, misalnya `python cursorbot.py click 50% 50%`.

**Hentikan bot kapan saja:** gerakkan mouse ke pojok kiri-atas layar, atau tekan Ctrl+C di terminal.

## Cara membuat perintah `click chrome` bekerja

1. Jalankan `save chrome --wait 5`.
2. Dalam 5 detik itu, arahkan mouse ke ikon Chrome (mis. di Dock) dan **biarkan diam**.
3. Setelah muncul `Tersimpan: chrome = ...`, perintah `click chrome` akan menggerakkan cursor ke sana dan mengklik.
4. Kalau ikon berpindah, jalankan `save chrome --wait 5` lagi untuk menimpa titiknya.

Cara yang lebih andal untuk membuka aplikasi adalah `open chrome`, karena tidak bergantung pada posisi ikon.

## Info & bantuan

| No | Perintah | Fungsi |
|---:|---|---|
| 1 | `pos` | posisi cursor sekarang |
| 2 | `size` | ukuran layar (lebar tinggi) |
| 3 | `track` | posisi cursor live untuk cari koordinat (Ctrl+C berhenti) |
| 4 | `titik` | daftar titik yang sudah disimpan |
| 5 | `move -h` | bantuan untuk satu perintah (ganti move dengan perintah lain) |
| 6 | `help` | daftar semua perintah (hanya di mode shell) |

## Pindah cursor: koordinat & persen

| No | Perintah | Fungsi |
|---:|---|---|
| 7 | `move 500 300` | pindah ke X=500, Y=300 |
| 8 | `move 20 20` | dekat pojok kiri-atas (jangan `move 0 0`, itu memicu fail-safe) |
| 9 | `move 1000 500 -d 1` | gerakan halus selama 1 detik |
| 10 | `move 800 600 -d 0.3` | gerakan cepat tapi tetap halus |
| 11 | `move 50% 50%` | tengah layar |
| 12 | `move 25% 75%` | seperempat dari kiri, tiga perempat dari atas |
| 13 | `move 90% 10%` | dekat pojok kanan-atas |
| 14 | `move 10% 10% -d 0.5` | dekat pojok kiri-atas, halus |
| 15 | `move 75% 50% -d 1` | tiga perempat ke kanan, tengah vertikal |
| 16 | `move 5% 95%` | dekat pojok kiri-bawah |

## Pindah cursor: posisi bawaan

| No | Perintah | Fungsi |
|---:|---|---|
| 17 | `move tengah` | tengah layar |
| 18 | `move atas` | tengah tepi atas |
| 19 | `move bawah` | tengah tepi bawah (area Dock di Mac) |
| 20 | `move kiri` | tengah tepi kiri |
| 21 | `move kanan` | tengah tepi kanan |
| 22 | `move kiriatas` | pojok kiri-atas (aman, jaraknya 15 px) |
| 23 | `move kananatas` | pojok kanan-atas |
| 24 | `move kiribawah` | pojok kiri-bawah |
| 25 | `move kananbawah` | pojok kanan-bawah |
| 26 | `move center -d 0.5` | tengah layar, halus (nama bawaan bahasa Inggris) |

## Pindah cursor: relatif dari posisi sekarang

| No | Perintah | Fungsi |
|---:|---|---|
| 27 | `move 100 0 -r` | geser 100 px ke kanan |
| 28 | `move -100 0 -r` | geser 100 px ke kiri |
| 29 | `move 0 100 -r` | geser 100 px ke bawah |
| 30 | `move 0 -100 -r` | geser 100 px ke atas |
| 31 | `move 50 50 -r -d 0.5` | geser diagonal kanan-bawah |
| 32 | `move -200 -200 -r -d 1` | geser diagonal kiri-atas, pelan |
| 33 | `move 10 0 -r` | geser kecil ke kanan (fine-tuning) |
| 34 | `move 0 10 -r` | geser kecil ke bawah |

## Klik

| No | Perintah | Fungsi |
|---:|---|---|
| 35 | `click` | klik kiri di posisi cursor sekarang |
| 36 | `click 500 300` | pindah lalu klik di 500 300 |
| 37 | `click 50% 50%` | klik di tengah layar |
| 38 | `click tengah` | klik di tengah layar (nama bawaan) |
| 39 | `click chrome` | klik titik yang kamu simpan dengan nama chrome |
| 40 | `click 500 300 -d 0.5` | gerak halus 0,5 detik, lalu klik |
| 41 | `click -n 2` | klik 2x di posisi sekarang |
| 42 | `click -n 3` | klik 3x (memilih satu baris/paragraf teks) |
| 43 | `click -b right` | klik kanan di posisi sekarang |
| 44 | `click 500 300 -b middle` | klik tombol tengah (roda mouse) |
| 45 | `double` | klik ganda di posisi sekarang |
| 46 | `double 500 300` | klik ganda di 500 300 |
| 47 | `double chrome` | klik ganda di titik chrome (mis. membuka file di Finder) |
| 48 | `right` | klik kanan di posisi sekarang |
| 49 | `right 500 300` | klik kanan di 500 300 |
| 50 | `right tengah` | klik kanan di tengah layar |

## Versi bahasa Indonesia (alias)

| No | Perintah | Fungsi |
|---:|---|---|
| 51 | `klik chrome` | sama dengan click chrome |
| 52 | `klik 50% 50%` | sama dengan click 50% 50% |
| 53 | `dobel 500 300` | sama dengan double 500 300 |
| 54 | `klikkanan tengah` | sama dengan right tengah |
| 55 | `pindah 50% 50%` | sama dengan move 50% 50% |
| 56 | `pindah 100 0 -r` | sama dengan move 100 0 -r |

## Drag (klik-tahan lalu seret)

| No | Perintah | Fungsi |
|---:|---|---|
| 57 | `drag 800 400` | seret dari posisi sekarang ke 800 400 |
| 58 | `drag 800 400 -d 1` | seret pelan selama 1 detik |
| 59 | `drag 200 0 -r` | seret 200 px ke kanan |
| 60 | `drag 0 200 -r` | seret 200 px ke bawah |
| 61 | `drag -300 0 -r -d 1` | seret ke kiri (memilih teks ke belakang) |
| 62 | `drag tengah` | seret ke tengah layar |
| 63 | `drag 50% 50% -d 0.8` | seret ke tengah, 0,8 detik |
| 64 | `seret 300 300 -d 0.6` | versi Indonesia dari drag |

## Scroll

| No | Perintah | Fungsi |
|---:|---|---|
| 65 | `scroll 5` | gulir naik sedikit |
| 66 | `scroll -5` | gulir turun sedikit |
| 67 | `scroll 20` | gulir naik jauh |
| 68 | `scroll -20` | gulir turun jauh |
| 69 | `scroll 3 --horizontal` | gulir ke kanan |
| 70 | `gulir -10` | versi Indonesia dari scroll (turun) |

## Ketik teks (hanya karakter ASCII)

| No | Perintah | Fungsi |
|---:|---|---|
| 71 | `type halo dunia` | ketik teks biasa |
| 72 | `type https://www.google.com` | ketik alamat web |
| 73 | `type hello@example.com` | ketik email |
| 74 | `type belajar python -i 0.1` | ketik pelan (jeda 0,1 detik per huruf) |
| 75 | `type 12345` | ketik angka |
| 76 | `ketik selamat pagi` | versi Indonesia dari type |

## Tekan tombol

| No | Perintah | Fungsi |
|---:|---|---|
| 77 | `key enter` | tekan Enter |
| 78 | `key tab` | tekan Tab |
| 79 | `key esc` | tekan Escape |
| 80 | `key backspace` | hapus satu karakter ke belakang |
| 81 | `key delete` | hapus karakter ke depan |
| 82 | `key space` | tekan spasi |
| 83 | `key down down down` | tekan panah bawah 3x |
| 84 | `key up` | tekan panah atas |
| 85 | `key pagedown` | Page Down |
| 86 | `key home` | tombol Home |
| 87 | `tekan tab tab enter` | versi Indonesia: Tab, Tab, lalu Enter |

## Kombinasi tombol: macOS

| No | Perintah | Fungsi |
|---:|---|---|
| 88 | `hotkey command space` | buka Spotlight |
| 89 | `hotkey command c` | copy |
| 90 | `hotkey command v` | paste |
| 91 | `hotkey command x` | cut |
| 92 | `hotkey command a` | pilih semua |
| 93 | `hotkey command z` | undo |
| 94 | `hotkey command s` | simpan |
| 95 | `hotkey command tab` | ganti aplikasi |
| 96 | `hotkey command w` | tutup tab/jendela |
| 97 | `hotkey command t` | tab baru (Chrome/Safari) |
| 98 | `hotkey command l` | fokus ke address bar browser |
| 99 | `hotkey command r` | reload halaman |
| 100 | `kombinasi command shift t` | buka lagi tab yang tertutup (alias Indonesia) |

## Kombinasi tombol: Windows/Linux

| No | Perintah | Fungsi |
|---:|---|---|
| 101 | `hotkey ctrl c` | copy |
| 102 | `hotkey ctrl v` | paste |
| 103 | `hotkey ctrl a` | pilih semua |
| 104 | `hotkey alt tab` | ganti aplikasi |
| 105 | `hotkey ctrl shift t` | buka lagi tab yang tertutup |

## Buka aplikasi & URL (tanpa perlu koordinat)

| No | Perintah | Fungsi |
|---:|---|---|
| 106 | `open chrome` | buka/aktifkan Google Chrome |
| 107 | `open safari` | buka Safari |
| 108 | `open Google Chrome` | nama lengkap juga bisa |
| 109 | `open finder` | buka Finder |
| 110 | `open notes` | buka aplikasi Notes |
| 111 | `open https://www.google.com` | buka URL di browser bawaan |
| 112 | `open chrome -w 3` | buka Chrome lalu tunggu 3 detik |
| 113 | `buka vscode` | versi Indonesia dari open |

## Simpan & kelola titik

| No | Perintah | Fungsi |
|---:|---|---|
| 114 | `save chrome --wait 5` | simpan posisi mouse 5 detik lagi sebagai chrome |
| 115 | `save chrome` | simpan posisi mouse saat ini sebagai chrome |
| 116 | `save tombol_kirim 640 400` | simpan koordinat tetap |
| 117 | `save tombol_kirim 50% 90%` | simpan posisi berbasis persen |
| 118 | `simpan dock --wait 5` | versi Indonesia dari save |
| 119 | `forget chrome` | hapus titik chrome |
| 120 | `hapus tombol_kirim` | versi Indonesia dari forget |

## Waktu & skrip

| No | Perintah | Fungsi |
|---:|---|---|
| 121 | `sleep 1` | tunggu 1 detik |
| 122 | `sleep 0.5` | tunggu setengah detik |
| 123 | `tunggu 2` | versi Indonesia dari sleep |
| 124 | `run macro.txt` | jalankan file macro |
| 125 | `jalankan macro.txt` | versi Indonesia dari run |

## Contoh macro (simpan sebagai file teks, jalankan dengan `run namafile.txt`)

Baris berawalan `#` dan baris kosong diabaikan.

**Buka Google di Chrome**

```
buka chrome -w 2
hotkey command l
ketik www.google.com
tekan enter
```

**Buka aplikasi lewat Spotlight**

```
hotkey command space
tunggu 0.5
ketik safari
tunggu 0.5
tekan enter
```

**Klik titik yang sudah disimpan, lalu ketik**

```
klik tombol_kirim
tunggu 0.3
ketik halo dunia
tekan enter
```

**Gerak-gerak lalu drag**

```
pindah 20% 30% -d 0.5
seret 60% 30% -d 1
pindah tengah -d 0.5
```

## Catatan penting

- **Nama tombol Mac:** `command`, `option`, `ctrl`, `shift`, `enter`, `esc`, `tab`, `space`, `up`, `down`, `left`, `right`.
- **Koordinat persen** (`50% 50%`) tetap benar walau resolusi layar berubah, sedangkan koordinat pixel tidak.
- **Titik tersimpan** berupa koordinat pixel di file `~/.cursorbot_points.json`. Jika Dock atau jendela berpindah, simpan ulang.
- **`type`** hanya mendukung karakter ASCII (huruf, angka, simbol biasa), bukan emoji atau huruf non-Latin.
- **macOS:** izin Accessibility untuk Terminal harus aktif, kalau tidak cursor tidak bergerak.
- **Jeda antar aksi:** macro yang berpindah aplikasi butuh `tunggu` supaya jendela sempat muncul sebelum aksi berikutnya.
