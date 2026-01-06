# imac_fan

This daemon helps controlling an iMac 19,1 fan even under heavy load.
I know that the maximum rpm of 4000 is a lil over the top but it works fine for me. This allows me to evenn play on an iMac.

Since most Arch Distros nowadays use hwmon to detect the devices, the sxript is adapted to be used OOTB.

Installation is simple

clone the git:

git clone https://github.com/DerNoli/imacfan_linux

then

cd imacfan_linux

makepkg -si
