import datetime as dt
import json
from bson import json_util
import pygal
import time
from pygal.style import BlueStyle


# These functions work on the GroupB totalStorage collection.

# as the dataset grows larger these methods will take too long
# in the future, may want to use "group by" equivalent and use map-reduce
def max_tb(collection):
    """Returns the maximum number of TB recorded in the collection"""
    max_TB = 0
    for doc in collection.find({}).sort([('total_TB',-1)]).limit(1):
        max_TB = doc['total_TB']
    return max_TB


def min_tb(collection):
    """Returns the minimum number of TB recorded in the collection"""
    min_TB = 0
    for doc in collection.find({}).sort([('total_TB',1)]).limit(1):
        min_TB = doc['total_TB']
    return min_TB


def min_farmers(collection):
    """Returns the minimum number of farmers recorded in the collection"""
    min_farmers = 0
    for doc in collection.find({}).sort([('total_farmers',1)]).limit(1):
        min_farmers = doc['total_farmers']
    return min_farmers


def max_farmers(collection):
    """Returns the maximum number of farmers recorded in the collection"""
    max_farmers = 0
    for doc in collection.find({}).sort([('total_farmers',-1)]).limit(1):
        max_farmers = doc['total_farmers']
    return max_farmers


def avg_gb_farmer(collection):
    """Returns the average storage capacity of a farmer in gigabytes.""" 
    avg_gb_farmer = 0
    for doc in collection.find({}).sort([('time', -1)]).limit(1):
        avg_gb_farmer = doc['total_TB'] / doc['total_farmers'] * 1000
    avg_gb_farmer = format(avg_gb_farmer, '.2f')
    return avg_gb_farmer


def is_noon_time(dt_time):
    """
    Returns True if the time is between 12:00-12:05, False otherwise.
    
    Args:
        dt_time: datetime.datetime
    """ 
    if dt.time(12, 5) > dt_time.time() > dt.time(12, 0):
        return True
    else: 
        return False 


def create_stats_table(conn, cursor):
    cursor.execute('''CREATE TABLE stats
                      (date           REAL    PRIMARY KEY    NOT NULL,
                       tb             REAL,
                       farmers        REAL);''')
    conn.commit()


def init_stats_table(conn, cursor, collection):
    for doc in collection.find({}, {'_id': False, 'total_TB': True,
                                  'time': True, 'total_farmers': True}):
        tb = doc['total_TB']
        farmers = doc['total_farmers']
        date = time.mktime(doc['time'].timetuple())
        cursor.execute('INSERT INTO stats(date, tb, farmers) VALUES (?, ?, ?)',
                       (date, tb, farmers))
    conn.commit()


def update_stats_table(cursor, collection):
    cursor.execute('SELECT MAX(time) from stats')
    last_date = dt.datetime.fromtimestamp(int(cursor.fetchone()[0]))
    for doc in collection.find({'time': {'$gt': last_date}}):
        tb = doc['total_TB']
        farmers = doc['total_farmers']
        date = time.mktime(doc['time'].timetuple())
        cursor.execute('INSERT INTO stats(date, tb, farmers) VALUES (?, ?, ?)',
                       (date, tb, farmers))
    conn.commit()


def total_storage_graph(collection):
    totals = collection.find({}, {'_id': False, 'total_TB': True,
                                  'time': True, 'total_farmers': True})
    json_totals = []
    for total in totals:
        json_totals.append(total)
    json_totals = json.dumps(json_totals, default=json_util.default)
    parsed = json.loads(json_totals)
    terabytes = []
    times = []
    for i in range(1, len(parsed) / 12):     #takes a data point from each hour
        j = i * 12
        terabytes.append(float(parsed[j]['total_TB']))
        d = dt.datetime.fromtimestamp(parsed[j]['time']['$date']/1e3)
        times.append('%i/%i %i:%i' % (d.month, d.day, d.hour, d.minute))

    tb_title = 'Total Storage Available Over Time'
    tb_min_range = min_tb(collection)
    tb_max_range = max_tb(collection) + 100
    tb_chart = pygal.Line(width=1000, height=600, explicit_size=True,
                          x_label_rotation=35, show_minor_x_labels=False,
                          x_labels_major_count=12, title=tb_title,
                          range=(tb_min_range, tb_max_range), dots_size=0.2,
                          style=BlueStyle, disable_xml_declaration=True)
    tb_chart.x_labels = times
    tb_chart.add('TB', terabytes)
    return tb_chart


def total_farmers_graph(collection):
    totals = collection.find({}, {'_id': False, 'total_TB': True,
                                  'time': True, 'total_farmers': True})
    json_totals = []
    for total in totals:
        json_totals.append(total)
    json_totals = json.dumps(json_totals, default=json_util.default)
    parsed = json.loads(json_totals)
    farmers = []
    times = []
    for i in range(1, len(parsed) / 12):     #takes a data point from each hour
        j = i * 12
        farmers.append(int(parsed[j]['total_farmers']))
        d = dt.datetime.fromtimestamp(parsed[j]['time']['$date']/1e3)
        times.append('%i/%i %i:%i' % (d.month, d.day, d.hour, d.minute))

    farmers_title = 'Number of Farmers Over Time'
    farmers_min_range = min_farmers(collection)
    farmers_max_range = max_farmers(collection) + 50
    farmers_chart = pygal.Line(width=1000, height=600, explicit_size=True,
                               x_label_rotation=35, show_minor_x_labels=False,
                               x_labels_major_count=12, title=farmers_title,
                               range=(farmers_min_range, farmers_max_range),
                               dots_size=0.2, style=BlueStyle,
                               disable_xml_declaration=True)
    farmers_chart.x_labels = times
    farmers_chart.add('farmers', farmers)
    return farmers_chart
