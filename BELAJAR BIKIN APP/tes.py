import customtkinter as ctk
from tkcalendar import DateEntry
import requests
from datetime import datetime

# Setting tampilan
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/formResponse"

def submit_form():
    try:
        tanggal = date_entry.get()
        tgl = datetime.strptime(tanggal, "%Y-%m-%d")

        day = tgl.day
        month = tgl.month
        year = tgl.year

        target = target_var.get()
        kode_toko = entry_kode.get()
        nama_komputer = entry_komputer.get()

        gabungan = f"{kode_toko} - {nama_komputer}"

        data = {
            "entry.283427473_day": day,
            "entry.283427473_month": month,
            "entry.283427473_year": year,
            "entry.729629067": "Andra Firmansyah",
            "entry.1590388624": "SBY",
            "entry.385266849": target,
            "entry.1885250742": gabungan
        }

        r = requests.post(FORM_URL, data=data)

        if r.status_code == 200:
            status_label.configure(text="✅ Berhasil Submit", text_color="green")
        else:
            status_label.configure(text="❌ Gagal Submit", text_color="red")

    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")


# APP
app = ctk.CTk()
app.title("Maintenance Form IT")
app.geometry("400x500")

# Title
title = ctk.CTkLabel(app, text="Maintenance Form IT", font=("Arial", 20, "bold"))
title.pack(pady=15)

# Tanggal
ctk.CTkLabel(app, text="Tanggal Maintenance").pack()
date_entry = DateEntry(app, date_pattern='yyyy-mm-dd')
date_entry.pack(pady=5)

# Info otomatis
ctk.CTkLabel(app, text="IT Support: Andra Firmansyah").pack(pady=5)
ctk.CTkLabel(app, text="Lokasi: SBY").pack(pady=5)

# Target
ctk.CTkLabel(app, text="Target Perawatan").pack(pady=5)
target_var = ctk.StringVar(value="Toko")

frame_radio = ctk.CTkFrame(app)
frame_radio.pack(pady=5)

ctk.CTkRadioButton(frame_radio, text="Toko", variable=target_var, value="Toko").pack(side="left", padx=10)
ctk.CTkRadioButton(frame_radio, text="Office", variable=target_var, value="Office").pack(side="left", padx=10)

# Kode Toko
ctk.CTkLabel(app, text="Kode Toko").pack(pady=5)
entry_kode = ctk.CTkEntry(app, placeholder_text="Contoh: SBY001")
entry_kode.pack(pady=5)

# Nama Komputer
ctk.CTkLabel(app, text="Nama Komputer").pack(pady=5)
entry_komputer = ctk.CTkEntry(app, placeholder_text="Contoh: PC Kasir 1")
entry_komputer.pack(pady=5)

# Submit Button
submit_btn = ctk.CTkButton(app, text="Submit", command=submit_form)
submit_btn.pack(pady=20)

# Status
status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()