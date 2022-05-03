to install the service:
1. run from terminal/cmd the command : pip install -r requirements.txt
2. cd to folder where you save the current project
3.run from cmd/terminal: 
pyinstaller.exe --onefile --runtime-tmpdir=. --hidden-import win32timezone main.py
dist\main.exe install
dist\main.exe start
6. to insure the service started run: mmc Services.msc

debug the service:
run from cmd: dist\main.exe debug

stop the service:
run from cmd: dist\main.exe stop

uninstall:
dist\main.exe remove
