import os
import sqlite3
from datetime import datetime


class ManageDB:
    def __init__(self, password_gen):
        self.password_gen = password_gen

        # Current Program Path 
        program_path = os.path.abspath(os.getcwd())
        # Data Folder Full Path
        data_path = os.path.join(program_path, "Data")

        # Create Data Folder If not Exist
        os.makedirs(data_path, exist_ok=True)

        # Path of DB File
        self.db_path = os.path.join(data_path, "DataBase.sqlite3")

        # Connection & Cursors
        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()

        # Index Page of registered users Table Format Create If not exist
        query = '''CREATE TABLE IF NOT EXISTS user_list 
                            (id         INTEGER     PRIMARY KEY     AUTOINCREMENT, 
                             user_id    TEXT,
                             f_name     TEXT,
                             l_name     TEXT, 
                             dob        TEXT,
                             salt       BLOB,
                             key        BLOB);'''
        self.cursor.execute(query)
        self.connect.commit()

        # Available Tables (except 'user_list' & 'sqlite_sequence')
        # Means Tables for Individual Users Data
        self.table_list: list = []  # List of User ID's
        self.all_table_list()  # Table Fetch & Filter Function

    # Available Tables (except 'user_list' & 'sqlite_sequence')
    # Means Tables for Individual Users Data
    # Table Fetch & Filter Function
    def all_table_list(self):

        # If Table List is not empty clear It
        if self.table_list:
            self.table_list = []

        # Query for Get Table List from Database
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        table_list = self.cursor.execute(query).fetchall()

        # Remove 'user_list' & 'sqlite_sequence' form Table List
        for table in table_list:
            if table[0] != 'user_list' and table[0] != 'sqlite_sequence':
                self.table_list.append(table[0])

    # Create New User, Insert User details in 'user_list' and
    # Create a.txt Table Named as User ID with The Structure
    def create_new_account(self, f_name, l_name, dob, user_id, m_password):

        # Create Table with User ID if Not Exist
        # Return Creation Status
        status = self.user_table_template(user_id)

        # If New Table Created Successfully
        if status == "Success":

            # Generate Salt and Key From the Master Password
            password_hash, salt = self.password_gen.user_password_hash(m_pass=m_password)

            # Query to Save User Details to Table 'user_list'
            query = f'''INSERT INTO user_list(
            user_id, f_name, l_name, dob, salt, key)
            VALUES(?, ?, ?, ?, ?, ?);'''

            # Values for the Query
            data = (user_id, f_name, l_name, dob, salt, password_hash)

            # Create query Execution
            try:
                self.cursor.execute(query, data)
                self.connect.commit()
                return "Success"
            except Exception as e:

                # If the User ID in 'user_list' but No table Named Used ID (Somehow created)
                return f"User Index Insertion Failed\n{e}"
        else:

            # If Table Named User ID Already Exist
            return status

    # Create a.txt User Table named User ID
    # If Not Exist
    def user_table_template(self, user_id):
        try:

            # Query To Create User Table Named User ID
            query = f"""CREATE TABLE {user_id}
                (id             INTEGER     PRIMARY KEY     AUTOINCREMENT,
                web_address      TEXT,
                user_id         TEXT,
                password        BLOB)"""
            self.cursor.execute(query)
            self.connect.commit()
            return "Success"
        except Exception as e:

            # If Table Creation Failed
            return f"Table Creation Failed\n{e}"

    # User Login Validation
    def login_process(self, m_username, m_password):
        password_hash = ""
        salt = ""

        # Query to Load Row Data Where 'user_id' is 'm_username'
        query = f"""SELECT * FROM user_list WHERE user_id=?"""

        # Load the Output of Query to Variable data
        # Excluding the Auto Number in Table
        data = list(self.cursor.execute(query, (m_username,)).fetchall()[0])[1:]

        # Generate Salt and Key from Master Password and Salt
        if salt == "" and password_hash == "":
            password_hash, salt = self.password_gen.user_password_hash(m_pass=m_password)

        # This is the List Contains First Name, Last Name, Date of Birth
        # Which should not be used in any Password
        reject_list = []

        # If Newly Generated Hash from Password and Salt
        # Match With The Hash From Database Means
        # The Master Password Entered is Correct
        if data[5] == password_hash:

            # Remove the Key Value From Memory To Be Safe
            # (Not Sure to preserve the Password & Salt in memory or Key)
            password_hash = ""
            data[5] = ""
            if not (password_hash or data[5]):

                # Load First Name, Last Name in 'reject_list'
                reject_list.extend(data[1:3])

                # Date of Birth Converted from String to datetime Data Type
                date = datetime.strptime(data[3], "%Y-%m-%d")

                # Load Date of Birth in datetime Data Type in 'reject_list'
                reject_list.append(datetime.date(date))

                # Reject List and Salt Return
                return reject_list, data[4]
        else:
            # Reject List and Salt Return Blank
            return reject_list, salt

    # Return the Data In Table Named Used_ID
    def db_load(self, user_id):

        # Query to Fetch All Data From The Table
        query = f"SELECT * FROM {user_id}"

        return self.cursor.execute(query).fetchall()

    # Insert Data To Table Named User ID
    def db_user_table_update(self, table_name, web_add, user_id, pass_hash):

        # Query to Insert or Replace Data
        query = f'INSERT OR REPLACE INTO {table_name}(web_address, user_id, password) VALUES (?, ?, ?)'
        data = (web_add, user_id, pass_hash)

        # Only to validate Program Error
        try:
            self.cursor.execute(query, data)
            self.connect.commit()
            return "Success"
        except Exception as e:
            return f"User Table {table_name} Data Insertion Error\n{e}"


if __name__ == "__main__":
    print("Please Open Main Program")
