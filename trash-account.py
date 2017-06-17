import scrapy
import json


class TrashSpider(scrapy.Spider):
    name = "trash"
    start_urls = ["https://paytrefuse.grcity.us/payt/default.aspx"]

    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    def parse(self, response):
        name_field = "ctl00$ctl00$Content$MainContent$boxLogin$boxUserName"
        pass_field = "ctl00$ctl00$Content$MainContent$boxLogin$boxPassword"
        submit_field = "ctl00$ctl00$Content$MainContent$boxLogin$LoginButton"
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                name_field: self.username,
                pass_field: self.password,
                submit_field: 'Submit'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # check login
        invalid = b'was not successful'
        if invalid in response.body:
            self.logger.error("failure to login")
            return

        balance = response.xpath('//span[@id="Content_MainContent_boxAccountSummary_labelAccountBalance_LabelBalanceValue1"]/text()').extract()[0]
        trash_account = {"gr_payt_balance": balance}
        # write balance to database in the future. for now, a file will do.
        with open("gr-payt-account.json", 'w') as f:
            f.write(json.dumps(trash_account, sort_keys=True, indent=4, separators=(',', ': ')))

        return None
