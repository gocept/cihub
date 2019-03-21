cihub
=====

Collect status of CI systems and return them via access point as XML or JSON.


Requirements
============

* Python 3.7


Installation
============

* hg clone
* cd cihub
* python3.7 -m venv .
* bin/pip install -r requirements.txt

Usage
=====

* bin/python main.py

Starts server on http://0.0.0.0:8000

Known URLs
==========

* http://0.0.0.0:8000/cc.xml XML representation
* http://0.0.0.0:8000/cc.json JSON representation
