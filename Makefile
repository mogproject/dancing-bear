PYTHON = python
PROG = dancing-bear

ARDUINO = /Applications/Arduino.app/Contents/MacOS/Arduino
ARDUINO_PORT = /dev/cu.usbmodem1451
ARDUINO_SRC = ./src/arduino/bear.ino

build:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

uninstall: dev-uninstall
	pip uninstall $(PROG)

dev-install:
	$(PYTHON) setup.py develop

dev-uninstall:
	$(PYTHON) setup.py develop -u

pep8:
	pep8 --max-line-length 120 --ignore E402,E731 src tests

test: pep8
	$(PYTHON) setup.py test

coverage:
	coverage run --source=src setup.py test

clean:
	$(PYTHON) setup.py clean

console:
	cd src && $(PYTHON)

upload:
	$(ARDUINO) --port $(ARDUINO_PORT) --upload $(ARDUINO_SRC) 2>&1 | egrep -v '^\s*at java|JmDNS|No route to host'

.PHONY: build install uninstall dev_install dev_uninstall pep8 test coverage clean console upload

