import socket

import windows_tools.antivirus
import windows_tools.windows_firewall
import windows_tools.powershell
import platform
from utils import run_shell_command, make_list_from_data

client_status = {"computer_name": socket.gethostname(),
                 "system_version":None,
                 "antivirus_installed": False,
                 "antivirus_enabled": False,
                 "antivirus_up_to_date": False,
                 "windows_firewall_is_active": None,
                 "max_pass_age": None,
                 "min_pass_len":None,
                 "number_of_connected_doks": None,
                 "chrome_version": None,
                 "failed_login_event": None}


def system_version():
    client_status["system_version"] = f"{platform.release()}"


def anti_virus():
    result = windows_tools.antivirus.get_installed_antivirus_software()
    enable_status = []
    is_up_to_date_status = []
    #check if there is at least one antivirus installed
    if len(result) != 0:
        client_status["antivirus_installed"] = True
        for antivirus in result:
            if antivirus["publisher"] == None:
                enable_status.append(antivirus["enabled"])
                is_up_to_date_status.append(antivirus["is_up_to_date"])
        for i in range(len(enable_status)):
            if enable_status[i] == False and is_up_to_date_status[i] == False:
                client_status["antivirus_enabled"] = False
                client_status["antivirus_up_to_date"] = False

            elif enable_status[i] == False and is_up_to_date_status[i] == True:
                client_status["antivirus_enabled"] = False
                client_status["antivirus_up_to_date"] = True

            elif enable_status[i] == True and is_up_to_date_status[i] == True:
                client_status["antivirus_enabled"] = True
                client_status["antivirus_up_to_date"] = True
                break



def dok():
    output = run_shell_command(
        "Get-ItemProperty -PATH 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\*\\*' | Select FriendlyName")
    result = make_list_from_data(output.stdout.decode("oem"))
    # 6 is the number of the extra data in the list
    dok_number = len(result) - 6
    client_status["number_of_connected_doks"] = dok_number


def chrome_version():
    output = run_shell_command(
        "reg query 'HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome'")
    lines = output.stdout.decode("oem").splitlines()
    for line in lines:
        if "DisplayVersion" in line:
            version_line = line
    version = (version_line.split("    "))[3]
    client_status["chrome_version"] = version


def windows_firewall_is_on():
    client_status["windows_firewall_is_active"] = windows_tools.windows_firewall.is_firewall_active()


def windows_firewall_policy():
    output = run_shell_command("Get-NetFirewallRule")


def password_policy():
    max_pass_age = ""
    min_pass_len = ""
    output = run_shell_command("net accounts")
    lines = output.stdout.decode("oem").splitlines()
    for line in lines:
        if "Maximum password age" in line:
            for char in line:
                if (char >= '0' and char <= '9'):
                    max_pass_age = max_pass_age + char

        if "Minimum password length" in line:
            for char in line:
                if (char >= '0' and char <= '9'):
                    min_pass_len = min_pass_len + char
    client_status["max_pass_age"] = int(max_pass_age)
    client_status["min_pass_len"] = int(min_pass_len)


def login_events():
    output = run_shell_command(
        "get-eventlog security  | where-object {$_.EventID -eq  '4625'} | select TimeGenerated |fl")
    result = make_list_from_data(output.stdout.decode("oem"))
    filtered_list = []
    for i in result:
        if i != '\r':
            filtered_list.append(i)
    client_status["failed_login_event"] = filtered_list


def reboot_events():
    output = run_shell_command("get-eventlog system | where-object {$_.eventid -eq 1074} | select Timegenerated, EntryType, Message")


if __name__ == '__main__':
    system_version()
    dok()
    chrome_version()
    windows_firewall_is_on()
    password_policy()
    login_events()
    anti_virus()
    print(client_status)




