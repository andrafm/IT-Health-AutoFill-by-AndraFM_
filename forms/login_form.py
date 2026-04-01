import customtkinter as ctk


class LoginForm(ctk.CTkFrame):
    def __init__(self, master, on_login, accent="#3b82f6", card="#111214"):
        super().__init__(master, fg_color="transparent")
        self.on_login = on_login
        self.accent = accent
        self.card = card

        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        panel = ctk.CTkFrame(wrap, fg_color=self.card, corner_radius=12)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            panel,
            text="Form Login",
            font=("Segoe UI", 18, "bold"),
            text_color="white",
        ).pack(padx=24, pady=(20, 6))

        ctk.CTkLabel(
            panel,
            text="Masukkan user terlebih dahulu",
            font=("Segoe UI", 11),
            text_color="#cbd5e1",
        ).pack(padx=24, pady=(0, 10))

        ctk.CTkLabel(panel, text="User", font=("Segoe UI", 11, "bold")).pack(
            padx=24, pady=(0, 4)
        )

        self.user_var = ctk.StringVar(value="")
        self.user_entry = ctk.CTkEntry(
            panel,
            textvariable=self.user_var,
            width=220,
            height=34,
            justify="center",
            placeholder_text="Ketik: andra / bagus / adi",
        )
        self.user_entry.pack(padx=24, pady=(0, 6))
        self.user_entry.bind("<Return>", lambda event: self._submit())

        ctk.CTkLabel(
            panel,
            text="Huruf besar/kecil bebas",
            font=("Segoe UI", 10),
            text_color="#94a3b8",
        ).pack(padx=24, pady=(0, 12))

        ctk.CTkButton(
            panel,
            text="Masuk",
            width=220,
            height=40,
            fg_color=self.accent,
            font=("Segoe UI", 11, "bold"),
            command=self._submit,
        ).pack(padx=24, pady=(0, 20))

        self.after(80, self.user_entry.focus_force)

    def _submit(self):
        key = self.user_var.get().strip().lower()
        self.on_login(key)
