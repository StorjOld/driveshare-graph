import os
from scrapy import Spider
from farmers.items import FarmerItem
import json
import datetime


HOST = os.environ.get("DATASERV_HOST", "status.driveshare.org")


class FarmerSpider(Spider):
	name = "farmer"
	allowed_domains = [HOST]
	start_urls = [
		"http://{0}/api/online/json".format(HOST)
	]

	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		item = FarmerItem()
		item["farmers"] = jsonresponse["farmers"]
		item["time"] = datetime.datetime.now()
		return item

