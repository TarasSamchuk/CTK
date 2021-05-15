import getpass
import os
from win32api import *
import hashlib
import winreg

username = str(getpass.getuser())
comp = str(os.environ['ComputerName'])
dir = str(os.environ['SystemRoot'])
keyboard_type = str(GetAsyncKeyState(0))
screen_height = str(GetSystemMetrics(1))
set_disk = str(GetLogicalDriveStrings())
tom = os.path.splitdrive(os.getcwd())[0].rstrip(':')
all_data = (username + comp + dir + keyboard_type + screen_height + set_disk + tom).encode('utf-8')
datahash = hashlib.md5(all_data).hexdigest()

def set_reg(value):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'Software')
    reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software', 0, winreg.KEY_ALL_ACCESS)
    set = winreg.SetValue(key, 'Samchuk', winreg.REG_SZ, 'Software')
    reg_key = winreg.SetValueEx(reg_key, 'Samchuk', 0, winreg.REG_SZ, datahash)
    reg_key = winreg.QueryValueEx(key, 'Samchuk')
    winreg.CloseKey(key)

set_reg(datahash)
