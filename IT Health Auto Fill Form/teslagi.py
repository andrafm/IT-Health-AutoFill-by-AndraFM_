import customtkinter as ctk
import requests
from tkinter import messagebox
from tkcalendar import DateEntry
import threading

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/formResponse"


class ITHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IT Health Auto Fill Form")
        self.geometry("350x700")
        self.minsize(350, 700)
        self.configure(fg_color="#0f1720")

        self.accent = "#3b82f6"
        self.card = "#111214"
        self.device_radio_buttons = []
        self._build()

    def _add_status_row(self, parent, label_text, variable):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", fill="x", padx=16, pady=0)

        ctk.CTkLabel(
            row,
            text=label_text,
            width=145,
            anchor="w",
            font=("Segoe UI", 10)
        ).pack(side="left")

        rb_baik = ctk.CTkRadioButton(
            row,
            text="Baik",
            variable=variable,
            value="Baik",
            font=("Segoe UI", 10),
            width=72,
            height=18
        )
        rb_baik.pack(side="left", padx=(4, 4))

        rb_rusak = ctk.CTkRadioButton(
            row,
            text="Rusak",
            variable=variable,
            value="Rusak",
            font=("Segoe UI", 10),
            width=72,
            height=18
        )
        rb_rusak.pack(side="left", padx=(0, 4))

        self.device_radio_buttons.extend([rb_baik, rb_rusak])

    def toggle_baik_semua(self):
        device_vars = [
            self.pc_kasir_var,
            self.keyboard_kasir_var,
            self.mouse_kasir_var,
            self.monitor_kasir_var,
            self.printer_thermal_var,
            self.ups_var,
        ]

        if self.all_baik_var.get():
            for var in device_vars:
                var.set("Baik")
            for rb in self.device_radio_buttons:
                rb.configure(state="disabled")
        else:
            for rb in self.device_radio_buttons:
                rb.configure(state="normal")

    def _build(self):
        header = ctk.CTkFrame(self, fg_color=self.accent, height=62, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="IT Health Auto Fill Form",
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        ).pack(pady=(6, 0))

        ctk.CTkLabel(
            header,
            text="Surabaya Branch",
            font=("Segoe UI", 10),
            text_color="#e6eefc"
        ).pack()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=6)

        card = ctk.CTkFrame(container, fg_color=self.card, corner_radius=12)
        card.pack(fill="both", expand=True, padx=2, pady=2)

        # Date
        ctk.CTkLabel(card, text="Tanggal Maintenance", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=12, pady=(6, 1)
        )

        self.cal = DateEntry(
            card,
            width=16,
            background=self.accent,
            foreground="white",
            borderwidth=2,
            font=("Segoe UI", 11),
            date_pattern="dd/mm/yyyy"
        )
        self.cal.pack(anchor="w", padx=12, ipady=0)

        # Kode
        ctk.CTkLabel(card, text="Kode Toko / Nama Komputer", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=12, pady=(5, 1)
        )

        self.entry_kode = ctk.CTkEntry(
            card,
            width=270,
            height=28,
            font=("Segoe UI", 11),
            placeholder_text="Contoh: SN-NB001 / SB-PC001"
        )
        self.entry_kode.pack(anchor="w", padx=12)

        # Target
        ctk.CTkLabel(card, text="Target Perawatan", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=12, pady=(5, 1)
        )

        self.target_var = ctk.StringVar(value="Toko Planet Ban")
        tf = ctk.CTkFrame(card, fg_color="transparent")
        tf.pack(anchor="w", padx=12, pady=0)

        ctk.CTkRadioButton(
            tf,
            text="Toko",
            variable=self.target_var,
            value="Toko Planet Ban",
            font=("Segoe UI", 11),
            height=18
        ).pack(side="left", padx=(0, 8))

        ctk.CTkRadioButton(
            tf,
            text="Office",
            variable=self.target_var,
            value="Office HO/Cabang",
            font=("Segoe UI", 11),
            height=18
        ).pack(side="left", padx=(0, 8))

        # Metode
        ctk.CTkLabel(card, text="Metode Maintenance", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=12, pady=(5, 1)
        )

        self.metode_var = ctk.StringVar(value="Perawatan Jarak Jauh (Remote Maintenance)")
        mf = ctk.CTkFrame(card, fg_color="transparent")
        mf.pack(anchor="w", padx=12, pady=0)

        ctk.CTkRadioButton(
            mf,
            text="Remote",
            variable=self.metode_var,
            value="Perawatan Jarak Jauh (Remote Maintenance)",
            font=("Segoe UI", 11),
            height=18
        ).pack(side="left", padx=(0, 8))

        ctk.CTkRadioButton(
            mf,
            text="Visit",
            variable=self.metode_var,
            value="Perawatan Langsung (Visit/Direct Maintenance)",
            font=("Segoe UI", 11),
            height=18
        ).pack(side="left", padx=(0, 8))

        # Kondisi perangkat toko
        kondisi_row = ctk.CTkFrame(card, fg_color="transparent")
        kondisi_row.pack(fill="x", padx=14, pady=(5, 1))

        ctk.CTkLabel(
            kondisi_row,
            text="Kondisi Perangkat Toko",
            width=135,
            anchor="w",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        ctk.CTkLabel(kondisi_row, text="", width=46).pack(side="left")

        self.all_baik_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            kondisi_row,
            text="Baik Semua",
            variable=self.all_baik_var,
            command=self.toggle_baik_semua,
            font=("Segoe UI", 11, "bold"),
            width=105,
            height=18
        ).pack(side="left", padx=(2, 0))

        self.pc_kasir_var = ctk.StringVar(value="Baik")
        self.keyboard_kasir_var = ctk.StringVar(value="Baik")
        self.mouse_kasir_var = ctk.StringVar(value="Baik")
        self.monitor_kasir_var = ctk.StringVar(value="Baik")
        self.printer_thermal_var = ctk.StringVar(value="Baik")
        self.ups_var = ctk.StringVar(value="Baik")

        self.device_radio_buttons = []
        self._add_status_row(card, "PC Kasir", self.pc_kasir_var)
        self._add_status_row(card, "Keyboard Kasir", self.keyboard_kasir_var)
        self._add_status_row(card, "Mouse Kasir", self.mouse_kasir_var)
        self._add_status_row(card, "Monitor Kasir", self.monitor_kasir_var)
        self._add_status_row(card, "Printer Thermal", self.printer_thermal_var)
        self._add_status_row(card, "UPS Kasir", self.ups_var)

        # Catatan
        ctk.CTkLabel(
            card,
            text="Catatan (bila ada)",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=12, pady=(6, 1))

        self.catatan_text = ctk.CTkTextbox(
            card,
            width=300,
            height=36,
            font=("Segoe UI", 11)
        )
        self.catatan_text.pack(anchor="w", padx=12, pady=(0, 4))

        # Buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(8, 6))

        self.status_label = ctk.CTkLabel(
            btn_frame,
            text="Ready",
            text_color="#9ca3af",
            font=("Segoe UI", 10)
        )
        self.status_label.pack(anchor="w")

        # lebar area tombol disamakan dengan textbox catatan
        actions = ctk.CTkFrame(btn_frame, fg_color="transparent", width=300, height=44)
        actions.pack(anchor="w", pady=(8, 2))
        actions.pack_propagate(False)

        self.submit_btn = ctk.CTkButton(
            actions,
            text="SUBMIT",
            width=170,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.accent,
            command=self.on_submit
        )
        self.submit_btn.pack(side="left", padx=(0, 10))

        preview = ctk.CTkButton(
            actions,
            text="Preview",
            width=120,
            height=40,
            corner_radius=8,
            font=("Segoe UI", 11),
            fg_color="#374151",
            command=self.preview
        )
        preview.pack(side="left")

    def preview(self):
        t = self.cal.get_date()
        catatan = self.catatan_text.get("1.0", "end").strip()

        s = (
            f"Tanggal: {t.strftime('%Y-%m-%d')}\n"
            f"Kode: {self.entry_kode.get() or '<kosong>'}\n"
            f"Target: {self.target_var.get()}\n"
            f"Metode: {self.metode_var.get()}\n"
            f"PC Kasir: {self.pc_kasir_var.get()}\n"
            f"Keyboard Kasir: {self.keyboard_kasir_var.get()}\n"
            f"Mouse Kasir: {self.mouse_kasir_var.get()}\n"
            f"Monitor Kasir: {self.monitor_kasir_var.get()}\n"
            f"Printer Thermal: {self.printer_thermal_var.get()}\n"
            f"UPS Kasir: {self.ups_var.get()}\n"
            f"Catatan: {catatan or '-'}"
        )
        messagebox.showinfo("Preview", s)

    def on_submit(self):
        kode = self.entry_kode.get().strip()
        if not kode:
            messagebox.showwarning("Validasi", "Isi Kode Toko / Nama Komputer terlebih dahulu")
            return

        self.submit_btn.configure(state="disabled", text="MENGIRIM...")
        self.status_label.configure(text="Mengirim...", text_color="#f97316")
        threading.Thread(target=self._submit_thread, daemon=True).start()

    def _submit_thread(self):
        try:
            tgl = self.cal.get_date()
            target = self.target_var.get()
            kode = self.entry_kode.get().strip()
            metode = self.metode_var.get()
            pc_kasir = self.pc_kasir_var.get()
            keyboard_kasir = self.keyboard_kasir_var.get()
            mouse_kasir = self.mouse_kasir_var.get()
            monitor_kasir = self.monitor_kasir_var.get()
            printer_thermal = self.printer_thermal_var.get()
            ups = self.ups_var.get()
            catatan = self.catatan_text.get("1.0", "end").strip()

            data = {
                "entry.283427473_day": tgl.day,
                "entry.283427473_month": tgl.month,
                "entry.283427473_year": tgl.year,
                "entry.729629067": "Andra Firmansyah",
                "entry.385266849": "SBY",
                "entry.1885250742": target,
                "entry.1590388624": kode,
                "entry.502122490": metode,
                "entry.1426045077": pc_kasir,
                "entry.792011826": keyboard_kasir,
                "entry.654245313": mouse_kasir,
                "entry.1199810138": monitor_kasir,
                "entry.1648101535": printer_thermal,
                "entry.447675297": ups,
                "entry.277276485": catatan,
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

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/viewform"
            }

            r = requests.post(FORM_URL, data=data, headers=headers, timeout=12)

            if r.status_code in (200, 302):
                self.after(0, self._on_success)
            else:
                self.after(0, lambda: self._on_error(f"HTTP {r.status_code}"))

        except requests.exceptions.Timeout:
            self.after(0, lambda: self._on_error("Timeout"))
        except requests.exceptions.ConnectionError:
            self.after(0, lambda: self._on_error("Connection error"))
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))
        finally:
            self.after(0, lambda: self.submit_btn.configure(state="normal", text="SUBMIT"))

    def _on_success(self):
        self.status_label.configure(text="Submit sukses ✅", text_color="#10b981")
        messagebox.showinfo("Sukses", "Form berhasil dikirim!")
        self.entry_kode.delete(0, "end")
        self.catatan_text.delete("1.0", "end")

    def _on_error(self, msg):
        self.status_label.configure(text="Submit gagal ❌", text_color="#ef4444")
        messagebox.showerror("Gagal", msg)


if __name__ == "__main__":
    app = ITHealthApp()
    app.mainloop()