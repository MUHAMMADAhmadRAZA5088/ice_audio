"""Module providingFunction printing python version."""

import scrapy
import re
import os
import openai
import json

import pandas as pd
from langchain.llms import OpenAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.agents import create_csv_agent

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")


class IceSpider(scrapy.Spider):
    """This class performs the data scraping of IceAudio.no""" 

    name = "one"
    allowed_domains = ["iceaudio.no"]
    start_urls = ["https://www.iceaudio.no/index.php?func=varer&vnr=15271"]


    def parse(self, response):

        price=response.xpath("//div[@id='PInfo_Right']//tr[3]/td[@align='right']/text()").get()
        if price != None:
            web_data = "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())
            brand_csv = []
            final_model = []
            years = []
            
            if web_data: 
                
                df = pd.read_csv('E:\\f_scraper\\car_models.csv')

                brand_csv = []
                for brand in set(df['Brand']):
                    if brand in web_data:
                        brand_csv.append(brand)

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
        #-------------------------------------------------------------------
        # brand_csv = []
        # final_model = []
        # years = []
        # web_data = " ".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())
        # if web_data: 
        #     web_data = web_data.split()
        #     agent = create_csv_agent (OpenAI(temperature=0, max_tokens = 1000), 'E:\\f_scraper\\car_model.csv', verbose = True)
        #     df = pd.read_csv('E:\\f_scraper\\car_model.csv')

        #     brand_csv = []
        #     for brand in set(df['Brand']):
        #         if brand in web_data:
        #             brand_csv.append(brand)

        #     model_csv = []
        #     for model in set(df['Model']):
        #         if model in web_data:
        #             model_csv.append(model)
                    

        #     final_model = []

        #     if brand_csv and model_csv :
                
        #         for brands in brand_csv:
        #             brand_df = df[df["Brand"] == brands]
        #             inner_model = []

        #             for model_df in set(brand_df["Model"]):

        #                 for models in set(model_csv):
        #                     if models in model_df:
        #                         inner_model.append(models)
                    
        #             final_model.append(set(inner_model))

        #     years = []
         
        #     if brand_csv and final_model:

        #         for brand_index in range(0,len(brand_csv)) :
        #             brand_year = []
        #             for model in final_model[brand_index]:
                        
        #                 years_df = df[(df['Brand'] == brand_csv[brand_index]) & (df['Model'] == model )]

        #                 model_year = []
        #                 for year in set(years_df['Year']):
                            
        #                     for web_site_year in re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(response.xpath('//div[@id="PInfo"]//ul//text()').getall())):
        #                         if str(year) in str(web_site_year):
        #                             model_year.append(web_site_year)

        #                 brand_year.append(set(model_year))

        #             years.append(brand_year)



                        


        # yield {"URl":response.url,
        #         "Brand": brand_csv,
        #         "Model": final_model,
        #         "years": years,
        #         }