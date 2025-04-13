import pandas as pd
import numpy as np


def handle_missing_values(df, method, fill_value=None):
    """
    Handle missing values in the dataframe.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe
    method : str
        The method to handle missing values ('drop', 'fill_value', 'fill_mean', 'fill_median')
    fill_value : str, optional
        The value to fill missing values with when method is 'fill_value'

    Returns:
    --------
    pandas.DataFrame
        The dataframe with missing values handled
    str
        The python code snippet representing this operation
    """
    df_result = df.copy()

    if method == 'drop':
        # Drop rows with any missing values
        df_result = df_result.dropna()
        step = "df = df.dropna()\n"

    elif method == 'fill_value':
        # Fill missing values with a specified value
        try:
            # Try to convert fill_value to numeric if possible
            numeric_fill = pd.to_numeric(fill_value)
            df_result = df_result.fillna(numeric_fill)
            step = f"df = df.fillna({numeric_fill})\n"
        except (ValueError, TypeError):
            # Otherwise use it as a string
            df_result = df_result.fillna(str(fill_value))
            step = f"df = df.fillna('{fill_value}')\n"

    elif method == 'fill_mean':
        # Fill missing values with column mean (for numeric columns only)
        numeric_cols = df_result.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            df_result[col] = df_result[col].fillna(df_result[col].mean())

        step = "# Fill missing values with mean (numeric columns only)\n"
        step += "numeric_cols = df.select_dtypes(include=np.number).columns\n"
        step += "for col in numeric_cols:\n"
        step += "    df[col] = df[col].fillna(df[col].mean())\n"

    elif method == 'fill_median':
        # Fill missing values with column median (for numeric columns only)
        numeric_cols = df_result.select_dtypes(include=np.number).columns
        for col in numeric_cols:
            df_result[col] = df_result[col].fillna(df_result[col].median())

        step = "# Fill missing values with median (numeric columns only)\n"
        step += "numeric_cols = df.select_dtypes(include=np.number).columns\n"
        step += "for col in numeric_cols:\n"
        step += "    df[col] = df[col].fillna(df[col].median())\n"

    else:
        # If no valid method is specified, just return the original dataframe
        step = ""

    return df_result, step


def fix_column_types(df, column_types):
    """
    Convert columns to specified types.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe
    column_types : dict
        Dictionary mapping column names to desired types

    Returns:
    --------
    pandas.DataFrame
        The dataframe with column types fixed
    str
        The python code snippet representing this operation
    """
    df_result = df.copy()
    step = "# Convert column types\n"

    for col, dtype in column_types.items():
        if col not in df.columns:
            continue

        try:
            if dtype == 'int':
                # Handle missing values before converting to int
                df_result[col] = df_result[col].fillna(0).astype('int64')
                step += f"df['{col}'] = df['{col}'].fillna(0).astype('int64')\n"

            elif dtype == 'float':
                df_result[col] = df_result[col].astype('float64')
                step += f"df['{col}'] = df['{col}'].astype('float64')\n"

            elif dtype == 'string' or dtype == 'str':
                df_result[col] = df_result[col].astype('string')
                step += f"df['{col}'] = df['{col}'].astype('string')\n"

            elif dtype == 'datetime':
                df_result[col] = pd.to_datetime(df_result[col])
                step += f"df['{col}'] = pd.to_datetime(df['{col}'])\n"

            elif dtype == 'category':
                df_result[col] = df_result[col].astype('category')
                step += f"df['{col}'] = df['{col}'].astype('category')\n"

        except (ValueError, TypeError) as e:
            # If conversion fails, keep the original type and log the issue
            step += f"# Conversion of '{col}' to {dtype} failed: {str(e)}\n"

    return df_result, step


def rename_columns(df, column_map):
    """
    Rename columns in the dataframe.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe
    column_map : dict
        Dictionary mapping old column names to new column names

    Returns:
    --------
    pandas.DataFrame
        The dataframe with renamed columns
    str
        The python code snippet representing this operation
    """
    df_result = df.copy()

    if column_map:
        df_result = df_result.rename(columns=column_map)

        # Create Python code for renaming columns
        columns_dict_str = "{"
        for old_name, new_name in column_map.items():
            columns_dict_str += f"'{old_name}': '{new_name}', "
        columns_dict_str = columns_dict_str.rstrip(", ") + "}"

        step = f"# Rename columns\ndf = df.rename(columns={columns_dict_str})\n"
    else:
        step = ""

    return df_result, step


def generate_script(original_df, cleaning_steps):
    """
    Generate a Python script with the cleaning steps.

    Parameters:
    -----------
    original_df : pandas.DataFrame
        The original dataframe (for metadata)
    cleaning_steps : list
        List of Python code snippets for each cleaning step

    Returns:
    --------
    str
        The complete Python script
    """
    script = "import pandas as pd\nimport numpy as np\n\n"
    script += "# CleanSheet: Automatically generated data cleaning script\n\n"

    script += "# Load the original CSV file\n"
    script += "df = pd.read_csv('your_file.csv')  # Replace with your file path\n\n"

    script += "# Original DataFrame info\n"
    script += "# Number of rows: {}\n".format(len(original_df))
    script += "# Number of columns: {}\n".format(len(original_df.columns))
    script += "# Columns: {}\n\n".format(list(original_df.columns))

    script += "# Print the first few rows of the original data\n"
    script += "print('Original data:')\n"
    script += "print(df.head())\n\n"

    script += "# Cleaning steps\n"
    for step in cleaning_steps:
        script += step + "\n"

    script += "# Print the first few rows of the cleaned data\n"
    script += "print('\\nCleaned data:')\n"
    script += "print(df.head())\n\n"

    script += "# Save the cleaned data to a new CSV file\n"
    script += "df.to_csv('cleaned_data.csv', index=False)  # Replace with your desired output path\n"
    script += "print('\\nCleaned data saved to cleaned_data.csv')\n"

    return script