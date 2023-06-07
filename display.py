from rich.console import Console
from rich.table import Table
import pandas as pd

def display_df(df):
    # Create a console object
    console = Console()

    # Transpose the DataFrame
    df_transposed = df.T

    # Create a table
    table = Table(show_header=True, header_style="bold magenta")

    # Add the index as the first column
    table.add_column("Metrics")

    # Add columns (from DataFrame's columns)
    for month in df_transposed.columns:
        table.add_column(str(month))

    # Add rows (from DataFrame's rows and data)
    for metric, row in df_transposed.iterrows():
        table.add_row(metric, *[str(x) for x in row.values])

    # Print the table
    console.print(table)
