import windows_tools.antivirus
import windows_tools.windows_firewall
import windows_tools.powershell
import platform
from utils import write_to_file, run_shell_command


def system_version():
    write_to_file("SYSTEM VERSION",f"{platform.system()} {platform.release()}")


def anti_virus():
    result = windows_tools.antivirus.get_installed_antivirus_software()
    write_to_file("ANTIVIRUS", f"{result}")


def dok():
    output = run_shell_command("Get-ItemProperty -PATH 'HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\*\\*' | Select FriendlyName")
    write_to_file("DOK", f"{output.stdout.decode('oem')}")

def chrome_version():
    output= run_shell_command("reg query 'HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome'")
    write_to_file("CHROME VERSION", f"{output.stdout.decode('oem')}")


def windows_firewall_is_on():
    result = windows_tools.windows_firewall.is_firewall_active()
    write_to_file("WINDOWS FIREWALL IS ACTIVE", result)


def windows_firewall_policy():
    output = run_shell_command("Get-NetFirewallRule")
    write_to_file("WINDOWS FIREWALL POLICY", f"{output.stdout.decode('oem')}")


def password_policy():
    output = run_shell_command("net accounts")
    write_to_file("PASSWORD POLICY", f"{output.stdout.decode('oem')}")


def login_events():
    output = run_shell_command("get-eventlog security  | where-object {$_.EventID -eq  '4625'} | select TimeGenerated |fl")
    write_to_file("FAILED LOGIN EVENTS", f"{output.stdout.decode('oem')}")


def reboot_events():
    output = run_shell_command("get-eventlog system | where-object {$_.eventid -eq 1074} | select Timegenerated, EntryType, Message")
    write_to_file("REBOOT EVENTS",f"{output.stdout.decode('oem')}")





