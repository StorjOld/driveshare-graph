#!/bin/bash
# Script name: scrapeAPI.sh
# Author: Andrew Kim

while true; do
	cd farmers
	scrapy crawl farmer
	cd ..
	cd totalStorage
	scrapy crawl total
	cd ..
	sleep 300
done
