import pandas as pd
from pathlib import Path

def prep_bls_cpi(
    input_file='data/raw/historical-cpi-u-202508.xlsx',
    output_file='data/cpi_1913_2024.csv',
    sheet_name='Index averages',
    usecols='B,E',
    skiprows=5,
    nrows=112
):
    """
    Prepare BLS CPI-U data from raw Excel file to clean CSV.
    
    Reads the historical CPI-U data from BLS and extracts the year and
    annual average index values. The base period is 1982-84=100.
    
    Parameters
    ----------
    input_file : str
        Path to the raw BLS Excel file
    output_file : str
        Path where cleaned CSV will be saved
    sheet_name : str
        Excel sheet name to read from
    usecols : str
        Columns to read (B=Year, E=Annual average)
    skiprows : int
        Number of rows to skip at start of sheet
    nrows : int
        Number of data rows to read
    
    Returns
    -------
    pd.DataFrame
        Cleaned CPI data with columns ['year', 'annual_avg_cpi']
    
    Notes
    -----
    Data source: U.S. Bureau of Labor Statistics
    CPI-U: All items, U.S. city average (1982-84=100)
    Downloaded: https://data.bls.gov/timeseries/CUUR0000SA0?years_option=all_years
    """
    # Read the Excel file with specified parameters
    cpi = pd.read_excel(
        input_file,
        sheet_name=sheet_name,
        usecols=usecols,      # Columns B and E (Year and Annual avg.)
        skiprows=skiprows,    # Skip header rows to start at data
        nrows=nrows           # Read specified number of data rows
    )
    
    # Rename columns for clarity
    cpi.columns = ['year', 'annual_avg_cpi']
    
    # Ensure output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    cpi.to_csv(output_file, index=False)
    
    print(f"CPI data processed successfully!")
    print(f"Years covered: {cpi['year'].min()} - {cpi['year'].max()}")
    print(f"Saved to: {output_file}")
    
    return cpi


# Allow script to be run standalone
# This will execute when the script is run directly using command line with: python ./src/data/prep_bls_cpi.py
if __name__ == "__main__":
    cpi_data = prep_bls_cpi()
    print("\nFirst few rows:")
    print(cpi_data.head())
    print("\nLast few rows:")
    print(cpi_data.tail())