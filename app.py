import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import qrcode
from PIL import ImageTk

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)


class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional QR Code & vCard Generator")
        self.root.geometry("760x720")
        self.root.resizable(False, False)

        # Store QR preview image reference
        self.qr_preview_image = None

        # Module drawer mapping
        self.module_drawers = {
            "Square": SquareModuleDrawer,
            "Gapped Square": GappedSquareModuleDrawer,
            "Circle": CircleModuleDrawer,
            "Rounded": RoundedModuleDrawer,
            "Vertical Bars": VerticalBarsDrawer,
            "Horizontal Bars": HorizontalBarsDrawer,
        }

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="QR Code & vCard Generator",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 15))

        # QR type selection
        type_frame = ttk.LabelFrame(main_frame, text="QR Type", padding=10)
        type_frame.pack(fill="x", pady=5)

        self.qr_type = tk.StringVar(value="Website")

        ttk.Radiobutton(
            type_frame,
            text="Website QR",
            variable=self.qr_type,
            value="Website",
            command=self.toggle_form
        ).grid(row=0, column=0, padx=10, sticky="w")

        ttk.Radiobutton(
            type_frame,
            text="vCard QR",
            variable=self.qr_type,
            value="vCard",
            command=self.toggle_form
        ).grid(row=0, column=1, padx=10, sticky="w")

        # Website input section
        self.website_frame = ttk.LabelFrame(main_frame, text="Website Information", padding=10)
        self.website_frame.pack(fill="x", pady=5)

        ttk.Label(self.website_frame, text="Website URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.url_entry = ttk.Entry(self.website_frame, width=65)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # vCard input section
        self.vcard_frame = ttk.LabelFrame(main_frame, text="vCard Information", padding=10)

        self.full_name_entry = self.create_labeled_entry(self.vcard_frame, "Full Name:", 0)
        self.phone_entry = self.create_labeled_entry(self.vcard_frame, "Phone:", 1)
        self.email_entry = self.create_labeled_entry(self.vcard_frame, "Email:", 2)
        self.company_entry = self.create_labeled_entry(self.vcard_frame, "Company:", 3)
        self.job_title_entry = self.create_labeled_entry(self.vcard_frame, "Job Title:", 4)
        self.website_entry = self.create_labeled_entry(self.vcard_frame, "Website:", 5)
        self.address_entry = self.create_labeled_entry(self.vcard_frame, "Address:", 6)

        # Style section
        style_frame = ttk.LabelFrame(main_frame, text="QR Style", padding=10)
        style_frame.pack(fill="x", pady=5)

        ttk.Label(style_frame, text="Module Style:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.module_var = tk.StringVar(value="Rounded")
        module_combo = ttk.Combobox(
            style_frame,
            textvariable=self.module_var,
            values=list(self.module_drawers.keys()),
            state="readonly",
            width=25
        )
        module_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(style_frame, text="File Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.filename_entry = ttk.Entry(style_frame, width=35)
        self.filename_entry.insert(0, "QR_Code")
        self.filename_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        ttk.Button(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr_code
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Save vCard Only",
            command=self.save_vcard_only
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="QR Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, pady=5)

        self.preview_label = ttk.Label(preview_frame, text="QR preview will appear here")
        self.preview_label.pack(pady=10)

        self.toggle_form()

    def create_labeled_entry(self, parent, label_text, row):
        # Create a label and entry field in one row
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=5)

        entry = ttk.Entry(parent, width=65)
        entry.grid(row=row, column=1, padx=5, pady=5)

        return entry

    def toggle_form(self):
        # Show the selected form and hide the other one
        if self.qr_type.get() == "Website":
            self.vcard_frame.pack_forget()
            self.website_frame.pack(fill="x", pady=5, after=self.root.winfo_children()[0].winfo_children()[1])
        else:
            self.website_frame.pack_forget()
            self.vcard_frame.pack(fill="x", pady=5, after=self.root.winfo_children()[0].winfo_children()[1])

    def generate_vcard_data(self):
        # Generate vCard text in standard VCF format
        full_name = self.full_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        company = self.company_entry.get().strip()
        job_title = self.job_title_entry.get().strip()
        website = self.website_entry.get().strip()
        address = self.address_entry.get().strip()

        if not full_name:
            raise ValueError("Full Name is required for vCard.")

        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{full_name}
ORG:{company}
TITLE:{job_title}
TEL;TYPE=CELL:{phone}
EMAIL:{email}
URL:{website}
ADR;TYPE=WORK:;;{address}
END:VCARD"""

        return vcard

    def get_qr_data(self):
        # Get QR data based on selected QR type
        if self.qr_type.get() == "Website":
            url = self.url_entry.get().strip()

            if not url:
                raise ValueError("Website URL is required.")

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            return url

        return self.generate_vcard_data()

    def generate_qr_code(self):
        try:
            qr_data = self.get_qr_data()

            selected_module = self.module_var.get()
            filename = self.filename_entry.get().strip()

            if not filename:
                filename = "QR_Code"

            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=f"{filename}.png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("All Files", "*.*")
                ]
            )

            if not save_path:
                return

            # Create QR object with high error correction for better scan reliability
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=3
            )

            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create styled QR image
            module_drawer_class = self.module_drawers[selected_module]

            img = qr.make_image(
                image_factory=StyledPilImage,
                module_drawer=module_drawer_class()
            )

            img.save(save_path)

            # Save vCard file automatically when vCard QR is generated
            if self.qr_type.get() == "vCard":
                vcf_path = save_path.rsplit(".", 1)[0] + ".vcf"
                with open(vcf_path, "w", encoding="utf-8") as file:
                    file.write(qr_data)

            self.show_preview(img)

            if self.qr_type.get() == "vCard":
                messagebox.showinfo(
                    "Success",
                    "QR Code and vCard file saved successfully."
                )
            else:
                messagebox.showinfo(
                    "Success",
                    "Website QR Code saved successfully."
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_vcard_only(self):
        try:
            if self.qr_type.get() != "vCard":
                messagebox.showwarning(
                    "vCard Mode Required",
                    "Please select vCard QR mode first."
                )
                return

            vcard_data = self.generate_vcard_data()

            full_name = self.full_name_entry.get().strip().replace(" ", "_")
            if not full_name:
                full_name = "Contact"

            save_path = filedialog.asksaveasfilename(
                defaultextension=".vcf",
                initialfile=f"{full_name}.vcf",
                filetypes=[
                    ("vCard File", "*.vcf"),
                    ("All Files", "*.*")
                ]
            )

            if not save_path:
                return

            with open(save_path, "w", encoding="utf-8") as file:
                file.write(vcard_data)

            messagebox.showinfo("Success", "vCard file saved successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_preview(self, img):
        # Resize image for preview without changing saved file quality
        preview_img = img.resize((260, 260))
        self.qr_preview_image = ImageTk.PhotoImage(preview_img)

        self.preview_label.config(
            image=self.qr_preview_image,
            text=""
        )

    def clear_form(self):
        # Clear all input fields
        self.url_entry.delete(0, tk.END)

        for entry in [
            self.full_name_entry,
            self.phone_entry,
            self.email_entry,
            self.company_entry,
            self.job_title_entry,
            self.website_entry,
            self.address_entry
        ]:
            entry.delete(0, tk.END)

        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, "QR_Code")

        self.preview_label.config(
            image="",
            text="QR preview will appear here"
        )

        self.qr_preview_image = None


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
