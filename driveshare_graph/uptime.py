from pymongo import MongoClient, IndexModel, ASCENDING
import datetime as dt
from datetime import timedelta
import sqlite3
import time
import pygal
from pygal.style import BlueStyle

connection = MongoClient('localhost', 27017)
collection = connection['GroupB']['farmers']


def create_farmers_table(conn, cursor):
    """Creates a farmer table."""
    cursor.execute(''' CREATE TABLE farmers 
        (address CHAR(34) PRIMARY KEY    NOT NULL,
         first_date       REAL           NOT NULL,
         last_date        REAL           NOT NULL, 
         uptime           REAL);''')
    conn.commit()


def create_time_index(collection):
    time_index = IndexModel([('time', ASCENDING)])
    collection.create_indexes([time_index])


def init_farmers_table(conn, cursor, collection):
    """
    Initializes the farmers table with the values from the MongoDB.
    
    Parameters:
        conn: connection to sqlite3 database containing the table, farmers 
        cursor: conn's cursor
        collection: MongoDB collection of farmers 
    """
    first_dates = {}
    last_dates = {}
    uptimes = {}
    previous_time = 0
    for doc in collection.find({}).sort('time', 1):
        doc_time = time.mktime(doc['time'].timetuple())
        for farmer in doc['farmers']:
            btc_address = farmer['btc_addr']
            if (btc_address in first_dates):
                if last_dates[btc_address] == previous_time:
                    uptimes[btc_address] += doc_time - previous_time
                last_dates[btc_address] = doc_time
            else:
                first_dates[btc_address] = doc_time
                last_dates[btc_address] = doc_time
                uptimes[btc_address] = 0
        previous_time = doc_time

    for key, value in first_dates.iteritems():
        address = key
        first_date = value
        last_date = last_dates[key]
        uptime = uptimes[key]

        cursor.execute('''INSERT INTO farmers (address, first_date, last_date,
                          uptime) VALUES(?, ?, ?, ?)''',
                       (str(address), first_date, last_date, uptime))
        conn.commit()


def address_in_db(cursor, address):
    """Returns true if address is in database, false otherwise."""
    cursor.execute('SELECT address FROM farmers WHERE address=?',
                   (str(address),))
    data = cursor.fetchone()
    if data is None:
        return False
    return True


def dt_from_timestamp(timestamp): # pragma: no cover
    datetime = dt.datetime.fromtimestamp(timestamp)
    return datetime


def timestamp_from_dt(datetime): # pragma: no cover
    timestamp = time.mktime(datetime.timetuple())
    return timestamp


def update_farmers_table(conn, cursor, collection):
    """
    Updates the farmers table with the new values in the MongoDB
    farmers collection.

    Parameters:
        conn: connection to sqlite3 database containing the table, farmers 
        cursor: conn's cursor
        collection: MongoDB collection of farmers 
    """ 
    cursor.execute('SELECT MAX(last_date) FROM farmers')
    last_time = int(cursor.fetchone()[0])
    last_date = dt_from_timestamp(last_time)

    for doc in collection.find({'time': {'$gt': last_date}}).sort('time', 1):
        doc_time = timestamp_from_dt(doc['time'])
        for farmer in doc['farmers']:
            address = farmer['btc_addr']
            if address_in_db(cursor, address):
                cursor.execute('''SELECT MAX(last_date) FROM farmers WHERE
                                  address=?''', (str(address),))
                farmer_time = int(cursor.fetchone()[0])
                if farmer_time == last_time:
                    uptime = doc_time - farmer_time
                    cursor.execute('''UPDATE farmers SET last_date=?, uptime=uptime+?
                                      WHERE address=?''', (farmer_time, uptime, str(address),))
                    conn.commit()
                else:
                    cursor.execute('''UPDATE farmers SET last_date=? WHERE
                                      address=?''', (farmer_time, str(address),))
                    conn.commit()
            else:
                cursor.execute('''INSERT INTO farmers (address, first_date,
                                  last_date, uptime) VALUES (?, ?, ?, ?) ''',
                                  (str(address), doc_time, doc_time, 0))
                conn.commit()
            last_time = doc_time
    conn.commit()


def compute_average_uptime(cursor): # pragma: no cover
    """Returns the average uptime of a farmer."""  
    cursor.execute('''SELECT avg(100 * uptime / (last_date - first_date)))
                      FROM farmers''')
    avg_uptime = cursor.fetchone()[0]
    return avg_uptime


def add_to_distribution(distribution, value): # pragma: no cover
    if value >= 95:
        distribution[95] += 1 
    elif 95 > value >= 90:
        distribution[90] += 1
    elif 90 > value >= 85:
        distribution[85] += 1
    elif 85 > value >= 80:
        distribution[80] += 1
    elif 80 > value >= 75:
        distribution[75] += 1
    elif 75 > value >= 70:
        distribution[70] += 1
    elif 70 > value >=65:
        distribution[65] += 1
    elif 65 > value >= 60:
        distribution[60] += 1
    elif 60 > value >= 55:
        distribution[55] += 1
    elif 55 > value >= 50:
        distribution[50] += 1
    elif 50 > value >= 45:
        distribution[45] += 1
    elif 45 > value >= 40:
        distribution[40] += 1
    elif 40 > value >= 35:
        distribution[35] += 1
    elif 35 > value >= 30:
        distribution[30] += 1
    elif 30 > value >= 25:
        distribution[25] += 1
    elif 25 > value >= 20:
        distribution[20] += 1
    elif 20 > value >= 15:
        distribution[15] += 1
    elif 15 > value >= 10:
        distribution[10] += 1
    elif 10 > value >= 5:
        distribution[5] += 1
    elif 5 > value >= 0:
        distribution[0] += 1


def uptime_distribution(cursor, collection): # pragma: no cover
    """ 
    Returns the distribution of active farmers' uptimes.

    Args:
        cursor: cursor for the sqlite3 connection to network.db
        collection: MongoDB collection of farmers
    """ 
    begin_date = dt.datetime.now() - timedelta(days = 7)
    farmers = collection.find({'time': {'$gte': begin_date}}
                              ).distinct('farmers.btc_addr')
    distribution = {0: 0, 5: 0, 10: 0, 15: 0, 20: 0, 25: 0, 30: 0, 35: 0, 40: 0,
                    45: 0, 50: 0, 55: 0, 60: 0, 65: 0, 70: 0, 75: 0, 80: 0,
                    85: 0, 90: 0, 95: 0}
    for farmer in farmers: 
        cursor.execute('''SELECT (uptime / (last_date - first_date)) * 100
                          FROM farmers WHERE address=?  AND
                          last_date - first_date > 0''', (str(farmer),))
        uptime = cursor.fetchone()
        if uptime is None:
            continue
        else: 
            add_to_distribution(distribution, uptime[0])
    return distribution

def active_average_uptime(cursor, collection): # pragma: no cover
    """
    Returns the uptime percentage of the active farmers (farmers
    who have been online in the past week).

    Args:
        cursor: cursor for the sqlite3 connection to network.db
        collection: MongoDB collection of farmers
    """ 
    begin_date = dt.datetime.now() - timedelta(days=7)
    farmers = collection.find({'time': {'$gte':begin_date}}
                              ).distinct('farmers.btc_addr')
    uptime_percentages = []
    for farmer in farmers:
        cursor.execute('''SELECT (uptime / (last_date - first_date)) * 100
                          FROM farmers WHERE address = ? AND (last_date - first_date) > 0''',
                       (farmer,))
        uptime = cursor.fetchone() 
        if uptime is None:
            continue
        else:
            uptime_percentages.append(uptime[0])
    print(uptime_percentages)
    if len(uptime_percentages) == 0:
        return 0
    avg = float(sum(uptime_percentages) / len(uptime_percentages))
    avg = format(avg, '.2f')
    print(len(uptime_percentages))
    return avg

def uptime_histogram(cursor, collection): # pragma: no cover
    histogram_title = 'Histogram of Active Farmers Uptime Percentages'
    uptime_histogram = pygal.Histogram(width=1000, height=600,
                                       explicit_size=True,
                                       title=histogram_title,
                                       style=BlueStyle, show_legend=False,
                                       xrange=(0, 100),
                                       disable_xml_declaration=True)
    distribution = uptime_distribution(cursor, collection)
    for key, value in distribution.iteritems():
        bucket = '%i%% to %i%%' % (key, key+5)
        uptime_histogram.add(bucket, [(value, key, key+5)])
    return uptime_histogram
