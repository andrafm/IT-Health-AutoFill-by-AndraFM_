import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/formResponse"

def submit_form():
    try:
        tanggal = entry_tanggal.get()
        target = combo_target.get()
        kode_komputer = entry_kode.get()
        metode = combo_metode.get()
        ups = combo_ups.get()

        tgl = datetime.strptime(tanggal, "%Y-%m-%d")

        data = {
            "entry.283427473_day": tgl.day,
            "entry.283427473_month": tgl.month,
            "entry.283427473_year": tgl.year,
            "entry.729629067": "Andra Firmansyah",
            "entry.385266849": "SBY",
            "entry.1590388624": target,
            "entry.1885250742": kode_komputer,

            "entry.502122490": metode,

            "entry.1426045077": "Baik",
            "entry.792011826": "Baik",
            "entry.654245313": "Baik",
            "entry.1199810138": "Baik",
            "entry.1648101535": "Baik",
            "entry.447675297": ups,

            "entry.1602601477": "Ya",
            "entry.1435005536": "Ya",
            "entry.263709496": "Ya",
            "entry.1181879015": "Ya",
            "entry.1843770921": "Ya",
            "entry.2069737290": "Ya",
            "entry.204296501": "Ya",
            "entry.1130533675": "Ya",
            "entry.1714876202": "Ya",
            "entry.1947646856": "Ya",
            "entry.2095211759": "Ya",
            "entry.118622321": "Ya",
            "entry.1645981144": "Ya",
            "entry.102152864": "Ya",
            "entry.1522634640": "Ya",
            "entry.1785081968": "Ya",
            "entry.923069771": "Ya",
            "entry.1983326232": "Ya",
            "entry.323979629": "Ya",
            "entry.1936393138": "Ya",
            "entry.806371825": "Ya",

            "pageHistory": "0,1,2,5",
            "fbzx": "-9125506300963112535"
        }

        r = requests.post(FORM_URL, data=data)

        if r.status_code == 200:
            messagebox.showinfo("Sukses", "Form berhasil dikirim!")
        else:
            messagebox.showerror("Error", "Gagal submit!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =========================
# GUI DARK THEME
# =========================
root = tk.Tk()
root.title("Auto Maintenance Form")
root.geometry("420x380")
root.configure(bg="#0f0f0f")

# Style
style = ttk.Style()
style.theme_use("default")

# Frame utama
frame = tk.Frame(root, bg="#1a1a1a", padx=20, pady=20)
frame.pack(pady=20)

title = tk.Label(root, text="AUTO MAINTENANCE", 
                 font=("Segoe UI", 14, "bold"), 
                 bg="#0f0f0f", fg="white")
title.pack()

# Label Style
label_style = {"bg": "#1a1a1a", "fg": "white", "font": ("Segoe UI", 9)}

# Tanggal
tk.Label(frame, text="Tanggal (YYYY-MM-DD)", **label_style).grid(row=0, column=0, sticky="w", pady=5)
entry_tanggal = tk.Entry(frame, bg="#2a2a2a", fg="white", insertbackground="white")
entry_tanggal.grid(row=0, column=1)

# Target
tk.Label(frame, text="Target Perawatan", **label_style).grid(row=1, column=0, sticky="w", pady=5)
combo_target = ttk.Combobox(frame, values=["Toko", "Office"])
combo_target.grid(row=1, column=1)
combo_target.current(0)

# Kode
tk.Label(frame, text="Kode Toko / Komputer", **label_style).grid(row=2, column=0, sticky="w", pady=5)
entry_kode = tk.Entry(frame, bg="#2a2a2a", fg="white", insertbackground="white")
entry_kode.grid(row=2, column=1)

# Metode
tk.Label(frame, text="Metode Maintenance", **label_style).grid(row=3, column=0, sticky="w", pady=5)
combo_metode = ttk.Combobox(frame, values=[
    "Perawatan Jarak Jauh (Remote Maintenance)",
    "Perawatan Langsung (Visit/Direct Maintenance)"
])
combo_metode.grid(row=3, column=1)
combo_metode.current(0)

# UPS
tk.Label(frame, text="UPS", **label_style).grid(row=4, column=0, sticky="w", pady=5)
combo_ups = ttk.Combobox(frame, values=["Baik", "Rusak"])
combo_ups.grid(row=4, column=1)
combo_ups.current(0)

# Tombol Submit
btn_submit = tk.Button(root,
                       text="SUBMIT",
                       command=submit_form,
                       bg="#1f6feb",
                       fg="white",
                       font=("Segoe UI", 10, "bold"),
                       width=20,
                       height=2,
                       bd=0)
btn_submit.pack(pady=20)

root.mainloop()