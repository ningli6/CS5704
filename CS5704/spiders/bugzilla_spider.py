import scrapy

from CS5704.models import BugReport
from CS5704.models import Patch
from CS5704.models import File

class BugzillaSpider(scrapy.Spider):
    name = "bugzilla"
    allowed_domains = ["bugzilla.mozilla.org"]
    start_urls = [ # starting url: fixed, perf, firfox
        "https://bugzilla.mozilla.org/buglist.cgi?keywords=perf&keywords_type=allwords&resolution=FIXED&query_format=advanced&product=Firefox"
    ]

    def parse(self, response):
        for href in response.css(".bz_bugitem .first-child a::attr(href)"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_bug_contents)

    def parse_bug_contents(self, response):
        bug = BugReport()
        # bug url
        bug['Url'] = response.url
        # bug id, [4:] needed for trim
        bug['BugId'] = response.xpath('//div[@class="bz_alias_short_desc_container edit_form"]/a/b/text()').extract()[0][4:]
        # bug title
        bug['Title'] = response.xpath('//div[@class="bz_alias_short_desc_container edit_form"]/span[@id="summary_alias_container"]/span/text()').extract()[0]
        # importance, replace(' ', '').replace('\n', ' ') needed for trim
        bug['Importance'] = response.xpath('//td[@id="bz_show_bug_column_1"]/table//tr[11]/td/text()').extract()[0].replace(' ', '').replace('\n', ' ')
        # tags, replace(' ', '').replace('\n', '').split(',') needed for trim
        bug['Keywords'] = response.xpath('//td[@id="bz_show_bug_column_1"]/table//tr[3]/td/text()').extract()[0].replace(' ', '').replace('\n', '').split(',')
        # report time, [:-4] needed for trim
        bug['ReportTime'] = response.xpath('//td[@id="bz_show_bug_column_2"]/table//tr[1]/td/text()').extract()[0][:-4]
        # number of comments
        bug['NumberOfComments'] = len(response.xpath('//div[@class="bz_comment"]|//div[@class="bz_comment bz_first_comment"]'))
        # number of developers
        bug['NumberOfDevelopers'] = len(set(response.xpath('(//div[@class="bz_comment"]|//div[@class="bz_comment bz_first_comment"])//span[@class="fn"]/text()').extract()))
        # count number of patches
        numOfPatches = len(response.xpath('//tr[@class="bz_contenttype_text_plain bz_patch"]'))
        bug['NumberOfPatches'] = numOfPatches
        # actual patches
        bug['Patches'] = []
        # if no patches attached to this bug report, output json summary for that bug
        if numOfPatches == 0:
            yield bug
        else:
            # get the patch url, request that page to retrive lines of code information
            patchurl = response.xpath('//tr[@class="bz_contenttype_text_plain bz_patch"]')[0].xpath('td[@class="bz_attach_actions"]/a/@href').extract()[1]
            request = scrapy.Request(response.urljoin(patchurl), callback=self.parse_patch_content)
            request.meta['bug'] = bug
            request.meta['selectors'] = response.xpath('//tr[@class="bz_contenttype_text_plain bz_patch"]')
            yield request


    def parse_patch_content(self, response):
        bug = response.meta['bug']
        selectors = response.meta['selectors']
        patchSelector = selectors[0]
        patch = Patch()
        # patch title
        patch['PatchTitle'] = patchSelector.xpath('td/a/b/text()').extract()[0]
        # patch size
        sz = patchSelector.xpath('td/span[@class="bz_attach_extra_info"]/text()').extract()[0]
        patch['PatchSize'] = sz.split(',')[0].strip()[1:]
        # patch time
        patch['PatchTime'] = patchSelector.xpath('td/span[@class="bz_attach_extra_info"]/a/text()').extract()[0]
        # patch url
        patchurl = patchSelector.xpath('td[@class="bz_attach_actions"]/a/@href').extract()[1]
        patch['PatchUrl'] = patchurl
        # diff review url of that patch
        patch['DiffUrl'] = response.url
        # number of files changed in one patch
        patch['NumberOfFilesChanged'] = len(response.xpath('//table[@class="file_table"]'))
        files = []
        for fileSelector in response.xpath('//table[@class="file_table"]'):
            changedFile = File()
            fileSummary = fileSelector.xpath('thead//td[@class="file_head"]/text()').extract()[0]
            fileSummaries = fileSummary.replace(" ", "").split('\n')
            # changed file name
            changedFile['FileName'] = fileSummaries[0]
            numbers = fileSummaries[1].split(u'\xa0')
            # number of lines added/deleted
            for num in numbers:
                if '-' in num:
                    changedFile['Deleted'] = num[num.index('-') + 1:]
                if '+' in num:
                    changedFile['Added'] = num[num.index('+') + 1:]
            files.append(changedFile)
        # actual changes
        patch['Changes'] = files
        bug['Patches'].append(patch)
        # advance patch selector
        selectors = selectors[1:]
        if len(selectors) == 0: # if no more patches to process, output the bug report in json
            yield bug
        else: # process next patch
            patchurl = selectors[0].xpath('td[@class="bz_attach_actions"]/a/@href').extract()[1]
            request = scrapy.Request(response.urljoin(patchurl), callback=self.parse_patch_content)
            request.meta['bug'] = bug
            request.meta['selectors'] = selectors
            yield request

