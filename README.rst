cihub
=====

Collect status of CI systems and return them via access point as XML or JSON.


Requirements
============

* Python 3.7
* pipenv (accessible via $PATH)


Installation
============

* git clone
* cd cihub
* pipenv install
* cp .env.in .env
* vi .env
* pipenv shell
* python cihub.py --init-db

Fill database with example content:

* python cihub.py --example-data


Usage
=====

* pipenv shell
* python cihub.py

Starts server on http://0.0.0.0:8000

Known URLs
==========

* http://0.0.0.0:8000/cc.xml XML representation
* http://0.0.0.0:8000/cc.json JSON representation

Run tests
=========

* Installation:

    - pipenv install --dev

* Activation:

    - pipenv shell

* Execution:

    - pipenv run pytest

Update depencencies
===================

* Activation:

    - pipenv shell

* Execution:

    - pipenv update --outdated
    - pipenv update

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


From Bitbucket Pipelines
------------------------

* Create a `webhook <https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html>`_
* URL: https://<cihub-host:port>/api/bitbucket.json
* Choose from a full list of triggers:

    - Build status updated

From Travis CI
--------------

* Add to your `.travis.yml`::

  notifications:
      webhooks: https://<cihub-host:port>/api/travis.json


From GitHub Actions
-------------------

* Add a webhook in Settings --> Webhooks in the repository or for the
  organization.
* URL: https://<cihub-host:port>/api/github.json
* Content type: ``application/json``
* Secret: leave this field empty
* Which events would you like to trigger this webhook?

    - Choose „Let me select individual events.“
    - Select only „Check suites“ (this may require to deselect some other
      check boxes)

From GitLab CI
--------------

* Add a webhook in Settings --> Webhooks in the repository or for the
  organization.
* URL: https://<cihub-host:port>/api/gitlab.json
* Secret Token: leave this field empty.
* Trigger:

  - Select only "Job events" (thus deselect "Push events")

* Add webhook.
