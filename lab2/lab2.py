import csv
from collections import Counter
from getpass import getpass
import getpass
import os
from win32api import *
import hashlib
import winreg

def gatherData():
    username = str(getpass.getuser())
    comp = str(os.environ['ComputerName'])
    dir = str(os.environ['SystemRoot'])
    keyboard_type = str(GetAsyncKeyState(0))
    screen_height = str(GetSystemMetrics(1))
    set_disk = str(GetLogicalDriveStrings())
    tom = os.path.splitdrive(os.getcwd())[0].rstrip(':')
    all_data = (username + comp + dir + keyboard_type + screen_height + set_disk + tom).encode('utf-8')
    datahash = hashlib.md5(all_data).hexdigest()
    return datahash

def get_reg():
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software')
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software', 0, winreg.KEY_READ)
    reg_key = winreg.QueryValueEx(key, 'Samchuk')
    winreg.CloseKey(key)
    return reg_key

def check(num_culumn, find_element):
    with open('output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            if len(row) == 4:
                if row[num_culumn] == find_element:
                    curuser = row
                    break
                else:
                    curuser = None
    return curuser

def login():
    attempt = 0
    usernameIn = str(input("Enter user name:"))
    print(usernameIn)
    curuser = check(0, usernameIn)
    if curuser == None:
        while usernameIn != "break":
            print('Not find user with this username')
            login()
        else:
            print("bb")
    else:
        passwordIn = str(input("Enter your password:"))
        while attempt < 2:
            if curuser[1] == passwordIn:
                print("Sucsessfull login")
                userpanel(curuser)
                break
            else:
                attempt += 1
                print("Not corect password")
                passwordIn = input("Enter your password:")
        else:
            print("you block")
    return curuser
    # print(username, password)

def userpanel(user):
    curuser = user
    if curuser[0] != "Admin":           #USER PANEL
        while True:
            print("1. Cange password:")
            print("2. Sign out:")
            cmd = input()
            if cmd == "1":
                password_update(curuser)
            elif cmd == "2":
                print("bb")
                break
            elif cmd == "3":
                print("1.About program")
                inp = input()
                if inp == "1":
                    print("Taras Samchuk FB-83")
                    print("=====Variant15======\nСharacters are not repeated")
                else:
                    continue
            else:
                print("Not correct")
    else:                                        #================ADMIN PANEL
        while True:
            print("1. Cange password:")
            print("2. Print all users")
            print("3. Add user")
            print("4. Block user")
            print("5. Change restriction:")
            print("6. Sign out:")
            print("7. Info:")
            cmd = input()

            if cmd == "1":
                password_update(curuser)
            elif cmd == "2":
                print_users()
            elif cmd == "3":
                add_user()
            elif cmd == "4":
                block_user()
            elif cmd == "5":
                username = input("enter username for change restriction")
                with open('output.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter='\t')
                    for row in csv_reader:
                        if len(row) == 4:
                            if row[0] == username:
                                user = row
                                change_restriction(user)
                                break
                    # print("user not found")
            elif cmd == "6":
                print("bb")
                break
            elif cmd == "7":
                print("1.About program")
                inp = input()
                if inp == "1":
                    print("Taras Samchuk FB-83")
                    print("=====Variant15======\ncharacters are not repeated")
                else:
                    continue
            else:
                print("Not correct")

def print_users():
    with open('output.csv') as File:
        reader = csv.reader(File, delimiter='\t', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            print(row)

def add_user():
    new_username = input("Enter unick username:")
    with open('output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            if len(row) == 4:
                if row[0] == new_username:
                    print("Username is not unique")
                    break
                else:
                    fields = [new_username, '', False, 8]
                    with open('output.csv', 'a') as f:
                        writer = csv.writer(f, delimiter='\t')
                        writer.writerow(fields)
                    print('user added')
                    break

def block_user():
    user_to_block = input("Enter username to block:")
    with open('output.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            if len(row) == 4:
                if row[0] == user_to_block:
                    if row[2] == "True":
                        while True:
                            print("User blocked.")
                            inp = input("You want unlock user?y/n")
                            if inp == 'y':
                                row[2] = "False"
                                with open('output.csv') as inf:
                                    reader = csv.reader(inf.readlines(), delimiter='\t')
                                with open('output.csv', 'w') as outf:
                                    writer = csv.writer(outf, delimiter='\t')
                                    for line in reader:
                                        if len(line) == 4:
                                            if line[0] == row[0]:
                                                writer.writerow(row)
                                            else:
                                                writer.writerow(line)
                                    writer.writerows(reader)
                                break
                            elif inp == 'n':
                                break
                            else:
                                print("not correct")
                    else:
                        while True:
                            print("User not blocked.")
                            inp = input("You want block user?y/n")
                            if inp == 'y':
                                row[2] = "True"
                                with open('output.csv') as inf:
                                    reader = csv.reader(inf.readlines(), delimiter='\t')
                                with open('output.csv', 'w') as outf:
                                    writer = csv.writer(outf, delimiter='\t')
                                    for line in reader:
                                        if len(line) == 4:
                                            if line[0] == row[0]:
                                                writer.writerow(row)
                                            else:
                                                writer.writerow(line)
                                    writer.writerows(reader)
                                break
                            elif inp == 'n':
                                break
                            else:
                                print("not correct")

def password_update(curuser):
    repet = str(input("Enter you old password"))
    if repet == curuser[1]:
        new_password = str(input("Enter new password"))
        if curuser[3] == '1':
            dict = Counter(new_password)
            all_values = dict.values()
            max_value = max(all_values)
            while max_value > 1:
                print("password not correct")
                new_password = str(input("Enter new password"))
                dict = Counter(new_password)
                all_values = dict.values()
                max_value = max(all_values)
            else:
                rep_new_password = str(input("Repeat new password"))
        else:
            rep_new_password = str(input("Repeat new password"))
            if new_password == rep_new_password:
                new_curuser = curuser
                new_curuser[1] = new_password
                # print(curuser, '44')
                with open('output.csv') as inf:
                    reader = csv.reader(inf.readlines(), delimiter='\t')

                with open('output.csv', 'w') as outf:
                    writer = csv.writer(outf, delimiter='\t')
                    for line in reader:
                        if len(line) == 4:
                            if line[0] == curuser[0]:
                                writer.writerow(new_curuser)
                            else:
                                writer.writerow(line)
                    writer.writerows(reader)
            else:
                password_update(curuser)
    else:
        password_update(curuser)

def change_restriction(user):
    if user[3] == "1":
        user[3] = "0"
    elif user[3] == "0":
        user[3] = "1"
    with open('output.csv') as inf:
        reader = csv.reader(inf.readlines(), delimiter='\t')

    with open('output.csv', 'w') as outf:
        writer = csv.writer(outf, delimiter='\t')
        for line in reader:
            if len(line) == 4:
                if line[0] == user[0]:
                    writer.writerow(user)
                else:
                    writer.writerow(line)
    print("User restriction is update")

if __name__ == "__main__":
    datahash = gatherData()
    checkhash = get_reg()[0]
    if datahash != checkhash:
        print("exit")
        exit(0)
    else:
        list1 = ['Usename', 'Password', 'block', 'restriction']
        list2 = ['Admin', '4', False, '1']
        list3 = ['na', '5', False, '1']
        list4 = ['so', '6', False, '1']
        list5 = ['re', '2', False, '1']
        list6 = ['fd', '23', True, '1']
        list7 = ['ta', '3', False, '0']

        data = [list1, list2, list3, list4, list5, list7, list6]

        path = "output.csv"
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='\t')
            # writer.writerows(data)
            for line in data:
                writer.writerow(line)

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            for row in csv_reader:
                if row[0] == '00':
                    print(type(row))
                    curuser = row
                    print(type(curuser))
                    print(curuser[1])

        login()

