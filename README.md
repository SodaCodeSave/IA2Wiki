# IA2Wiki

[![GitHub stars](https://img.shields.io/github/stars/SodaCodeSave/IA2Wiki.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/SodaCodeSave/IA2Wiki/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/SodaCodeSave/IA2Wiki.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/SodaCodeSave/IA2Wiki/network/)
[![GitHub license](https://img.shields.io/github/license/SodaCodeSave/IA2Wiki.svg)](https://github.com/SodaCodeSave/IA2Wiki/blob/master/LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)

## 📋 Project Overview

IA2Wiki is a powerful automation tool designed for Minecraft server administrators and developers to automatically identify ItemsAdder files and generate beautiful item documentation.

## ✨ Core Features

- 🤖 **Automatic Identification**: Intelligently scans ItemsAdder configuration files
- 📝 **Automatic Generation**: One-click generation of Markdown format item documentation
- 🎨 **Beautiful Recipe Display**: Visual representation of item crafting recipes
- 📊 **Complete Item Information**: Includes item name, description, attributes, durability, etc.
- 🚀 **Easy to Use**: Intuitive user interface based on Streamlit
- 📱 **Responsive Design**: Generated documentation adapts to various devices

##  Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run main.py
```

### 3. Usage Steps

1. Enter the location of your ItemsAdder files in the text box
2. Click the "Start" button to begin scanning
3. Wait for the scan to complete and view the generated documentation
4. Find the generated Markdown files in the `wiki` directory

## 📖 Usage Guide

### Configuration File Structure

IA2Wiki supports the standard ItemsAdder configuration file structure:

```
items_adder_path/
├── contents/
│   ├── your_namespace/
│   │   ├── items/
│   │   │   └── your_item.yml
│   │   └── recipes/
│   │       └── your_recipe.yml
│   └── ...
└── ...
```

### Generated Documentation Structure

```
wiki/
├── your_namespace.md
└── static/
    ├── 1.png
    ├── 2.png
    ├── 404.png
    └── your_item.png
```

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: User interface framework
- **PyYAML**: YAML file parsing
- **Markdown**: Documentation generation format

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**If this project helps you, please give it a ⭐️!**