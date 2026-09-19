#!/usr/bin/env python3
"""
cursorbot v2 - kendalikan cursor & keyboard lewat terminal.
Jalan di Windows, macOS, dan Linux (X11).

Instalasi:
    pip install pyautogui

Tiga cara pakai:
    python cursorbot.py klik chrome          # satu perintah
    python cursorbot.py shell                # mode interaktif
    python cursorbot.py run macro.txt        # jalankan file skrip

Cara "klik chrome":
    1. Simpan posisi ikon Chrome (sekali saja):
         python cursorbot.py simpan chrome --wait 5
       lalu dalam 5 detik arahkan mouse ke ikon Chrome dan biarkan diam.
    2. Sesudah itu:
         python cursorbot.py klik chrome
    Atau langsung buka aplikasinya (lebih andal, tanpa perlu koordinat):
         python cursorbot.py buka chrome

Target (untuk move/click/double/right/drag) bisa berupa:
    500 300          koordinat pixel
    50% 50%          persen layar (aman kalau resolusi berbeda)
    chrome           nama titik yang sudah disimpan (simpan NAMA)
    tengah, atas, bawah, kiri, kanan, kiriatas, kananatas, kiribawah, kananbawah

Keamanan: gerakkan mouse ke pojok kiri-atas layar (0,0) untuk menghentikan
bot secara paksa (fail-safe pyautogui). Ctrl+C di terminal juga bisa.
"""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
import webbrowser

try:
    import pyautogui
except (Exception, SystemExit) as e:
    # SystemExit ikut ditangkap: di Linux, pyautogui/mouseinfo menutup program
    # secara diam-diam bila tkinter belum terpasang.
    sys.exit(
        f"Gagal memuat pyautogui: {e or 'program dihentikan saat import'}\n"
        "Kemungkinan penyebab:\n"
        "  - belum terpasang    -> python -m pip install pyautogui\n"
        "  - Linux: tkinter     -> sudo apt install python3-tk python3-dev\n"
        "  - Linux: bukan X11   -> pakai sesi 'Xorg' (Wayland tidak didukung)\n"
        "  - Linux: DISPLAY     -> jalankan dari terminal di dalam desktop, bukan SSH"
    )

pyautogui.FAILSAFE = True   # pojok kiri-atas = emergency stop
pyautogui.PAUSE = 0.05      # jeda kecil antar aksi

POINTS_FILE = os.path.join(os.path.expanduser("~"), ".cursorbot_points.json")


# ------------------------------------------------------------ titik & target --
def load_points():
    try:
        with open(POINTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def store_points(points):
    with open(POINTS_FILE, "w", encoding="utf-8") as f:
        json.dump(points, f, indent=2, ensure_ascii=False)


def _builtin(name):
    """Nama posisi bawaan. Pojok diberi jarak 15px supaya tidak memicu fail-safe."""
    w, h = pyautogui.size()
    m = 15
    table = {
        "tengah": (w // 2, h // 2), "center": (w // 2, h // 2),
        "atas": (w // 2, m), "bawah": (w // 2, h - m),
        "kiri": (m, h // 2), "kanan": (w - m, h // 2),
        "kiriatas": (m, m), "topleft": (m, m),
        "kananatas": (w - m, m), "topright": (w - m, m),
        "kiribawah": (m, h - m), "bottomleft": (m, h - m),
        "kananbawah": (w - m, h - m), "bottomright": (w - m, h - m),
    }
    return table.get(name)


def _coord(token, total):
    """'500' -> 500 ; '50%' -> setengah dari lebar/tinggi layar."""
    if token.endswith("%"):
        return round(float(token[:-1]) / 100 * total)
    return int(token)


def resolve_target(tokens):
    """['500','300'] | ['50%','50%'] | ['chrome']  ->  (x, y)"""
    if len(tokens) == 2:
        w, h = pyautogui.size()
        try:
            return _coord(tokens[0], w), _coord(tokens[1], h)
        except ValueError:
            raise ValueError("Koordinat harus angka, mis. '500 300' atau '50% 50%'.")
    if len(tokens) == 1:
        name = tokens[0].lower()
        try:
            float(name.rstrip("%"))
        except ValueError:
            pass
        else:
            raise ValueError("Koordinat butuh dua angka: X Y  (mis. 500 300 atau 50% 50%).")
        points = load_points()
        if name in points:
            return tuple(points[name])
        b = _builtin(name)
        if b:
            return b
        raise ValueError(
            f"Titik '{tokens[0]}' belum dikenal. Simpan dulu:  simpan {tokens[0]} --wait 5"
            "   (lihat daftar titik: titik)")
    raise ValueError("Target harus 'X Y' (angka atau persen) atau satu NAMA titik.")


def _xy_rel(tokens):
    if len(tokens) != 2:
        raise ValueError("Mode --rel butuh dua angka: dx dy")
    return int(tokens[0]), int(tokens[1])


# ----------------------------------------------------------------- perintah --
def _show_pos():
    x, y = pyautogui.position()
    print(f"pos: {x} {y}")


def cmd_pos(a):
    x, y = pyautogui.position()
    print(f"{x} {y}")


def cmd_size(a):
    w, h = pyautogui.size()
    print(f"{w} {h}")


def cmd_move(a):
    if a.rel:
        dx, dy = _xy_rel(a.target)
        pyautogui.moveRel(dx, dy, duration=a.duration)
    else:
        x, y = resolve_target(a.target)
        pyautogui.moveTo(x, y, duration=a.duration)
    _show_pos()


def _click(a, button=None, clicks=None):
    x = y = None
    if a.target:
        x, y = resolve_target(a.target)
    pyautogui.click(
        x=x, y=y,
        button=button or a.button,
        clicks=clicks or a.clicks,
        interval=0.1,
        duration=a.duration,
    )
    _show_pos()


def cmd_click(a):
    _click(a)


def cmd_double(a):
    _click(a, button="left", clicks=2)


def cmd_right(a):
    _click(a, button="right", clicks=1)


def cmd_drag(a):
    if a.rel:
        dx, dy = _xy_rel(a.target)
        pyautogui.dragRel(dx, dy, duration=a.duration, button=a.button)
    else:
        x, y = resolve_target(a.target)
        pyautogui.dragTo(x, y, duration=a.duration, button=a.button)
    _show_pos()


def cmd_scroll(a):
    if a.horizontal:
        pyautogui.hscroll(a.amount)
    else:
        pyautogui.scroll(a.amount)


def cmd_type(a):
    pyautogui.write(" ".join(a.text), interval=a.interval)


def cmd_key(a):
    for k in a.keys:
        pyautogui.press(k)


def cmd_hotkey(a):
    pyautogui.hotkey(*a.keys)


def cmd_sleep(a):
    time.sleep(a.seconds)


def cmd_track(a):
    print("Menampilkan posisi cursor. Tekan Ctrl+C untuk berhenti.")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rX: {x:5d}  Y: {y:5d}", end="", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print()


def cmd_save(a):
    name = a.name.lower()
    if _builtin(name) is not None and name not in load_points():
        print(f"Catatan: '{name}' adalah nama bawaan; titik simpananmu akan menimpanya.")
    if a.target:
        x, y = resolve_target(a.target)
    else:
        if a.wait > 0:
            print(f"Arahkan mouse ke posisi yang mau disimpan sebagai '{name}'...")
            for i in range(int(a.wait), 0, -1):
                print(f"  {i}...", end="\r", flush=True)
                time.sleep(1)
        x, y = pyautogui.position()
    points = load_points()
    points[name] = [int(x), int(y)]
    store_points(points)
    print(f"Tersimpan: {name} = {x} {y}   (file: {POINTS_FILE})")


def cmd_points(a):
    points = load_points()
    if not points:
        print("Belum ada titik tersimpan. Contoh:  simpan chrome --wait 5")
        return
    for name, (x, y) in sorted(points.items()):
        print(f"{name:20s} {x} {y}")


def cmd_forget(a):
    points = load_points()
    name = a.name.lower()
    if name not in points:
        raise ValueError(f"Titik '{a.name}' tidak ada.")
    del points[name]
    store_points(points)
    print(f"Dihapus: {name}")


APP_ALIASES = {
    "darwin": {
        "chrome": "Google Chrome", "safari": "Safari", "firefox": "Firefox",
        "finder": "Finder", "terminal": "Terminal", "notes": "Notes",
        "vscode": "Visual Studio Code", "settings": "System Settings",
        "spotify": "Spotify", "calculator": "Calculator",
    },
    "win32": {
        "chrome": "chrome", "edge": "msedge", "firefox": "firefox",
        "notepad": "notepad", "explorer": "explorer", "calculator": "calc",
        "vscode": "code",
    },
    "linux": {
        "chrome": "google-chrome", "firefox": "firefox", "files": "nautilus",
        "terminal": "gnome-terminal", "vscode": "code", "calculator": "gnome-calculator",
    },
}


def cmd_open(a):
    target = " ".join(a.app)
    if target.startswith(("http://", "https://")):
        if not webbrowser.open(target):
            raise RuntimeError("Tidak bisa membuka browser untuk URL itu.")
        print(f"Dibuka: {target}")
    else:
        plat = "win32" if sys.platform.startswith("win") else sys.platform
        name = APP_ALIASES.get(plat, {}).get(target.lower(), target)
        if plat == "darwin":
            r = subprocess.run(["open", "-a", name], capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(r.stderr.strip() or f"Aplikasi '{name}' tidak ditemukan.")
        elif plat == "win32":
            subprocess.Popen(["cmd", "/c", "start", "", name])
        else:
            exe = shutil.which(name)
            if not exe:
                raise RuntimeError(f"Program '{name}' tidak ditemukan di PATH.")
            subprocess.Popen([exe], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        print(f"Dibuka: {name}")
    time.sleep(a.wait)  # beri waktu aplikasi tampil sebelum perintah berikutnya


def cmd_run(a):
    with open(a.file, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            print(f"[{n}] {line}")
            if not execute(line):
                print(f"Berhenti di baris {n}.")
                break


def cmd_shell(a):
    print("cursorbot shell. Ketik 'help' untuk daftar perintah, 'exit' untuk keluar.")
    while True:
        try:
            line = input("bot> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ("exit", "quit", "keluar"):
            break
        if line == "help":
            PARSER.print_help()
            continue
        execute(line)


# ------------------------------------------------------------------- parser --
def build_parser():
    p = argparse.ArgumentParser(
        prog="cursorbot",
        description="Kontrol cursor & keyboard lewat terminal. "
                    "Nama dalam kurung = alias bahasa Indonesia.",
    )
    sub = p.add_subparsers(dest="command", metavar="perintah")

    def add(name, func, help_, aliases=()):
        sp = sub.add_parser(name, help=help_, description=help_, aliases=list(aliases))
        sp.set_defaults(func=func)
        return sp

    add("pos", cmd_pos, "tampilkan posisi cursor saat ini", ["posisi"])
    add("size", cmd_size, "tampilkan ukuran layar", ["ukuran"])
    add("track", cmd_track, "tampilkan posisi cursor live (untuk cari koordinat)", ["lacak"])

    sp = add("move", cmd_move, "pindahkan cursor ke target (X Y | X% Y% | NAMA)", ["pindah"])
    sp.add_argument("target", nargs="+")
    sp.add_argument("-d", "--duration", type=float, default=0.0,
                    help="lama gerakan (detik), supaya halus")
    sp.add_argument("-r", "--rel", action="store_true",
                    help="relatif dari posisi sekarang: dx dy")

    for name, func, h, al in (
        ("click", cmd_click, "klik (opsional di target)", ["klik"]),
        ("double", cmd_double, "klik ganda (opsional di target)", ["dobel"]),
        ("right", cmd_right, "klik kanan (opsional di target)", ["klikkanan"]),
    ):
        sp = add(name, func, h, al)
        sp.add_argument("target", nargs="*", help="X Y | X% Y% | NAMA (kosong = posisi sekarang)")
        sp.add_argument("-d", "--duration", type=float, default=0.0)
        if name == "click":
            sp.add_argument("-b", "--button", default="left",
                            choices=["left", "right", "middle"])
            sp.add_argument("-n", "--clicks", type=int, default=1)

    sp = add("drag", cmd_drag, "tahan klik & seret ke target", ["seret"])
    sp.add_argument("target", nargs="+")
    sp.add_argument("-d", "--duration", type=float, default=0.5)
    sp.add_argument("-r", "--rel", action="store_true", help="relatif: dx dy")
    sp.add_argument("-b", "--button", default="left",
                    choices=["left", "right", "middle"])

    sp = add("scroll", cmd_scroll, "scroll (positif = naik, negatif = turun)", ["gulir"])
    sp.add_argument("amount", type=int)
    sp.add_argument("--horizontal", action="store_true")

    sp = add("type", cmd_type, "ketik teks (hanya karakter ASCII)", ["ketik"])
    sp.add_argument("text", nargs="+")
    sp.add_argument("-i", "--interval", type=float, default=0.02)

    sp = add("key", cmd_key, "tekan satu/lebih tombol, mis. enter, tab, esc", ["tekan"])
    sp.add_argument("keys", nargs="+")

    sp = add("hotkey", cmd_hotkey, "kombinasi tombol, mis. command c / ctrl c", ["kombinasi"])
    sp.add_argument("keys", nargs="+")

    sp = add("sleep", cmd_sleep, "tunggu beberapa detik", ["tunggu"])
    sp.add_argument("seconds", type=float)

    sp = add("save", cmd_save, "simpan posisi sebagai nama (default: posisi cursor sekarang)",
             ["simpan"])
    sp.add_argument("name")
    sp.add_argument("target", nargs="*", help="opsional: X Y; kosong = posisi cursor")
    sp.add_argument("-w", "--wait", type=float, default=0,
                    help="tunggu N detik dulu agar sempat mengarahkan mouse")

    add("points", cmd_points, "daftar titik tersimpan", ["titik"])

    sp = add("forget", cmd_forget, "hapus titik tersimpan", ["hapus"])
    sp.add_argument("name")

    sp = add("open", cmd_open, "buka aplikasi atau URL (chrome, safari, https://...)", ["buka"])
    sp.add_argument("app", nargs="+")
    sp.add_argument("-w", "--wait", type=float, default=1.0,
                    help="tunggu N detik setelah membuka (default 1)")

    sp = add("run", cmd_run, "jalankan file skrip berisi perintah per baris", ["jalankan"])
    sp.add_argument("file")

    add("shell", cmd_shell, "mode interaktif")
    return p


PARSER = build_parser()


def execute(line):
    """Jalankan satu baris perintah. Return False jika terjadi error."""
    try:
        args = PARSER.parse_args(shlex.split(line))
    except SystemExit:          # argparse sudah mencetak pesan error/help
        return False
    except ValueError as e:     # kutip tidak seimbang, dll
        print(f"Error: {e}")
        return False

    if not getattr(args, "func", None):
        PARSER.print_help()
        return False
    try:
        args.func(args)
        return True
    except pyautogui.FailSafeException:
        print("Fail-safe aktif (cursor di pojok kiri-atas). Aksi dihentikan.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    args = PARSER.parse_args()
    if args.command is None:
        cmd_shell(args)
        return
    try:
        args.func(args)
    except pyautogui.FailSafeException:
        sys.exit("Fail-safe aktif (cursor di pojok kiri-atas). Dihentikan.")
    except KeyboardInterrupt:
        sys.exit("\nDihentikan.")
    except Exception as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()
