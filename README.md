# driveshare-graph

Go to [graph.driveshare.org](graph.driveshare.org) to see network statistics. Built using the Flask framework. MongoDB contains raw data on farmers. 
Currently displays:
* total storage capacity over time 
* average capacity per farmer 
* number of farmers over time
* min/max number of farmers over time
* histogram of active farmers' uptime percentages (active farmers are farmers who have been seen on the network in the past week)
* average uptime percentage of active farmers

## How to set up and deploy website

### Ubuntu

**Setup**
`sudo apt-get install sqlite3 gunicorn
`pip install -r requirements.txt

**Deploy**
`cd project
`gunicorn -b 0.0.0.0:80 --workers=4 app:app


