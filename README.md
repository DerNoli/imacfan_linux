# imacfan_linux

This script allowed me to control my fan in my iMac19,1 model in Arch linux.

There is some prerequisites to get the script running.

sudo pacman -S bc stress-ng python-pyqt6
Check if applesmc-dkms is running by typing:

sudo lsmod | grep applesmc


then you need lm-sensors and find the proper fles for the fan:

type sensors:

<details>
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +48.0°C  (high = +82.0°C, crit = +100.0°C)
Core 0:        +45.0°C  (high = +82.0°C, crit = +100.0°C)
Core 1:        +47.0°C  (high = +82.0°C, crit = +100.0°C)
Core 2:        +46.0°C  (high = +82.0°C, crit = +100.0°C)
Core 3:        +45.0°C  (high = +82.0°C, crit = +100.0°C)
Core 4:        +44.0°C  (high = +82.0°C, crit = +100.0°C)
Core 5:        +50.0°C  (high = +82.0°C, crit = +100.0°C)

pch_cannonlake-virtual-0
Adapter: Virtual device
temp1:        +59.0°C  

nvme-pci-0200
Adapter: PCI adapter
Composite:    +36.9°C  

applesmc-isa-0300
Adapter: ISA adapter
Main :       2274 RPM  (min = 2000 RPM, max = 2755 RPM)
TA0P:         +18.8°C  
TA0V:         +27.2°C  
TA0p:         +38.8°C  
TC0E:         -52.0°C  
TC0F:         -51.0°C  
TC0J:          +0.8°C  
TC0P:         +44.8°C  
TC0T:          -0.2°C  
TC0c:         +45.0°C  
TC0p:         +44.8°C  
TC1c:         +47.0°C  
TC2c:         +47.0°C  
TC3c:         +44.0°C  
TCGc:         +48.0°C  
TCSc:         +45.0°C  
TCXR:         -52.2°C  
TCXc:         +47.8°C  
TCXr:         -52.2°C  
TG0D:         +43.0°C  
TG0E:         +43.0°C  
TG0F:         +43.8°C  
TG0J:          +0.5°C  
TG0P:         +46.8°C  
TG0T:          +0.0°C  
TG0d:         +43.0°C  
TG0p:         +46.8°C  
TG1D:        -127.0°C  
TG1E:        -127.0°C  
TG1F:        -127.0°C  
TG1J:          +0.0°C  
TG1P:         +44.8°C  
TG1T:        -127.0°C  
TG1d:        -127.0°C  
TG1p:         +44.8°C  
TG2P:         +45.2°C  
TG2d:        -127.0°C  
TG2p:         +45.2°C  
TH0A:        -127.0°C  
TH0B:        -127.0°C  
TH0C:        -127.0°C  
TH0F:        -127.0°C  
TH0O:          -7.0°C  
TH0P:          -7.0°C  
TH0R:        -127.0°C  
TH0a:        -127.0°C  
TH0b:        -127.0°C  
TH0c:        -127.0°C  
TH0e:          +0.0°C  
TH1A:         +36.8°C  
TH1B:         +39.5°C  
TH1C:         +41.2°C  
TH1F:         -42.2°C  
TH1O:          +9.0°C  
TH1P:        -127.0°C  
TH1R:         -42.2°C  
TH1a:         +36.8°C  
TH1b:         +39.5°C  
TH1c:         +41.2°C  
TL0P:         +38.8°C  
TL0V:         +38.8°C  
TL0p:         +38.8°C  
TL1P:         +38.8°C  
TL1V:         +37.8°C  
TL1p:         +38.8°C  
TL1v:         +37.8°C  
TM0P:         +40.8°C  
TM0V:         +38.5°C  
TM0p:         +40.8°C  
TM1P:         +34.0°C  
TM1a:         +44.0°C  
TM1p:         +34.0°C  
TM2P:         +36.2°C  
TM2a:         +42.5°C  
TM2b:         +43.0°C  
TM2c:         +42.0°C  
TM2d:         +43.5°C  
TM2p:         +36.2°C  
TM3P:         +38.5°C  
TM3a:         +42.5°C  
TM3b:         +44.0°C  
TM3c:         +42.0°C  
TM3d:         +42.2°C  
TM3p:         +38.5°C  
TM4a:         +38.5°C  
TMXP:         +40.8°C  
TPCD:         +57.0°C  
TS0V:         +37.5°C  
Tb0P:         +49.8°C  
Tb0p:         +49.8°C  
Tm0P:         +42.0°C  
Tm0p:         +42.0°C  
Tm1P:         +43.2°C  
Tm1p:         +43.2°C  
Tm2P:         +42.8°C  
Tm2p:         +42.8°C  
Tm3P:         +39.0°C  
Tm3p:         +39.0°C  
Tp2F:         +39.0°C  
Tp2H:         +39.0°C  
Tp2h:         +39.0°C  

amdgpu-pci-0100
Adapter: PCI adapter
vddgfx:      856.00 mV 
edge:         +43.0°C  (crit = +108.0°C, hyst = -273.1°C)
PPT:           9.11 W  (cap = 103.00 W)
sclk:         349 MHz 
mclk:         300 MHz 
</details>

then find the proper file to change:

for f in /sys/devices/platform/applesmc.768/temp*_input; do echo -n "$f: "; cat "$f"; done
<details>
/sys/devices/platform/applesmc.768/temp100_input: 39000
/sys/devices/platform/applesmc.768/temp10_input: 44750
/sys/devices/platform/applesmc.768/temp11_input: 48000
/sys/devices/platform/applesmc.768/temp12_input: 46000
/sys/devices/platform/applesmc.768/temp13_input: 44000
/sys/devices/platform/applesmc.768/temp14_input: 48000
/sys/devices/platform/applesmc.768/temp15_input: 45000
/sys/devices/platform/applesmc.768/temp16_input: -52250
/sys/devices/platform/applesmc.768/temp17_input: 47750
/sys/devices/platform/applesmc.768/temp18_input: -52250
/sys/devices/platform/applesmc.768/temp19_input: 43000
/sys/devices/platform/applesmc.768/temp1_input: 18750
/sys/devices/platform/applesmc.768/temp20_input: 43000
/sys/devices/platform/applesmc.768/temp21_input: 43750
/sys/devices/platform/applesmc.768/temp22_input: 500
/sys/devices/platform/applesmc.768/temp23_input: 46750
/sys/devices/platform/applesmc.768/temp24_input: -250
/sys/devices/platform/applesmc.768/temp25_input: 43000
/sys/devices/platform/applesmc.768/temp26_input: 46750
/sys/devices/platform/applesmc.768/temp27_input: -127000
/sys/devices/platform/applesmc.768/temp28_input: -127000
/sys/devices/platform/applesmc.768/temp29_input: -127000
/sys/devices/platform/applesmc.768/temp2_input: 27500
/sys/devices/platform/applesmc.768/temp30_input: 0
/sys/devices/platform/applesmc.768/temp31_input: 44750
/sys/devices/platform/applesmc.768/temp32_input: -127000
/sys/devices/platform/applesmc.768/temp33_input: -127000
/sys/devices/platform/applesmc.768/temp34_input: 44750
/sys/devices/platform/applesmc.768/temp35_input: 45250
/sys/devices/platform/applesmc.768/temp36_input: -127000
/sys/devices/platform/applesmc.768/temp37_input: 45250
/sys/devices/platform/applesmc.768/temp38_input: -127000
/sys/devices/platform/applesmc.768/temp39_input: -127000
/sys/devices/platform/applesmc.768/temp3_input: 38750
/sys/devices/platform/applesmc.768/temp40_input: -127000
/sys/devices/platform/applesmc.768/temp41_input: -127000
/sys/devices/platform/applesmc.768/temp42_input: -7000
/sys/devices/platform/applesmc.768/temp43_input: -7000
/sys/devices/platform/applesmc.768/temp44_input: -127000
/sys/devices/platform/applesmc.768/temp45_input: -127000
/sys/devices/platform/applesmc.768/temp46_input: -127000
/sys/devices/platform/applesmc.768/temp47_input: -127000
/sys/devices/platform/applesmc.768/temp48_input: 0
/sys/devices/platform/applesmc.768/temp49_input: 36750
/sys/devices/platform/applesmc.768/temp4_input: -52000
/sys/devices/platform/applesmc.768/temp50_input: 39500
/sys/devices/platform/applesmc.768/temp51_input: 41250
/sys/devices/platform/applesmc.768/temp52_input: -42250
/sys/devices/platform/applesmc.768/temp53_input: 9000
/sys/devices/platform/applesmc.768/temp54_input: -127000
/sys/devices/platform/applesmc.768/temp55_input: -42250
/sys/devices/platform/applesmc.768/temp56_input: 36750
/sys/devices/platform/applesmc.768/temp57_input: 39500
/sys/devices/platform/applesmc.768/temp58_input: 41250
/sys/devices/platform/applesmc.768/temp59_input: 39000
/sys/devices/platform/applesmc.768/temp5_input: -51000
/sys/devices/platform/applesmc.768/temp60_input: 38750
/sys/devices/platform/applesmc.768/temp61_input: 39000
/sys/devices/platform/applesmc.768/temp62_input: 38750
/sys/devices/platform/applesmc.768/temp63_input: 37750
/sys/devices/platform/applesmc.768/temp64_input: 38750
/sys/devices/platform/applesmc.768/temp65_input: 37750
/sys/devices/platform/applesmc.768/temp66_input: 40750
/sys/devices/platform/applesmc.768/temp67_input: 38500
/sys/devices/platform/applesmc.768/temp68_input: 40750
/sys/devices/platform/applesmc.768/temp69_input: 34000
/sys/devices/platform/applesmc.768/temp6_input: 750
/sys/devices/platform/applesmc.768/temp70_input: 43750
/sys/devices/platform/applesmc.768/temp71_input: 34000
/sys/devices/platform/applesmc.768/temp72_input: 36250
/sys/devices/platform/applesmc.768/temp73_input: 42500
/sys/devices/platform/applesmc.768/temp74_input: 43000
/sys/devices/platform/applesmc.768/temp75_input: 42000
/sys/devices/platform/applesmc.768/temp76_input: 43500
/sys/devices/platform/applesmc.768/temp77_input: 36250
/sys/devices/platform/applesmc.768/temp78_input: 38500
/sys/devices/platform/applesmc.768/temp79_input: 42250
/sys/devices/platform/applesmc.768/temp7_input: 44750
/sys/devices/platform/applesmc.768/temp80_input: 44000
/sys/devices/platform/applesmc.768/temp81_input: 42000
/sys/devices/platform/applesmc.768/temp82_input: 42250
/sys/devices/platform/applesmc.768/temp83_input: 38500
/sys/devices/platform/applesmc.768/temp84_input: 38500
/sys/devices/platform/applesmc.768/temp85_input: 40750
/sys/devices/platform/applesmc.768/temp86_input: 58000
/sys/devices/platform/applesmc.768/temp87_input: 37750
/sys/devices/platform/applesmc.768/temp88_input: 49500
/sys/devices/platform/applesmc.768/temp89_input: 49500
/sys/devices/platform/applesmc.768/temp8_input: -250
/sys/devices/platform/applesmc.768/temp90_input: 42000
/sys/devices/platform/applesmc.768/temp91_input: 42000
/sys/devices/platform/applesmc.768/temp92_input: 43250
/sys/devices/platform/applesmc.768/temp93_input: 43250
/sys/devices/platform/applesmc.768/temp94_input: 42750
/sys/devices/platform/applesmc.768/temp95_input: 42750
/sys/devices/platform/applesmc.768/temp96_input: 39000
/sys/devices/platform/applesmc.768/temp97_input: 39000
/sys/devices/platform/applesmc.768/temp98_input: 39000
/sys/devices/platform/applesmc.768/temp99_input: 39000
/sys/devices/platform/applesmc.768/temp9_input: 45000
After that set the proper temp file in the script
</details>
Since my sensor for CPU is TC0p and the GPU Sensor is TG0p i used following lines, as these represented the real temps best.


CPU_TEMP="/sys/devices/platform/applesmc.768/temp10_input"
GPU_TEMP="/sys/devices/platform/applesmc.768/temp23_input"

The script can be installed using makpkg -si

it will also sow a tray icon in KDE Plasma 6

stress-ng --cpu 4
