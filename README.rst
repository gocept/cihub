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
* bin/python cihub.py --init-db

Fill database with example content:

* bin/python cihub.py --example-data


Usage
=====

* bin/python cihub.py

Starts server on http://0.0.0.0:8000

Known URLs
==========

* http://0.0.0.0:8000/cc.xml XML representation
* http://0.0.0.0:8000/cc.json JSON representation


Pushing data to cihub
=====================

From Jenkins
------------

* Install `Notification Plugin <https://wiki.jenkins.io/display/JENKINS/Notification+Plugin>`_.
* Create Notification endpoint in the job configuration.

    - Format: JSON
    - Protokoll: HTTP
    - Event: "Job completed"
    - URL Source: https://<cihub-host:port>/api/jenkins.json
