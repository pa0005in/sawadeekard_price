# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 04:24:31 2023

@author: khin_
"""
#=========================================================================
#Version 1
#Created the base structure of the menu using OOP
#Created initial options for Japanese and English sets
#Inserted options for SV2a 151 for Japanese and S12a VSU for Japanese
#Succesfully imported SV2a 151 script to run
#=========================================================================
#Version 2
#Inserted SV2a_main script into current script
#Inserted options for SV6 twilight masquerade for English
#Inserted options for run all (to be finished)
#Inserted SV6 twilight masquerade for English into current script
#SV6 script includes automated feature to do the shopify csv and to create a changelog for prices
#=========================================================================
#Version 3
#Inserted SV5 temporal forces for English
#Changed TnT scraping method to account for multiple prices for a single card, always use first option
#Included self.name to reflect current set, so _main will not have to be updated
#=========================================================================
#Version 4
#Inserted self.csvexist for non-shopify modes (simplemerge will be given instead)
#Inserted csvexist query for user
#Inserted full set list of all 7 SV sets
#Inserted jp_151_main
#Updated xerates.com scraping
#=============
#To do
#SV0x for all set names
#3 digits format for card ID e.g. 001/1xx, 037/1xx
#Include check for last card for pokellector


import pandas as pd
import sys
import math
from datetime import datetime, timedelta
import os
import re
import requests
from bs4 import BeautifulSoup
#from Sawadeekard_151 import swdk_main
#from Yuyutei_151 import yyt_main
#import Japanese_151_price

#adding csv file reading 2 versions (singular and entire list)
def csvfile(setname):
    csvname = input(f"What is the csv file name for {setname}?")
    return csvname

def csvlist(setlist):
    namelist = []
    for setname in setlist:
        csvname = input(f"What is the csv file name for {setname}?")
        namelist.append(csvname)
    return namelist

#Set a custom exception to be raised when it is necessary to exit the application
class ExitException(Exception):
    pass

# SV5 imported
class SV5_english:
    def __init__(self,csvexist = False):
        print("SV05 Loading...")
        self.name = "SV5_English"
        self.csvexist = csvexist

    def swdk_sv5(self):
        newlist = []
        namelist = []
        IDlist = []

        for i in range(1, 16):  # page range
            url = "https://sawadeekard.com/collections/eng-scarlet-violet-sv05-temporal-forces" + "?page=" + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            data = soup.find_all("h3", class_="card__heading h5")

            for each in data:
                each = str(each)
                holder1 = re.split('>', each)
                holder2 = re.split('<', holder1[2].strip())
                newlist.append(holder2[0].strip())

        for i in range(len(newlist)):
            #     # newlist[i]=re.search(r"^([).*())$",newlist[i])
            newlist[i] = newlist[i].replace('\t', " ")
            newlist[i] = newlist[i].replace("[ENG] SV05 Temporal Forces: ", "")
            newlist[i] = newlist[i].strip()
            # holder = newlist[i].split(" [")
            # newlist[i] = holder[0]

        for i in range(len(newlist)):
            holder = newlist[i].split("/162 ")
            IDlist.append(holder[0] + "/162")
            namelist.append(holder[1])

        df_swdk = pd.DataFrame({"ID": IDlist, "Name": namelist})
        df_swdk.sort_values(["ID", "Name"], ascending=True, inplace=True)
        df_swdk.reset_index(drop=True, inplace=True)
        return (df_swdk)

    def tnt_sv5(self):
        pricelist = []
        namelist = []
        IDlist = []

        for i in range(1, 4):
            url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19895?Keywords=&page-no=' + str(
                i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                priceholder0 = re.split("col-2 text-center p-1", each)
                priceholder1 = re.split(">", priceholder0[3])
                priceholder2 = re.split("<", priceholder1[1])
                priceholder3 = priceholder2[0].replace("$", "")
                priceholder3 = priceholder3.strip()
                pricelist.append(float(priceholder3))
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                nameholder1 = re.split(">", each)
                nameholder2 = re.split("<", nameholder1[1])
                nameholder3 = re.split("- ", nameholder2[0])
                namelist.append(nameholder3[0].strip())
                IDlist.append(nameholder3[1].strip())
        df_sv5_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_sv5_rh.sort_values(["ID"], ascending=True, inplace=True)
        df_sv5_rh.reset_index(drop=True, inplace=True)

        pricelist = []
        namelist = []
        IDlist = []
        for i in range(1, 5):
            url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19897?Keywords=&page-no=' + str(
                i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                priceholder0 = re.split("col-2 text-center p-1", each)
                priceholder1 = re.split(">", priceholder0[3])
                priceholder2 = re.split("<", priceholder1[1])
                priceholder3 = priceholder2[0].replace("$", "")
                priceholder3 = priceholder3.strip()
                pricelist.append(float(priceholder3))
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                nameholder1 = re.split(">", each)
                nameholder2 = re.split("<", nameholder1[1])
                nameholder3 = re.split("- ", nameholder2[0])
                namelist.append(nameholder3[0].strip())
                IDlist.append(nameholder3[1].strip())
        df_sv5_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_sv5_singles.sort_values(["ID"], ascending=True, inplace=True)
        df_sv5_singles.reset_index(drop=True, inplace=True)
        return (df_sv5_rh, df_sv5_singles)

    def sv5_merge(self, df_swdk, df_rh, df_singles):
        df_merged = pd.DataFrame(columns=['ID', 'Name', 'Price in USD'])
        rh_counter = 0
        singles_counter = 0
        correctcounter = 0
        wrongcounter = 0
        wronglist = []
        rates = SV5_english().xe_rates()
        usdtosgd = float(rates)
        for i in range(len(df_swdk)):
            if re.search('Reverse Holo', df_swdk.iloc[i][1]):
                if re.search(df_singles.iloc[singles_counter - 1][1], df_swdk.iloc[i][1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter - 1][1])
                    wronglist.append(df_swdk.iloc[i][1])
                sgdvalue = df_rh.iloc[rh_counter][2] * usdtosgd
                if sgdvalue < 1:
                    sgdvalue = 1
                else:
                    sgdvalue = round(sgdvalue * 10) / 10
                new_row = {
                    'ID': df_swdk.iloc[i][0],
                    'Name': df_swdk.iloc[i][1],
                    'Price in USD': df_rh.iloc[rh_counter][2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                rh_counter += 1
            else:
                if re.search(df_singles.iloc[singles_counter][1], df_swdk.iloc[i][1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter][1])
                    wronglist.append(df_swdk.iloc[i][1])
                sgdvalue = df_singles.iloc[singles_counter][2] * usdtosgd
                if sgdvalue < 0.5:
                    sgdvalue = 0.5
                else:
                    sgdvalue = round(sgdvalue * 10) / 10
                new_row = {
                    'ID': df_swdk.iloc[i][0],
                    'Name': df_swdk.iloc[i][1],
                    'Price in USD': df_singles.iloc[singles_counter][2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                singles_counter += 1
        # print(f"The number of correct entries are {correctcounter} and the number of wrong entries are {wrongcounter}.")
        # print(wronglist)
        return (df_merged)

    def shopify_sv5(self, productcsv="products_export_1 (3).csv"):
        df_shopify = pd.read_csv(productcsv)
        df_shopify.sort_values(["Title"], ascending=True, inplace=True)
        df_shopify.reset_index(drop=True, inplace=True)
        return (df_shopify)

    def shopify_merge(self,df_swdk, df_shopify):
        df_changelog = pd.DataFrame(columns=['Before', 'Change', 'After'])
        # aftercheck = []
        for i in range(len(df_shopify)):
            holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
            new_row = {
                'Before': df_shopify.iloc[i][20],
                'Change': holder,
                'After': df_swdk.iloc[i][3]
            }
            new_row = pd.DataFrame(new_row, index=[0])
            df_changelog = pd.concat([df_changelog, new_row], ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
        #     aftercheck.append(holder)
        return (df_shopify, df_changelog)

    def xe_rates(self):
        # USD to SGD
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ratedata = soup.find_all('div', style='margin-top:24px')
        for each in ratedata:
            each = str(each)
            holder1 = re.split(">", each)
            holder21 = re.split("<", holder1[6])
            holder22 = re.split("<", holder1[7])
            rates = holder21[0] + holder22[0]
        return (rates)

    def sv5_main(self,filename=""):
        swdk_name = SV5_english().swdk_sv5()
        tnt_rh, tnt_singles = SV5_english().tnt_sv5()
        simplemerge = SV5_english().sv5_merge(swdk_name, tnt_rh, tnt_singles)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = SV5_english().shopify_sv5(filename)  # include error handling here
            finalmerge, changelog = SV5_english().shopify_merge(simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename, index=False)
            changelog.to_csv(f"Changelog {self.name}.csv", index=False)
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index = False)
        print(f"{self.name} completed")

#SV6 imported
class SV6_english:
    def __init__(self,csvexist = False):
        print("SV6 Loading...")
        self.name = "SV06_english"
        self.csvexist = csvexist
        
    def swdk_sv6(self):
        url = "https://sawadeekard.com/collections/eng-scarlet-violet-sv06-twilight-masquerade"
        newlist = []
        namelist = []
        IDlist = []

        for i in range(1, 17): #page range
            url = "https://sawadeekard.com/collections/eng-scarlet-violet-sv06-twilight-masquerade" + "?page=" + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            data = soup.find_all("h3", class_="card__heading h5")

            for each in data:
                each = str(each)
                holder1 = re.split('>',each)
                holder2 = re.split('<',holder1[2].strip())
                newlist.append(holder2[0].strip())

        for i in range(len(newlist)):
        #     # newlist[i]=re.search(r"^([).*())$",newlist[i])
            newlist[i] = newlist[i].replace('\t'," ")
            newlist[i] = newlist[i].replace("[ENG] SV06 Twilight Masquerade: ", "")
            newlist[i] = newlist[i].strip()
            # holder = newlist[i].split(" [")
            # newlist[i] = holder[0]

        for i in range(len(newlist)):
            holder = newlist[i].split("/167 ")
            IDlist.append(holder[0] + "/167")
            namelist.append(holder[1])

        df_swdk = pd.DataFrame({"ID": IDlist, "Name": namelist})
        df_swdk.sort_values(["ID","Name"], ascending=True, inplace=True)
        df_swdk.reset_index(drop = True,inplace=True)
        return (df_swdk)

    def tnt_sv6(self):
        pricelist = []
        namelist = []
        IDlist = []
        for i in range(1,4):
            url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-twilight-masquerade/19923?Keywords=&page-no=' + str(
                i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                priceholder0 = re.split("col-2 text-center p-1", each)
                priceholder1 = re.split(">", priceholder0[3])
                priceholder2 = re.split("<", priceholder1[1])
                priceholder3 = priceholder2[0].replace("$", "")
                priceholder3 = priceholder3.strip()
                pricelist.append(float(priceholder3))
            name = soup.find_all('a',class_="card-text")
            for each in name:
                each = str(each)
                nameholder1 = re.split(">",each)
                nameholder2 = re.split("<",nameholder1[1])
                nameholder3 = re.split("- ",nameholder2[0])
                namelist.append(nameholder3[0].strip())
                IDlist.append(nameholder3[1].strip())
        df_sv6_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_sv6_rh.sort_values(["ID"], ascending=True, inplace=True)
        df_sv6_rh.reset_index(drop = True,inplace=True)
        
        pricelist = []
        namelist = []
        IDlist = []
        for i in range(1,5):
            url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-twilight-masquerade/19925?Keywords=&page-no='+str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                priceholder0 = re.split("col-2 text-center p-1", each)
                priceholder1 = re.split(">", priceholder0[3])
                priceholder2 = re.split("<", priceholder1[1])
                priceholder3 = priceholder2[0].replace("$", "")
                priceholder3 = priceholder3.strip()
                pricelist.append(float(priceholder3))
            name = soup.find_all('a',class_="card-text")
            for each in name:
                each = str(each)
                nameholder1 = re.split(">",each)
                nameholder2 = re.split("<",nameholder1[1])
                nameholder3 = re.split("- ",nameholder2[0])
                namelist.append(nameholder3[0].strip())
                IDlist.append(nameholder3[1].strip())
        df_sv6_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_sv6_singles.sort_values(["ID"], ascending=True, inplace=True)
        df_sv6_singles.reset_index(drop = True,inplace=True)
        return(df_sv6_rh,df_sv6_singles)

    def sv6_merge(self,df_swdk,df_rh,df_singles):
        df_merged = pd.DataFrame(columns = ['ID','Name','Price in USD'])
        rh_counter = 0
        singles_counter = 0
        correctcounter = 0
        wrongcounter = 0
        wronglist = []
        rates = SV6_english().xe_rates()
        usdtosgd = float(rates)
        for i in range(len(df_swdk)):
            if re.search('Reverse Holo', df_swdk.iloc[i][1]):
                if re.search(df_singles.iloc[singles_counter-1][1],df_swdk.iloc[i][1]):
                   correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter-1][1])
                    wronglist.append(df_swdk.iloc[i][1])
                sgdvalue = df_rh.iloc[rh_counter][2] * usdtosgd
                if sgdvalue < 1:
                    sgdvalue = 1
                else:
                    sgdvalue = round(sgdvalue*10)/10
                new_row = {
                    'ID': df_swdk.iloc[i][0],
                    'Name': df_swdk.iloc[i][1],
                    'Price in USD': df_rh.iloc[rh_counter][2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row,index=[0])
                df_merged = pd.concat([df_merged,new_row], ignore_index=True)
                rh_counter += 1
            else:
                if re.search(df_singles.iloc[singles_counter][1],df_swdk.iloc[i][1]):
                   correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter][1])
                    wronglist.append(df_swdk.iloc[i][1])
                sgdvalue = df_singles.iloc[singles_counter][2] * usdtosgd
                if sgdvalue < 0.5:
                    sgdvalue = 0.5
                else:
                    sgdvalue = round(sgdvalue*10)/10
                new_row = {
                    'ID': df_swdk.iloc[i][0],
                    'Name': df_swdk.iloc[i][1],
                    'Price in USD': df_singles.iloc[singles_counter][2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row,index=[0])
                df_merged = pd.concat([df_merged,new_row], ignore_index=True)
                singles_counter += 1
        # print(f"The number of correct entries are {correctcounter} and the number of wrong entries are {wrongcounter}.")
        # print(wronglist)
        return(df_merged)

    def shopify_sv6(self,productcsv = "products_export_1 (3).csv" ):
        df_shopify = pd.read_csv(productcsv)
        df_shopify.sort_values(["Title"], ascending=True, inplace=True)
        df_shopify.reset_index(drop = True,inplace=True)
        return (df_shopify)

    def shopify_merge(self,df_swdk,df_shopify):
        df_changelog = pd.DataFrame(columns = ['Before','Change','After'])
        # aftercheck = []
        for i in range(len(df_shopify)):
            holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
            new_row = {
                'Before':df_shopify.iloc[i][20],
                'Change':holder,
                'After':df_swdk.iloc[i][3]
                }
            new_row = pd.DataFrame(new_row,index = [0])
            df_changelog = pd.concat([df_changelog,new_row],ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
        #     aftercheck.append(holder)
        return(df_shopify,df_changelog)

    def xe_rates(self):
        #USD to SGD
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        ratedata = soup.find_all('div', style='margin-top:24px')
        for each in ratedata:
            each = str(each)
            holder1 = re.split(">", each)
            holder21 = re.split("<", holder1[6])
            holder22 = re.split("<", holder1[7])
            rates = holder21[0] + holder22[0]
        return (rates)

    def sv6_main(self,filename = ""):
        print(f"Shopify file is {filename}.")
        swdk_name = SV6_english().swdk_sv6()
        tnt_rh,tnt_singles = SV6_english().tnt_sv6()
        simplemerge = SV6_english().sv6_merge(swdk_name, tnt_rh, tnt_singles)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = SV6_english().shopify_sv6(filename) #include error handling here
            finalmerge,changelog = SV6_english().shopify_merge(simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename,index=False)
            changelog.to_csv(f"Changelog {self.name}.csv",index = False)
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index = False)
        print(f"{self.name} completed")

class SV2a_Japanese():
    def __init__(self, csvexist = False):
        print("SV2a Loading...")
        self.name = "SV2a_Japanese"
        self.csvexist = csvexist

    #from Sawadeekard_151
    def swdk_main(self):
        url = "https://sawadeekard.com/collections/jap-pokemon-151"
        newlist = []
        namelist = []
        IDlist = []

        for i in range(1, 23):
            if i == 1:
                url = "https://sawadeekard.com/collections/jap-pokemon-151"
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                data = soup.find_all("h3", class_="card__heading h5")

                # print (data)
                for each in data:
                    newlist.append(str(each))
            else:
                url = "https://sawadeekard.com/collections/jap-pokemon-151" + "?page=" + str(i)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')

                data = soup.find_all("h3", class_="card__heading h5")

                # print (data)
                for each in data:
                    newlist.append(str(each))

        for i in range(len(newlist)):
            # newlist[i]=re.search(r"^([).*())$",newlist[i])
            newlist[i] = str(re.findall(r"\[.*\)", newlist[i]))

        for i in range(len(newlist)):
            a = newlist[i]
            IDlist.append(a[18:25])
            # namelist.append(a[26:-2])
            namelist.append(a[2:-2])

        df_swdk = pd.DataFrame({"ID": IDlist, "Name": namelist})
        df_swdk.sort_values("ID", ascending=True, inplace=True)
        return df_swdk
    #from yuyutei_151
    def yyt_main(self):
        page = requests.get("https://yuyu-tei.jp/sell/poc/s/sv02a")
        soup = BeautifulSoup(page.content, "html.parser")

        # page2 = requests.get("https://jp.pokellector.com/Pokemon-151-Expansion/")
        # soup2 = BeautifulSoup(page2.content,"html.parser")

        # ggwp = soup2.find_all("div",class_="plaque")
        # for each in ggwp:
        #     print (each)

        # print(soup.find_all('h4','strong','span'))
        ID = soup.find_all('span', class_="d-block border border-dark p-1 w-100 text-center my-2")
        name = soup.find_all('h4', class_="text-primary fw-bold")
        price = soup.find_all('strong', class_=re.compile('^d-block text-end'))

        ID_str = []
        name_str = []
        price_1 = []
        price_str = []

        for each in ID:
            ID_str.append(str(each))

        for each in name:
            name_str.append(str(each))

        for each in price:
            price_1.append(str(each))

        for i in range(len(ID_str)):
            ID_str[i] = ID_str[i].replace('<span class="d-block border border-dark p-1 w-100 text-center my-2">', '')
            ID_str[i] = ID_str[i].replace('</span>', '')
            price_1[i] = price_1[i].replace('<strong class="d-block text-end">', '')
            price_1[i] = price_1[i].replace('<strong class="d-block text-end text-danger">', '')
            price_1[i] = price_1[i].replace('</strong>', '')
            price_1[i] = price_1[i].replace('円', '')
            price_1[i] = price_1[i].replace(',', '')
            name_str[i] = name_str[i].replace('<h4 class="text-primary fw-bold">', '')
            name_str[i] = name_str[i].replace('</h4>', '')
            name_str[i] = name_str[i].strip()
            price_str.append(int(price_1[i].strip()))

        # dttm = datetime.datetime.now()
        # filename = f"Japanese 151 {dttm.strftime('%y%m%d')}.csv"

        df_yyt = pd.DataFrame({"ID": ID_str, "Name": name_str, "Price in Yen": price_str})
        df_yyt.sort_values(["ID", "Price in Yen"], ascending=True, inplace=True)
        df_yyt.reset_index(drop=True, inplace=True)
        # df_yyt.to_csv(filename,index=False)
        return df_yyt

    #from Japanese_151_price
    def namechk(self,string, df):
        chk = string
        strvar = ''
        for each in range(len(df.index)):
            strhold = df.loc[each]['Name']
            if re.findall(chk, strhold):
                strvar = strhold
        return strvar

    def jp_151_merge(self,df_swdk,df_yyt):
        #df_swdk = SV2a_Japanese().swdk_main()
        #df_yyt = SV2a_Japanese().yyt_main()
        rates = SV2a_Japanese().xe_rates()
        jpytosgd = float(rates)

        df_final = pd.DataFrame(columns=['ID', 'Name', 'Price'])
        # df_yyt.Name = df_swdk[df_swdk.ID==df_yyt.iloc[5][0]].Name
        for i in range(len(df_yyt.index)):
            # df_yyt.Name = df_swdk[df_swdk.ID==df_yyt.iloc[5][0]].Name
            if (len(df_swdk[df_swdk.ID == df_yyt.iloc[i][0]].index) > 1):
                df_swdk_hold = df_swdk[df_swdk.ID == df_yyt.iloc[i][0]].reset_index(drop=True)
                df_yyt_hold = df_yyt[df_yyt.ID == df_yyt.iloc[i][0]].reset_index(drop=True)
                sgdvalue = round(df_yyt.loc[i]['Price in Yen']*10)/10
                if re.search(r".*マスターボール柄.*", df_yyt.loc[i]['Name']):
                    namestr = namechk(r".*Master Ball.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.loc[i]['ID'],
                        'Name': namestr,
                        'Price in JPY': df_yyt.loc[i]['Price in Yen'],
                        'Price in SGD': sgdvalue
                    }
                elif re.search(r".*モンスターボール柄.*", df_yyt.loc[i]['Name']):
                    namestr = namechk(r".*Reverse Holo.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.loc[i]['ID'],
                        'Name': namestr,
                        'Price in JPY': df_yyt.loc[i]['Price in Yen'],
                        'Price in SGD': sgdvalue
                    }
                else:
                    namestr = namechk(r".*Foil.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.loc[i]['ID'],
                        'Name': namestr,
                        'Price in JPY': df_yyt.loc[i]['Price in Yen'],
                        'Price in SGD': sgdvalue
                    }
            elif (len(df_swdk[df_swdk.ID == df_yyt.iloc[i][0]].index) == 1):
                new_row = {
                    'ID': df_yyt.loc[i]['ID'],
                    'Name': df_swdk.loc[i]['Name'],
                    'Price in JPY': df_yyt.loc[i]['Price in Yen'],
                    'Price in SGD': sgdvalue
                }
            new_row = pd.DataFrame(new_row, index=[0])
            df_final = pd.concat([df_final, new_row], ignore_index=True)

        #    directory="\data\Japanese_151"
        #    if not os.path.exists(directory):
        #        os.makedirs(directory)
        return (df_final)

    def shopify_sv2a(self,productcsv = "products_export_1 (3).csv" ):
        df_shopify = pd.read_csv(productcsv)
        df_shopify.sort_values(["Title"], ascending=True, inplace=True)
        df_shopify.reset_index(drop = True,inplace=True)
        return (df_shopify)

    def shopify_merge(self,df_swdk,df_shopify):
        df_changelog = pd.DataFrame(columns = ['Before','Change','After'])
        # aftercheck = []
        for i in range(len(df_shopify)):
            holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
            new_row = {
                'Before':df_shopify.iloc[i][20],
                'Change':holder,
                'After':df_swdk.iloc[i][3]
                }
            new_row = pd.DataFrame(new_row,index = [0])
            df_changelog = pd.concat([df_changelog,new_row],ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i][3] - df_shopify.iloc[i][20]
        #     aftercheck.append(holder)
        return(df_shopify,df_changelog)
    def xe_rates(self):
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=JPY&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ratedata = soup.find_all('div', style='margin-top:24px')
        for each in ratedata:
            each = str(each)
            holder1 = re.split(">", each)
            holder21 = re.split("<", holder1[6])
            holder22 = re.split("<", holder1[7])
            rates = holder21[0] + holder22[0]
        return (rates)
    def jp_151_main(self,filename = ""):
        swdk_name = SV2a_Japanese().swdk_main()
        yyt_list = SV2a_Japanese().yyt_main()
        simplemerge = SV2a_Japanese().jp_151_merge(swdk_name, yyt_list)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = SV2a_Japanese().shopify_sv6(filename) #include error handling here
            finalmerge,changelog = SV2a_Japanese.shopify_merge(simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename,index=False)
            changelog.to_csv(f"Changelog {self.name}.csv",index = False)
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index = False)
        print(f"{self.name} completed")
class controller:
    def __init__(self):
        print('\n===========================================')
        print('              Price list')
        print('============================================')
        
    # Set a function that checks if user input is "exit" every time, in order to allow the user to exiy the system anywhere
    def exit_check(self,prompt):
        user_input=input(prompt)
        if user_input.lower()=='exit':
            print("System terminated. Thank you!")
            raise ExitException()
        return user_input
    
    def main(self):
        #menu options
        while True:
            #Split by language, Japanese cards will use YYT, English cards are undecided
            print("1. Japanese Pokemon Cards")
            print("2. English Pokemon Cards")
            print("X. Exit\n")
            
            #choice obtained using input
            choice = input("What type of cards? \n")
            choice = choice.strip()
            
            #option 1 will be Japanese YYT
            if choice == '1':
                try:
                    while True:
                        print("1. 151 Pokémon")
                        print("2. V Star Universe")
                        print("X. Exit\n")
                        
                        choice = input("What set are you interested in? \n")
                        choice = choice.strip()
                        if choice == '1':
                            Japanese_151_price.jp_151_main()
                            dttm = datetime.now()
                            df = pd.read_csv(f"Japanese 151 {dttm.strftime('%y%m%d')}.csv")
                            print(df)
                        elif choice.lower() == 'x':
                            break
                except ExitException():
                    sys.exit()
            elif choice == '2':
                try:
                    csvdict = {}
                    setdict = {
                        'SV6': "SV06 Twilight Masquerade",
                        'SV5': "SV05 Temporal Forces"}
                        #'SV4': "SV04 Paldean Fates",
                        #'SV3.5': "SV3.5 Scarlet Violet 151",
                        #'SV3': "SV03 Paradox Rift",
                        #'SV2': "SV02 Paldea Evolved",
                        #'SV1': "SV01 Scarlet & Violet Base set"
                    #} #manual include set names
                    objdict ={}

                    while True:
                        #options are included manually, but will just be setlist[i]
                        print(f"1. {setdict['SV6']}")
                        print("00. All listed series")
                        print("X. Exit\n")
                        #To know which set to scrape
                        choice = input("What set are you interested in? \n")
                        choice = choice.strip()
                        choiceflag = False
                        #To check if shopify csv file exists
                        while choiceflag == False:
                            shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                            if shpfychoice.upper() == "Y" or shpfychoice.upper() == "YES" or shpfychoice.upper() == "YE" or re.match("YES", shpfychoice.upper()):
                                csvexist = True
                                print(f"The option is {csvexist}.")
                                print("Final CSV file is ready for Shopify upload.")
                                choiceflag = True
                            elif shpfychoice.upper() == "N" or shpfychoice.upper() == "NO" or re.match("NO", shpfychoice.upper()):
                                csvexist = False
                                print(f"The option is {csvexist}.")
                                print("Final CSV file is cannot be uploaded.")
                                choiceflag = True
                            else:
                                print("UNACCEPTABLE INPUT!\n")
                        if choice == '1':
                            csvdict['SV6'] = 'products_export_1 (3).csv'
                            sv6obj = SV6_english(csvexist=csvexist)
                            sv6obj.sv6_main(filename = csvdict['SV6'])
                            dttm = datetime.now()
                            #df = pd.read_csv(f"SV6 Shopify English {dttm.strftime('%y%m%d')}.csv")
                            #print(df)
                        elif choice == "00":
                            if csvexist:
                                for each in setdict:
                                    print("Please copy the file name directly, but .csv is not needed.")
                                    print("E.g. products_export_1 (3).csv just write 'products_export_1 (3)'\n")
                                    csvholder = input(f"What is the csv file name for {setdict[each]}: ")
                                    csvholder = csvholder + ".csv"
                                    csvdict[each]=csvholder
                                    print(csvdict[each])
                            else:
                                SV6obj = SV6_english(csvexist)
                                SV6obj.sv6_main()
                                SV5obj = SV5_english(csvexist)
                                SV5obj.sv5_main()
                                print("All sets are processed.")
                        elif choice.lower() == 'x':
                            break
                except ExitException():
                    sys.exit()
            elif choice.lower() == 'x':
                break

if __name__ == "__main__":
    a = controller()
    a.main()