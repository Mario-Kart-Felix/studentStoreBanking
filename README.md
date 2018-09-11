### Necessary Downloads and Library Installation  for R-Pi
* $ sudo apt-get install autoconf automake libtool libusb-dev libpcsclite-dev git
* $ sudo git clone https://github.com/nfc-tools/libnfc.git
* $ cd libnfc
* $ mkdir /etc/nfc
* $ mkdir /etc/nfc/devices.d/
* $ sudo cp contrib/libnfc/pn532_uart_on_rpi.conf.sample /etc/nfc/devices.d/pn532_uart_on_rpi.conf
* $ sudo vim /etc/nfc/devices.d/pn532_uart_on_rpi.conf

Add the following lines  to the bottom of this file
> allow_intrusive_scan = true
> log_level = 3


Change
> connstring = pn532_uart:/dev/ttyAMA0


to
> connstring = pn532_uart:/dev/ttyUSB0


* $ sudo autoreconf -vis --force --install
* $ sudo ./configure --prefix=/usr --with-drivers=pn532_uart --sysconfdir=/etc
* $ sudo make clean
* $ sudo make
* $ sudo make install all

## Testing
Plug in the PN532 via a FTDI USB cable into the R-Pi

* $ cd examples
* $ sudo ./nfc-poll

Place a card and if it reads great

