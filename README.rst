================
driveshare-graph
================

|BuildLink|_ |CoverageLink|_ |LicenseLink|_ 

.. |BuildLink| image:: https://travis-ci.org/Storj/driveshare-graph.svg?branch=master
.. _BuildLink: https://travis-ci.org/Storj/driveshare-graph

.. |CoverageLink| image:: https://coveralls.io/repos/Storj/driveshare-graph/badge.svg?branch=master&service=github
.. _CoverageLink: https://coveralls.io/github/Storj/driveshare-graph?branch=master

.. |LicenseLink| image:: https://img.shields.io/badge/license-MIT-blue.svg
.. _LicenseLink: https://raw.githubusercontent.com/Storj/sjcx-payments

Go to [graph.driveshare.org](http://graph.driveshare.org) to see network statistics. Built using the Flask framework. MongoDB contains raw data on farmers. Data in MongoDB is collected from the farmers and totalStorage scrapy scripts which are located in the scrapers directory. 

Currently displays:
* total storage capacity over time 
* average capacity per farmer 
* number of farmers over time
* min/max number of farmers over time
* histogram of active farmers' uptime percentages (active farmers are farmers who have been seen on the network in the past week)
* average uptime percentage of active farmers

Ubuntu Digital Ocean Node
=========================

Setup
-----
Install required packages
::
  $ git clone https://github.com/Storj/driveshare-graph.git
  $ cd driveshare-graph
  $ sudo apt-get install sqlite3 gunicorn tmux
  $ pip install -r requirements.txt

MongoDB Setup
-------------
For instructions on how to migrate/copy the existing MongoDB, look at the README in the scrapers folder. After restoring the MongoDB on a machine, run the scrapers in order to continue collecting data on farmers. 
:: 
  $ tmux attach -t crawler
  $ cd ~/driveshare-graph/scrapers
  $ ./scrapeAPI.sh
Detach the tmux session (ctrl-b then d) after starting the scrapeAPI script. 

Deploy
------
::
  $ tmux attach -t driveshare-graph
  $ cd project
  $ gunicorn -b 0.0.0.0:80 --workers=4 app:app
Detach the tmux session after running gunicorn.

Then, create a new tmux session that will update the network.db.
::
  $ tmux attach -t updateSQL
  $ cd project
  $ python updateSQL.py
Detach the tmux session after beginning the updateSQL script. 

Databases
=========

network.db in the project directory is a sqlite database. The farmers table contains duration and uptime information for each payout address. updateSQL.py updates the network.db every 30 seconds. MongoDB queries take a lot of time to execute, so the farmers table is used to generate the uptime histogram and average uptime percentage. 

