#!/bin/bash
VENVBIN = ./venv/bin
PYTHON = $(VENVBIN)/python
PIP = $(VENVBIN)/pip

all: clean env

env:
	virtualenv -p python3 venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf venv
