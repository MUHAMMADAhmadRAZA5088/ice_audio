"""Module providingFunction printing python version."""
import scrapy
import re


class IceSpider(scrapy.Spider):
    """This class performs the data scraping of IceAudio.no"""
    name = "iceaudio"
    allowed_domains = ["iceaudio.no"]
    start_urls = ["https://www.iceaudio.no/"]


    def parse(self, response):
        """Text is used to collect data (product name) for the main_category.
           anchors is used to collect all  link for the main categories.
           This function send the information to the parse_product.
          """
        text=response.xpath('//ul[@id="treemenu1"]/li/a/text()').getall()
        anchors=response.xpath('//ul[@id="treemenu1"]/li/a/@href').getall()
        for count in range(0,len(anchors)):
            yield  response.follow  (anchors[count], callback=self.parse_product,
                                     meta={'Main_categories' : text[count]}
                                    )


    def parse_product(self, response):
        """
        anchors is used to collect all  link for the Sub categories.
        products is used to collect all  product links"
        category_1 is used to collect data (product name) for the sub_category
        This function send the information to the parse_product_item and parse_product_scraping
        """
        products=response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        anchors = response.xpath("//div[@id='sub_content']//a/@href").getall()
        sub_category=[]
        category=response.xpath("//div[@id='sub_content']//a/img/@alt").getall()
        for i in range(0,len(category)):
            number = re.findall("[0-9]", category[i])

            if number:
                sub_category.append(category[i]+'"')
            else:
                sub_category.append(category[i])

        if products:
            if products is not None:
                yield from response.follow_all  (
                            products,
                            callback=self.parse_product_scraping ,
                            dont_filter = True,
                            meta={
                            'Main_categories':response.meta.get('Main_categories')}
                                                )

        elif anchors:
            for count in range(0,len(anchors)):
                yield  response.follow  ( 
                    anchors[count],
                    callback=self.parse_product_item, 
                    meta={
                        'Main_categories':response.meta.get('Main_categories'),
                        'Category_1':sub_category[count]
                        }
                                        )


    def parse_product_item(self, response):
        """
        anchors is used to collect all  link products.
        pagination_links is used to collect link for the Sub categories
        This function send the information to the  parse_product_scraping
        """
       
        anchors = response.xpath('//div[@id="container"]//div[@id="sub_content"]//tr[1]/td/a/@href').getall()
        yield from response.follow_all  ( 
            anchors,
            callback=self.parse_product_scraping ,
            dont_filter = True, 
            meta={
                'Main_categories':response.meta.get('Main_categories'),
                'Category_1':response.meta.get('Category_1'),
                'Category_2':response.meta.get('Category_2')
                }
                                        )

        pagination_links = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/@href').getall()
        category = response.xpath('//div[@id="container"]/div[@id="left"]/div[@id="sub_content"]/a/img/@alt').getall()
        sub_category=[]
        for i in range(0,len(category)):
            
            try:
                number = re.findall("[0-9]", category[i])

                if number:
                    sub_category.append(category[i]+'"')
                else:
                    sub_category.append(category[i])

            except Exception as ex:
               sub_category.append(category[i])

        if pagination_links is not None:
            for counter in range(0,len(pagination_links)):
                yield  response.follow  (
                        pagination_links[counter], 
                        callback=self.parse_product_item,
                        meta={
                            'Main_categories':response.meta.get('Main_categories'),
                            'Category_1':response.meta.get('Category_1'),
                            'Category_2':sub_category[counter]
                            }
                                        )
            

    def parse_product_scraping(self, response):
        """
        The function is to scrap the data.
        """
        price=response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get()
        if price != None:
            product_images=[]
            images =  response.xpath("//div[@id='PInfo_Left']/img/@src").getall()
            for count in range(0,17):
                try:
                    product_images.append(images[count])

                except Exception as ex: 
                    product_images.append("")

            brand_names=[ 
                    "4 Connect",
                    "5 Connect",
                    "4 Power",
                    "4POWER",
                    "4 Connect",
                    "ACV",
                    "ACX",
                    "AH",
                    "AI-SONIC",
                    "Alpine",
                    "Antenne (DAB)",
                    "Antenne adapter",
                    "Antennepisk",
                    "Antennesplitter",
                    "Asuka",
                    "Audio/Video interface",
                    "Audison",
                    "Aura",
                    "BLACKVUE",
                    "Blam",
                    "Blaupunkt",
                    "BOSS",
                    "Brax",
                    "Cadence",
                    "Caliber",
                    "CarAudio Systems",
                    "CDS",
                    "Cerwin Vega",
                    "Clarion",
                    "Comfort Modul",
                    "ConnectED",
                    "Connection",
                    "Connects2",
                    "Continental",
                    "Crunch",
                    "DAB integrering",
                    "DAB-antenne",
                    "DASHCAM",
                    "DD Audio",
                    "DEFA",
                    "Dension",
                    "ESX",
                    "Fiamm",
                    "Firefly",
                    "Focal",
                    "G4Audiio",
                    "Garmin",
                    "Ground Zero",
                    "Halo",
                    "Hardstone",
                    "Harman/Kardon",
                    "Helix",
                    "HELIX Q",
                    "Hertz",
                    "Hertz Marine",
                    "Hifonics",
                    "In2digi",
                    "JBL",
                    "Jensen",
                    "JL Audio",
                    "JVC",
                    "Kenwood",
                    "Kicker",
                    "Kram Telecom",
                    "Kufatec",
                    "Lukas",
                    "MAGNAT",
                    "Match",
                    "MB Quart",
                    "Metra",
                    "MTX Audio",
                    "MUSWAY",
                    "MOSCONI",
                    "Nextbase",
                    "NVX",
                    "PAC",
                    "Parrot",
                    "PhoenixGold",
                    "Pioneer",
                    "Polk Audio",
                    "Power",
                    "Prime",
                    "Punch",
                    "Pure",
                    "Pyle",
                    "QVIA",
                    "Renegade",
                    "Roberts",
                    "Rockford Fosgate",
                    "Sangean",
                    "Scosche",
                    "Sony",
                    "Sound Marine",
                    "Soundmagus",
                    "SoundQuest",
                    "Stinger",
                    "Strands",
                    "TARAMPS",
                    "Teleskopantenne",
                    "TFT",
                    "AutoDAB",
                    "Toma Carparts",
                    "uniDAB",
                    "VCAN",
                    "Video in motion",
                    "Xplore",
                    "Gladen",
                    "4Connect",
                    "SounDigital",
                    "Blam",
                    "SoundQubed",
                    "Diamond Audio",
                    "BLAM",
                    "DIRECTOR",
                    "FOUR Connect",
                    "GLADEN",
                    "PEXMAN",
                    "Boss",
                        ]
            
            heading= response.xpath("//div[@id='PInfo_Top']/h3/strong/text()").get()
            company_brand=""
            for brand in brand_names:
                try:
                    if brand.upper() in heading.upper():
                        if brand:
                            company_brand=brand
                            break
                except Exception as ex:
                    company_brand=""

            description =  response.xpath('//div[@id="PInfo_Right"]/ul/li/text()').getall()
            data_specific=response.xpath('//div[@id="PInfo_Right"]/ul/li[3]//text()').get()
            data_condition=response.xpath('//div[@id="PInfo_Right"]/ul/li[1]//text()').get()
            years=[]
            car_years=[]
            car_brand=[]
            try:
                for interger_value in description:
                    for i in range(1985,2023):
                        if str(i) in interger_value:
                            years.append(interger_value)
                            break
            
                for data in years:
                    
                    if ")" in data and "/" in data and len(data)<40 and 30<=len(data) and re.findall("[0-9]", data_specific) and len(data_specific)<40 :
                        value=data.split(")")
                        car_years.append(value[1])
                        car_information=data.rsplit(" ",4)
                        car_brand.append(car_information[0])
                    elif "/" in data and ">" in data and len(data)<40 and 30<=len(data) and re.findall("[0-9]", data_condition) and len(data_condition)<40 :
                        value=data.split(" ",2)
                        car_years.append(value[2])
                        car_information=data.rsplit(" ",4)
                        car_brand.append(car_information[0])
                    elif ">" in data and "-" in data and len(data)<30  and 15<=len(data) and (len(re.findall("-", data)))==1 and re.findall("[0-9]", data_specific) and  len(data_specific)<30:
                        value=data.rsplit(" ",2)
                        car_years.append(value[1])
                        car_brand.append(value[0])

            except Exception as ex:
                car_years.append("")
                car_brand.append("")

            response_obj = dict({
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
                    "Car year" : "".join(car_years),
                    "url":response.url,
                    "Main Price" : response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get(),
                    "Discount Price" : "",
                    "Product Discription" :"".join(response.xpath("//div[@id='PInfo']//ul//li/text()").getall()) ,
                    "source" : "www.iceaudio.no",
            })
            for i in range(1, 18):
                response_obj["Picture {}".format(i)] = product_images[i-1]

            yield response_obj
                