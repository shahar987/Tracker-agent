import sys
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
from systen_checks import password_policy,dok, chrome_version,system_version,anti_virus,windows_firewall_policy,windows_firewall_is_on, login_events, reboot_events

class MyService:
    """Silly little application stub"""
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        self.running = True
        while self.running:
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