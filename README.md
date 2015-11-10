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

### Ubuntu Digital Ocean Node

**Setup**
```
sudo apt-get install sqlite3 gunicorn tmux
pip install -r requirements.txt
```

**Setup MongoDB**
For instructions on how to migrate/copy the existing MongoDB, look at the README in the scrapers folder. After restoring the MongoDB on a machine, run the scrapers in order to continue collecting data on farmers. 
```
tmux attach -t crawler
cd ~/driveshare-graph/scrapers
./scrapeAPI.sh
```
Detach the tmux session (ctrl-b then d) after starting the scrapeAPI script. 

**Deploy**
```
tmux attach -t driveshare-graph
cd project
gunicorn -b 0.0.0.0:80 --workers=4 app:app
```
Detach the tmux session after running gunicorn.

Then, create a new tmux session that will update the network.db every 30 seconds.
```
tmux attach -t updateSQL
cd project
python updateSQL.py
```
Detach the tmux session after beginning the updateSQL script. 

## Databases

network.db in the project directory is a sqlite database containing duration and uptime information for each payout address. 
