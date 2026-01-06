#!/usr/bin/env python3
# Save this file as: macfantray
# Then run: chmod +x macfantray

import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer

CPU_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/temp10_input"
GPU_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/temp23_input"
FAN_SENSOR = "/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0A08:00/device:5e/APP0001:00/fan1_input"

def read_int(path):
    try:
        return int(open(path).read().strip())
    except:
        return 0

class MacFanTray:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Default icon (dynamic icons will replace this)
        ICON_PATH = "/usr/share/icons/breeze/status/22/temperature-normal.svg"
        icon = QIcon(ICON_PATH)

        self.tray = QSystemTrayIcon(icon)
        self.tray.setVisible(True)

        # Right-click menu
        menu = QMenu()
        refresh_action = menu.addAction("Refresh Now")
        refresh_action.triggered.connect(self.update)

        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.app.quit)

        self.tray.setContextMenu(menu)

        # Update every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(2000)

        self.update()

    def update(self):
        cpu = read_int(CPU_SENSOR) // 1000
        gpu = read_int(GPU_SENSOR) // 1000
        fan = read_int(FAN_SENSOR)

        weighted = int(cpu * 0.4 + gpu * 0.6)

        # Dynamic icon selection
        if weighted < 45:
            icon_path = "/usr/share/icons/breeze/status/22/temperature-cold.svg"
            mode = "COOL"
        elif weighted < 70:
            icon_path = "/usr/share/icons/breeze/status/22/temperature-normal.svg"
            mode = "NORMAL"
        else:
            icon_path = "/usr/share/icons/breeze/status/22/temperature-hot.svg"
            mode = "HOT"

        self.tray.setIcon(QIcon(icon_path))

        tooltip = (
            f"CPU: {cpu}°C\n"
            f"GPU: {gpu}°C\n"
            f"Weighted: {weighted}°C\n"
            f"Fan: {fan} RPM\n"
            f"Mode: {mode}"
        )

        self.tray.setToolTip(tooltip)

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    MacFanTray().run()
