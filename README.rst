Featureless Tunnelblick KDE imitation
=====================================


For those of you who are familiar with Mac OS X Tunnelblick app
and miss it on your linux, this is simple PyQt4 app that allow you
to connect/disconnect VPNs in one click in system tray in same manner.
It calls sudo systemctl <restart/stop/is-active> openvpn@<name>.service
under the hood, so you're VPNs must be configured using systemctl services
to use it. My motivation was just get rid of repeating this commands
with simplest UI possible from my point of view :)


Requirements
------------

* PyQt4 (should be OK, you're on KDE4 right?)

* python-sh

* Passwordless sudo for systemctl <restart/stop/is-active> on your openvpn@<name>.services

* Installed notify-send

Configuration
-------------

There is just one json config file (conf.json).

Replace "services" with your openvpn services names that you're want to use.

Replace "on-click" with one or more openvpn services names that you're want to connect on tray icon click.

Replace "chains" with dictionary of one or more openvpn services names list (useful to connect several VPNs, for example your corporate VPN, then another VPN)


Launch
------

Simple run `python tunnelblick-kde.py` from project directory or write own bash wrapper:

.. code-block:: bash

    #!/bin/bash
    cd $PROJECT_DIR
    nohup python tunnelblick-kde.py > tunnelblick-kde.log 2>&1 &

and wire it to your KDE setup.
Have fun!
