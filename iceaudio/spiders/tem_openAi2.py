"""Module providingFunction printing python version."""
import scrapy
import re
import os
import pandas as pd
import openai
import json

# from langchain.llms import OpenAI
# from langchain.document_loaders.csv_loader import CSVLoader
# os.environ["OPENAI_API_KEY"]="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"
# openai.api_key = os.getenv("OPENAI_API_KEY")


class IceSpider(scrapy.Spider):
    """This class performs the data scraping of IceAudio.no"""
    name = "ai5"
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
            # number = re.findall("[0-9]", category[i])

            if category[i].isdigit() or category[i]=="6,5" or category[i]=="6x9" or category[i]=="5,25" or category[i]=="18 - 33":
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
                # number = re.findall("[0-9]", category[i])

                if category[i].isdigit() or category[i]=="6,5" or category[i]=="6x9" or category[i]=="5,25" or category[i]=="18 - 33":
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
        price=response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get()
        if price != None:
            web_data = "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())
            final_brand = []
            final_model = []
            final_years = []
            if web_data: 
                
                df = pd.read_csv('E:\\f_scraper\\car_models.csv')

                brand_csv = []
                for brand in set(df['Brand']):
                    if brand in web_data:
                        brand_csv.append(brand.strip())

                model_csv = []
                for model in set(df['Model']):
                    if model in web_data:
                        model_csv.append(model)
                
                model_csv  = [item for item in model_csv if len(item.strip()) > 0]
                years = re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall()))
                years = set(years)
                final_brand = []
                final_model = []
                final_years = []

                last_brand = []
                last_model = []
                last_years = []
                
                if  brand_csv and model_csv:
                    for brands in brand_csv: 
                        brand_df = df[df["Brand"] == brands]

                        for model_df in set(brand_df["Model"]):
                            
                            for models in set(model_csv):
                                if model_df == models:
                                    final_model.append(model_df)
                                    final_brand.append(brands)

                if brand_csv and final_model == []:
                    final_brand.extend(brand_csv)


                if years and  final_model:   
                    for count in range(0,len(final_brand)):
                        inner_year = [] 
                        csv_year = df[(df['Brand'] == final_brand[count]) & (df['Model'] == final_model[count] )]
                    
                        for  year in years:
                            for df_year in csv_year['Year']:
                                if str(df_year) == year:
                                    inner_year.append(year)
                        

                        inner_year  = [item for item in inner_year if len(item.strip()) > 0]
                        try:
                            for year in inner_year:
                                last_brand.append(final_brand[count])
                                last_model.append(final_model[count])
                                last_years.append(year)
                        except :
                            last_brand.append(final_brand[count])
                            last_model.append(final_model[count]) 
                            last_years.append('')

                if last_brand and last_model:
                    final_brand.clear()
                    final_model.clear()
                    final_years.clear()
                    final_brand.extend(last_brand)
                    final_model.extend(last_model)
                    final_years.extend(last_years)

                yield {
                    "Car Brand " :final_brand,
                    "Car Model" : final_model,
                    "Car years" : final_years,
                    "URL" : response.url
                }       

        
                