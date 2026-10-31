import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import qrcode

from PIL import Image, ImageDraw, ImageTk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ZeusQR(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ZEUS QR")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.configure(fg_color="#090909")

        self.qr_image = None
        self.qr_photo = None

        self.sizes = [
            "128 px",
            "256 px",
            "512 px",
            "768 px",
            "1024 px",
            "2048 px"
        ]

        self.foreground_colors = {
            "Black": "#101014",
            "White": "#FFFFFF",
            "Gold": "#D6B45A",
            "Blue": "#3478F6",
            "Red": "#C94B4B"
        }

        self.background_colors = {
            "White": "#FFFFFF",
            "Black": "#101014",
            "Transparent": None
        }

        self.error_levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H
        }

        self.build_interface()

    # ================= INTERFACE =================

    def build_interface(self):

        main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(
            main,
            fg_color="#111111",
            corner_radius=15
        )
        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        self.right_panel = ctk.CTkFrame(
            main,
            fg_color="#111111",
            corner_radius=15
        )
        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0)
        )

        self.build_generator()
        self.build_preview()

    # ================= GENERATOR =================

    def build_generator(self):

        panel = self.left_panel

        ctk.CTkLabel(
            panel,
            text="ZEUS QR",
            font=("Arial", 35, "bold"),
            text_color="#D6B45A"
        ).pack(
            anchor="w",
            padx=30,
            pady=(16, 0)
        )

        ctk.CTkLabel(
            panel,
            text="QR CODE GENERATOR",
            font=("Arial", 11),
            text_color="#777777"
        ).pack(
            anchor="w",
            padx=32,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            panel,
            text="URL ADDRESS",
            font=("Arial", 11, "bold"),
            text_color="#AAAAAA"
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 6)
        )

        url_frame = ctk.CTkFrame(
            panel,
            fg_color="#1B1B1B",
            corner_radius=8,
            height=38
        )
        url_frame.pack(
            fill="x",
            padx=30
        )
        url_frame.pack_propagate(False)

        ctk.CTkLabel(
            url_frame,
            text="https://",
            text_color="#D6B45A",
            font=("Arial", 13, "bold")
        ).pack(
            side="left",
            padx=(12, 3)
        )

        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="example.com",
            border_width=0,
            fg_color="transparent",
            text_color="#FFFFFF",
            font=("Arial", 13)
        )
        self.url_entry.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.url_entry.bind(
            "<Control-v>",
            self.handle_paste
        )
        self.url_entry.bind(
            "<Control-V>",
            self.handle_paste
        )

        # SETTINGS TITLE

        ctk.CTkLabel(
            panel,
            text="OUTPUT SETTINGS",
            font=("Arial", 13, "bold"),
            text_color="#D6B45A"
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 8)
        )

        settings = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        settings.pack(
            fill="x",
            padx=30
        )

        settings.grid_columnconfigure(0, weight=1)
        settings.grid_columnconfigure(1, weight=1)

        # SIZE

        self.add_setting(
            settings,
            "IMAGE SIZE",
            self.sizes,
            "512 px",
            0,
            0
        )

        # ERROR CORRECTION

        self.add_setting(
            settings,
            "ERROR CORRECTION",
            ["L", "M", "Q", "H"],
            "M",
            0,
            1
        )

        # QR COLOR

        self.add_setting(
            settings,
            "QR COLOR",
            list(self.foreground_colors.keys()),
            "Black",
            1,
            0
        )

        # BACKGROUND

        self.add_setting(
            settings,
            "BACKGROUND",
            list(self.background_colors.keys()),
            "White",
            1,
            1
        )

        # BORDER

        self.add_setting(
            settings,
            "BORDER",
            [str(i) for i in range(11)],
            "4",
            2,
            0
        )

        # BUTTONS

        buttons = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        buttons.pack(
            fill="x",
            padx=30,
            pady=(8, 0)
        )

        ctk.CTkButton(
            buttons,
            text="GENERATE QR",
            height=36,
            fg_color="#D6B45A",
            hover_color="#B99742",
            text_color="#090909",
            font=("Arial", 12, "bold"),
            command=self.generate_qr
        ).pack(
            fill="x",
            pady=(0, 8)
        )

        button_row = ctk.CTkFrame(
            buttons,
            fg_color="transparent"
        )
        button_row.pack(fill="x")

        button_row.grid_columnconfigure(0, weight=1)
        button_row.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            button_row,
            text="SAVE PNG",
            height=32,
            fg_color="#252525",
            hover_color="#353535",
            text_color="#FFFFFF",
            font=("Arial", 11, "bold"),
            command=self.save_qr
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ctk.CTkButton(
            button_row,
            text="CLEAR",
            height=32,
            fg_color="#252525",
            hover_color="#353535",
            text_color="#FFFFFF",
            font=("Arial", 11, "bold"),
            command=self.clear_input
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        # STATUS

        self.status_label = ctk.CTkLabel(
            panel,
            text="READY",
            font=("Arial", 10),
            text_color="#777777"
        )
        self.status_label.pack(
            side="bottom",
            anchor="w",
            padx=30,
            pady=8
        )

    # ================= SETTINGS =================

    def add_setting(
        self,
        parent,
        title,
        values,
        default,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(0, 10),
            pady=(0, 7)
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 10, "bold"),
            text_color="#777777"
        ).pack(
            anchor="w",
            pady=(0, 3)
        )

        option = ctk.CTkOptionMenu(
            frame,
            values=values,
            height=29,
            fg_color="#222222",
            button_color="#333333",
            button_hover_color="#444444",
            text_color="#FFFFFF",
            dropdown_fg_color="#191919",
            dropdown_hover_color="#333333",
            font=("Arial", 11),
            width=160
        )

        option.set(default)
        option.pack(
            anchor="w",
            fill="x"
        )

        if title == "IMAGE SIZE":
            self.size_option = option

        elif title == "ERROR CORRECTION":
            self.error_option = option

        elif title == "QR COLOR":
            self.foreground_option = option

        elif title == "BACKGROUND":
            self.background_option = option

        elif title == "BORDER":
            self.border_option = option

    # ================= PREVIEW =================

    def build_preview(self):

        panel = self.right_panel

        ctk.CTkLabel(
            panel,
            text="PREVIEW",
            font=("Arial", 18, "bold"),
            text_color="#FFFFFF"
        ).pack(
            anchor="w",
            padx=30,
            pady=(30, 5)
        )

        ctk.CTkLabel(
            panel,
            text="YOUR GENERATED QR CODE",
            font=("Arial", 10),
            text_color="#777777"
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 30)
        )

        self.preview_stage = ctk.CTkFrame(
            panel,
            fg_color="#181818",
            corner_radius=12
        )
        self.preview_stage.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        self.preview_card = tk.Frame(
            self.preview_stage,
            bg="#FFFFFF",
            width=260,
            height=260
        )
        self.preview_card.place(
            relx=0.5,
            rely=0.48,
            anchor="center"
        )

        self.preview_card.pack_propagate(False)

        self.preview_label = tk.Label(
            self.preview_card,
            text="ZEUS QR",
            bg="#FFFFFF",
            fg="#111111",
            font=("Arial", 20, "bold")
        )
        self.preview_label.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            panel,
            text="ZEUS QR  /  AQUAmmm",
            font=("Arial", 10),
            text_color="#555555"
        ).pack(pady=(0, 20))

    # ================= QR GENERATION =================

    def generate_qr(self):

        raw_url = self.url_entry.get().strip()

        if not raw_url:
            self.set_status(
                "ENTER A URL",
                "#C94B4B"
            )
            return

        url = raw_url

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        if "." not in url:
            self.set_status(
                "INVALID URL",
                "#C94B4B"
            )
            return

        try:

            size = int(
                self.size_option.get().replace(" px", "")
            )

            foreground = self.foreground_colors[
                self.foreground_option.get()
            ]

            background = self.background_colors[
                self.background_option.get()
            ]

            correction = self.error_levels[
                self.error_option.get()
            ]

            border = int(
                self.border_option.get()
            )

            if background == foreground:
                self.set_status(
                    "QR AND BACKGROUND COLORS MATCH",
                    "#C94B4B"
                )
                return

            qr = qrcode.QRCode(
                version=None,
                error_correction=correction,
                box_size=1,
                border=border
            )

            qr.add_data(url)
            qr.make(fit=True)

            matrix = qr.get_matrix()
            matrix_size = len(matrix)

            if background is None:
                bg_color = (0, 0, 0, 0)
            else:
                bg_color = background

            small_image = Image.new(
                "RGBA",
                (matrix_size, matrix_size),
                bg_color
            )

            draw = ImageDraw.Draw(small_image)

            for y, row in enumerate(matrix):
                for x, module in enumerate(row):

                    if module:
                        draw.point(
                            (x, y),
                            fill=foreground
                        )

            final_image = small_image.resize(
                (size, size),
                Image.Resampling.NEAREST
            )

            self.qr_image = final_image

            # PREVIEW

            preview = final_image.copy()

            preview.thumbnail(
                (240, 240),
                Image.Resampling.NEAREST
            )

            preview_background = Image.new(
                "RGBA",
                preview.size,
                "#FFFFFF"
            )

            preview_background.alpha_composite(preview)

            preview = preview_background.convert("RGB")

            new_photo = ImageTk.PhotoImage(
                preview,
                master=self
            )

            self.qr_photo = new_photo

            self.preview_label.configure(
                image=self.qr_photo,
                text=""
            )

            self.set_status(
                f"QR GENERATED / {size} PX",
                "#D6B45A"
            )

        except Exception as error:

            self.set_status(
                f"ERROR: {error}",
                "#C94B4B"
            )

    # ================= SAVE =================

    def save_qr(self):

        if self.qr_image is None:
            self.set_status(
                "GENERATE QR FIRST",
                "#C94B4B"
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png")
            ],
            initialfile="zeus_qr.png"
        )

        if not path:
            return

        try:

            self.qr_image.save(
                path,
                format="PNG"
            )

            self.set_status(
                "PNG SUCCESSFULLY SAVED",
                "#D6B45A"
            )

        except Exception as error:

            self.set_status(
                f"SAVE ERROR: {error}",
                "#C94B4B"
            )

    # ================= CLEAR =================

    def clear_input(self):

        self.url_entry.delete(0, "end")

        self.qr_image = None

        self.preview_label.configure(
            image="",
            text="ZEUS QR"
        )

        self.qr_photo = None

        self.set_status(
            "READY",
            "#777777"
        )

    # ================= HELPERS =================

    def handle_paste(self, event=None):

        try:
            clipboard = self.clipboard_get()

            self.url_entry.insert(
                tk.INSERT,
                clipboard
            )

        except tk.TclError:
            pass

        return "break"

    def set_status(self, message, color):

        self.status_label.configure(
            text=message,
            text_color=color
        )


# ================= MAIN =================

if __name__ == "__main__":

    app = ZeusQR()

    try:
        app.mainloop()

    except KeyboardInterrupt:
        pass

    finally:
        try:
            app.destroy()
        except tk.TclError:
            pass
