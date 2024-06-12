# QR Code Generation App with Python

This Python application allows users to generate QR codes with various visual styles by specifying a URL and selecting a module drawer. The generated QR code can be saved and displayed within the application.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Supported Module Drawers](#supported-module-drawers)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- User-friendly GUI for generating QR codes.
- Selection of different module drawers for customized QR code appearance.
- Ability to save the generated QR code image.

## Requirements

To run the application, you need the following:

- Python 3.x
- tkinter library
- qrcode library

You can install the required libraries via pip:

```bash
pip install tk qrcode
```

## Usage

1. Copy this script to your local machine:
#### qr_code_generator.py
```python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import qrcode

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import SquareModuleDrawer
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers import HorizontalBarsDrawer

def generate_qr_code():
    url = url_entry.get()
    selected_module = module_var.get()
    
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    
    module_drawers = {
        "SquareModuleDrawer": SquareModuleDrawer,
        "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
        "CircleModuleDrawer": CircleModuleDrawer,
        "RoundedModuleDrawer": RoundedModuleDrawer,
        "VerticalBarsDrawer": VerticalBarsDrawer,
        "HorizontalBarsDrawer": HorizontalBarsDrawer,
    }
    
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawers[selected_module]())
    img.save("QRcode.png")
    qr_code_img.config(file='./QRcode.png')

root = tk.Tk()
root.title("QR Code Generation App")
root.geometry("550x600")

# URL Entry
url_label = ttk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = ttk.Entry(root)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Module Selection
module_var = tk.StringVar(value="SquareModuleDrawer")

module_label = ttk.Label(root, text="Select Module:")
module_label.grid(row=1, column=0, padx=5, pady=5)

modules = [
    "SquareModuleDrawer",
    "GappedSquareModuleDrawer",
    "CircleModuleDrawer",
    "RoundedModuleDrawer",
    "VerticalBarsDrawer",
    "HorizontalBarsDrawer"
]

for i, module in enumerate(modules):
    module_radio = ttk.Radiobutton(root, text=module, variable=module_var, value=module)
    module_radio.grid(row=1, column=i+1, padx=5, pady=5)

# QR Code Generation Button
generate_button = ttk.Button(root, text="QR Code Generation", command=generate_qr_code)
generate_button.grid(row=2, column=0, columnspan=len(modules)+1, padx=5, pady=5)

# QR Code Image Display
qr_code_img = tk.PhotoImage(file='./QRcode.png')
qr_code_img_label = ttk.Label(root, image=qr_code_img)
qr_code_img_label.grid(row=3, column=0, columnspan=len(modules)+1, padx=5, pady=5)

root.mainloop()
```

2. Navigate to the script directory:

```bash
cd qr-code-generator
```

3. Run the application:

```bash
python qr_code_generator.py
```

## Supported Module Drawers

The application supports the following module drawers for styling QR codes:

- Square Module Drawer
- Gapped Square Module Drawer
- Circle Module Drawer
- Rounded Module Drawer
- Vertical Bars Drawer
- Horizontal Bars Drawer

![image](https://github.com/MuhammadRaheelNaseem/GUI-Based-QRCode-Generator/assets/63813881/b487823d-2bb3-4191-9c5c-d8d6eb99d132)
