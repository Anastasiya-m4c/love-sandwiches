import gspread
from google.oauth2.service_account import Credentials

SCOPE = [n
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
        else:
            print("Invalid data, please try again.\n")

    return sales_data

def validate_data(values):
    """
    Validate the input data to ensure it is a list of six integers.
    Raise ValueError if the data is invalid.
    """
    try:
        [int(value) for value in values
            ]  # Convert all values to integers
        
        if len(values) != 6:
            raise ValueError(
                f"Exactly six values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again\n")

    return True

get_sales_data()