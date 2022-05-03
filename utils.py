import subprocess
from datetime import date

def write_to_file(check_name, check_result):
    today = date.today()
    file1 = open(f".\\{today}.txt", "a")
    file1.write(f"{check_name}: {check_result}\n")
    file1.close()

def make_list_from_data(data):
    strOutput = data
    listRes = list(strOutput.split("\n"))
    return listRes


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
