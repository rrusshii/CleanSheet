import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import pandas as pd
from werkzeug.utils import secure_filename
from cleaning.cleaner import (
    handle_missing_values,
    fix_column_types,
    rename_columns,
    generate_script
)

# Create a Flask app instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("exports", exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        # Generate a unique filename to avoid collisions
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join("uploads", unique_filename)
        file.save(file_path)

        # Read the CSV file
        try:
            df = pd.read_csv(file_path)
            # If we successfully read the CSV, redirect to the preview page
            return redirect(url_for('preview', filename=unique_filename))
        except Exception as e:
            flash(f'Error reading CSV file: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('File type not allowed. Please upload a CSV file.')
        return redirect(url_for('index'))


@app.route('/preview/<filename>')
def preview(filename):
    file_path = os.path.join("uploads", filename)

    try:
        df = pd.read_csv(file_path)

        # Get basic information about the dataframe
        column_types = {col: str(df[col].dtype) for col in df.columns}
        missing_values = {col: int(df[col].isna().sum()) for col in df.columns}
        total_rows = len(df)

        # Generate HTML table for preview
        preview_html = df.head().to_html(classes='table table-striped table-hover')

        return render_template(
            'preview.html',
            filename=filename,
            preview_html=preview_html,
            column_types=column_types,
            missing_values=missing_values,
            total_rows=total_rows,
            columns=df.columns.tolist()
        )
    except Exception as e:
        flash(f'Error processing CSV file: {str(e)}')
        return redirect(url_for('index'))


@app.route('/clean/<filename>', methods=['POST'])
def clean_data(filename):
    file_path = os.path.join("uploads", filename)

    try:
        df = pd.read_csv(file_path)
        original_df = df.copy()  # Keep a copy of the original data

        # Track the cleaning steps for code generation
        cleaning_steps = []

        # Handle missing values
        missing_method = request.form.get('missing_method')
        if missing_method and missing_method != 'none':
            fill_value = request.form.get('fill_value', '')
            df, step = handle_missing_values(df, missing_method, fill_value)
            if step:
                cleaning_steps.append(step)

        # Fix column types
        column_types = {}
        for col in df.columns:
            col_type = request.form.get(f'type_{col}')
            if col_type and col_type != 'original':
                column_types[col] = col_type

        if column_types:
            df, step = fix_column_types(df, column_types)
            if step:
                cleaning_steps.append(step)

        # Rename columns
        column_renames = {}
        for col in df.columns:
            new_name = request.form.get(f'rename_{col}', '').strip()
            if new_name and new_name != col:
                column_renames[col] = new_name

        if column_renames:
            df, step = rename_columns(df, column_renames)
            if step:
                cleaning_steps.append(step)

        # Save the cleaned data to a new file
        cleaned_filename = f"cleaned_{filename}"
        cleaned_file_path = os.path.join("exports", cleaned_filename)
        df.to_csv(cleaned_file_path, index=False)

        # Generate Python script
        script_content = generate_script(original_df, cleaning_steps)
        script_filename = f"script_{filename.rsplit('.', 1)[0]}.py"
        script_file_path = os.path.join("exports", script_filename)

        with open(script_file_path, 'w') as f:
            f.write(script_content)

        # Generate HTML tables for comparison
        original_html = original_df.head().to_html(classes='table table-striped table-hover')
        cleaned_html = df.head().to_html(classes='table table-striped table-hover')

        return render_template(
            'result.html',
            original_html=original_html,
            cleaned_html=cleaned_html,
            cleaned_filename=cleaned_filename,
            script_filename=script_filename,
            cleaning_steps=cleaning_steps
        )

    except Exception as e:
        flash(f'Error during data cleaning: {str(e)}')
        return redirect(url_for('preview', filename=filename))


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join("exports", filename)

    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    else:
        flash('File not found')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)