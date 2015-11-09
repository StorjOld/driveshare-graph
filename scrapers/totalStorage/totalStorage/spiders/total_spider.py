from scrapy import Spider
from totalStorage.items import TotalStorageItem
import json
import datetime

class TotalSpider(Spider):
	name = "total"
	allowed_domains = ["switch.driveshare.org"]
	start_urls = [
		"http://status.driveshare.org/api/total"
	]

	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		item = TotalStorageItem()
		item["total_id"] = jsonresponse["id"]
		item["total_TB"] = jsonresponse["total_TB"]
		item["total_farmers"] = jsonresponse["total_farmers"]
		item["time"] = datetime.datetime.now()
		return item


