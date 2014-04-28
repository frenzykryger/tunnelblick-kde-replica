#!/usr/bin/python
import json
import sys
import traceback
from PyQt4 import QtCore, QtGui
from functools import partial
from sh import sudo, notify_send, ErrorReturnCode


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    status = {}
    timer = QtCore.QTimer()

    def __init__(self, icon, parent=None, conf=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        if conf:
            self.services = conf.get('services', [])
            self.on_click = conf.get('on-click', [])
            self.chains = conf.get('chains', {})
            for service in self.services:
                action = menu.addAction("Connect " + service)
                action.triggered.connect(partial(self.connect_vpn, service))
            for service in self.services:
                action = menu.addAction("Disconnect " + service)
                action.triggered.connect(partial(self.disconnect_vpn, service))
            self.activated.connect(partial(self.chain_connect, self.on_click))
            for name, chain in self.chains.iteritems():
                action = menu.addAction("[+]" + name)
                action.triggered.connect(partial(self.chain_connect, chain))
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.setContextMenu(menu)
        self.timer.timeout.connect(self.poll_status)
        self.timer.start(5000)

    def chain_connect(self, on_click):
        for service in on_click:
            self.connect_vpn(service)

    def connect_vpn(self, service):
        try:
            sudo.systemctl.restart("openvpn@%s.service" % service).wait()
        except ErrorReturnCode:
            notify_send("Failed to connect to %s" % service)
            traceback.print_exc()

    def disconnect_vpn(self, service):
        try:
            sudo.systemctl.stop("openvpn@%s.service" % service).wait()
        except ErrorReturnCode:
            notify_send("Failed to disconnect %s" % service).wait()
            traceback.print_exc()

    def poll_status(self):
        for service in self.services:
            try:
                sudo.systemctl("is-active",
                               "openvpn@%s.service" % service).wait()
                service_status = "Connected to %s" % service
            except ErrorReturnCode:
                service_status = "Disconnected from %s" % service
            if self.status.get(service) != service_status:
                notify_send(service_status).wait()
            self.status[service] = service_status
        self.setToolTip("\n".join(self.status.values()))

def main():
    with open("conf.json", "r") as f:
        conf = json.loads(f.read())
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("Tunnelblick.png"), w,
                              conf=conf)

    trayIcon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
