"""Module providingFunction printing python version."""
import scrapy
import re
import os
import pandas as pd
import openai
import json

from langchain.llms import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
os.environ["OPENAI_API_KEY"]="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"
openai.api_key = os.getenv("OPENAI_API_KEY")


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
                # if len(brand_csv) > 1 and model_csv and len(years) < 2 :
                    
                #     for brands in brand_csv:
                #         brand_df = df[df["Brand"] == brands]
                #         inner_model = []

                #         for model_df in set(brand_df["Model"]):

                #             for models in set(model_csv):
                #                 if models in model_df:
                #                     inner_model.append(models)
                #         if inner_model:
                #             final_model.append(set(inner_model))
                #         else:
                #             final_model.append(set(' '))
                    
                            
                # years = re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall()))
                

                # years = []
            
                # if brand_csv and final_model:

                #     for brand_index in range(0,len(brand_csv)) :
                #         brand_year = []
                #         for model in final_model[brand_index]:
                            
                #             years_df = df[(df['Brand'] == brand_csv[brand_index]) & (df['Model'] == model )]

                #             model_year = []
                #             for year in set(years_df['Year']):
                                
                #                 for web_site_year in re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())):
                #                     if str(year) in str(web_site_year):
                #                         model_year.append(web_site_year)

                #             if  model_year:
                #                 brand_year.append(set(model_year))
                #         if brand_year:
                #             years.append(brand_year)

        # df = pd.read_csv("E:\\openai\\car_model.csv",encoding='utf-8')
        # web_data = " ".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())
        # data=["""niche dya gy text mein se Car Brand,Car Model aur Car Year nikalo.agr Car Brand,Car Model ,Car Year nahi milta tu empty json return kro python ki otherwise mjy json m data  aur complete data do please. json ko complete close kro.ap }] close krta wqt nahi lga .ap mujhy df wala brand do Answer mein bs""", ]
        # for text in data:
        #     if web_data:
        #         text_1 = f"us  dataframe {df} mein se data read kro us mein se answer answer do."
        #         # text="""
        #         # niche dya gy text mein se Car Brand,Car Model aur Car Year nikalo.agr Car Brand,Car Model ,Car Year nahi milta tu empty json return kro python ki otherwise mjy json m data  aur complete data do please. json ko complete close kro.ap }] close krta wqt nahi lga .ap mujhy df wala brand do Answer mein bs     
                
        #         # """

        #         text = text_1+text+web_data
        #         text.format
        #         text=text.strip()
        #         llms=OpenAI(temperature = 0, max_tokens = 2000)
        #         filter_data=llms(f""" {text}  """)

        #         def extract_dicts(input_string):
        #             dictionaries = []
        #             start = 0
                    
        #             while start < len(input_string):
        #                 # Find the index of the first opening curly brace '{'
        #                 opening_brace = input_string.find('{', start)
        #                 if opening_brace == -1:
        #                     break
                        
        #                 # Find the index of the corresponding closing curly brace '}'
        #                 closing_brace = input_string.find('}', opening_brace)
        #                 if closing_brace == -1:
        #                     break
                        
        #                 # Extract the substring containing the dictionary
        #                 dictionary_string = input_string[opening_brace:closing_brace+1]
        #                 try:
        #                     dictionary = json.loads(dictionary_string)
        #                     dictionaries.append(dictionary)
        #                 except json.JSONDecodeError:
        #                     pass
                        
        #                 start = closing_brace + 1
                    
        #             return dictionaries
                
        #         filter_data = extract_dicts(filter_data)
        #         if filter_data == [{}] or filter_data == [] or filter_data == [{"data": [], "complete_data": []}]:
        #             filter_data = [{'Car Brand': '', 'Car Model': '', 'Car Year': ''}]
            
        #     else:
        #         filter_data = [{'Car Brand': '', 'Car Model': '', 'Car Year': ''}]

        # try:
        #     car_brands = [item['Car Brand'] for item in filter_data]
        #     car_models = [item['Car Model'] for item in filter_data]
        #     car_years = [item['Car Year'] for item in filter_data]
        # except:
        #     car_brands = [item['Brand'] for item in filter_data]
        #     car_models = [item['Model'] for item in filter_data]
        #     car_years = [item['Year'] for item in filter_data]
        
        # if car_brands == [[]]:
        #     car_brands = [""]

        # if car_models == [[]]:
        #     car_models = [""]

        # if car_years == [[]]:
        #     car_years = [""]

        # csv_brand = []
        # csv_model = []

        # Brand=set(df['brand'])
        
        # Model=set(df['Model'])
        # years = set(df['years'])

        # if car_brands or car_models or car_years:
        #     for api_brand in car_brands:
        #         for brand in Brand:
        #             if brand.lower() in api_brand.lower():
        #                 pass
        
        #     for api_model in car_models:
        #         for model in Model:
        #             if model.lower() in api_model.lower():
        #                 pass
            
        #     for api_years in car_years:
        #         for model in Model:
        #             if model.lower() in api_years.lower():
        #                 pass
            
        # if car_brands or car_models:
        #     for api_brand in car_brands:
        #         for brand in Brand:
        #             if brand.lower() in api_brand.lower():
        #                 csv_brand.append(brand)

        #     for api_model in car_models:
        #         for model in Model:
        #             if model.lower() in api_model.lower():
        #                 csv_model.append(model)

             

        
        # yield {
        #     "Car Brand " : car_brands,
        #     "Car Model" : car_models,
        #     "Car Years" : car_years,
        # }
        # agent = create_csv_agent (OpenAI(temperature=0, max_tokens = 1000), 'E:\\f_scraper\\car_model.csv', verbose = True)
        #         # print(agent)
        #         # print(agent.agent.llm_chain.prompt.template)
        #         agent = agent.run(f"""Find the Brand, Model and Year from the below text and answer into json form.if not find  Brand, Model and Year then return empty json from . please json close properly .
                                
        #         {web_data}
        #                         """)
        #         print(agent)
        #         print(type(agent))
        #         agent = json.loads(agent)
        #         yield {"data" : agent}

        #-------------------------------------------------------------------
        # web_data = " ".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())
        # if web_data:
        #     text="""
        #     us  dataframe {df} mein se data read kro us k mutabik answer do.

        #     niche dya gy text mein se Car Brand,Car Model aur Car Year nikalo.agr Car Brand,Car Model ,Car Year nahi milta tu empty json return kro python ki otherwise mjy json m data  aur complete data do please. json ko complete close kro.ap }] close krta wqt nahi lga raha and Answer nah show kro output pr.       


        #     """
        #     text=text+web_data
        #     text.format
        #     text=text.strip()
        #     llms=OpenAI(temperature=0,max_tokens=2000)
        #     filter_data=llms(f""" {text}  """)
        #     filter_data=filter_data.replace("Answer:","")
        #     print(type(filter_data))
        #     print(filter)
        #     filter_data=json.loads(filter_data)
        #     print(bool(filter_data))
        #     if bool(filter_data) == False:
        #         filter_data = [{'Car Brand': '', 'Car Model': '', 'Car Year': ''}]
        #     print(type(filter_data))
        #     print(bool(filter_data))

        #     yield filter_data 

        # else:
        #     filter_data = {'Car Brand': '', 'Car Model': '', 'Car Year': ''}
        #     yield filter_data
        
                