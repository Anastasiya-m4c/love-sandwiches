import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():

    """
    Get sales figures input from the user.
    """

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Validate the input data to ensure it is a list of six integers.
    Raise ValueError if the data is invalid.
    """
    try:
        [int(value) for value in values]  # Convert all values to integers
        if len(values) != 6:
            raise ValueError(
                f"Exactly six values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again\n")
        return False
    return True


# def update_sales_worksheet(data):
#     """
#     Update the sales worksheet with the provided data.
#     """
#     print("Updating sales worksheet...\n")
#     # Open the sales worksheet and append the data
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")


# def update_surplus_worksheet(surplus_data):
#     """
#     Update the surplus worksheet with the calculated surplus data.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(surplus_data)
#     print("Surplus worksheet updated successfully.\n"


def update_worksheet(data, worksheet):
    """
    Update a given worksheet with the provided data.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Calculate surplus data based on sales and stock data.
    - Positive surplus indicates excess stock.
    - Negative surplus indicates stock shortage.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collect the last 5 entries from the sales worksheet.
    Returns a list of lists containing the last 5 entries.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock data for each sandwich type.
    Returns a list of average stock data.
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = round(average * 1.1)
        new_stock_data.append(stock_num)
    return new_stock_data


def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')


print('Wellcome to Love Sandwiches Data Automation')
main()
