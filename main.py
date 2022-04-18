import sys
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import socket
from systen_checks import password_policy,dok, chrome_version,system_version,anti_virus,windows_firewall_policy,windows_firewall_is_on, login_events, reboot_events
from utils import write_to_file
"""
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

"""

class MyService:
    """Silly little application stub"""
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        while self.running:
            write_to_file("computer name: ", f"{socket.gethostname()}")
            system_version()
            anti_virus()
            windows_firewall_is_on()
            password_policy()
            dok()
            chrome_version()
            login_events()
            reboot_events()
            windows_firewall_policy()
            self.stop()

class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = 'test'
    _svc_display_name_ = 'test'

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
      #Start the service; does not return until stopped
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == '__main__':
    init()