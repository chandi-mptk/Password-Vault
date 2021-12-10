from datetime import datetime
from tkinter import Tk, Menu, StringVar, IntVar, Frame, Label, RAISED, BOTH, Entry, Button, Toplevel, Scrollbar, \
    VERTICAL, RIGHT, HORIZONTAL, BOTTOM
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry


class Window:
    # Window Initialisation
    root = Tk()
    root.title("Random Password Tool")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")
    root.state('zoomed')
    # root.resizable(False, False) # Enabled Task Bar will not Show

    # Menu Bar Initialize
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # User Must Be Age or above
    min_age = 18

    def __init__(self, db_mgr, password_gen, state):

        # Tkinter Variables
        self.m_password_var = StringVar()
        self.m_user_name_var = StringVar()
        self.first_name_var = StringVar()
        self.last_name_var = StringVar()
        self.web_address_var = StringVar()
        self.user_name_var = StringVar()
        self.other_var = StringVar()
        self.password_length_var = IntVar(value=8)
        self.special_character_var = StringVar()
        self.password_var = StringVar()

        # Other Variables
        self.date_of_birth_var = ""
        self.salt = ""

        self.password_data_all = []

        self.password_view_Toplevel = None
        self.pass_list_Treeview = None
        self.open_Toplevel = None

        # Disable Clos Button Call Back Function
        self.root.protocol("WM_DELETE_WINDOW", self.__callback)

        # File Menu Creation
        self.db_mgr = db_mgr
        self.password_gen = password_gen
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Create User", underline=0, state='normal', command=self.create_user)
        self.file_menu.add_command(label="Open User", underline=0, state=state, command=self.open_user)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, state='normal', command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu, underline=0)

        # Frame Creation
        self.title_Frame = Frame(self.root)
        self.title_Frame.place(x=0, y=0, width=self.width, height=50)
        self.entry_Frame = Frame(self.root)
        self.entry_Frame.place(x=0, y=50, width=self.width // 3, height=self.height)
        self.tree_Frame = Frame(self.root)
        self.tree_Frame.place(x=self.width // 3, y=50, width=self.width * 2 // 3, height=self.height)

        # Sub Frame of Title Frame
        self.entry_title_Frame = Frame(self.entry_Frame)
        self.entry_title_Frame.place(x=0, y=0, width=self.width // 3, height=50)

        # Sub Frame of Data Entry Frame
        self.data_entry_Frame = Frame(self.entry_Frame)
        self.data_entry_Frame.place(x=0, y=50, width=self.width // 3, height=400)

        # Tree Frame Title
        self.tree_title_Frame = Frame(self.tree_Frame)
        self.tree_title_Frame.place(x=0, y=0, width=self.width * 2 // 3, height=50)

        # Tree View Frame
        self.tree_view_Frame = Frame(self.tree_Frame)
        self.tree_view_Frame.place(x=0, y=50, width=self.width * 2 // 3, height=self.height - 150)

        # Title Creation
        self.title_Label = Label(self.title_Frame, height=5, relief=RAISED, text="Generate Password",
                                 font=("Arial", 20))
        self.title_Label.pack(fill=BOTH)

        # Entry Title
        self.entry_title_Label = Label(self.entry_title_Frame, height=5, relief=RAISED, text="", font=("Arial", 15))
        self.entry_title_Label.pack(fill=BOTH)

        # Tree Title
        self.tree_title_Label = Label(self.tree_title_Frame, height=5, relief=RAISED, text="", font=("Arial", 15))
        self.tree_title_Label.pack(fill=BOTH)

    # Menu > Create User
    # The window and Process of Creating New User
    def create_user(self):

        # Validate Create User Data
        def validate_signup():

            # Get Data From Calendar Widget
            self.date_of_birth_var = date_of_birth_DateEntry.get_date()

            # Validation Method in Password Generator called
            validation_state = self.password_gen.validate_master_data(f_name=self.first_name_var.get(),
                                                                      l_name=self.last_name_var.get(),
                                                                      dob=self.date_of_birth_var,
                                                                      m_user_id=self.m_user_name_var.get(),
                                                                      m_password=self.m_password_var.get(),
                                                                      min_age=self.min_age)
            # Based On 'validation_state' Error Message
            if validation_state == 1:
                messagebox.showerror("Error", "All Columns Must be Filled")
            elif validation_state == 2:
                messagebox.showerror("Error", "First Name and User ID Must be \n\
Minimum of 4 letters and Maximum of 16 Letters Long")
            elif validation_state == 3:
                messagebox.showerror("Error", "Password Must be at least 8 Character Long")
            elif validation_state == 4:
                messagebox.showerror("Not a Good Password",
                                     "Your Password is not Strong\nUse at least One Lower case Letter")
            elif validation_state == 5:
                messagebox.showerror("Not a Good Password",
                                     "Your Password is not Strong\nUse at least One Upper case Letter")
            elif validation_state == 6:
                messagebox.showerror("Not a Good Password",
                                     "Your Password is not Strong\nUse at least One Number ")
            elif validation_state == 7:
                messagebox.showerror("Not a Good Password",
                                     "Your Password is not Strong\nUse at least One of the Special Char \n!@#$%^&*()?")
            elif validation_state == 8:
                messagebox.showerror("Not a Good Password",
                                     "Blank Space in Password\nDo Not Use Space In Password")
            elif validation_state == 9:
                messagebox.showerror("Wrong Date Of Birth",
                                     f"Please Enter A valid Date of Birth \nUser Must Be {self.min_age} Years Old")
            elif validation_state == 10:
                messagebox.showerror("Unsupported Charterer", "For user id only Use Letters and '_'")

            # Validation Success
            elif validation_state == 0:

                # Create Master Password Hash
                # Create Account by Saving Data To User List Table and
                # Create Table Named User ID
                status = self.db_mgr.create_new_account(f_name=self.first_name_var.get(),
                                                        l_name=self.last_name_var.get(),
                                                        dob=self.date_of_birth_var,
                                                        user_id=self.m_user_name_var.get(),
                                                        m_password=self.m_password_var.get()
                                                        )
                if status == "Success":
                    messagebox.showinfo("Success", """New User Created Successful\n\
Go to File > Open User to login\n\
Please Notedown The Username & Password\n\
Password Recovery Option is Not Available in this Software\n""")
                    self.destroy_create_user()
                else:
                    messagebox.showerror("Duplicate Error", f"{status}")

        # Menu Bar Disable For Preventing Parallel Work
        self.menu_bar.entryconfig("File", state="disabled")

        # Heading Label Show Name
        self.entry_title_Label.config(text="Create Account")

        # Data Entry Field Creation
        first_name_Label = Label(self.data_entry_Frame, text="First Name: ")
        first_name_Entry = Entry(self.data_entry_Frame, textvariable=self.first_name_var)
        first_name_Entry.focus()
        last_name_Label = Label(self.data_entry_Frame, text="Last Name: ")
        last_name_Entry = Entry(self.data_entry_Frame, textvariable=self.last_name_var)
        date_of_birth_Label = Label(self.data_entry_Frame, text="Date of Birth: ")

        # Date Entry Field Required Data Prepare
        year = datetime.today().year - self.min_age

        # Check Year Selection Possible to set as Drop Down Menu
        date_of_birth_DateEntry = DateEntry(self.data_entry_Frame, firstweekday='sunday',
                                            date_pattern='dd-mm-yyyy', year=year)
        user_name_Label = Label(self.data_entry_Frame, text="User ID: ")
        user_name_Entry = Entry(self.data_entry_Frame, textvariable=self.m_user_name_var)
        password_Label = Label(self.data_entry_Frame, text="Password: ")
        password_Entry = Entry(self.data_entry_Frame, show="*", textvariable=self.m_password_var)

        ok_Button = Button(self.data_entry_Frame, text='OK', width=5, command=validate_signup)
        cancel_Button = Button(self.data_entry_Frame, text="Cancel", width=5, command=self.destroy_create_user)

        self.data_entry_Frame.grid_columnconfigure(0, minsize=50)
        self.data_entry_Frame.grid_columnconfigure(2, minsize=50)

        first_name_Label.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        first_name_Entry.grid(row=1, column=3, columnspan=2, padx=10, pady=10, sticky='e')
        last_name_Label.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        last_name_Entry.grid(row=2, column=3, columnspan=2, padx=10, pady=10, sticky='e')
        date_of_birth_Label.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        date_of_birth_DateEntry.grid(row=3, column=3, columnspan=2, padx=10, pady=10, sticky='e')
        user_name_Label.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        user_name_Entry.grid(row=4, column=3, columnspan=2, padx=10, pady=10, sticky='e')
        password_Label.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        password_Entry.grid(row=5, column=3, columnspan=2, padx=10, pady=10, sticky='e')

        ok_Button.grid(row=6, column=2, sticky='e')
        cancel_Button.grid(row=6, column=3, sticky='e')

    # Destroy Create User Menu To Proceed
    def destroy_create_user(self):

        # Set Part Heading Blank
        self.entry_title_Label.config(text="")
        self.tree_title_Label.config(text="")

        # Get Child Widget list For Destroy
        entry_widget_list = self.data_entry_Frame.winfo_children()
        treeview_widget_list = self.tree_view_Frame.winfo_children()

        # Remove Entry Frame Widgets
        if entry_widget_list:
            for widget in entry_widget_list:
                widget.destroy()

        # Remove Tree Frame Widgets
        if treeview_widget_list:
            for widget in treeview_widget_list:
                widget.destroy()

        # File Menu Enable
        self.menu_bar.entryconfig("File", state='normal')

        # If User Available Enable Open User else Disable
        self.db_mgr.all_table_list()
        if self.db_mgr.table_list:
            self.file_menu.entryconfigure("Open User", state='normal')
        else:
            self.file_menu.entryconfigure("Open User", state='disable')

        # Flush Variable Data
        self.m_password_var.set("")
        self.m_user_name_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.web_address_var.set("")
        self.user_name_var.set("")
        self.other_var.set("")
        self.password_length_var.set(8)
        self.special_character_var.set("")
        self.password_var.set("")

        self.date_of_birth_var = ""
        self.salt = ""

    # Open User
    def open_user(self):

        # Close Open User Menu
        def close_win():
            self.open_Toplevel.grab_release()
            self.open_Toplevel.destroy()
            self.m_user_name_var.set("")
            self.m_password_var.set("")

        # Open User Pop-up Window
        width = 250
        height = 175
        self.open_Toplevel = Toplevel(self.root)
        self.open_Toplevel.grab_set()
        self.open_Toplevel.attributes('-topmost', 'true')
        self.open_Toplevel.overrideredirect(True)
        self.open_Toplevel.geometry(f"{width}x{height}+0+150")
        open_Frame = Frame(self.open_Toplevel)
        open_Frame.pack()
        small_title = Label(open_Frame, text="Open Account", font=("Arial", 15))
        user_name_Label = Label(open_Frame, text="User ID: ")
        user_name_Entry = Entry(open_Frame, textvariable=self.m_user_name_var)
        user_name_Entry.focus()
        password_Label = Label(open_Frame, text="Password: ")
        password_Entry = Entry(open_Frame, show="*", textvariable=self.m_password_var)

        ok_Button = Button(open_Frame, text='OK', width=5, command=self.login_validate)
        cancel_Button = Button(open_Frame, text="Cancel", width=5, command=close_win)

        small_title.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        user_name_Label.grid(row=1, column=0, padx=10, pady=10)
        user_name_Entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='n')
        password_Label.grid(row=2, column=0, padx=10, pady=10)
        password_Entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        ok_Button.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        cancel_Button.grid(row=3, column=2, padx=10, pady=10, sticky='w')

        # Escape To Cancel Button
        self.open_Toplevel.bind('<Escape>', lambda e: close_win())

        # Enter to OK Button
        self.open_Toplevel.bind('<Return>', lambda e: self.login_validate())

    # Login Validation
    def login_validate(self):

        # User ID and Password not Blank Continue
        if self.m_user_name_var.get() != "" and self.m_password_var.get() != "":

            # Get Table List(User ID List)
            self.db_mgr.all_table_list()
            if self.m_user_name_var.get() in self.db_mgr.table_list:
                reject_list, self.salt = self.db_mgr.login_process(m_username=self.m_user_name_var.get(),
                                                                   m_password=self.m_password_var.get())

                # If First Name, Last Name, Date of Birth in 'reject_list' and
                # 'salt' in Variable
                if reject_list and self.salt != "":

                    # Set Variable from 'reject_list'
                    self.first_name_var.set(reject_list[0])
                    self.last_name_var.set(reject_list[1])
                    self.date_of_birth_var = reject_list[2]

                    # Toplevel lock to Window Removed
                    self.open_Toplevel.grab_release()

                    # Destroy Toplevel
                    self.open_Toplevel.destroy()

                    # Disable File Menu
                    self.menu_bar.entryconfig("File", state="disabled")

                    # Create User Data Show Window as Treeview
                    self.create_treeview_window()

                    # Create Entry Field for Generate Random Password
                    self.load_entry_field()
                else:

                    # Login Failed
                    messagebox.showerror("Login Error", "Username, Password Combination is not Valid")

                    # Flush Variable
                    self.m_user_name_var.set("")
                    self.m_password_var.set("")

            else:

                # Entered User ID Not in Table
                messagebox.showerror("Login Error", "Invalid User ID")
        else:

            # Username or Password is Blank
            messagebox.showerror("Login Error", "Username or Password is Blank\n\nPlease Enter Valid Data")

    # Password List Treeview Creation
    def create_treeview_window(self):

        # Double-Click the Treeview to Get Password
        def OnDoubleClick(e):

            # Where User Double-Clicked
            region = self.pass_list_Treeview.identify("region", e.x, e.y)

            # If Clicked in Data Area Get Password Hash
            if region == "cell":

                # Get Item ID
                item = self.pass_list_Treeview.selection()[0]

                # Get Row Number
                row_select = self.pass_list_Treeview.item(item, "text")

                # Get Row data from Database (List of List)
                row_to_list = self.password_data_all[row_select - 1]

                # Decrypt Password Hash from Selected Row
                decrypted = self.password_gen.decrypt_password(m_pass=self.m_password_var.get(),
                                                               salt_in=self.salt,
                                                               password_hash=row_to_list[3])
                # Set Variable to Show Password in Popup
                self.web_address_var.set(row_to_list[1])
                self.user_name_var.set(row_to_list[2])
                self.password_var.set(decrypted.decode())
                self.password_popup()

        # Password List Treeview Creation Heading
        self.tree_title_Label.config(text="Saved Passwords")

        # Column Heading List
        df_col = ["Website", "User ID", "Password"]

        # Treeview Initialisation
        self.pass_list_Treeview = ttk.Treeview(self.tree_view_Frame)

        # Scroll Bar Initialisation
        vertical_Scrollbar = Scrollbar(self.tree_view_Frame, orient=VERTICAL)
        vertical_Scrollbar.pack(side=RIGHT, fill='y')
        horizontal_Scrollbar = Scrollbar(self.tree_view_Frame, orient=HORIZONTAL)
        horizontal_Scrollbar.pack(side=BOTTOM, fill='x')

        # Scroll Bar Config
        self.pass_list_Treeview.config(xscrollcommand=horizontal_Scrollbar.set, yscrollcommand=vertical_Scrollbar.set)
        vertical_Scrollbar.config(command=self.pass_list_Treeview.yview)
        horizontal_Scrollbar.config(command=self.pass_list_Treeview.xview)

        # Set Column Heading
        self.pass_list_Treeview['columns'] = df_col

        # Hide First Blank Column
        self.pass_list_Treeview['show'] = 'headings'

        # Set Column and Heading with Alignment
        for i in df_col:
            self.pass_list_Treeview.column(i, anchor="w", minwidth=5, width=10, stretch=True)
            self.pass_list_Treeview.heading(i, text=i, anchor='w')

        # Data Inserting Function
        self.insert_data_treeview()

        self.pass_list_Treeview.place(x=0, y=0, width=self.width * 2 // 3, height=self.height - 150)

        # Bind Double Click Function
        self.pass_list_Treeview.bind("<Double-1>", lambda e: OnDoubleClick(e))

    # Insert Data From Data Base to Treeview
    def insert_data_treeview(self):

        # Delete Available Data in Treeview
        self.pass_list_Treeview.delete(*self.pass_list_Treeview.get_children())

        # Get Data From Database
        self.password_data_all = self.db_mgr.db_load(self.m_user_name_var.get())

        # Loop all Data and Insert in Treeview One By One
        for row in self.password_data_all:
            modified_row = list(row[1:-1])
            modified_row.append('*' * 10)
            self.pass_list_Treeview.insert("", row[0], text=row[0], values=modified_row)

    # Toplevel to Show Web Address, User ID, Decrypted Password
    def password_popup(self):

        # Close Button Function to Clear Variable and remove Popup
        def close_win():

            # Clear Variable Data
            self.clea_field()

            # Toplevel lock to Window Removed
            self.password_view_Toplevel.grab_release()

            # Destroy Toplevel
            self.password_view_Toplevel.destroy()

        # Setup Popup Window for Show Password
        width = 200
        height = 175

        # Assign Local Variable
        web_address_view_var = StringVar(value=self.web_address_var.get())
        user_view_name_var = StringVar(value=self.user_name_var.get())
        password_view_var = StringVar(value=self.password_var.get())

        self.clea_field()

        self.password_view_Toplevel = Toplevel(self.root)
        self.password_view_Toplevel.grab_set()
        self.password_view_Toplevel.attributes('-topmost', 'true')
        self.password_view_Toplevel.overrideredirect(True)
        self.password_view_Toplevel.geometry(f"{width}x{height}+50+450")
        password_view_Frame = Frame(self.password_view_Toplevel, bg="lightblue")
        password_view_Frame.pack(fill=BOTH)

        # Password View Title
        details_view_Label = Label(password_view_Frame, text="Details", font=("Arial", 15), bg="lightblue")

        web_name_view_Label = Label(password_view_Frame, text="Web Site: ", bg="lightblue")
        web_name_view_Entry = Entry(password_view_Frame, width=20, textvariable=web_address_view_var,
                                    state='readonly', bg="lightblue")
        user_name_view_Label = Label(password_view_Frame, text="User ID: ", bg="lightblue")
        user_name_view_Entry = Entry(password_view_Frame, width=20, textvariable=user_view_name_var,
                                     state='readonly', bg="lightblue")
        password_view_Label = Label(password_view_Frame, text="Password: ", bg="lightblue")
        password_view_Entry = Entry(password_view_Frame, width=20, textvariable=password_view_var,
                                    state='readonly', bg="lightblue")
        close_Button = Button(password_view_Frame, text="Close", command=close_win, bg="lightblue")
        details_view_Label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='n')

        web_name_view_Label.grid(row=1, column=0, columnspan=2, sticky="W")
        web_name_view_Entry.grid(row=1, column=2)
        user_name_view_Label.grid(row=2, column=0, columnspan=2, sticky="W")
        user_name_view_Entry.grid(row=2, column=2)
        password_view_Label.grid(row=3, column=0, columnspan=2, sticky="W")
        password_view_Entry.grid(row=3, column=2)
        close_Button.grid(row=4, column=2, padx=10, pady=10, sticky="e")

        # Escape To Cancel Button
        self.password_view_Toplevel.bind('<Escape>', lambda e: close_win())
        self.password_view_Toplevel.focus()

    # Clear Variable Data
    def clea_field(self):
        self.web_address_var.set("")
        self.user_name_var.set("")
        self.other_var.set("")
        self.special_character_var.set("")
        self.password_length_var.set(8)
        self.password_var.set("")

    # Create Entry Field for Generate Random Password
    def load_entry_field(self):

        # Validate Random Password Generation Data
        def validate_data():
            data_valid = self.password_gen.validate_password_generation_data(
                web_add=self.web_address_var.get(),
                u_name=self.user_name_var.get(),
                other=self.other_var.get(),
                sp_chr=self.special_character_var.get(),
                pass_len=self.password_length_var.get())
            if data_valid == 1:
                messagebox.showerror("Invalid Data",
                                     "Mandatory fields are\n\
1. Website address\n\
2. User ID\n\
3. Password Length\n\
May not be Blank")
            elif data_valid == 2:
                messagebox.showerror("Invalid Data", "Entered Special Character is Out of Scope or Repeated")
            elif data_valid == 3:
                messagebox.showerror("Invalid Data", "Password Length Must Be 8 to 16")

            # Random Password Generation Data Validated Successfully
            else:

                # Generate Random password
                random_password = self.password_gen.random_password_gen(
                    u_name=self.user_name_var.get(),
                    pass_len=self.password_length_var.get(),
                    f_name=self.first_name_var.get(),
                    l_name=self.last_name_var.get(),
                    dob=self.date_of_birth_var,
                    sp_chr=self.special_character_var.get())

                # If Password Generated
                if random_password:
                    confirm = True

                    # If Web Address and User ID Combination already In Database Ask To Update or Not
                    duplicate = any(
                        filter(lambda x: x[1] == self.web_address_var.get() and x[2] == self.user_name_var.get(),
                               self.password_data_all))

                    # Update or Not
                    if duplicate:
                        confirm = messagebox.askyesno("Duplicate Error",
                                                      "Entry Already Exist Do you want New Password?")

                    # Update Allowed
                    if confirm:

                        # Password Converted to Hash
                        password_hash = self.password_gen.encrypt_random_password(
                            m_pass=self.m_password_var.get(),
                            salt_in=self.salt,
                            random_pass=random_password)

                        # If Password Hash Generated
                        if password_hash:

                            # Update Database with New Details
                            status_update = self.db_mgr.db_user_table_update(table_name=self.m_user_name_var.get(),
                                                                             web_add=self.web_address_var.get(),
                                                                             user_id=self.user_name_var.get(),
                                                                             pass_hash=password_hash)

                            # If Update Successful
                            if status_update == "Success":

                                # Display Newly Generated Random Password
                                self.password_var.set(random_password)

                                # Flesh Critical Data and other Variable
                                password_hash = ""
                                data_valid = None
                                status_update = None

                                # Always True Condition
                                if not (password_hash or data_valid or status_update):

                                    # Reload Treeview
                                    self.insert_data_treeview()

                                    # Show New Random Password
                                    self.password_popup()
                            else:

                                # If Database Not Updated
                                messagebox.showerror("DB Update Error", f"DB Update error{status_update}")
                    else:

                        # If you Don't Want to Update Clear All Data
                        self.clea_field()

        # Logout User
        def logout_user():

            # Destroy Data Entry and Treeview Area
            self.destroy_create_user()

        # Show Title Name and Create Entry Field
        self.entry_title_Label.config(text="Create Account")

        entry_title_Label = Label(self.entry_title_Frame, height=5, relief=RAISED, text="Generate Area",
                                  font=("Arial", 15))
        web_name_Label = Label(self.data_entry_Frame, text="Website address(eg. facebook.com): ", pady=10, padx=10)
        web_name_Entry = Entry(self.data_entry_Frame, width=20, textvariable=self.web_address_var)
        web_name_Entry.focus()
        user_name_Label = Label(self.data_entry_Frame, text="User ID: ", pady=10, padx=10)
        user_name_Entry = Entry(self.data_entry_Frame, width=20, textvariable=self.user_name_var)
        other_Label = Label(self.data_entry_Frame,
                            text='Numbers, words are not to be used in Password\n(Vehicle Number, Some other Words)',
                            pady=10,
                            padx=10)
        other_Entry = Entry(self.data_entry_Frame, width=20, textvariable=self.other_var)
        sp_chr_Label = Label(self.data_entry_Frame, text=f"Special character not to used in Password\n!@#$%^&*()?",
                             pady=10,
                             padx=10)
        sp_chr_Entry = Entry(self.data_entry_Frame, width=20, textvariable=self.special_character_var)
        pass_len_Label = Label(self.data_entry_Frame, text="Password Length: ", pady=10, padx=10)
        pass_len_Entry = Entry(self.data_entry_Frame, width=20, textvariable=self.password_length_var)

        logoff_Button = Button(self.data_entry_Frame, width=8, text="Logout", command=logout_user)
        generate_Button = Button(self.data_entry_Frame, width=8, text="Generate", command=validate_data)
        clear_Button = Button(self.data_entry_Frame, width=8, text="Clear", command=self.clea_field)

        entry_title_Label.pack(fill=BOTH)
        web_name_Label.grid(row=0, column=0, columnspan=2, sticky="W")
        web_name_Entry.grid(row=0, column=2)
        user_name_Label.grid(row=1, column=0, columnspan=2, sticky="W")
        user_name_Entry.grid(row=1, column=2)
        other_Label.grid(row=2, column=0, columnspan=2, sticky="W")
        other_Entry.grid(row=2, column=2)
        sp_chr_Label.grid(row=3, column=0, columnspan=2, sticky="W")
        sp_chr_Entry.grid(row=3, column=2)
        pass_len_Label.grid(row=4, column=0, columnspan=2, sticky="W")
        pass_len_Entry.grid(row=4, column=2)
        logoff_Button.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        generate_Button.grid(row=5, column=1, padx=10, pady=10, sticky="e")
        clear_Button.grid(row=5, column=2, padx=10, pady=10, sticky="e")

    # Run Tkinter Window
    def run(self):
        self.root.mainloop()

    # Call Back Function For Disable Close Button
    @staticmethod
    def __callback():
        return


if __name__ == "__main__":
    print("Please Open Main Program")
