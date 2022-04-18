import windows_tools.antivirus
import windows_tools.windows_firewall
import windows_tools.powershell
import platform
from utils import write_to_file
import subprocess


def system_version():
    write_to_file("SYSTEM VERSION",f"{platform.system()} {platform.release()}")


def anti_virus():
    result = windows_tools.antivirus.get_installed_antivirus_software()
    write_to_file("ANTIVIRUS", f"{result}")


def dok():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        "Get-ItemProperty -PATH 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\*\\*' | Select FriendlyName"
    ],
        capture_output=True)
    write_to_file("DOK", f"{output.stdout.decode('oem')}")

def chrome_version():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        "reg query 'HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome'"
    ],
        capture_output=True)
    write_to_file("CHROME VERSION", f"{output.stdout.decode('oem')}")



def windows_firewall_is_on():
    result = windows_tools.windows_firewall.is_firewall_active()
    write_to_file("WINDOWS FIREWALL IS ACTIVE", result)


def windows_firewall_policy():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        'Get-NetFirewallRule'
    ],
        capture_output=True)
    write_to_file("WINDOWS FIREWALL POLICY", f"{output.stdout.decode('oem')}")


def password_policy():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        'net accounts'
    ],
        capture_output=True)
    write_to_file("PASSWORD POLICY", f"{output.stdout.decode('oem')}")

def login_events():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        'get-eventlog security  | where-object {$_.EventID -eq  "4625"} | select TimeGenerated |fl'
    ],
        capture_output=True)
    write_to_file("FAILED LOGIN EVENTS", f"{output.stdout.decode('oem')}")


def reboot_events():
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        'get-eventlog system | where-object {$_.eventid -eq 1074} | select Timegenerated, EntryType, Message'
    ],
        capture_output=True)
    write_to_file("REBOOT EVENTS",f"{output.stdout.decode('oem')}")





