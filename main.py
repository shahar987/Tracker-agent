import datetime
import sys
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import requests

from systen_checks import password_policy, dok, chrome_version, system_version, anti_virus, windows_firewall_is_on, \
    login_events, get_result


class MyService:
    """Silly little application stub"""
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        now = datetime.now()
        while now.hour == 0 and now.minute == 0 and now.second == 0:
            system_version()
            anti_virus()
            windows_firewall_is_on()
            password_policy()
            dok()
            chrome_version()
            login_events()
            result = get_result()
            requests.post(f"http://127.0.0.1:8000/client/status?client_status={result}")

class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = 'Tracker'
    _svc_display_name_ = 'Tracker'

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