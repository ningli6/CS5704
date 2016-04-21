# Define here the models for your scraped items

import scrapy


class BugReport(scrapy.Item):
	# define the fields for your item here like:
	Url = scrapy.Field()
	BugId = scrapy.Field()
	Title = scrapy.Field()
	Importance = scrapy.Field()
	Keywords = scrapy.Field()
	ReportTime = scrapy.Field()

	# uncomment if need actual comments and developer names
	# comments = scrapy.Field()
	# developers = scrapy.Field()

	NumberOfComments = scrapy.Field()
	NumberOfDevelopers = scrapy.Field()
	
	Patches = scrapy.Field()
	# patchTime = scrapy.Field()
	# patchSize = scrapy.Field()
	NumberOfPatches = scrapy.Field()


class Patch(scrapy.Item):
	PatchTitle = scrapy.Field()
	PatchSize = scrapy.Field()
	PatchTime = scrapy.Field()
	PatchUrl = scrapy.Field()
	DiffUrl = scrapy.Field()
	NumberOfFilesChanged = scrapy.Field()
	Changes = scrapy.Field()

class File(scrapy.Item):
	FileName = scrapy.Field()
	Added = scrapy.Field()
	Deleted = scrapy.Field()

