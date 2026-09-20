# Cursorbot

Kendalikan cursor mouse dan keyboard lewat terminal. Bisa dipakai di macOS, Windows, dan Linux (X11).

Isi folder:

| File | Fungsi |
|---|---|
| `cursorbot.py` | program |
| `cheatsheet.md` | perintah siap salin |
| `README.md` | panduan |


## 1. Instalasi

```bash
python -m pip install pyautogui
```

- **macOS:** setelah instal, aktifkan izin **Accessibility** untuk Terminal di *System Settings → Privacy & Security → Accessibility*. Tanpa ini cursor tidak akan bergerak. Setelah mengaktifkan, tutup Terminal dengan **Cmd+Q** lalu buka lagi.
- **Linux:** jalankan `sudo apt install python3-tk python3-dev` dan pakai sesi **X11** (Wayland tidak didukung).
- **Windows:** langsung jalan. Jalankan dari Command Prompt atau PowerShell.

Kalau instalasi gagal di Mac dengan pesan `Cannot locate a working compiler`, lihat bagian [Pemecahan masalah](#7-pemecahan-masalah).


## 2. Cara menghentikan bot (baca dulu sebelum mencoba)

Kalau bot melakukan sesuatu yang tidak kamu inginkan:

1. **Gerakkan mouse ke pojok kiri-atas layar** dan tahan sampai bot berhenti. Ini pengaman utama dan bekerja di jendela mana pun.
2. **Ctrl+C** di Terminal. Hanya bekerja kalau jendela Terminal sedang aktif, jadi tekan **Cmd+Tab** dulu untuk kembali ke Terminal.
3. **Cmd+Q** pada Terminal. Ini cara paling pasti untuk mematikan semuanya.


## 3. Panduan pemakaian yang aman, langkah demi langkah

Ikuti berurutan. Jangan lompat ke langkah besar sebelum langkah kecilnya berhasil.

### Langkah 1: Siapkan Terminal

```bash
cd ~/cursorbot
ls
```

Harus muncul `cursorbot.py`. Kalau kamu memakai environment conda khusus, aktifkan dulu (contoh: `conda activate bot`) sebelum `cd`.

> **Windows:** gunakan `cd %USERPROFILE%\cursorbot` dan `dir`.

### Langkah 2: Tes perintah yang hanya membaca

Dua perintah ini tidak menggerakkan apa-apa:

```bash
python cursorbot.py size
python cursorbot.py pos
```

Kalau angka keluar, bot sudah bisa membaca layarmu.

### Langkah 3: Tes gerak tanpa klik

```bash
python cursorbot.py pindah 50% 50% -d 1
```

Cursor harus meluncur pelan ke tengah layar. Coba juga:

```bash
python cursorbot.py pindah kanan -d 1
python cursorbot.py pindah tengah -d 1
```

Kalau cursor tidak bergerak, cek izin Accessibility (bagian 1).

### Langkah 4: Klik pertama di tempat yang aman

Jangan langsung mengklik di aplikasi lain. Cari dulu koordinat area kosong, misalnya bagian kosong jendela Terminal:

```bash
python cursorbot.py track
```

Arahkan mouse ke area kosong itu, catat angka X dan Y, lalu tekan Ctrl+C. Setelah itu:

```bash
python cursorbot.py klik 400 300
```

Ganti `400 300` dengan angka yang kamu catat.

### Langkah 5: Simpan titik Chrome dan verifikasi sebelum klik

```bash
python cursorbot.py simpan chrome --wait 5
```

Setelah menekan Enter, arahkan mouse ke ikon Chrome dan **biarkan diam** sampai muncul `Tersimpan: chrome = ...`.

**Jangan langsung `klik`.** Lihat dulu ke mana cursor akan pergi:

```bash
python cursorbot.py pindah chrome -d 1
```

Kalau cursor tepat di ikon Chrome, baru lanjut:

```bash
python cursorbot.py klik chrome
```

Nama titik bebas, misalnya `simpan tombol_kirim --wait 5` lalu `klik tombol_kirim`.

### Langkah 6: Buka aplikasi tanpa koordinat

```bash
python cursorbot.py buka chrome
```

Ini lebih andal daripada mengklik ikon, karena tidak bergantung pada posisi Dock atau jendela.

### Langkah 7: Mode interaktif untuk mencoba serangkaian perintah

```bash
python cursorbot.py shell
```

Ketik satu perintah per baris (tanpa `python cursorbot.py`), misalnya:

```
bot> pindah tengah -d 1
bot> klik
bot> pos
bot> exit
```

Ini cara terbaik untuk menguji urutan perintah sebelum dijadikan macro.

### Langkah 8: Membuat macro

Buat file teks bernama `macro.txt` di folder `cursorbot`, satu perintah per baris:

```
buka chrome -w 2
hotkey command l
ketik www.google.com
tekan enter
```

Di macOS/Linux, kamu bisa membuatnya langsung dari Terminal dengan menyalin semua baris ini sekaligus:

```bash
cat > ~/cursorbot/macro.txt <<'EOF'
buka chrome -w 2
hotkey command l
ketik www.google.com
tekan enter
EOF
```

Lalu jalankan:

```bash
cd ~/cursorbot
python cursorbot.py run macro.txt
```

Baris kosong dan baris berawalan `#` diabaikan. Jangan mulai dengan macro panjang: uji tiap baris di mode shell (langkah 7), baru gabungkan.

> **Windows/Linux:** ganti `command` dengan `ctrl` pada baris `hotkey`.


## 4. Aturan aman

- **Awasi bot saat berjalan.** Jangan tinggalkan dan jangan jalankan tanpa dilihat.
- **Gerak dulu, klik kemudian.** Pakai `pindah` untuk memastikan lokasinya benar sebelum `klik`.
- **Hindari kombinasi tombol berisiko** seperti `hotkey command q` (keluar aplikasi) atau `key delete`, terutama kalau ada dokumen yang belum disimpan.
- **Jangan mengetik password lewat `ketik`.** Perintah tersimpan di riwayat Terminal dan di file macro.
- **`ketik` masuk ke jendela yang sedang aktif.** Kalau jendela yang salah sedang di depan, teksnya nyasar. Beri `tunggu 1` setelah `buka` supaya aplikasinya sempat muncul.
- **Titik simpanan bisa meleset** kalau Dock atau jendela berpindah. Simpan ulang dan cek dengan `pindah`.
- **Matikan izin Accessibility Terminal** kalau sedang tidak memakai bot.


## 5. Jenis target

Perintah `pindah`, `klik`, `dobel`, `klikkanan`, dan `seret` menerima target berikut:

| Bentuk | Contoh | Arti |
|---|---|---|
| Koordinat pixel | `500 300` | posisi X dan Y |
| Persen layar | `50% 50%` | tetap benar walau resolusi berubah |
| Nama titik | `chrome` | titik yang kamu simpan dengan `simpan` |
| Nama bawaan | `tengah`, `atas`, `bawah`, `kiri`, `kanan`, `kiriatas`, `kananatas`, `kiribawah`, `kananbawah` | posisi standar di layar |

Kalau `klik` dijalankan tanpa target, klik terjadi di posisi cursor sekarang.


## 6. Ringkasan perintah

Setiap perintah punya nama Inggris dan alias Indonesia. Daftar lengkap ada di [`cheatsheet.md`](cheatsheet.md).

| Perintah (alias) | Fungsi |
|---|---|
| `pos` (`posisi`) | posisi cursor sekarang |
| `size` (`ukuran`) | ukuran layar |
| `track` (`lacak`) | posisi cursor live untuk mencari koordinat |
| `move` (`pindah`) | pindahkan cursor; `-d 1` untuk gerak halus, `-r` untuk relatif |
| `click` (`klik`) | klik; `-n 2` untuk 2x, `-b right` untuk klik kanan |
| `double` (`dobel`) | klik ganda |
| `right` (`klikkanan`) | klik kanan |
| `drag` (`seret`) | tahan klik lalu seret |
| `scroll` (`gulir`) | gulir; angka negatif = turun |
| `type` (`ketik`) | ketik teks (hanya karakter ASCII) |
| `key` (`tekan`) | tekan tombol: `enter`, `tab`, `esc`, dan sebagainya |
| `hotkey` (`kombinasi`) | kombinasi tombol: `command c`, `ctrl v`, dan sebagainya |
| `sleep` (`tunggu`) | jeda dalam detik |
| `save` (`simpan`) | simpan posisi sebagai nama; `--wait 5` menunggu 5 detik dulu |
| `points` (`titik`) | daftar titik tersimpan |
| `forget` (`hapus`) | hapus titik tersimpan |
| `open` (`buka`) | buka aplikasi atau URL |
| `run` (`jalankan`) | jalankan file macro |
| `shell` | mode interaktif |

Bantuan untuk satu perintah: `python cursorbot.py pindah -h`.


## 7. Pemecahan masalah

**Cursor tidak bergerak (macOS).** Aktifkan Terminal di *System Settings → Privacy & Security → Accessibility*, lalu **Cmd+Q** dan buka Terminal lagi. Kalau kamu menjalankan dari iTerm atau VS Code, aktifkan aplikasi itu.

**`Operation not permitted` saat `ls` atau `pip` di folder Downloads (macOS).** macOS memblokir Terminal dari folder Downloads. Pindahkan folder `cursorbot` ke folder Home lewat Finder (seret ke folder dengan nama akunmu), lalu kerjakan dari `~/cursorbot`. Alternatifnya, beri izin di *System Settings → Privacy & Security → Files & Folders → Terminal → Downloads Folder*.

**`Cannot locate a working compiler` / gagal membangun `pyobjc-core` (macOS, Python 3.9).** Python 3.9 terlalu tua untuk PyObjC terbaru. Instal versi lama yang sudah berupa paket siap pakai:

```bash
cd ~
python -m pip install --only-binary=pyobjc-core,pyobjc-framework-Cocoa,pyobjc-framework-Quartz "pyobjc-core<12" "pyobjc-framework-Cocoa<12" "pyobjc-framework-Quartz<12" pyautogui
```

Kalau masih gagal, buat environment dengan Python yang lebih baru:

```bash
cd ~
conda create -n bot python=3.11 -y
conda activate bot
python -m pip install pyautogui
```

Setiap kali membuka Terminal baru, jalankan `conda activate bot` dulu.

**`Titik 'xxx' belum dikenal`.** Titik itu belum disimpan. Jalankan `simpan xxx --wait 5`, atau lihat daftar dengan `titik`.

**`Koordinat butuh dua angka`.** Target koordinat harus lengkap: `klik 500 300`, bukan `klik 500`.

**`Fail-safe aktif`.** Cursor berada di pojok kiri-atas layar, jadi bot berhenti. Itu pengaman yang bekerja. Jangan memakai `pindah 0 0`; pakai `pindah 20 20` atau `pindah kiriatas`.

**`buka chrome` error.** Coba nama lengkap: `buka Google Chrome`. Di Windows pastikan Chrome terpasang normal, di Linux pastikan `google-chrome` ada di PATH.

**Linux: program berhenti tanpa pesan atau `DISPLAY` error.** Pasang `python3-tk`, gunakan sesi X11, dan jalankan dari terminal di dalam desktop, bukan lewat SSH.

**Teks yang diketik salah atau kosong.** `ketik` hanya mendukung karakter ASCII. Emoji dan huruf non-Latin tidak bisa. Pastikan juga jendela tujuan sedang aktif.
