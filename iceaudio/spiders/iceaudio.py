"""Module providingFunction printing python version."""
import scrapy
import re
class IceSpider(scrapy.Spider):
    """hello"""
    name = "iceaudio"
    allowed_domains = ["iceaudio.no"]
    start_urls = ["https://www.iceaudio.no/"]

    def parse(self, response):
        anchor_text=response.xpath('//ul[@id="treemenu1"]/li/a/text()').getall()
        anchor=response.xpath('//ul[@id="treemenu1"]/li/a/@href').getall()
        
        for count in range(0,len(anchor)):
            yield  response.follow(anchor[count], callback=self.parse_product, meta={'Main_categories' : anchor_text[count]})

    def parse_product(self, response):

        new_product_anchor=response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        anchor = response.xpath("//div[@id='sub_content']//a/@href").getall()
        category_1=response.xpath("//div[@id='sub_content']//a/img/@alt").getall()
        if new_product_anchor:
            if new_product_anchor is not None:
                yield from response.follow_all(new_product_anchor, callback=self.parse_product_scraping ,dont_filter = True, meta={'Main_categories':response.meta.get('Main_categories')})

        elif anchor:
            for count in range(0,len(anchor)):
                yield  response.follow(anchor[count], callback=self.parse_product_item, meta={'Main_categories':response.meta.get('Main_categories'),'Category_1':category_1[count]})
    
    def parse_product_item(self, response):
        """by defualt Function"""
        anchor = response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        yield from response.follow_all(anchor, callback=self.parse_product_scraping ,dont_filter = True, meta={'Main_categories':response.meta.get('Main_categories'),'Category_1':response.meta.get('Category_1'),'Category_2':response.meta.get('Category_2')})

        pagination_links = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/@href').getall()
        category_2 = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/img/@alt').getall()
        if pagination_links is not None:
            for count in range(0,len(pagination_links)):
                yield  response.follow(pagination_links[count], callback=self.parse_product_item, meta={'Main_categories':response.meta.get('Main_categories'),'Category_1':response.meta.get('Category_1'),'Category_2':category_2[count]})
            


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

        com_brand=[ "Mercedes", "4 Connect", "5 Connect", "ACV", "ACX", "AH", "AI-SONIC", "Alpine","Antenne (DAB)","Antenne adapter","Antennepisk",  "Antennesplitter", "Asuka","Audio/Video interface","Audison","Aura","BLACKVUE","Blam","Blaupunkt","BOSS","Brax","Cadence","Caliber","CarAudioSystems","CDS","Cerwin Vega","Clarion","Comfort Modul","ConnectED","Connection","Connects2","Continental","Crunch","DAB integrering","DAB-antenne","DASHCAM","DD Audio","DEFA","Dension","ESX","Fiamm","Firefly","Focal","G4Audiio","Garmin","Ground Zero","Halo","Hardstone","Harman/Kardon","Helix","HELIX Q","Hertz","Hertz Marine","Hifonics","In2digi","JBL","Jensen","JL Audio","JVC","Kenwood","Kicker","Kram Telecom","Kufatec","Lukas","MAGNAT","Match","MB Quart","Metra","MTX Audio","MUSWAY","MOSCONI","Nextbase","NVX","PAC","Parrot","PhoenixGold","Pioneer","Polk Audio","Power","Prime","Punch","Pure","Pyle","QVIA","Renegade","Roberts","Rockford Fosgate","Sangean","Scosche","Sony","Sound Marine","Soundmagus","SoundQuest","Stinger","Strands","TARAMPS","Teleskopantenne","Tesla","TFT","AutoDAB","Toma Carparts","uniDAB","VCAN","Video in motion","Xplore","Gladen","4Connect","SounDigital","Blam","SoundQubed" ]
        heading= response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get()
        company_brand=""

        for brand in com_brand:

            if brand in heading:
                if brand:
                    company_brand=brand
                else:
                    company_brand=""

        description =  response.xpath('//div[@id="PInfo_Right"]/ul/li/text()').getall()
        data_specific=response.xpath('//div[@id="PInfo_Right"]/ul/li[3]//text()').get()
        data_condition=response.xpath('//div[@id="PInfo_Right"]/ul/li[1]//text()').get()
        years=[]
        Car_years=[]
        car_brand=[]
        """"""
        
        for web_count in description:
            for count in range(1985,2023):
                if str(count) in web_count:
                    years.append(web_count)
                    break
        
        for data in years:
            
            if ")" in data and "/" in data and len(data)<40 and 30<=len(data) and re.findall("[0-9]", data_specific) and len(data_specific)<40 :
                val=data.split(")")
                Car_years.append(val[1])
                car_val=data.rsplit(" ",4)
                car_brand.append(car_val[0])
            elif "/" in data and ">" in data and len(data)<40 and 30<=len(data) and re.findall("[0-9]", data_condition) and len(data_condition)<40 :
                val=data.split(" ",2)
                Car_years.append(val[2])
                car_val=data.rsplit(" ",4)
                car_brand.append(car_val[0])
            elif ">" in data and "-" in data and len(data)<30  and 15<=len(data) and (len(re.findall("-", data)))==1 and re.findall("[0-9]", data_specific) and  len(data_specific)<30:
                val=data.rsplit(" ",2)
                Car_years.append(val[1])
                car_brand.append(val[0])
  
        yield{
                "product Id" : response.xpath("//div[@id='PInfo_Right']//tr[1]/td[@align='right']/text()").get(),
                "Main Category" : response.meta.get('Main_categories'),
                "Category 1" : response.meta.get('Category_1'),
                "Category 2" : response.meta.get('Category_2'),
                "Category 3" : "",
                "Category 4" : "",
                "Category 5" : "",
                "Brand" :company_brand,
                "Product Name" : response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get(),
                "Product Information" : response.xpath("//div[@id='PInfo_Top']/text()").get(),
                "Car brand" : company_brand,
                "Car model" :"".join( car_brand),
                "Car year" : "".join(Car_years),
                "url":str(response),
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
               