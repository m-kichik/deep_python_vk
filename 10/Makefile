VENV_BIN = venv/bin
SHELL = bash

all:
	python3 -m venv venv
	test -d venv
	. venv/bin/activate
	$(VENV_BIN)/python setup.py -q install
	$(VENV_BIN)/python  -m pip install -r requirements.txt
	$(VENV_BIN)/python test_cjson.py

clean:
	rm -rf venv
	rm -rf build
	rm -rf cjson.egg-info
	rm -rf dist