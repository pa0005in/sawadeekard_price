# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 04:24:31 2023

@author: khin_
"""
#=========================================================================
#To resolve from Version 1.4:
#SV02: inventory audit so price cannot be extracted
#Try check for price, exception made when price not found
#SV04: remove duplicated card in df_swdk
#==========================================================================
#Version 2.0
#inheritance to make code neater
#Resolved: SV02 non-price issue
#Resolved: SV04 duplicate issue
#==========================================================================
#Version 2.1
#Removed repeated codes for SV01-SV06
#Able to work with Shopify CSV files
#Tidied up dictionary lists for main menu
#Issue: Sawadeekard website having slightly different formatting
#To be added: SV6.5 (currently unavailable at 30 Jul 2024)
#To be added: Other previous series (Sun & Moon, Sword and Shield)
#To be added: Menu options/updates with the new neater code
#Considering: Inserting the urls and pages as dataframe to collate
#===========================================================================
#Version 2.2
#Resolved Website formatting issue due to missing picture
#Added error checks to inform user of errors in CSV file and website
#Removed csvfile functions (using fixed file names)
#updated all iloc to be .iloc[x,y] from .iloc[x][y]
#===========================================================================
#Version 2.3
#Updated Japanese set codes
#--changed jpy to sgd rates to be from 1000:1
#--changed all column reference to iloc with more confidence of shopify csv structure
#--added the conversion variable multiplier
#Adjusted initial menu for SV series, SWSH series and Japanese instead of English and Japanese
#Bugfix for xe_rates
#--css was changed, new method used re.search for specific keyword instead
# added SV6.5 and SV07 for tnt webpages



import pandas as pd
import sys
import math
import numpy as np
from datetime import datetime, timedelta
import os
import re
import requests
from bs4 import BeautifulSoup

#Set a custom exception to be raised when it is necessary to exit the application
class ExitException(Exception):
    pass

#yes/no checking for user inputs
def yesnochk(shpfychoice,choiceflag):
    if shpfychoice.upper() == "Y" or shpfychoice.upper() == "YES" or shpfychoice.upper() == "YE" or re.match("YES", shpfychoice.upper()):
        csvexist = True
        print(f"The option is {csvexist}.")
        print("Final CSV file is ready for Shopify upload.")
        choiceflag = True
    elif shpfychoice.upper() == "N" or shpfychoice.upper() == "NO" or re.match("NO", shpfychoice.upper()):
        csvexist = False
        print(f"The option is {csvexist}.")
        print("Final CSV file cannot be uploaded.")
        choiceflag = True
    else:
        print("UNACCEPTABLE INPUT!\n")
    return(csvexist, choiceflag)

### English Sets
## Scarlet Violet code
#Url for swdk website
swdkurl = {
    "SV01": "https://sawadeekard.com/collections/eng-sv01-scarlet-violet-base-set",
    "SV02": "https://sawadeekard.com/collections/eng-scarlet-violet-paldea-evolved",
    "SV03": "https://sawadeekard.com/collections/eng-scarlet-violet-sv03-obsidian-flames",
    "SV3.5": "https://sawadeekard.com/collections/eng-scarlet-violet-sv3-5-pokemon-151",
    "SV04": "https://sawadeekard.com/collections/eng-scarlet-violet-sv04-paradox-rift",
    "SV4.5": "https://sawadeekard.com/collections/eng-scarlet-violet-sv4-5-paldean-fates",
    "SV05": "https://sawadeekard.com/collections/eng-scarlet-violet-sv05-temporal-forces",
    "SV06": "https://sawadeekard.com/collections/eng-scarlet-violet-sv06-twilight-masquerade",
    "SV6.5": "",
    "SV07": "",
    "SWSH12.5": "https://sawadeekard.com/collections/eng-swsh-12-5-crown-zenith"
}

#Last page for swdk website
swdkurl_page = {
    "SV01": 20,
    "SV02": 20,
    "SV03": 18,
    "SV3.5": 17,
    "SV04": 19,
    "SV4.5": 15,
    "SV05": 16,
    "SV06": 17,
    "SV6.5": "",
    "SV07": "",
    "SWSH12.5": 16
}

#Name to replace for sawadeekard website
setnamereplace = {
    "SV01": "[ENG] SV01 Scarlet Violet Base Set: ",
    "SV02": "[ENG] SV02 Paldea Evolved: ",
    "SV03": "[ENG] SV03 Obsidian Flames: ",
    "SV3.5": "[ENG] SV3.5 151: ",
    "SV04": "[ENG] SV04 Paradox Rift: ",
    "SV4.5": "[ENG] Pokemon SV4.5 Paldean Fates: ",
    "SV05": "[ENG] SV05 Temporal Forces: ",
    "SV06": "[ENG] SV06 Twilight Masquerade: ",
    "SV6.5": "[ENG] SV6.5 Shrouded Fable: ",
    "SV07": "[ENG] SV07 Stellar Crown",
    "SWSH12.5": "[ENG] SWSH12 Crown Zenith: ",
}

#set size of each set
setsize = {
    "SV01": "198",
    "SV02": "193",
    "SV03": "197",
    "SV3.5": "165",
    "SV04": "182",
    "SV4.5": "091",
    "SV05": "162",
    "SV06": "167",
    "SV6.5": "064",
    "SV07": "142",
    "SWSH12.5": "159",
    "SWSH12.5GG": "GG70",
}

#Url for tntrh website
tntrh = {
    "SV01": "https://www.trollandtoad.com/pokemon/scarlet-violet-base-set-reverse-holo-singles/19465",
    "SV02": "https://www.trollandtoad.com/pokemon/scarlet-violet-paldea-evolved/19616",
    "SV03": "https://www.trollandtoad.com/obsidian-flames-reverse-holo-singles/19670",
    "SV3.5": "https://www.trollandtoad.com/pokemon/scarlet-violet-151/19702",
    "SV04": "https://www.trollandtoad.com/pokemon/scarlet-violet-paradox-rift/19725",
    "SV4.5": "https://www.trollandtoad.com/pokemon/paldean-fates/19795",
    "SV05": "https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19895",
    "SV06": "https://www.trollandtoad.com/pokemon/scarlet-violet-twilight-masquerade/19923",
    "SV6.5": "https://www.trollandtoad.com/shrouded-fable-singles/19996",
    "SV07": "https://www.trollandtoad.com/scarlet-violet-stellar-crown-singles/20019",
    "SWSH12.5" : "https://www.trollandtoad.com/crown-zenith-singles/19428"
}

#Last page for tntrh website
tntrh_page = {
    "SV01": 5,
    "SV02": 4,
    "SV03": 4,
    "SV3.5": 4,
    "SV04": 4,
    "SV4.5": 3,
    "SV05": 4,
    "SV06": 4,
    "SV6.5": 3,
    "SV07": 4,
    "SWSH12.5": 3
}

#Url for tntsingles website
tntsingles = {
    "SV01": "https://www.trollandtoad.com/pokemon/scarlet-violet-base-set-reverse-holo-singles/19467",
    "SV02": "https://www.trollandtoad.com/pokemon/scarlet-violet-paldea-evolved/19618",
    "SV03": "https://www.trollandtoad.com/pokemon/scarlet-violet-obsidian-flame/19669",
    "SV3.5": "https://www.trollandtoad.com/pokemon/scarlet-violet-151/19701",
    "SV04": "https://www.trollandtoad.com/pokemon/scarlet-violet-paradox-rift/19726",
    "SV4.5": "https://www.trollandtoad.com/pokemon/paldean-fates/19797",
    "SV05": "https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19897",
    "SV06": "https://www.trollandtoad.com/pokemon/scarlet-violet-twilight-masquerade/19925",
    "SV6.5": "https://www.trollandtoad.com/shrouded-fable-singles/19997",
    "SV07": "https://www.trollandtoad.com/scarlet-violet-stellar-crown-singles/20018",
    "SWSH12.5": "https://www.trollandtoad.com/crown-zenith-singles/19429"
}

#Last page for tntsingles website
tntsingles_page = {
    "SV01": 6,
    "SV02": 6,
    "SV03": 5,
    "SV3.5": 5,
    "SV04": 6,
    "SV4.5": 6,
    "SV05": 5,
    "SV06": 5,
    "SV6.5": 3,
    "SV07": 5,
    "SWSH12.5": 5
}

#Elemenetal order for energy cards
energycard = {
    "grass": -7,
    "fire": -6,
    "water": -5,
    "electric": -4,
    "psychic": -3,
    "fighting": -2,
    "dark": -1,
    "steel": 0
}

#Parent class
class ScarletViolet:
    def __init__(self, setkey, csvexist=False):
        print(f"{setkey} Loading...")
        self.name = setkey + "_english"
        self.csvexist = csvexist
        self.setkey = setkey
        self.shpfy_dupe = False
        self.nanflag = False
        self.df_nan = pd.DataFrame(columns=['ID', 'Name'])

    def swdk(self,swdkurl,swdkurl_page,setnamereplace,setsize):
        newlist = []
        namelist = []
        testlist = []
        IDlist = []

        for i in range(1, swdkurl_page[self.setkey]):  # page range
            url = swdkurl[self.setkey] + "?page=" + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            data = soup.find_all("h3", class_="card__heading")
            for each in data:
                each = str(each)
                if re.search('[ENG]', each):
                    holder1 = re.split('>', each)
                    holder2 = re.split('<', holder1[2].strip())
                    testlist.append(holder2[0].strip())

        for i in range(len(testlist)):
            if testlist[i - 1] != testlist[i]:
                newlist.append(testlist[i])

        for i in range(len(newlist)):
            #     # newlist[i]=re.search(r"^([).*())$",newlist[i])
            newlist[i] = newlist[i].replace('\t', " ")
            newlist[i] = newlist[i].replace(setnamereplace[self.setkey], "")
            newlist[i] = newlist[i].strip()
            # holder = newlist[i].split(" [")
            # newlist[i] = holder[0]

        for i in range(len(newlist)):
            if re.search("SVE", newlist[i]): #checking for holo energy cards for SV3.5
                ID = re.search(r"\d+", newlist[i]).group(0)
                holder = newlist[i].split(ID)
                IDlist.append('SVE En ' + ID)
                holder2 = holder[1].replace('\t', ' ')
                holder2 = " ".join(holder2.split())
                namelist.append(holder2.strip())
            else:
                holder = newlist[i].split("/"+setsize[self.setkey]+ " ")
                IDlist.append(holder[0] + "/" +setsize[self.setkey])
                holder2 = holder[1].replace('\t', ' ')
                holder2 = " ".join(holder2.split())
                namelist.append(holder2)

        df_swdk = pd.DataFrame({"ID": IDlist, "Name": namelist})
        df_swdk.drop_duplicates(["ID","Name"], keep="first", inplace=True)
        df_swdk.sort_values(["ID", "Name"], ascending=True, inplace=True)
        df_swdk.reset_index(drop=True, inplace=True)
        return (df_swdk)

    def tnt(self,rh_url,rh_page,singles_url,singles_page):
        pricelist = []
        namelist = []
        IDlist = []
        for i in range(1, rh_page[self.setkey]):
            url = rh_url[self.setkey] +'?Keywords=&page-no=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                try:
                    each = str(each)
                    if re.search("Promo", each):
                        pass
                    else:
                        priceholder0 = re.split("col-2 text-center p-1", each)
                        priceholder1 = re.split(">", priceholder0[3])
                        priceholder2 = re.split("<", priceholder1[1])
                        priceholder3 = priceholder2[0].replace("$", "")
                        priceholder3 = priceholder3.strip()
                        pricelist.append(float(priceholder3))
                except:
                    pricelist.append(np.nan)
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                if re.search("Promo", each):  # promo cards were added
                    pass
                else:
                    nameholder1 = re.split(">", each)
                    nameholder2 = re.split("<", nameholder1[1])
                    nameholder3 = re.split("- ", nameholder2[0])
                    namelist.append(nameholder3[0].strip())
                    IDlist.append(nameholder3[1].strip())
        df_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_rh.sort_values(["ID"], ascending=True, inplace=True)
        df_rh.reset_index(drop=True, inplace=True)

        pricelist = []
        namelist = []
        IDlist = []
        promocounter = 0
        for i in range(1, singles_page[self.setkey]):
            url = singles_url[self.setkey]+'?Keywords=&page-no=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                if re.search("Promo", each):
                    pass
                else:
                    try:
                        priceholder0 = re.split("col-2 text-center p-1", each)
                        priceholder1 = re.split(">", priceholder0[3])
                        priceholder2 = re.split("<", priceholder1[1])
                        priceholder3 = priceholder2[0].replace("$", "")
                        priceholder3 = priceholder3.strip()
                        pricelist.append(float(priceholder3))
                    except:
                        pricelist.append(np.nan)
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                if re.search("Promo", each):  # promo cards were added
                    pass
                else:
                    nameholder1 = re.split(">", each)
                    nameholder2 = re.split("<", nameholder1[1])
                    nameholder3 = re.split("- ", nameholder2[0])
                    namelist.append(nameholder3[0].strip())
                    IDlist.append(nameholder3[1].strip())
        #print(f"Number of price is {len(pricelist)}, ID is {len(IDlist)} and name is {len(namelist)}.")
        df_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_singles.sort_values(["ID"], ascending=True, inplace=True)
        df_singles.reset_index(drop=True, inplace=True)
        return df_rh, df_singles

    def merge(self, df_swdk, df_rh, df_singles):
        df_merged = pd.DataFrame(columns=['ID', 'Name', 'Price in USD','Price in SGD'])
        rh_counter = 0
        singles_counter = 0
        correctcounter = 0
        wrongcounter = 0
        wronglist = []
        rates = ScarletViolet.xe_rates(self)
        usdtosgd = float(rates)
        for i in range(len(df_swdk)):
            if re.search('Reverse Holo', df_swdk.iloc[i,1]):
                if re.search(df_singles.iloc[singles_counter - 1,1], df_swdk.iloc[i,1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter - 1,1])
                    wronglist.append(df_swdk.iloc[i,1])
                try: #checking for NaN values
                    sgdvalue = df_rh.iloc[rh_counter,2] * usdtosgd
                    if sgdvalue < 1:
                        sgdvalue = 1
                    else:
                        sgdvalue = round(sgdvalue * 10) / 10
                except: #reverting to previous price if current price unavailable
                    sgdvalue = np.nan
                    self.nanflag = True
                    nan_row = {
                        'ID':df_swdk.iloc[i,0],
                        'Name':df_swdk.iloc[i,1]
                    }
                    nan_row = pd.DataFrame(nan_row,index = [0])
                    self.df_nan = pd.concat([self.df_nan, nan_row],ignore_index=True)
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Name': df_swdk.iloc[i,1],
                    'Price in USD': df_rh.iloc[rh_counter,2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                rh_counter += 1
            else:
                if re.search(df_singles.iloc[singles_counter,1], df_swdk.iloc[i,1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter,1])
                    wronglist.append(df_swdk.iloc[i,1])
                try:
                    sgdvalue = df_singles.iloc[singles_counter,2] * usdtosgd
                    if sgdvalue < 0.5:
                        sgdvalue = 0.5
                    else:
                        sgdvalue = round(sgdvalue * 10) / 10
                except:
                    sgdvalue = np.nan
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Name': df_swdk.iloc[i,1],
                    'Price in USD': df_singles.iloc[singles_counter,2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                singles_counter += 1
        # print(f"The number of correct entries are {correctcounter} and the number of wrong entries are {wrongcounter}.")
        # print(wronglist)
        return df_merged

    def shopify_sv(self, productcsv=""):
        df_shopify = pd.read_csv(productcsv)
        #df_shopify = df_shopify[~df_shopify.Handle.str.contains("copy-of-")]
        if df_shopify.Title.nunique() != len(df_shopify.index):
            self.shpfy_dupe = True
            self.df_dupe = df_shopify[df_shopify.Title.duplicated(keep = 'first')]
        df_shopify.sort_values(["Title"], ascending=True, inplace=True)
        df_shopify.drop_duplicates(['Title'], keep='first', inplace=True)
        df_shopify.reset_index(drop=True, inplace=True)
        #print(df_shopify)
        return df_shopify
#look to check for price = 0, do no changes if new price is 0
    def shopify_merge(self, df_swdk, df_shopify):
        df_changelog = pd.DataFrame(columns=['ID','Shopify Name','Sawadeekard Name','Before', 'Change','After'])
        # aftercheck = []
        for i in range(len(df_shopify)):
            #textsplit = re.split("\t",df_shopify.iloc[i,1])
            #print(f"Shopify: {textsplit[3]} Sawadeekard: {df_swdk.iloc[i,0], df_swdk.iloc[i,1]}.")
            try:
                holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,23]
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Shopify Name': df_shopify.iloc[i,1],
                    'Sawadeekard Name': df_swdk.iloc[i,1],
                    'Before': df_shopify.iloc[i,23],
                    'Change': holder,
                    'After': df_swdk.iloc[i,3]
                }
            except:
                holder = np.nan
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Shopify Name': df_shopify.iloc[i,1],
                    'Sawadeekard Name': df_swdk.iloc[i,1],
                    'Before': df_shopify.iloc[i,23],
                    'Change': holder,
                    'After': df_shopify.iloc[i,23]
                }
            new_row = pd.DataFrame(new_row, index=[0])
            df_changelog = pd.concat([df_changelog, new_row], ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,20]
        #     aftercheck.append(holder)
        return df_shopify, df_changelog

    def xe_rates(self):
        # USD to SGD
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ratedata = soup.find_all('div')
        filterlist = []
        for each in ratedata:
            each = str(each)
            if re.search("faded-digits", each):
                filterlist.append(each)
            filterlist.sort(key=len)
            holder1 = re.split(">", filterlist[0])
            holder21 = re.split("<", holder1[4])
            holder22 = re.split("<", holder1[5])
            rates = holder21[0] + holder22[0]
        return (rates)

    def sv_main(self, filename=""):
        swdk_name = ScarletViolet.swdk(self,swdkurl = swdkurl,swdkurl_page = swdkurl_page,setnamereplace = setnamereplace, setsize = setsize)
        tnt_rh, tnt_singles = ScarletViolet.tnt(self,rh_url = tntrh,rh_page = tntrh_page,singles_url= tntsingles,singles_page=tntsingles_page)
        simplemerge = ScarletViolet.merge(self,swdk_name, tnt_rh, tnt_singles)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = ScarletViolet.shopify_sv(self,filename)  # include error handling here
            # Check if there are repeated listings
            finalmerge, changelog = ScarletViolet.shopify_merge(self,simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename, index=False)
            changelog.to_csv(f"Changelog {self.name}.csv", index=False,na_rep="")
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index=False)
        if self.shpfy_dupe == True:
            print("The following entries are duplicated in the Sawadeekard website:")
            print(f"{self.df_dupe.Title}")
            print("But has been removed in the final CSV.")
        if self.nanflag == True:
            print("The following entries are not updated as no price was found on TnT:")
            print(f"{self.df_nan}")
            print("So the price is unchanged.")
        print(f"{self.name} completed")

#Sword and Shield
class SwordShield:
    def __init__(self, setkey, csvexist=False):
        print(f"{setkey} Loading...")
        self.name = setkey + "_english"
        self.csvexist = csvexist
        self.setkey = setkey
        self.shpfy_dupe = False
        self.nanflag = False
        self.df_nan = pd.DataFrame(columns=['ID', 'Name'])

    def swdk(self,swdkurl,swdkurl_page,setnamereplace,setsize):
        newlist = []
        namelist = []
        testlist = []
        IDlist = []

        for i in range(1, swdkurl_page[self.setkey]):  # page range
            url = swdkurl[self.setkey] + "?page=" + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            data = soup.find_all("h3", class_="card__heading")
            for each in data:
                each = str(each)
                if re.search('[ENG]', each):
                    holder1 = re.split('>', each)
                    holder2 = re.split('<', holder1[2].strip())
                    testlist.append(holder2[0].strip())

        for i in range(len(testlist)):
            if testlist[i - 1] != testlist[i]:
                newlist.append(testlist[i])

        for i in range(len(newlist)):
            #     # newlist[i]=re.search(r"^([).*())$",newlist[i])
            newlist[i] = newlist[i].replace('\t', " ")
            newlist[i] = newlist[i].replace(setnamereplace[self.setkey], "")
            newlist[i] = newlist[i].strip()
            # holder = newlist[i].split(" [")
            # newlist[i] = holder[0]

        for i in range(len(newlist)):
            if re.search("SVE", newlist[i]): #checking for holo energy cards for SV3.5
                ID = re.search(r"\d+", newlist[i]).group(0)
                holder = newlist[i].split(ID)
                IDlist.append('SVE En ' + ID)
                holder2 = holder[1].replace('\t', ' ')
                holder2 = " ".join(holder2.split())
                namelist.append(holder2.strip())
            else:
                holder = newlist[i].split("/"+setsize[self.setkey]+ " ")
                IDlist.append(holder[0] + "/" +setsize[self.setkey])
                holder2 = holder[1].replace('\t', ' ')
                holder2 = " ".join(holder2.split())
                namelist.append(holder2)

        df_swdk = pd.DataFrame({"ID": IDlist, "Name": namelist})
        df_swdk.drop_duplicates(["ID","Name"], keep="first", inplace=True)
        df_swdk.sort_values(["ID", "Name"], ascending=True, inplace=True)
        df_swdk.reset_index(drop=True, inplace=True)
        return (df_swdk)

    def tnt(self,rh_url,rh_page,singles_url,singles_page):
        pricelist = []
        namelist = []
        IDlist = []
        for i in range(1, rh_page[self.setkey]):
            url = rh_url[self.setkey] +'?Keywords=&page-no=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                try:
                    each = str(each)
                    if re.search("Promo", each):
                        pass
                    else:
                        priceholder0 = re.split("col-2 text-center p-1", each)
                        priceholder1 = re.split(">", priceholder0[3])
                        priceholder2 = re.split("<", priceholder1[1])
                        priceholder3 = priceholder2[0].replace("$", "")
                        priceholder3 = priceholder3.strip()
                        pricelist.append(float(priceholder3))
                except:
                    pricelist.append(np.nan)
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                if re.search("Promo", each):  # promo cards were added
                    pass
                else:
                    nameholder1 = re.split(">", each)
                    nameholder2 = re.split("<", nameholder1[1])
                    nameholder3 = re.split("- ", nameholder2[0])
                    namelist.append(nameholder3[0].strip())
                    IDlist.append(nameholder3[1].strip())
        df_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_rh.sort_values(["ID"], ascending=True, inplace=True)
        df_rh.reset_index(drop=True, inplace=True)

        pricelist = []
        namelist = []
        IDlist = []
        promocounter = 0
        for i in range(1, singles_page[self.setkey]):
            url = singles_url[self.setkey]+'?Keywords=&page-no=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
                each = str(each)
                if re.search("Promo", each):
                    pass
                else:
                    try:
                        priceholder0 = re.split("col-2 text-center p-1", each)
                        priceholder1 = re.split(">", priceholder0[3])
                        priceholder2 = re.split("<", priceholder1[1])
                        priceholder3 = priceholder2[0].replace("$", "")
                        priceholder3 = priceholder3.strip()
                        pricelist.append(float(priceholder3))
                    except:
                        pricelist.append(np.nan)
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                if re.search("Promo", each):  # promo cards were added
                    pass
                else:
                    nameholder1 = re.split(">", each)
                    nameholder2 = re.split("<", nameholder1[1])
                    nameholder3 = re.split("- ", nameholder2[0])
                    namelist.append(nameholder3[0].strip())
                    IDlist.append(nameholder3[1].strip())
        #print(f"Number of price is {len(pricelist)}, ID is {len(IDlist)} and name is {len(namelist)}.")
        df_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
        df_singles.sort_values(["ID"], ascending=True, inplace=True)
        df_singles.reset_index(drop=True, inplace=True)
        return df_rh, df_singles

    def merge(self, df_swdk, df_rh, df_singles):
        df_merged = pd.DataFrame(columns=['ID', 'Name', 'Price in USD','Price in SGD'])
        rh_counter = 0
        singles_counter = 0
        correctcounter = 0
        wrongcounter = 0
        wronglist = []
        rates = SwordShield.xe_rates(self)
        usdtosgd = float(rates)
        for i in range(len(df_swdk)):
            if re.search('Reverse Holo', df_swdk.iloc[i,1]):
                if re.search(df_singles.iloc[singles_counter - 1,1], df_swdk.iloc[i,1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter - 1,1])
                    wronglist.append(df_swdk.iloc[i,1])
                try: #checking for NaN values
                    sgdvalue = df_rh.iloc[rh_counter,2] * usdtosgd
                    if sgdvalue < 1:
                        sgdvalue = 1
                    else:
                        sgdvalue = round(sgdvalue * 10) / 10
                except: #reverting to previous price if current price unavailable
                    sgdvalue = np.nan
                    self.nanflag = True
                    nan_row = {
                        'ID':df_swdk.iloc[i,0],
                        'Name':df_swdk.iloc[i,1]
                    }
                    nan_row = pd.DataFrame(nan_row,index = [0])
                    self.df_nan = pd.concat([self.df_nan, nan_row],ignore_index=True)
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Name': df_swdk.iloc[i,1],
                    'Price in USD': df_rh.iloc[rh_counter,2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                rh_counter += 1
            else:
                if re.search(df_singles.iloc[singles_counter,1], df_swdk.iloc[i,1]):
                    correctcounter += 1
                else:
                    wrongcounter += 1
                    wronglist.append(df_singles.iloc[singles_counter,1])
                    wronglist.append(df_swdk.iloc[i,1])
                try:
                    sgdvalue = df_singles.iloc[singles_counter,2] * usdtosgd
                    if sgdvalue < 0.5:
                        sgdvalue = 0.5
                    else:
                        sgdvalue = round(sgdvalue * 10) / 10
                except:
                    sgdvalue = np.nan
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Name': df_swdk.iloc[i,1],
                    'Price in USD': df_singles.iloc[singles_counter,2],
                    'Price in SGD': sgdvalue
                }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
                singles_counter += 1
        # print(f"The number of correct entries are {correctcounter} and the number of wrong entries are {wrongcounter}.")
        # print(wronglist)
        return df_merged

    def shopify_sv(self, productcsv=""):
        df_shopify = pd.read_csv(productcsv)
        #df_shopify = df_shopify[~df_shopify.Handle.str.contains("copy-of-")]
        if df_shopify.Title.nunique() != len(df_shopify.index):
            self.shpfy_dupe = True
            self.df_dupe = df_shopify[df_shopify.Title.duplicated(keep = 'first')]
        df_shopify.sort_values(["Title"], ascending=True, inplace=True)
        df_shopify.drop_duplicates(['Title'], keep='first', inplace=True)
        df_shopify.reset_index(drop=True, inplace=True)
        #print(df_shopify)
        return df_shopify
#look to check for price = 0, do no changes if new price is 0
    def shopify_merge(self, df_swdk, df_shopify):
        df_changelog = pd.DataFrame(columns=['ID','Shopify Name','Sawadeekard Name','Before', 'Change','After'])
        # aftercheck = []
        for i in range(len(df_shopify)):
            #textsplit = re.split("\t",df_shopify.iloc[i,1])
            #print(f"Shopify: {textsplit[3]} Sawadeekard: {df_swdk.iloc[i,0], df_swdk.iloc[i,1]}.")
            try:
                holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,23]
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Shopify Name': df_shopify.iloc[i,1],
                    'Sawadeekard Name': df_swdk.iloc[i,1],
                    'Before': df_shopify.iloc[i,23],
                    'Change': holder,
                    'After': df_swdk.iloc[i,3]
                }
            except:
                holder = np.nan
                new_row = {
                    'ID': df_swdk.iloc[i,0],
                    'Shopify Name': df_shopify.iloc[i,1],
                    'Sawadeekard Name': df_swdk.iloc[i,1],
                    'Before': df_shopify.iloc[i,23],
                    'Change': holder,
                    'After': df_shopify.iloc[i,23]
                }
            new_row = pd.DataFrame(new_row, index=[0])
            df_changelog = pd.concat([df_changelog, new_row], ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,20]
        #     aftercheck.append(holder)
        return df_shopify, df_changelog

    def xe_rates(self):
        # USD to SGD
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ratedata = soup.find_all('div')
        filterlist = []
        for each in ratedata:
            each = str(each)
            if re.search("faded-digits", each):
                filterlist.append(each)
            filterlist.sort(key=len)
            holder1 = re.split(">", filterlist[0])
            holder21 = re.split("<", holder1[4])
            holder22 = re.split("<", holder1[5])
            rates = holder21[0] + holder22[0]
        return (rates)

    def swsh_main(self, filename=""):
        swdk_name = SwordShield.swdk(self,swdkurl = swdkurl,swdkurl_page = swdkurl_page,setnamereplace = setnamereplace, setsize = setsize)
        tnt_rh, tnt_singles = SwordShield.tnt(self,rh_url = tntrh,rh_page = tntrh_page,singles_url= tntsingles,singles_page=tntsingles_page)
        simplemerge = SwordShield.merge(self,swdk_name, tnt_rh, tnt_singles)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = SwordShield.shopify_sv(self,filename)  # include error handling here
            # Check if there are repeated listings
            finalmerge, changelog = SwordShield.shopify_merge(self,simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename, index=False)
            changelog.to_csv(f"Changelog {self.name}.csv", index=False,na_rep="")
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index=False)
        if self.shpfy_dupe == True:
            print("The following entries are duplicated in the Sawadeekard website:")
            print(f"{self.df_dupe.Title}")
            print("But has been removed in the final CSV.")
        if self.nanflag == True:
            print("The following entries are not updated as no price was found on TnT:")
            print(f"{self.df_nan}")
            print("So the price is unchanged.")
        print(f"{self.name} completed")

### Japanese Sets
## Individual codes
class SV2a_Japanese():
    def __init__(self, setkey, csvexist = False):
        print(f"{setkey} Loading...")
        self.name = "SV2a_Japanese"
        self.csvexist = csvexist
        self.setkey = setkey
        self.shpfy_dupe = False
        self.nanflag = False
        self.df_nan = pd.DataFrame(columns=['ID', 'Name'])

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
        #df_swdk = SV2a_Japanese.swdk_main(self)
        #df_yyt = SV2a_Japanese.yyt_main(self)
        rates = SV2a_Japanese.xe_rates(self)
        jpytosgd = float(rates)/1000

        df_final = pd.DataFrame(columns=['ID', 'Name', 'Price in JPY', 'Price in SGD'])
        # df_yyt.Name = df_swdk[df_swdk.ID==df_yyt.iloc[5,0]].Name
        for i in range(len(df_yyt.index)):
            # df_yyt.Name = df_swdk[df_swdk.ID==df_yyt.iloc[5,0]].Name
            if (len(df_swdk[df_swdk.ID == df_yyt.iloc[i,0]].index) > 1):
                df_swdk_hold = df_swdk[df_swdk.ID == df_yyt.iloc[i,0]].reset_index(drop=True)
                df_yyt_hold = df_yyt[df_yyt.ID == df_yyt.iloc[i,0]].reset_index(drop=True)
                sgdvalue = round(df_yyt.iloc[i,2]*jpytosgd*10)/10
                if re.search(r".*マスターボール柄.*", df_yyt.iloc[i,1]):
                    namestr = SV2a_Japanese.namechk(self,r".*Master Ball.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.iloc[i,0],
                        'Name': namestr,
                        'Price in JPY': df_yyt.iloc[i,2],
                        'Price in SGD': sgdvalue
                    }
                elif re.search(r".*モンスターボール柄.*", df_yyt.iloc[i,1]):
                    namestr = SV2a_Japanese.namechk(self,r".*Reverse Holo.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.iloc[i,0],
                        'Name': namestr,
                        'Price in JPY': df_yyt.iloc[i,2],
                        'Price in SGD': sgdvalue
                    }
                else:
                    namestr = SV2a_Japanese.namechk(self,r".*Foil.*", df_swdk_hold)
                    new_row = {
                        'ID': df_yyt.iloc[i,0],
                        'Name': namestr,
                        'Price in JPY': df_yyt.iloc[i,2],
                        'Price in SGD': sgdvalue
                    }
            elif (len(df_swdk[df_swdk.ID == df_yyt.iloc[i,0]].index
            ) == 1):
                new_row = {
                    'ID': df_yyt.iloc[i,0],
                    'Name': df_swdk.iloc[i,1],
                    'Price in JPY': df_yyt.iloc[i,2],
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
        df_swdk.sort_values(['Name'], ascending = True, inplace = True)
        df_swdk.reset_index(drop = True, inplace = True)
        for i in range(len(df_shopify)):
            holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,23]
            new_row = {
                'Before':df_shopify.iloc[i,23],
                'Change':holder,
                'After':df_swdk.iloc[i,3]
                }
            new_row = pd.DataFrame(new_row,index = [0])
            df_changelog = pd.concat([df_changelog,new_row],ignore_index=True)
        df_shopify['Variant Price'] = df_swdk['Price in SGD']
        # for i in range(len(df_shopify)):
        #     holder = df_swdk.iloc[i,3] - df_shopify.iloc[i,20]
        #     aftercheck.append(holder)
        return(df_shopify,df_changelog)

    def xe_rates(self):
        url = 'https://www.xe.com/currencyconverter/convert/?Amount=1000&From=JPY&To=SGD'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        ratedata = soup.find_all('div')
        filterlist = []
        for each in ratedata:
            each = str(each)
            if re.search("faded-digits", each):
                filterlist.append(each)
            filterlist.sort(key=len)
            holder1 = re.split(">", filterlist[0])
            holder21 = re.split("<", holder1[4])
            holder22 = re.split("<", holder1[5])
            rates = holder21[0] + holder22[0]
        return (rates)

    def jp_main(self, filename = ""):
        swdk_name = SV2a_Japanese.swdk_main(self)
        yyt_list = SV2a_Japanese.yyt_main(self)
        simplemerge = SV2a_Japanese.jp_151_merge(self,swdk_name, yyt_list)
        dttm = datetime.now()
        if self.csvexist:
            shpfy_name = SV2a_Japanese.shopify_sv2a(self,filename) #include error handling here
            finalmerge,changelog = SV2a_Japanese.shopify_merge(self,simplemerge, shpfy_name)
            filename = f"{self.name} Shopify {dttm.strftime('%y%m%d')}.csv"
            finalmerge.to_csv(filename,index=False)
            changelog.to_csv(f"Changelog {self.name}.csv",index = False)
        else:
            simplemerge.to_csv(f"{self.name} Merged {dttm.strftime('%y%m%d')}.csv", index = False)
        print(f"{self.name} completed")
class controller:
    def __init__(self):
        print('\n============================================')
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
        #only included for google colab because the pathway is different from exe
        gdriveprefix = "/content/drive/MyDrive/Shopify Program/"
        #menu options
        while True:
            #Split by language, Japanese cards will use YYT, English cards are undecided
            print("1. Scarlet and Violet Series")
            print("2. Sword and Shield Series")
            print("3. Japanese Sets")
            print("X. Exit\n")

            #choice obtained using input
            choice = input("What type of cards? \n")
            choice = choice.strip()

            if choice == '1':
                try:
                    csvdict = {
                        'SV01': "ENG SV01 SV1.csv",
                        'SV02': "ENG SV02 PAL.csv",
                        'SV03': "ENG SV03 OBF.csv",
                        'SV3.5': "ENG SV3.5 MEW.csv",
                        'SV04': "ENG SV04 PAR.csv",
                        'SV4.5': "ENG SV4.5 PAF.csv",
                        'SV05': "ENG SV05 TEF.csv",
                        'SV06': "ENG SV06 TWM.csv",
                        'SV6.5': "ENG SV6.5 SFA.csv",
                        'SV07': "ENG SV07 SCR.csv"
                    }
                    setdict = {
                        'SV01': "SV01 Scarlet & Violet Base set",
                        'SV02': "SV02 Paldea Evolved",
                        'SV03': "SV03 Obsidian Flames",
                        'SV3.5': "SV3.5 Scarlet Violet 151",
                        'SV04': "SV04 Paradox Rift",
                        'SV4.5': "SV4.5 Paldean Fates",
                        'SV05': "SV05 Temporal Forces",
                        'SV06': "SV06 Twilight Masquerade",
                        'SV6.5': "SV6.5 Shrouded Fable",
                        'SV07': "SV07 Stellar Crown"
                    }
                    #} #manual include set names
                    objdict ={}

                    while True:
                        #options are included manually, but will just be setlist[i]
                        print(f"1. {setdict['SV01']}")
                        print(f"2. {setdict['SV02']}")
                        print(f"3. {setdict['SV03']}")
                        print(f"4. {setdict['SV3.5']}")
                        print(f"5. {setdict['SV04']}")
                        print(f"6. {setdict['SV4.5']}")
                        print(f"7. {setdict['SV05']}")
                        print(f"8. {setdict['SV06']}")
                        print(f"9. {setdict['SV6.5']}")
                        print(f"10. {setdict['SV07']}")
                        print("00. All listed series")
                        print("X. Exit\n")
                        #To know which set to scrape
                        choice = input("What set are you interested in? \n")
                        choice = choice.strip()
                        choiceflag = False
                        if choice == "00":
                            # To check if shopify csv file exists
                            while choiceflag == False:
                                print("The required files are:")
                                for key in csvdict:
                                    print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist,choiceflag = yesnochk(shpfychoice,choiceflag)
                            if csvexist:
                                for key in setdict:
                                    sv_holder = ScarletViolet(setkey = key, csvexist = csvexist)
                                    sv_holder.sv_main(filename = csvdict[key])
                            else:
                                for key in setdict:
                                    sv_holder = ScarletViolet(setkey = key, csvexist = csvexist)
                                    sv_holder.sv_main()
                                print("All sets are processed.")
                        elif choice.lower() == 'x':
                            break
                        else:
                            if choice == '1':
                                key = 'SV01'
                            elif choice == '2':
                                key = 'SV02'
                            elif choice == '3':
                                key = 'SV03'
                            elif choice == '4':
                                key = 'SV3.5'
                            elif choice == '5':
                                key = 'SV04'
                            elif choice == '6':
                                key = 'SV4.5'
                            elif choice == '7':
                                key = 'SV05'
                            elif choice == '8':
                                key = 'SV06'
                            elif choice == '9':
                                key = 'SV6.5'
                            elif choice == '10':
                                key = 'SV07'
                            # To check if shopify csv file exists
                            while choiceflag == False:
                                print("The required files are:")
                                print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist,choiceflag = yesnochk(shpfychoice,choiceflag)
                            svobj = ScarletViolet(setkey = key, csvexist = csvexist)
                            svobj.sv_main(filename = csvdict[key])
                            print("This is done!")
                except ExitException():
                    sys.exit()
            elif choice == "2":
                try:
                    csvdict = {
                        'CZ': "Crown Zenith",
                        'ST': "Silver Tempest",
                        'LO': "Lost Origins",
                        'PoGo': "Pokemon Go",
                        'AR': "Astral Radiance",
                        'BRS': "Brilliant Stars",
                        'FS': "Fusion Strike",
                        'Celeb': "Celebrations"
                    }
                    setdict = {
                        'CZ': "Crown Zenith",
                        'ST': "Silver Tempest",
                        'LO': "Lost Origins",
                        'PoGo': "Pokemon Go",
                        'AR': "Astral Radiance",
                        'BRS': "Brilliant Stars",
                        'FS': "Fusion Strike",
                        'Celeb': "Celebrations"
                    }
                    while True:
                        print(f"1. {setdict['CZ']}")
                        print(f"2. {setdict['ST']}")
                        print(f"3. {setdict['LO']}")
                        print(f"4. {setdict['PoGo']}")
                        print(f"5. {setdict['AR']}")
                        print(f"6. {setdict['BRS']}")
                        print(f"7. {setdict['FS']}")
                        print(f"8. {setdict['Celeb']}")
                        print("X. Exit\n")

                        choice = input("What set are you interested in? \n")
                        choice = choice.strip()
                        choiceflag = False
                        if choice == '00':
                            while choiceflag == False:
                                print("The required files are:")
                                print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist, choiceflag = yesnochk(shpfychoice, choiceflag)
                            svobj = ScarletViolet(setkey=key, csvexist=csvexist)
                            svobj.sv_main(filename=csvdict[key])
                            print("This is done!")
                        elif choice.lower() == 'x':
                            break
                        else:
                            if choice == '1':
                                key = 'CZ'
                            elif choice == '2':
                                key = 'ST'
                            elif choice == '3':
                                key = 'LO'
                            elif choice == '4':
                                key = 'PoGo'
                            elif choice == '5':
                                key = 'AR'
                            elif choice == '6':
                                key = 'BRS'
                            elif choice == '7':
                                key = 'FS'
                            elif choice == '8':
                                key = 'Celeb'
                            # To check if shopify csv file exists
                            while choiceflag == False:
                                print("The required files are:")
                                print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist,choiceflag = yesnochk(shpfychoice,choiceflag)
                            swshobj = SwordShield(setkey = key, csvexist = csvexist)
                            swshobj.swsh_main(filename = csvdict[key])
                            print("This is done!")
                except ExitException():
                    sys.exit()
            elif choice == "3":
                try:
                    csvdict = {
                        'SV2a': "JAP SV2a 151.csv"
                    }
                    setdict = {
                        'SV2a': "Pokemon 151"
                    }
                    while True:
                        #options are included manually, but will just be setlist[i]
                        print(f"1. {setdict['SV2a']}")
                        print("00. All listed series")
                        print("X. Exit\n")
                        #To know which set to scrape
                        choice = input("What set are you interested in? \n")
                        choice = choice.strip()
                        choiceflag = False
                        if choice == "00":
                            # To check if shopify csv file exists
                            while choiceflag == False:
                                print("The required files are:")
                                for key in csvdict:
                                    print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist,choiceflag = yesnochk(shpfychoice,choiceflag)
                            if csvexist:
                                for key in setdict:
                                    jp_holder = SV2a_Japanese(setkey = key, csvexist = csvexist)
                                    jp_holder.jp_main(filename = csvdict[key])
                            else:
                                for key in setdict:
                                    jp_holder = SV2a_Japanese(setkey = key, csvexist = csvexist)
                                    jp_holder.jp_main()
                                print("All sets are processed.")
                        elif choice.lower() == 'x':
                            break
                        else:
                            if choice == '1':
                                key = 'SV2a'
                            # To check if shopify csv file exists
                            while choiceflag == False:
                                print("The required files are:")
                                print(f"{csvdict[key]}")
                                shpfychoice = input("Do you have the Shopify csv files? (Y/N) \n")
                                csvexist,choiceflag = yesnochk(shpfychoice,choiceflag)
                            jpobj = SV2a_Japanese(setkey = key, csvexist = csvexist)
                            jpobj.jp_main(filename = csvdict[key])
                            print("This is done!")
                except ExitException():
                    sys.exit()
            elif choice.lower() == 'x':
                break

if __name__ == "__main__":
    a = controller()
    a.main()