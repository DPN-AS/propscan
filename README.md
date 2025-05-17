# Property Scan Application

This repository contains a simple CLI and GUI application for ordering property listings by geographic proximity and generating Google Maps routing links.

## Requirements

- Python 3.9+
- PyQt6 (for the GUI)

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

## Command Line Usage

```
python main.py <properties.csv>
```

The CSV file must include `ADDRESS`, `LATITUDE`, and `LONGITUDE` columns (case-insensitive). The script prints the ordered addresses with Google Maps links.

## GUI Usage

```
python gui.py
```

A window will open allowing you to select a CSV file and view the ordered list of addresses.

