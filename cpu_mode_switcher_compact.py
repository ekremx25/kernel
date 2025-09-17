#!/usr/bin/env python3
# UltraMode Tarafından Yaratılmış, 4 Kişilikli, Nihai CPU Hükümdarı

import subprocess
from tkinter import Tk, Button, messagebox, simpledialog

# === RENK PALETİ (Catppuccin Mocha) ===
PALETTE = {
    "base":     "#1E1E2E",
    "surface0": "#313244",
    "text":     "#CDD6F4",
    "red":      "#F38BA8", # Performans
    "yellow":   "#F9E2AF", # Dengeli
    "sapphire": "#74C7EC", # Özel Eco Modu
    "green":    "#A6E3A1", # Derin Güç Tasarrufu
    "crust":    "#11111B"
}

# === AYARLAR (4 Farklı Savaş Modu) ===
MODES = {
    "Performance": {
        "governor": "performance",
        "min_freq": "4.0GHz",
        "max_freq": "5.6GHz",
        "color": PALETTE["red"],
        "desc": "Tam güç, sıfır taviz. Tüm çekirdekler coşar."
    },
    "Balanced": {
        "governor": "schedutil",
        "min_freq": "2.5GHz",
        "max_freq": "5.0GHz",
        "color": PALETTE["yellow"],
        "desc": "Akıllı güç yönetimi. İhtiyaca göre hızlanır."
    },
    "Custom Eco": {
        "governor": "userspace", # Frekansları ZORLA ayarlamak için
        "min_freq": "3.0GHz",
        "max_freq": "4.7GHz",
        "color": PALETTE["sapphire"],
        "desc": "Belirlenen frekans aralığında kalır. Kontrol tamamen sizde."
    },
    "Deep Powersave": {
        "governor": "powersave",
        "min_freq": "En Düşük", # Bu mod frekans dinlemez
        "max_freq": "En Düşük",
        "color": PALETTE["green"],
        "desc": "İşlemciyi en düşük frekansa kilitler. Maksimum tasarruf."
    }
}

# === ÇEKİRDEK FONKSİYONLAR ===
def run_sudo_commands(commands, password):
    for cmd in commands:
        try:
            subprocess.run(
                ["sudo", "-S"] + cmd,
                input=password.encode('utf-8'),
                capture_output=True,
                check=True,
                timeout=5
            )
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8').strip()
            # Önemli olmayan hataları görmezden gel
            if "Invalid argument" not in error_message:
                 return False, f"Komut başarısız: {' '.join(cmd)}\n\nHata: {error_message}"
        except FileNotFoundError:
            return False, f"Komut bulunamadı: {cmd[0]}. 'cpupower' paketi kurulu mu?"
        except Exception as e:
            return False, f"Beklenmedik bir hata oluştu: {e}"
    return True, "Tüm komutlar başarıyla çalıştırıldı."

def set_cpu_mode(mode_name, root_window):
    password = simpledialog.askstring("Yetki Gerekli", "Lütfen sudo şifrenizi girin:", show='*')
    if not password:
        return

    config = MODES[mode_name]

    # Çalıştırılacak komutları dinamik olarak oluştur
    commands_to_run = [
        ["cpupower", "frequency-set", "-g", config["governor"]]
    ]
    # Sadece frekans değeri olan modlar için frekans komutlarını ekle
    if "GHz" in config.get("min_freq", ""):
        commands_to_run.append(["cpupower", "frequency-set", "-d", config["min_freq"]])
        commands_to_run.append(["cpupower", "frequency-set", "-u", config["max_freq"]])

    success, output = run_sudo_commands(commands_to_run, password)

    if success:
        messagebox.showinfo("Başarı",
                            f"CPU modu başarıyla ayarlandı:\n\n"
                            f"Mod: {mode_name}\n"
                            f"Açıklama: {config['desc']}")
        root_window.destroy()
    else:
        messagebox.showerror("Hata!", f"Bir sorun oluştu:\n\n{output}")

# === GRAFİK ARAYÜZ ===
def create_gui():
    root = Tk()
    root.title("CPU Hükümdarı")
    root.geometry("300x350") # 4 buton için boyutu artırdık
    root.resizable(False, False)
    root.configure(background=PALETTE["base"])
    root.attributes('-topmost', True)

    for mode, details in MODES.items():
        btn = Button(
            root,
            text=mode,
            width=15, font=("Noto Sans", 10, "bold"),
            bg=details["color"], fg=PALETTE["crust"],
            activebackground=PALETTE["surface0"], activeforeground=details["color"],
            relief="flat", borderwidth=0,
            command=lambda m=mode: set_cpu_mode(m, root)
        )
        btn.pack(pady=10)

    root.mainloop()

# === BAŞLANGIÇ NOKTASI ===
if __name__ == "__main__":
    create_gui()
