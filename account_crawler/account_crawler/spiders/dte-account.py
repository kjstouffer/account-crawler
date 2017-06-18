import scrapy
import json


class TrashSpider(scrapy.Spider):
    name = "dte"
    start_urls = ["https://www.newlook.dteenergy.com/wps/wcm/connect/dte-web/home"]

    def __init__(self, username="", password=""):
        self.username = username
        self.password = password

    def parse(self, response):
        name_field = "username"
        pass_field = "password"
        body = json.dumps({name_field: self.username, pass_field: self.password})
        self.logger.error(body)
        return scrapy.Request(
            url="https://www.newlook.dteenergy.com/api/signIn",
            method="POST",
            body=body,
            callback=self.after_login
        )

    def after_login(self, response):
        self.logger.error("!!!")
        #400 is ignored, so we can assume safety here
        return scrapy.Request(
                url="https://www.newlook.dteenergy.com/wps/wcm/connect/dte-web/home/billing-and-payments/residential/billing/current-bill",
                headers={"Cookie": response.headers['SET-COOKIE']},
                callback=self.after_after_login
            )

    def after_after_login(self, response):
        self.logger.error(response.body)
        balance = response.xpath('//h1[@class="leftnav_price dte-michigan"]/text()').extract()[0]
        dte_account = {"dte_balance": balance}
        # write balance to database in the future. for now, a file will do.
        with open("dte_balance.json", 'w') as f:
            f.write(json.dumps(dte_account, sort_keys=True, indent=4, separators=(',', ': ')))

        return None
