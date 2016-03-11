from scrapy import Spider
from farmers.items import FarmerItem
import json
import datetime

class FarmerSpider(Spider):
	name = "farmer"
	allowed_domains = ["status.driveshare.org"]
	start_urls = [
		"http://status.driveshare.org/api/online/json"
	]
	
	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		item = FarmerItem()
		item["farmers"] = jsonresponse["farmers"]
		item["time"] = datetime.datetime.now()
		return item
		
