from datetime import date


def write_to_file(check_name, check_result):
    today = date.today()
    file1 = open(f"C:\\Users\\Shahar\\Desktop\\{today}.txt", "a")
    file1.write(f"{check_name}: {check_result}\n")
    file1.close()