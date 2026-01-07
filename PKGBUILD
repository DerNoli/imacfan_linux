# Maintainer: DerNoli

pkgname=imac_fancontrol
pkgver=1.2
pkgrel=1
pkgdesc="Mac Fan Tray + Fan Daemon for Linux"
arch=('any')
url="https://example.com"
license=('MIT')
depends=('python' 'python-pyqt6' 'bc' 'lm_sensors' 'breeze-icons')
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
        "$pkgdir/usr/bin/macfan"

    # Install tray Python application (renamed to executable)
    install -Dm755 "$srcdir/macfan-tray.py" \
        "$pkgdir/usr/bin/macfantray"

    # Install desktop launcher
    install -Dm644 "$srcdir/macfantray.desktop" \
        "$pkgdir/usr/share/applications/macfantray.desktop"

    # Install systemd system service (fan daemon)
    install -Dm644 "$srcdir/macfan.service" \
        "$pkgdir/usr/lib/systemd/system/macfan.service"

    # Install systemd user service (tray icon)
    install -Dm644 "$srcdir/macfantray.service" \
        "$pkgdir/usr/lib/systemd/user/macfantray.service"
}

post_install() {
    echo "Systemd units installed."
    echo "To enable services:"
    echo "  sudo systemctl enable --now macfan.service"
    echo "  systemctl --user enable --now macfantray.service"
}

post_upgrade() {
    echo "Reloading systemd units..."
    systemctl daemon-reload >/dev/null 2>&1 || true
    systemctl --user daemon-reload >/dev/null 2>&1 || true
}

post_remove() {
    echo "Removing systemd units..."
    systemctl disable --now macfan.service >/dev/null 2>&1 || true
    systemctl --user disable --now macfantray.service >/dev/null 2>&1 || true
}
