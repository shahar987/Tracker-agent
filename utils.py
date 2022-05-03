import subprocess

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
