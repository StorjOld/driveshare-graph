from scrapy import Spider
from totalStorage.items import TotalStorageItem
import json
import datetime


HOST = os.environ.get("DATASERV_HOST", "status.driveshare.org")


class TotalSpider(Spider):
	name = "total"
	allowed_domains = [HOST]
	start_urls = [
		"http://{0}/api/total".format(HOST)
	]

	def parse(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		item = TotalStorageItem()
		item["total_id"] = jsonresponse["id"]
		item["total_TB"] = jsonresponse["total_TB"]
		item["total_farmers"] = jsonresponse["total_farmers"]
		item["time"] = datetime.datetime.now()
		return item


