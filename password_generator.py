import base64
import hashlib
import os
import random
import re
from datetime import datetime, timedelta
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordGenerator:
    def __init__(self):

        # usable Character Loading
        self.lower_letters = ascii_lowercase
        self.upper_letters = ascii_uppercase
        self.numbers = f"{digits}"
        self.special_characters = "!@#$%^&*()?"
        self.all_char_usable = ""

        # Encryption F
        self.f = ""

        # Other Variables
        self.other_list = []
        self.sp_chr_used = ""
        self.password_length = 0

    @staticmethod
    # Salt and Key Generator From Master Password
    def key_generate(m_pass, salt):

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                         length=32,
                         salt=salt,
                         iterations=390000,
                         )

        key = base64.urlsafe_b64encode(kdf.derive(m_pass.encode()))

        # Remove Password From Memory(Don't Know Is it Useful or Not)
        m_pass = ""
        if not m_pass:
            return key

    @staticmethod
    # Salt and Key Generator From Master Password
    def user_password_hash(m_pass):

        # Salt will Be Generated
        salt = os.urandom(16)

        # Master Password Hashed
        password_hash = hashlib.sha512(m_pass.encode()).hexdigest()

        # Return Password Hash and Salt
        return password_hash, salt

    # Validate The Data Entered to Create New User
    def validate_master_data(self, f_name, l_name, dob, m_user_id, m_password, min_age):

        # First Name, Last Name , User ID, Password Must not Be Blank
        if f_name == "" or l_name == "" or m_user_id == "" or m_password == "":

            # Return to show Error Message Box
            return 1
        else:

            # First Name and User ID Must be
            # Minimum of 4 letters and Maximum of 16 Letters Long

            if 4 > len(f_name) or len(f_name) > 16 or 4 > len(m_user_id) or len(m_user_id) > 16:

                # Return to show Error Message Box
                return 2
            else:

                # First Name and User ID are Valid
                if len(m_password) < 8:

                    # Password Must Be 8 Char Long
                    return 3
                elif not re.search(f'[{self.lower_letters}]', m_password):

                    # Password Must Contain At least one Lowercase Letter
                    return 4
                elif not re.search(f'[{self.upper_letters}]', m_password):

                    # Password Must Contain At least one Uppercase Letter
                    return 5
                elif not re.search(f'[{self.numbers}]', m_password):

                    # Password Must Contain At least one Digit
                    return 6
                elif not re.search(f'[{self.special_characters}]', m_password):

                    # Password Must Contain At least one punctuation Mentioned in 'special_characters' Variable
                    return 7
                elif re.search(" ", m_password):

                    # Password Must Not Contain Blank Space
                    return 8

                # Password Validation Done
                elif re.search(f'[{punctuation.replace("_", "#")}{digits}]', m_user_id):

                    # User ID Must Contain _ and Letters
                    return 10

                # User ID Validation Done
                else:

                    # Date of Birth Validation User Must Be of Minimum Age 'min_age'
                    present = datetime.now() - timedelta(days=min_age * 365)
                    if dob < present.date():
                        return 0  # Success
                    else:

                        # Date of Birth is Not Acceptable
                        return 9

    # Decrypt Hash To Password
    def decrypt_password(self, m_pass, salt_in, password_hash):

        # Clear Encryption Function 'f' and 'password'
        self.f = ""
        password = ""

        # Salt and Key Created From Password and Salt
        key = self.key_generate(m_pass=m_pass, salt=salt_in)

        # If Both Salts are Equal Create Encryption Function
        self.f = Fernet(key)

        # Remove Key from Memory( For Security, is it Necessary?)
        key = ""

        if (not key) and self.f:
            # Return Password
            password = self.f.decrypt(password_hash)
        return password

    # Validate Entry Field Data and Generate Random Password
    def validate_password_generation_data(self, web_add, u_name, other, sp_chr, pass_len):

        self.other_list = []
        self.sp_chr_used = self.special_characters
        self.password_length = 0

        # Data Validation
        if web_add == "" or u_name == "" or not pass_len:
            # 'web_add' 'u_name' 'pass_len' Must Not Be Blank
            return 1
        if other:

            # If Comma Split Words By Coma
            if ',' in other:
                self.other_list.extend(other.split(','))

            # If space or other Character Consider as a Single Word
            else:
                self.other_list.append(other)

        # If User Don't Want any Supported Special Character in His Password
        if sp_chr != "":

            # Iterate The User List
            for i in sp_chr:

                # Is the Mentioned Special Character in Supported List
                if i not in self.sp_chr_used:

                    # User Entry is Invalid
                    return 2

        # Password Length is In Range Or Not
        if 8 > pass_len or 16 < pass_len:
            return 3

    # Random Password Generator
    def random_password_gen(self, u_name, pass_len, f_name, l_name, dob, sp_chr):
        random_password = ""

        # Allowed Characters in String
        self.all_char_usable = self.lower_letters + self.upper_letters + self.numbers + self.sp_chr_used

        # Date of Birth split as list any of the 3 numbers Must Not be used
        dob_list = dob.strftime('%d-%m-%Y').split('-')

        # List of Not Usable Words
        reject_list = [f_name, l_name, u_name]
        reject_list.extend(self.other_list)
        reject_list.extend(dob_list)
        reject_list.extend([i for i in sp_chr])

        # Random Password From Python Random Function
        random_password = "".join(random.sample(self.all_char_usable, pass_len))

        # Check If Password Contains any Unwanted Words Stored in 'reject_list'
        while any(filter(lambda w: w in random_password, reject_list)):
            # If Unwanted word in Password Generate New Password
            random_password = "".join(random.sample(self.all_char_usable, pass_len))

        # Reset All Variable Dedicated to This Password Generation
        self.sp_chr_used = self.special_characters
        self.other_list = []
        self.password_length = 0
        return random_password

    # Encrypt Password to Hash
    def encrypt_random_password(self, m_pass, salt_in, random_pass):
        password_hash = ""

        # Clear Encryption Function
        self.f = ""

        # Salt and Key Created From Password and Salt
        key = self.key_generate(m_pass, salt_in)

        # If Both Salts are Equal Create Encryption Function
        self.f = Fernet(key)

        # Remove Key from Memory( For Security, is it Necessary?)
        key = ""

        if (not key) and self.f:
            # Encrypt Password
            password_hash = self.f.encrypt(random_pass.encode())

        # Clear Encryption Function
        self.f = ""
        return password_hash


if __name__ == "__main__":
    print("Please Open Main Program")
