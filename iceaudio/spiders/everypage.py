"""Module providingFunction printing python version."""
import scrapy

class IceSpider(scrapy.Spider):
    """hello"""

    name = "every_one"
    allowed_domains = ["iceaudio.no"]
    start_urls = ["https://www.iceaudio.no/?func=varer&VID=58"]

    def parse(self, response):
        new_product_anchor=response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        anchor = response.xpath("//div[@id='sub_content']//a/@href").getall()
        
        if new_product_anchor:
            if new_product_anchor is not None:
                yield from response.follow_all(new_product_anchor, callback=self.parse_product_scraping ,dont_filter = True)
        elif anchor:
            if anchor is not None:
                yield from response.follow_all(anchor, callback=self.parse_product )

    def parse_product(self, response):
        """by defualt Function"""
        anchor = response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        yield from response.follow_all(anchor, callback=self.parse_product_scraping ,dont_filter = True)

        pagination_links = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/@href').getall()
        if pagination_links is not None:
            yield from response.follow_all(pagination_links, self.parse_product)

    def parse_product_scraping(self, response):
        """by defualt Function"""
        img_1 = []
        img_2 = []
        img_3 = []
        img_4 = []
        img_5 = []
        img_6 = []
        img_7 = []
        img_8 = []
        img_9 = []
        img_10 = []
        img_11 = []
        img_12 = []
        img_13 = []
        img_14 = []
        img_15 = []
        img_16 = []
        img_17 = []

        images =  response.xpath("//div[@id='PInfo_Left']/img/@src").getall()
        for count in range(len(images)+1):
            if count == 1:
                img_1.append(images[0])

            elif count == 2:
                img_2.append(images[1])

            elif count == 3:
                img_3.append(images[2])

            elif count == 4:
                img_4.append(images[3])

            elif count == 5:
                img_5.append(images[4])

            elif count == 6:
                img_6.append(images[5])

            elif count == 7:
                img_7.append(images[6])

            elif count == 8:
                img_8.append(images[7])

            elif count == 9:
                img_9.append(images[8])

            elif count == 10:
                img_10.append(images[9])

            elif count == 11:
                img_11.append(images[10])

            elif count == 12:
                img_12.append(images[11])

            elif count == 13:
                img_13.append(images[12])

            elif count == 14:
                img_14.append(images[13])

            elif count == 15:
                img_15.append(images[14])

            elif count == 16:
                img_16.append(images[15])

            elif count == 17:
                img_17.append(images[16])
        yield{
                "product Id" : response.xpath("//div[@id='PInfo_Right']//tr[1]/td[@align='right']/text()").get(),
                "Main Category" : "",
                "Category 1" : "",
                "Category 2" : "",
                "Category 3" : "",
                "Category 4" : "",
                "Category 5" : "",
                "Brand" :"",
                "Product Name" : response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get(),
                "Product Information" : response.xpath("//div[@id='PInfo_Top']/text()").get(),
                "Car brand" : "",
                "Car model" : "",
                "Car year" : "",
                "Main Price" : response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get(),
                "Discount Price" : "",
                "Product Discription" :"".join(response.xpath("//div[@id='PInfo']//ul//li/text()").getall()) ,
                "picture 1" : ''.join(img_1),
                "picture 2" : ''.join(img_2),
                "picture 3" : ''.join(img_3),
                "picture 4" : ''.join(img_4),
                "picture 5" : ''.join(img_5),
                "picture 6" : ''.join(img_6),
                "picture 7" : ''.join(img_7),
                "picture 8" : ''.join(img_8),
                "picture 9" : ''.join(img_9),
                "picture 10" : ''.join(img_10),
                "picture 11" : ''.join(img_11),
                "picture 12" : ''.join(img_12),
                "picture 13" : ''.join(img_13),
                "picture 14" : ''.join(img_14),
                "picture 15" : ''.join(img_15),
                "picture 16" : ''.join(img_16),
                "picture 17" : ''.join(img_17),
                "source" : "www.iceaudio.no",
             }
