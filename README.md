# CleanSheet - CSV Data Cleaning Tool

A simple web application that helps you clean and prepare CSV data files with an intuitive interface.

## Features

- Upload and preview CSV files
- Handle missing values (drop rows or fill with values/statistics)
- Convert column data types (int, float, string, datetime, category)
- Rename columns for better clarity
- Export cleaned data as CSV
- Generate reproducible Python cleaning scripts

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/cleansheet.git
cd cleansheet

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask pandas numpy

# Run the application
python app.py
```

Then open http://127.0.0.1:5000/ in your browser.

## Usage

1. **Upload** - Select and upload your CSV file
2. **Preview & Configure** - View your data and select cleaning operations:
   - Choose how to handle missing values
   - Select column type conversions
   - Rename columns as needed
3. **Clean & Export** - Apply changes and download:
   - Cleaned CSV file
   - Python script with all applied operations

## Development Process

1. **Requirements Analysis** - Identified common data cleaning needs
2. **Application Design** - Flask backend with Bootstrap frontend
3. **Core Functionality** - Implemented data cleaning operations using Pandas
4. **User Interface** - Created intuitive workflow with multiple steps
5. **Testing & Refinement** - Improved error handling and edge cases

## Project Structure

```
cleansheet/
├── app.py                # Main Flask application
├── cleaning/cleaner.py   # Data cleaning functions
├── static/               # CSS, JavaScript, and images
├── templates/            # HTML templates
├── uploads/              # Temporary storage for uploaded files
└── exports/              # Storage for cleaned files and scripts
```

## Technologies

Python, Flask, Pandas, NumPy, jinja2, HTML/CSS/JavaScript