pkgname=imacfancontrol
pkgver=1.0
pkgrel=1
pkgdesc="Mac Fan Tray + Fan Daemon for Linux"
arch=('any')
url="https://example.com"
license=('MIT')
depends=('python' 'python-pyqt6' 'bc' 'lm_sensors')
source=(
    'macfan'
    'macfan.service'
    'macfan-tray.py'
    'macfantray.desktop'
    'macfantray.service'
)
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {

    # Install system-level fan script
    install -Dm755 "$srcdir/macfan" \
        "$pkgdir/usr/local/bin/macfan"

    # Install tray Python application (renamed to executable)
    install -Dm755 "$srcdir/macfan-tray.py" \
        "$pkgdir/usr/local/bin/macfantray"

    # Install desktop launcher
    install -Dm644 "$srcdir/macfantray.desktop" \
        "$pkgdir/usr/share/applications/macfantray.desktop"

    # Install systemd system service (fan daemon)
    install -Dm644 "$srcdir/macfan.service" \
        "$pkgdir/etc/systemd/system/macfan.service"

    # Install systemd user service (tray icon)
    install -Dm644 "$srcdir/macfantray.service" \
        "$pkgdir/usr/lib/systemd/user/macfantray.service"
}

post_install() {
    echo "Enabling macfan.service (system daemon)..."
    systemctl enable macfan.service >/dev/null 2>&1 || true

    echo "Enabling macfantray.service for the current user..."
    systemctl --user enable macfantray.service >/dev/null 2>&1 || true
}

post_upgrade() {
    systemctl daemon-reload >/dev/null 2>&1 || true
    systemctl --user daemon-reload >/dev/null 2>&1 || true
}
