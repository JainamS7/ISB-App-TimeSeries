import camelot

def extract_tables_from_pdf(pdf_path):
    """
    Extracts tables from a PDF file using Camelot.

    Args:
        pdf_path (str): The file path of the PDF.

    Returns:
        tables (camelot.core.TableList): A list of tables extracted by Camelot.
    """
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

    if tables:
        print(f"Found {tables.n} tables in the PDF.")
    else:
        print("No tables found in the PDF.")
    
    return tables

def save_tables_as_csv(tables, base_filename='table'):
    """
    Saves each table in the Camelot TableList as a CSV file.

    Args:
        tables (camelot.core.TableList): A list of tables extracted by Camelot.
        base_filename (str): Base name for the CSV files.
    """
    for i, table in enumerate(tables):
        csv_filename = f"{base_filename}_{i+1}.csv"
        table.to_csv(csv_filename)
        print(f"Table {i+1} saved as {csv_filename}")

def display_tables(tables):
    """
    Displays the extracted tables in the console.

    Args:
        tables (camelot.core.TableList): A list of tables extracted by Camelot.
    """
    for i, table in enumerate(tables):
        print(f"\nTable {i + 1}:")
        print(table.df.to_string(index=False))

def main():
    # Specify the path to your PDF file
    pdf_path = 'test1.pdf'

    # Extract tables from the PDF
    tables = extract_tables_from_pdf(pdf_path)
    
    # Display the extracted tables
    display_tables(tables)

    # Save tables to CSV files
    save_tables_as_csv(tables, base_filename='test5_table')

# Execute the main function
if __name__ == '__main__':
    main()
