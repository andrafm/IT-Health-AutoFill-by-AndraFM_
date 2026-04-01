import threading
from datetime import date
import customtkinter as ctk
from tkcalendar import Calendar


class TokoForm(ctk.CTkFrame):
    def __init__(self, master, user_name, send_form, show_info, show_warning, show_error, accent="#3b82f6", card="#111214", on_open_office=None, show_success=None):
        super().__init__(master, fg_color="transparent")
        self.user_name = user_name
        self.send_form = send_form
        self.show_info = show_info
        self.show_success = show_success or show_info
        self.show_warning = show_warning
        self.show_error = show_error
        self.accent = accent
        self.card = card
        self.on_open_office = on_open_office
        self.device_radio_buttons = []
        self.selected_date = date.today()
        self.date_var = ctk.StringVar(value=self.selected_date.strftime("%d/%m/%Y"))
        self.calendar_popup = None

        self._build()

    def _add_status_row(self, parent, label_text, variable):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", fill="x", padx=16, pady=0)

        ctk.CTkLabel(row, text=label_text, width=145, anchor="w", font=("Segoe UI", 11)).pack(side="left")

        rb_baik = ctk.CTkRadioButton(row, text="Baik", variable=variable, value="Baik", font=("Segoe UI", 11), width=72, height=18)
        rb_baik.pack(side="left", padx=(4, 4))

        rb_rusak = ctk.CTkRadioButton(row, text="Rusak", variable=variable, value="Rusak", font=("Segoe UI", 11), width=72, height=18)
        rb_rusak.pack(side="left", padx=(0, 4))

        self.device_radio_buttons.extend([rb_baik, rb_rusak])

    def toggle_baik_semua(self):
        device_vars = [
            self.pc_var,
            self.keyboard_var,
            self.mouse_var,
            self.monitor_var,
            self.printer_var,
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
        header = ctk.CTkFrame(self, fg_color="#1d4ed8", height=64, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(header, text="FORM TOKO", font=("Segoe UI", 18, "bold"), text_color="white").pack(pady=(8, 0))
        ctk.CTkLabel(
            header,
            text="IT Health Auto Fill Form - Surabaya Branch",
            font=("Segoe UI", 10),
            text_color="#e6eefc",
        ).pack()

        if self.on_open_office:
            nav_bar = ctk.CTkFrame(self, fg_color="#172554", height=40, corner_radius=0)
            nav_bar.pack(fill="x")
            nav_bar.pack_propagate(False)


            ctk.CTkButton(
                nav_bar,
                text="  Pindah Form OFFICE  ▶",
                height=26,
                width=150,
                corner_radius=10,
                font=("Segoe UI", 10, "bold"),
                fg_color="#1e40af",
                hover_color="#2563eb",
                border_width=0,
                text_color="#ffffff",
                command=self.on_open_office,
            ).pack(side="right", padx=10, pady=4)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=6)

        card = ctk.CTkFrame(container, fg_color=self.card, corner_radius=12)
        card.pack(fill="both", expand=True, padx=2, pady=2)

        date_row = ctk.CTkFrame(card, fg_color="transparent")
        date_row.pack(fill="x", padx=12, pady=(8, 2))

        ctk.CTkLabel(date_row, text="Tanggal Maintenance", font=("Segoe UI", 11, "bold")).pack(side="left")
        ctk.CTkLabel(date_row, text=self.user_name, font=("Segoe UI", 10, "bold"), text_color="#e5e7eb").pack(side="right")

        date_picker_row = ctk.CTkFrame(card, fg_color="transparent")
        date_picker_row.pack(anchor="w", padx=12, pady=(0, 0))

        self.date_entry = ctk.CTkEntry(
            date_picker_row,
            width=200,
            height=28,
            font=("Segoe UI", 11),
            textvariable=self.date_var,
            state="readonly",
            justify="center",
        )
        self.date_entry.pack(side="left")
        self.date_entry.bind("<Button-1>", self._on_date_entry_click)

        ctk.CTkLabel(card, text="Kode Toko", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(6, 1))
        self.entry_kode = ctk.CTkEntry(card, width=200, height=28, font=("Segoe UI", 11), placeholder_text="Contoh: 3031001")
        self.entry_kode.pack(anchor="w", padx=12)

        self.target_value = "Toko Planet Ban"

        ctk.CTkLabel(card, text="Metode Maintenance", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(6, 1))
        self.metode_var = ctk.StringVar(value="Perawatan Jarak Jauh (Remote Maintenance)")
        mf = ctk.CTkFrame(card, fg_color="transparent")
        mf.pack(anchor="w", padx=12, pady=0)
        ctk.CTkRadioButton(mf, text="Remote", variable=self.metode_var, value="Perawatan Jarak Jauh (Remote Maintenance)", font=("Segoe UI", 11), height=18).pack(side="left", padx=(0, 8))
        ctk.CTkRadioButton(mf, text="Visit", variable=self.metode_var, value="Perawatan Langsung (Visit/Direct Maintenance)", font=("Segoe UI", 11), height=18).pack(side="left", padx=(0, 8))

        kondisi_row = ctk.CTkFrame(card, fg_color="transparent")
        kondisi_row.pack(fill="x", padx=14, pady=(5, 1))
        ctk.CTkLabel(kondisi_row, text="Kondisi Perangkat Toko", width=135, anchor="w", font=("Segoe UI", 11, "bold")).pack(side="left")
        ctk.CTkLabel(kondisi_row, text="", width=46).pack(side="left")

        self.all_baik_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            kondisi_row,
            text="Baik Semua",
            variable=self.all_baik_var,
            command=self.toggle_baik_semua,
            font=("Segoe UI", 11, "bold"),
            width=105,
            height=18,
        ).pack(side="left", padx=(2, 0))

        self.pc_var = ctk.StringVar(value="Baik")
        self.keyboard_var = ctk.StringVar(value="Baik")
        self.mouse_var = ctk.StringVar(value="Baik")
        self.monitor_var = ctk.StringVar(value="Baik")
        self.printer_var = ctk.StringVar(value="Baik")
        self.ups_var = ctk.StringVar(value="Baik")

        self._add_status_row(card, "PC Kasir", self.pc_var)
        self._add_status_row(card, "Keyboard Kasir", self.keyboard_var)
        self._add_status_row(card, "Mouse Kasir", self.mouse_var)
        self._add_status_row(card, "Monitor Kasir", self.monitor_var)
        self._add_status_row(card, "Printer Thermal", self.printer_var)
        self._add_status_row(card, "UPS Kasir", self.ups_var)

        ctk.CTkLabel(card, text="Catatan (bila ada)", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(6, 1))
        self.catatan_text = ctk.CTkTextbox(card, width=300, height=36, font=("Segoe UI", 11))
        self.catatan_text.pack(anchor="w", padx=12, pady=(0, 4))

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=12, pady=(8, 6))

        self.status_label = ctk.CTkLabel(btn_frame, text="Ready", text_color="#9ca3af", font=("Segoe UI", 10))
        self.status_label.pack(pady=(0, 4))

        actions = ctk.CTkFrame(btn_frame, fg_color="transparent", width=300, height=54)
        actions.pack(anchor="w", pady=(8, 2))
        actions.pack_propagate(False)

        self.submit_btn = ctk.CTkButton(
            actions,
            text="SUBMIT",
            width=170,
            height=46,
            corner_radius=8,
            font=("Segoe UI", 11, "bold"),
            fg_color=self.accent,
            command=self.on_submit,
        )
        self.submit_btn.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            actions,
            text="Preview",
            width=120,
            height=46,
            corner_radius=8,
            font=("Segoe UI", 11),
            fg_color="#374151",
            command=self.preview,
        ).pack(side="left")

    def _collect_payload(self):
        tgl = self.selected_date
        catatan = self.catatan_text.get("1.0", "end").strip()

        return {
            "entry.283427473_day": tgl.day,
            "entry.283427473_month": tgl.month,
            "entry.283427473_year": tgl.year,
            "entry.385266849": "SBY",
            "entry.1885250742": self.target_value,
            "entry.1590388624": self.entry_kode.get().strip(),
            "entry.502122490": self.metode_var.get(),
            "entry.1426045077": self.pc_var.get(),
            "entry.792011826": self.keyboard_var.get(),
            "entry.654245313": self.mouse_var.get(),
            "entry.1199810138": self.monitor_var.get(),
            "entry.1648101535": self.printer_var.get(),
            "entry.447675297": self.ups_var.get(),
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
            "fbzx": "-9125506300963112535",
        }

    def preview(self):
        text = self._build_preview_text()
        self.show_info("Preview Form Toko", text)

    def _build_preview_text(self):
        t = self.selected_date
        catatan = self.catatan_text.get("1.0", "end").strip()
        return (
            f"User: {self.user_name}\n"
            f"Tanggal: {t.strftime('%Y-%m-%d')}\n"
            f"Kode: {self.entry_kode.get() or '<kosong>'}\n"
            f"Target: {self.target_value}\n"
            f"Metode: {self.metode_var.get()}\n"
            f"PC Kasir: {self.pc_var.get()}\n"
            f"Keyboard Kasir: {self.keyboard_var.get()}\n"
            f"Mouse Kasir: {self.mouse_var.get()}\n"
            f"Monitor Kasir: {self.monitor_var.get()}\n"
            f"Printer Thermal: {self.printer_var.get()}\n"
            f"UPS Kasir: {self.ups_var.get()}\n"
            f"Catatan: {catatan or '-'}"
        )

    def _center_popup_over_parent(self, popup, width, height):
        self.update_idletasks()
        root = self.winfo_toplevel()
        root.update_idletasks()

        parent_x = root.winfo_rootx()
        parent_y = root.winfo_rooty()
        parent_w = root.winfo_width()
        parent_h = root.winfo_height()

        x = parent_x + (parent_w // 2) - (width // 2)
        y = parent_y + (parent_h // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")

    def _open_calendar_popup(self):
        if self.calendar_popup and self.calendar_popup.winfo_exists():
            self.calendar_popup.lift()
            self.calendar_popup.focus_force()
            return

        popup = ctk.CTkToplevel(self)
        self.calendar_popup = popup
        popup.title("Pilih Tanggal")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.resizable(False, False)
        popup.configure(fg_color="#f8fafc")

        def on_close():
            self.calendar_popup = None
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_close)

        box = ctk.CTkFrame(popup, fg_color="#ffffff", corner_radius=12)
        box.pack(fill="both", expand=True, padx=12, pady=12)

        cal = Calendar(
            box,
            selectmode="day",
            year=self.selected_date.year,
            month=self.selected_date.month,
            day=self.selected_date.day,
            date_pattern="dd/mm/yyyy",
            background="#ffffff",
            foreground="#111827",
            headersbackground="#e5e7eb",
            normalbackground="#ffffff",
            weekendbackground="#ffffff",
            othermonthbackground="#f3f4f6",
            bordercolor="#d1d5db",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            normalforeground="#111827",
            weekendforeground="#111827",
            othermonthforeground="#6b7280",
        )
        cal.pack(padx=10, pady=(10, 8))

        actions = ctk.CTkFrame(box, fg_color="transparent")
        actions.pack(fill="x", padx=10, pady=(0, 10))

        def apply_date():
            self.selected_date = cal.selection_get()
            self.date_var.set(self.selected_date.strftime("%d/%m/%Y"))
            on_close()

        ctk.CTkButton(
            actions,
            text="Batal",
            width=100,
            height=30,
            fg_color="#374151",
            hover_color="#4b5563",
            command=on_close,
        ).pack(side="right")

        ctk.CTkButton(
            actions,
            text="Pilih",
            width=100,
            height=30,
            fg_color=self.accent,
            hover_color="#2563eb",
            command=apply_date,
        ).pack(side="right", padx=(0, 8))

        popup.update_idletasks()
        self._center_popup_over_parent(popup, 330, 320)

    def _on_date_entry_click(self, _event):
        self._open_calendar_popup()
        return "break"

    def on_submit(self):
        kode = self.entry_kode.get().strip()
        if not kode:
            self.show_warning("Validasi", "Isi Kode Toko terlebih dahulu")
            return

        self.submit_btn.configure(state="disabled", text="MENGIRIM...")
        self.status_label.configure(text="Mengirim...", text_color="#f97316")
        threading.Thread(target=self._submit_thread, daemon=True).start()

    def _submit_thread(self):
        payload = self._collect_payload()
        payload["entry.729629067"] = self.user_name
        ok, message = self.send_form(payload)

        def done():
            self.submit_btn.configure(state="normal", text="SUBMIT")
            if ok:
                self.status_label.configure(text="Submit sukses", text_color="#10b981")
                self.show_success("✅ SUBMIT SUKSES", self._build_preview_text())
                self.entry_kode.delete(0, "end")
                self.catatan_text.delete("1.0", "end")
            else:
                self.status_label.configure(text="Submit gagal", text_color="#ef4444")
                self.show_error("Gagal", message)

        self.after(0, done)
