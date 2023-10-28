# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

"""
Used to test API is working and pull info from sales in the spread sheet

sales = SHEET.worksheet('sales')

data = sales.get_all_values()
print(data)
"""

def get_sales_data():
    """
    This is the function:
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated by commas. 
    The loop will repeadtedly request the data, until it is valid.
    """
    
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        """
        /n gives an extra line under the example data
        """

        data_str = input("Enter your data here:")
        """print(f"The data provided is {data_str}")"""

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break 
        """ This stops the while look if data is true otherwise code keeps running"""
    
    return sales_data

"""
This calls the function to run
"""

def validate_data(values):
    """
    Inside the try, converts all string values to integers.
    Raises a ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
   
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")

    except ValueError as e:
        """
        e variable is standard python short and for error
        """
        print(f"Invalid data: {e}, please try again.\n")
        return False 
        """ if the error occurs return false"""


    return True
    """ If the try works and data valied return true"""


"""
def update_sales_worksheet(data):
    
    Update sales worksheet, add new row with the list of data provided.
    
    print("Updating sales worksheet... \n")

    
    adding data to google sheets in sales tab
    adding a row to out google sheet
    
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)

    print("Sales sheet updated successfully. \n")

def update_surplus_worksheet(data):
    
    Update surplus worksheet, add new row with the list of data provided.
    
    print("Updating surplus worksheet... \n")

    
    adding data to google sheets in surplus tab
    adding a row to out google sheet
    
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)

    print("Surplus sheet updated successfully. \n") 
"""

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    positive is waste
    negative need extra
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surples = int(stock) - sales
        surplus_data.append(surples)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting the
    last 5 entries for each sandwich and returns the data as a 
    list of lists
    """
    sales= SHEET.worksheet("sales")
   
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted into a worksheet.
    Update the relevant worksheet with the data provided
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_stock_data(data):
    """
    calculate average stock for each sandwich and add 10%
    """

    print("calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data



def main():
    """
    Run all Functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation")
main()


