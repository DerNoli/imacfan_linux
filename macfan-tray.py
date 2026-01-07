#!/usr/bin/python
# Save as: macfantray
# chmod +x macfantray

import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from gi.repository import Gio
import configparser
import xml.etree.ElementTree as ET

CPU_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/temp10_input"
GPU_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/temp23_input"
FAN_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/fan1_input"

def read_int(path):
    try:
        return int(open(path).read().strip())
    except:
        return 0

# ---------------------------------------------------------
# UNIVERSAL THEME DETECTION
# ---------------------------------------------------------

def detect_gnome_dark():
    try:
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        scheme = settings.get_string("color-scheme")
        return scheme == "prefer-dark"
    except:
        return None

def detect_cinnamon_dark():
    try:
        settings = Gio.Settings.new("org.cinnamon.desktop.interface")
        theme = settings.get_string("gtk-theme").lower()
        return "dark" in theme
    except:
        return None

def detect_mate_dark():
    try:
        settings = Gio.Settings.new("org.mate.interface")
        theme = settings.get_string("gtk-theme").lower()
        return "dark" in theme
    except:
        return None

def detect_kde_dark():
    path = os.path.expanduser("~/.config/kdeglobals")
    if not os.path.exists(path):
        return None
    cfg = configparser.ConfigParser()
    cfg.read(path)
    try:
        scheme = cfg["General"]["ColorScheme"].lower()
        return "dark" in scheme
    except:
        return None

def detect_xfce_dark():
    path = os.path.expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml")
    if not os.path.exists(path):
        return None
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        for prop in root.findall("property"):
            if prop.get("name") == "ThemeName":
                theme = prop.get("value", "").lower()
                return "dark" in theme
    except:
        pass
    return None

def detect_lxqt_dark():
    path = os.path.expanduser("~/.config/lxqt/session.conf")
    if not os.path.exists(path):
        return None
    cfg = configparser.ConfigParser()
    cfg.read(path)
    try:
        theme = cfg["General"]["theme"].lower()
        return "dark" in theme
    except:
        return None

def detect_env_dark():
    for var in ["GTK_THEME", "QT_QPA_PLATFORMTHEME"]:
        if var in os.environ:
            if "dark" in os.environ[var].lower():
                return True
    return None

def is_dark_theme():
    """Universal theme detection across all major desktop environments."""
    detectors = [
        detect_gnome_dark,
        detect_cinnamon_dark,
        detect_mate_dark,
        detect_kde_dark,
        detect_xfce_dark,
        detect_lxqt_dark,
        detect_env_dark,
    ]
    for fn in detectors:
        result = fn()
        if result is not None:
            return result
    return False  # fallback: assume light theme

# ---------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------

class MacFanTray:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.menu = QMenu()
        self.info_action = self.menu.addAction("Loading…")
        self.info_action.setDisabled(True)
        self.menu.addSeparator()

        refresh_action = self.menu.addAction("Refresh Now")
        refresh_action.triggered.connect(self.update)

        quit_action = self.menu.addAction("Quit")
        quit_action.triggered.connect(self.app.quit)

        self.tray = QSystemTrayIcon()
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(2000)

        self.update()

    def themed_icon(self, cold, normal, hot, weighted):
        dark = is_dark_theme()
        if weighted < 45:
            return QIcon(cold["dark" if dark else "light"])
        elif weighted < 70:
            return QIcon(normal["dark" if dark else "light"])
        else:
            return QIcon(hot["dark" if dark else "light"])

    def update(self):
        cpu = read_int(CPU_SENSOR) // 1000
        gpu = read_int(GPU_SENSOR) // 1000
        fan = read_int(FAN_SENSOR)
        weighted = int(cpu * 0.4 + gpu * 0.6)

        cold_icons = {
            "light": "/usr/share/icons/breeze/status/22/temperature-cold.svg",
            "dark": "/usr/share/icons/breeze-dark/status/22/temperature-cold.svg"
        }
        normal_icons = {
            "light": "/usr/share/icons/breeze/status/22/temperature-normal.svg",
            "dark": "/usr/share/icons/breeze-dark/status/22/temperature-normal.svg"
        }
        hot_icons = {
            "light": "/usr/share/icons/breeze/status/22/temperature-hot.svg",
            "dark": "/usr/share/icons/breeze-dark/status/22/temperature-hot.svg"
        }

        icon = self.themed_icon(cold_icons, normal_icons, hot_icons, weighted)
        self.tray.setIcon(icon)

        mode = "COOL" if weighted < 45 else "NORMAL" if weighted < 70 else "HOT"
        self.info_action.setText(
            f"CPU: {cpu}°C | GPU: {gpu}°C | Fan: {fan} RPM | Mode: {mode}"
        )

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    MacFanTray().run()
