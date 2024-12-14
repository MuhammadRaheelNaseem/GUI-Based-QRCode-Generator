
## 📦 Project Overview

*Project Name:* QR Code Generation App

*Description:* A Python-based GUI application using Tkinter that allows users to generate and save customized QR codes with various module styles.

---

## 🚀 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [Sample Files](#sample-files)
   - [1. main.py](#1-mainpy)
   - [2. requirements.txt](#2-requirementstxt)
   - [3. README.md](#3-readmemd)
   - [4. .gitignore](#4-gitignore)
5. [Pushing to GitHub](#pushing-to-github)
6. [Additional Tips](#additional-tips)

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your system:

1. *Git:* Version control system.
   - *Download:* [Git Downloads](https://git-scm.com/downloads)

2. *Python:* Programming language.
   - *Download:* [Python Downloads](https://www.python.org/downloads/)

3. *Pip:* Python package installer (usually comes with Python).

4. *GitHub Account:* If you don't have one, sign up at [GitHub](https://github.com/).

---

## 📁 Project Structure

Organizing your project files systematically makes it easier to manage and collaborate. Here's a recommended structure for your QR Code Generation App:


QR-Code-Generator-App/
│
├── src/
│   └── main.py
│
├── assets/
│   └── placeholder.png  # Optional: Placeholder image before QR code generation
│
├── .gitignore
├── README.md
└── requirements.txt


- *src/*: Contains all source code files.
- *assets/*: Stores assets like images, icons, etc.
- *.gitignore*: Specifies intentionally untracked files to ignore.
- *README.md*: Provides an overview and instructions for the project.
- *requirements.txt*: Lists all Python dependencies.

---

## 📝 Step-by-Step Guide

### 1. *Create the Project Directory*

Open your terminal or command prompt and execute the following commands:

bash
# Navigate to your desired directory
cd path/to/your/projects/directory

# Create the project directory
mkdir QR-Code-Generator-App

# Navigate into the project directory
cd QR-Code-Generator-App


### 2. *Initialize Git Repository*

Initialize a new Git repository to track your project:

bash
git init


### 3. *Create Necessary Folders and Files*

Create the src and assets directories, and add the main Python script:

bash
# Create directories
mkdir src
mkdir assets

# Navigate into src directory
cd src

# Create the main Python script
touch main.py

# Navigate back to the project root
cd ..


### 4. *Create requirements.txt*

List all your project dependencies in requirements.txt:

bash
# Create requirements.txt
touch requirements.txt


### 5. *Create .gitignore*

Specify files and directories to ignore in your Git repository:

bash
# Create .gitignore
touch .gitignore


### 6. *Create README.md*

Provide an overview and instructions in README.md:

bash
# Create README.md
touch README.md


---

## 📄 Sample Files

Below are sample contents for each of the essential files. You can customize them as needed.

### 1. src/main.py

Here's the updated Python script incorporating the "Save QR Code" functionality:

python
# src/main.py
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk  # Import PIL for better image handling

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    CircleModuleDrawer,
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer,
)

def generate_qr_code():
    url = url_entry.get()
    selected_module = module_var.get()

    if not url:
        messagebox.showerror("Input Error", "Please enter a URL.")
        return

    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    module_drawers = {
        "SquareModuleDrawer": SquareModuleDrawer,
        "GappedSquareModuleDrawer": GappedSquareModuleDrawer,
        "CircleModuleDrawer": CircleModuleDrawer,
        "RoundedModuleDrawer": RoundedModuleDrawer,
        "VerticalBarsDrawer": VerticalBarsDrawer,
        "HorizontalBarsDrawer": HorizontalBarsDrawer,
    }

    try:
        img = qr.make_image(
            image_factory=StyledPilImage, 
            module_drawer=module_drawers[selected_module]()
        )
        img.save("QRcode.png")

        # Load the image using PIL and update the label
        pil_image = Image.open("QRcode.png")
        
        # Check if Image.Resampling exists (Pillow >=10.0.0)
        if hasattr(Image, 'Resampling'):
            resample_method = Image.Resampling.LANCZOS
        else:
            resample_method = Image.LANCZOS  # For older Pillow versions

        pil_image = pil_image.resize((300, 300), resample=resample_method)  # Resize if needed
        qr_image = ImageTk.PhotoImage(pil_image)

        qr_code_img_label.config(image=qr_image)
        qr_code_img_label.image = qr_image  # Keep a reference

        # Enable the Save button since a QR code is now generated
        save_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR Code: {e}")

def save_qr_code():
    # Check if QR code image exists
    try:
        pil_image = Image.open("QRcode.png")
    except FileNotFoundError:
        messagebox.showerror("Save Error", "No QR code to save. Please generate one first.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Error opening QR code image: {e}")
        return

    # Open a file dialog to choose save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Save QR Code As"
    )

    if not file_path:
        # User cancelled the save dialog
        return

    try:
        pil_image.save(file_path)
        messagebox.showinfo("Success", f"QR Code saved successfully at:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save QR Code: {e}")

# Initialize the main window
root = tk.Tk()
root.title("QR Code Generation App")
root.geometry("600x800")  # Adjusted size for better layout

# URL Entry
url_label = ttk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Module Selection
module_var = tk.StringVar(value="SquareModuleDrawer")

module_label = ttk.Label(root, text="Select Module:")
module_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

modules = [
    "SquareModuleDrawer",
    "GappedSquareModuleDrawer",
    "CircleModuleDrawer",
    "RoundedModuleDrawer",
    "VerticalBarsDrawer",
    "HorizontalBarsDrawer"
]

# Use a frame to organize radio buttons
module_frame = ttk.Frame(root)
module_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

for i, module in enumerate(modules):
    module_radio = ttk.Radiobutton(
        module_frame, text=module, variable=module_var, value=module
    )
    module_radio.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="w")

# QR Code Generation Button
generate_button = ttk.Button(root, text="Generate QR Code", command=generate_qr_code)
generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

# QR Code Image Display
qr_code_img_label = ttk.Label(root)
qr_code_img_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Save QR Code Button
save_button = ttk.Button(root, text="Save QR Code", command=save_qr_code, state=tk.DISABLED)
save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

root.mainloop()

```


*Notes:*

- *File Paths:* The QR code image is saved as QRcode.png in the current working directory. Ensure that this path is accessible.
- *Dependencies:* Make sure all required libraries (tkinter, qrcode, Pillow) are listed in requirements.txt.

---

### 2. requirements.txt

List all the Python libraries your project depends on. This allows others to install them easily.

txt
qrcode
Pillow


*Optional:* If you're using specific versions, you can specify them like so:

txt
qrcode==7.3
Pillow>=10.0.0


*Note:* To generate requirements.txt automatically based on your current environment, you can use:

bash
pip freeze > requirements.txt


However, this may include more packages than necessary. It's often better to manually specify only the required dependencies.

---

### 3. README.md

A well-documented README.md helps others understand what your project does, how to set it up, and how to use it.

markdown
# QR Code Generation App

A Python-based GUI application that allows users to generate and save customized QR codes with various module styles.

## 🛠️ Features

- **Generate QR Codes:** Input a URL and generate a QR code.
- **Customize Module Styles:** Choose from multiple module styles like Square, Circle, Rounded, etc.
- **Save QR Codes:** Save the generated QR code to your desired directory.

## 🎨 Module Styles

- SquareModuleDrawer
- GappedSquareModuleDrawer
- CircleModuleDrawer
- RoundedModuleDrawer
- VerticalBarsDrawer
- HorizontalBarsDrawer

## 📸 Screenshots

*(Optional: Include screenshots of your application here)*

## 💻 Installation

### 1. **Clone the Repository**

bash
git clone https://github.com/yourusername/QR-Code-Generator-App.git


### 2. **Navigate to the Project Directory**

bash
cd QR-Code-Generator-App


### 3. **Create a Virtual Environment (Optional but Recommended)**

bash
python -m venv venv


Activate the virtual environment:

- **Windows:**
  bash
  venv\Scripts\activate
  
- **macOS/Linux:**
  bash
  source venv/bin/activate
  

### 4. **Install Dependencies**

bash
pip install -r requirements.txt


## 🏃‍♂️ Usage

Navigate to the `src` directory and run the application:

bash
cd src
python main.py


**Steps:**

1. **Enter URL:** Input the URL you want to convert into a QR code.
2. **Select Module Style:** Choose your preferred QR code module style.
3. **Generate QR Code:** Click the "Generate QR Code" button.
4. **Save QR Code:** After generation, click the "Save QR Code" button to save the image to your desired location.

## 📝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## 📄 License

*(Specify your project's license here. For example:)*

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgements

- [qrcode](https://pypi.org/project/qrcode/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)


*Notes:*

- *Replace yourusername* with your actual GitHub username in the clone URL.
- *Screenshots:* Adding screenshots enhances the README's visual appeal and helps users understand the application better.
- *License:* It's good practice to include a license. [Choose a License](https://choosealicense.com/) to find one that fits your needs.

---

### 4. .gitignore

This file tells Git which files or directories to ignore in the repository. Here's a sample .gitignore for Python projects:

gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
ENV/
env/
env.bak/
venv.bak/

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# VS Code
.vscode/

# MacOS
.DS_Store

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# QR Code Images
QRcode.png


*Notes:*

- *Virtual Environments:* The venv/ directory is ignored to prevent committing virtual environment files.
- *Generated Images:* If you prefer not to commit generated QR code images, include QRcode.png in .gitignore.
- *IDE Specific Files:* .vscode/ is ignored for VS Code settings. Modify based on your IDE.

---

## 📤 Pushing to GitHub

### 1. *Create a New Repository on GitHub*

1. Log in to your [GitHub](https://github.com/) account.
2. Click on the *+* icon in the top-right corner and select *New repository*.
3. *Repository Name:* QR-Code-Generator-App
4. *Description:* (Optional) A brief description of your project.
5. *Privacy:* Choose between *Public* or *Private*.
6. *Initialize Repository:* *Do not* check any boxes since you already have local files.
7. Click *Create repository*.

### 2. *Connect Local Repository to GitHub*

Back in your terminal, ensure you're in the project root directory (QR-Code-Generator-App/):

bash
# Add the remote repository
git remote add origin https://github.com/yourusername/QR-Code-Generator-App.git

# Verify the remote URL
git remote -v


*Replace yourusername* with your actual GitHub username.

### 3. *Stage and Commit Your Files*

bash
# Stage all files
git add .

# Commit with a message
git commit -m "Initial commit - QR Code Generation App"


### 4. *Push to GitHub*

bash
# Push the commits to GitHub
git push -u origin master


*Note:* If you receive an error about the master branch not existing, you might need to push to main instead:

bash
git push -u origin main


Alternatively, you can rename your local master branch to main:

bash
git branch -M main
git push -u origin main


---

## 💡 Additional Tips

### 1. *Using Virtual Environments*

It's good practice to use virtual environments to manage your project's dependencies. This ensures that your project remains isolated and doesn't interfere with other Python projects on your system.

*Creating a Virtual Environment:*

bash
# Create a virtual environment named 'venv'
python -m venv venv


*Activating the Virtual Environment:*

- *Windows:*
  bash
  venv\Scripts\activate
  
- *macOS/Linux:*
  bash
  source venv/bin/activate
  

*Deactivating the Virtual Environment:*

bash
deactivate


### 2. *Updating Dependencies*

When you add new dependencies, update requirements.txt:

bash
pip install package_name
pip freeze > requirements.txt


### 3. *Branching and Pull Requests*

For new features or bug fixes, create separate branches:

bash
# Create a new branch
git checkout -b feature/new-feature-name

# After making changes
git add .
git commit -m "Add new feature"

# Push the branch to GitHub
git push origin feature/new-feature-name

# Create a Pull Request on GitHub


### 4. *Adding a License*

Including a license clarifies how others can use your project. To add an MIT License:

1. Create a LICENSE file in the project root.
2. Copy the [MIT License text](https://choosealicense.com/licenses/mit/) into the LICENSE file.
3. Replace [year] and [fullname] with the appropriate values.

### 5. *Continuous Integration (CI)*

Consider setting up CI tools like GitHub Actions to automate testing, linting, or deployment.

---

## 🎉 Congratulations!

You've successfully organized your QR Code Generation App as a GitHub repository! Here's a summary of what you've achieved:

- *Structured Project Files:* Organized code, assets, and documentation systematically.
- *Version Control:* Initialized Git and committed your project.
- *GitHub Integration:* Pushed your local repository to GitHub for collaboration and sharing.
- *Documentation:* Created a comprehensive README.md to guide users and contributors.
- *Dependency Management:* Listed required Python packages in requirements.txt.
- *Best Practices:* Implemented .gitignore to exclude unnecessary files.

---

## 📚 Next Steps

1. *Enhance Functionality:*
   - Add more customization options for QR codes.
   - Implement error handling for invalid URLs.
   - Allow users to choose the size and colors of the QR code.

2. *Improve UI/UX:*
   - Add icons or better styling to the GUI.
   - Provide real-time previews of the QR code.

3. *Testing:*
   - Write unit tests to ensure the reliability of your application.

4. *Deployment:*
   - Package your application using tools like PyInstaller to create executable files.

5. *Collaborate:*
   - Share your repository with others.
   - Encourage contributions and feedback.
