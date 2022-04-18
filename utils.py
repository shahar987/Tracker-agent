import subprocess
from datetime import date


def write_to_file(check_name, check_result):
    today = date.today()
    file1 = open(f"C:\\Users\\Shahar\\Desktop\\{today}.txt", "a")
    file1.write(f"{check_name}: {check_result}\n")
    file1.close()


def run_shell_command(command):
    output = subprocess.run([
        'powershell.exe',
        '-noprofile',
        '-executionpolicy',
        '-bypass',
        '-c',
        command],
        capture_output=True)
    return output
