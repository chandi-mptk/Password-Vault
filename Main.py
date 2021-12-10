import db_manage
import password_generator as pg
import window as win

if __name__ == "__main__":

    # Initialize Password Generate Class
    password_gen = pg.PasswordGenerator()

    # Initialize Database Manager Class
    db_mgr = db_manage.ManageDB(password_gen)

    # Get the Table List and update the Variable "table_list"
    # "table_list" save data excluding 'user_list' and 'sqlite_sequence'
    db_mgr.all_table_list()

    # If users are available
    if db_mgr.table_list:

        # Initialize Window Class with an active Open User Menu
        window = win.Window(db_mgr, password_gen, 'normal')
    else:
        # Initialize Window Class with a.txt disabled Open User Menu
        window = win.Window(db_mgr, password_gen, 'disable')

    # Run The Main Loop
    window.run()
