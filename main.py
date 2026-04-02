import customtkinter as ctk
import requests
from pathlib import Path

from forms.login_form import LoginForm
from forms.office_form import OfficeForm
from forms.toko_form import TokoForm


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
try:
    ctk.deactivate_automatic_dpi_awareness()
except Exception:
    pass
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/formResponse"

USERS = {
    "andra": "Andra Firmansyah",
    "bagus": "Bagus Mardiyanto",
    "adi": "Adi Mbayun Sisnandar",
}


class ITHealthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IT Health AutoFill")
        self.configure(fg_color="#0f1720")
        self._apply_scaled_window(390, 680)

        self.accent = "#3b82f6"
        self.card = "#111214"

        self.current_user_key = ""
        self.current_user_name = ""
        self.icon_path = self._resolve_icon_path()

        self._apply_window_icon(self)

        self._build_login()

    def _apply_scaled_window(self, min_width, min_height):
        self.minsize(min_width, min_height)
        # Make initial size exactly follow minsize for consistent startup size.
        self.geometry(f"{min_width}x{min_height}")

    def _resolve_icon_path(self):
        base_dir = Path(__file__).resolve().parent
        candidates = [
            base_dir / "app.ico",
            base_dir / "icon.ico",
            base_dir / "assets" / "app.ico",
            base_dir / "assets" / "icon.ico",
        ]

        for icon_file in candidates:
            if icon_file.exists():
                return str(icon_file)
        return None

    def _apply_window_icon(self, window):
        if not self.icon_path:
            return

        try:
            window.iconbitmap(self.icon_path)
        except Exception:
            pass

    def _center_window_on_screen(self):
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or height <= 1:
            width = self.winfo_reqwidth()
            height = self.winfo_reqheight()

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _center_dialog_over_parent(self, dialog, width, height):
        self.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()

        if parent_w <= 1 or parent_h <= 1:
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
        else:
            x = parent_x + (parent_w // 2) - (width // 2)
            y = parent_y + (parent_h // 2) - (height // 2)

        x = max(0, x)
        y = max(0, y)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_login(self):
        self._clear_window()
        self._apply_scaled_window(400, 280)
        self.resizable(False, False)
        self._center_window_on_screen()

        form = LoginForm(
            self,
            on_login=self._handle_login,
            accent=self.accent,
            card=self.card,
        )
        form.pack(fill="both", expand=True)

    def _handle_login(self, user_key):
        full_name = USERS.get(user_key)
        if not full_name:
            self._show_warning("Login", "User tidak valid. silahkan hubungi admin.")
            return

        self.current_user_key = user_key
        self.current_user_name = full_name
        self.show_toko_form()

    def show_toko_form(self):
        self._clear_window()
        self._apply_scaled_window(350, 700)
        self.resizable(True, True)
        self._center_window_on_screen()

        form = TokoForm(
            self,
            user_name=self.current_user_name,
            send_form=self.send_form,
            show_info=self._show_info,
            show_success=self._show_success,
            show_warning=self._show_warning,
            show_error=self._show_error,
            accent=self.accent,
            card=self.card,
            on_open_office=self.show_office_form,
        )
        form.pack(fill="both", expand=True)

    def show_office_form(self):
        self._clear_window()
        self._apply_scaled_window(350, 600)
        self.resizable(True, True)
        self._center_window_on_screen()

        form = OfficeForm(
            self,
            user_name=self.current_user_name,
            send_form=self.send_form,
            show_info=self._show_info,
            show_success=self._show_success,
            show_warning=self._show_warning,
            show_error=self._show_error,
            accent=self.accent,
            card=self.card,
            on_open_toko=self.show_toko_form,
        )
        form.pack(fill="both", expand=True)

    def send_form(self, payload):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://docs.google.com/forms/d/e/1FAIpQLSfrOo8V2nhoo1MNd8UZj19e8Sa9etfYWbMNSzHRXtiYx3dn4g/viewform",
        }

        try:
            response = requests.post(FORM_URL, data=payload, headers=headers, timeout=12)
            if response.status_code in (200, 302):
                return True, "OK"
            return False, f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as exc:
            return False, str(exc)

    def _show_dialog(self, title, text, color, title_color="white", title_font_size=15, body_justify="center"):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(fg_color="#0f1720")
        self._apply_window_icon(dialog)

        box = ctk.CTkFrame(dialog, fg_color=self.card, corner_radius=12)
        box.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(
            box,
            text=title,
            font=("Segoe UI", title_font_size, "bold"),
            text_color=title_color,
        ).pack(padx=16, pady=(16, 8))

        ctk.CTkLabel(
            box,
            text=text,
            wraplength=320,
            justify=body_justify,
            font=("Segoe UI", 11),
        ).pack(padx=16, pady=(0, 16))

        ctk.CTkButton(
            box,
            text="OK",
            width=100,
            height=36,
            fg_color=color,
            command=dialog.destroy,
        ).pack(pady=(0, 16))

        dialog.update_idletasks()
        min_dialog_w = 360
        min_dialog_h = 180
        width = max(min_dialog_w, dialog.winfo_reqwidth())
        height = max(min_dialog_h, dialog.winfo_reqheight())
        self._center_dialog_over_parent(dialog, width, height)

        self.wait_window(dialog)

    def _show_info(self, title, text):
        self._show_dialog(title, text, self.accent)

    def _show_success(self, title, text):
        self._show_dialog(
            title,
            text,
            "#16a34a",
            title_color="#22c55e",
            title_font_size=20,
            body_justify="left",
        )

    def _show_warning(self, title, text):
        self._show_dialog(title, text, "#f59e0b")

    def _show_error(self, title, text):
        self._show_dialog(title, text, "#ef4444")


if __name__ == "__main__":
    app = ITHealthApp()
    app.mainloop()
