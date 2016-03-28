import pymongo
from pymongo import MongoClient
from collections import defaultdict
import datetime as dt
import pygal
from pygal.style import BlueStyle
from datetime import timedelta

# Used for storage collection

def first_date(collection): # pragma: no cover
    """Returns the first date in the collection"""
    for doc in collection.find({}, {'time': 1, '_id': 0}
                               ).sort('time', 1).limit(1):
        begin_date = doc['time']
    return begin_date


def last_date(collection): # pragma: no cover
    """Returns the first date in the collection"""
    for doc in collection.find({}, {'time': 1, '_id': 0}
                               ).sort('time', -1).limit(1):
        last_date = doc['time']
    return last_date


def min_farmers_date(collection, date): # pragma: no cover
    """Returns the minimum number of farmers online during
    the specified date."""
    next_date = date + timedelta(days=1)
    min_farmers = 0
    for doc in collection.find({'time': {'$gte': date, '$lt': next_date}},
                               {'total_farmers': 1}
                               ).sort('total_farmers', 1).limit(1):
        min_farmers = doc['total_farmers'] 
    return min_farmers


def max_farmers_date(collection, date): #pragma: no cover
    """Returns the minimum number of farmers online during
    the specified date."""
    next_date = date + timedelta(days=1)
    max_farmers = 0
    for doc in collection.find({'time': {'$gte': date, '$lt': next_date}},
                               {'total_farmers': 1}
                               ).sort('total_farmers', -1).limit(1):
        max_farmers = doc['total_farmers'] 
    return max_farmers


def min_max_farmers(collection):
    """
    Returns a dictionary of the max and min number of
    farmers (values) on each day (keys)

    :param collection: MongoDB "storage" collection
    :return: dictionary with days (keys) and max/min number
             of farmers (values)
    """
    minmax_dict = defaultdict(list)
    begin_date = first_date(collection)
    end_date = last_date(collection)
    day_count = (end_date - begin_date).days + 1
    for single_date in (begin_date + timedelta(days=n)
                        for n in range(day_count)):
        min_farmers = min_farmers_date(collection, single_date)
        max_farmers = max_farmers_date(collection, single_date)
        minmax_dict[single_date].append(min_farmers)
        minmax_dict[single_date].append(max_farmers)
    return minmax_dict


def minmax_chart(collection):
    """
    Returns a line graph showing the maximum and minimum
    number of farmers over time on an hourly basis.

    :param collection: MongoDB "storage" collection
    :return: Pygal line chart showing max/min number of
             farmers over time
    """
    minmax_title = 'Min/Max Number of Farmers Over Time'
    minmax_chart = pygal.Line(width=1000, height=600, explicit_size=True,
                             title=minmax_title, x_label_rotation=45,
                             style=BlueStyle, disable_xml_declaration=True)
    minmax_dict = min_max_farmers(collection)
    dates = []
    min_counts = []
    max_counts = []
    for key in minmax_dict.keys():
        dates.append(key)
    dates.sort()
    for date in dates:
        min_counts.append(minmax_dict[date][0])
        max_counts.append(minmax_dict[date][1])
    minmax_chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), dates)
    minmax_chart.add('min online farmers', min_counts)
    minmax_chart.add('max online farmers', max_counts)
    return minmax_chart
