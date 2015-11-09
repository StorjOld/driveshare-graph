# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field	


class TotalStorageItem(Item):
	total_id = Field()
	total_TB = Field()
	total_farmers = Field()
	time = Field()

