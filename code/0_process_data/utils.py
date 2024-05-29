# This file contains various functions used multiple times throughout the project. It is imported in other scripts to avoid code duplication.
import os
import inspect

def make_output_path(file_name):
    """
    Create the output path to save a file in the output folder, orgaized in the same way as the code folder.
    """

    # get the name of the current file
    current_script_path = inspect.stack()[1].filename
    print(current_script_path)

    # remove the extension
    current_script_path = os.path.splitext(current_script_path)[0]
    print(current_script_path)

    # edit the current script path to replace the folder "code" the folder "output"
    output_path = current_script_path.replace("code", "output")
    print(output_path)

    # create the output folder if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # create the output path
    output_path = os.path.join(output_path, file_name)

    return output_path


def create_lagged_column(df, value_col, lag, new_col_name=None):
    """
    Create a lagged column for a given variable in the DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    value_col (str): The name of the column containing the values to be lagged.
    lag (int): The number of years to lag.
    new_col_name (str): The name of the new lagged column. If None, defaults to 'value_col_lagX'.
    
    Returns:
    pd.DataFrame: The DataFrame with the new lagged column.
    """
    df = df.copy()
    if new_col_name is None:
        new_col_name = f'{value_col}_lag{lag}'
    
    df[new_col_name] = None  # Initialize the new column with None
    for idx, row in df.iterrows():
        country = row['Country']
        year = row['Year']
        lagged_year = year - lag
        lagged_value = df[(df['Country'] == country) & (df['Year'] == lagged_year)][value_col]
        if not lagged_value.empty:
            df.at[idx, new_col_name] = lagged_value.values[0]
    return df