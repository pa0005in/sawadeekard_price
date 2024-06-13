# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 07:13:38 2024

@author: khin_
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


def swdk_sv6():
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

def tnt_sv6():
    pricelist = []
    namelist = []
    IDlist = []
    for i in range(1,4):
        url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-twilight-masquerade/19923?Keywords=&page-no='+str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        price = soup.find_all('div',class_="col-2 text-center p-1")
        for each in price:
            each = str(each)
            if re.search("button",each):
                pass
            elif re.search("Price",each):
                pass
            elif re.search("Quantity",each):
                pass
            else:
                each = each.replace('<div class="col-2 text-center p-1">',"")
                each = each.replace('</div>',"")
                each = each.replace('$',"")
                each = float(each)
                pricelist.append(each)
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
        soup = BeautifulSoup(page.content,"html.parser")
        price = soup.find_all('div',class_="col-2 text-center p-1")
        for each in price:
            each = str(each)
            if re.search("button",each):
                pass
            elif re.search("Price",each):
                pass
            elif re.search("Quantity",each):
                pass
            else:
                each = each.replace('<div class="col-2 text-center p-1">',"")
                each = each.replace('</div>',"")
                each = each.replace('$',"")
                each = float(each)
                pricelist.append(each)
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

def sv6_merge(df_swdk,df_rh,df_singles):
    df_merged = pd.DataFrame(columns = ['ID','Name','Price in USD'])
    rh_counter = 0
    singles_counter = 0
    correctcounter = 0
    wrongcounter = 0
    wronglist = []
    usdtosgd = xe_rates()
    usdtosgd = float(usdtosgd)
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

def shopify_sv6(productcsv = "products_export_1 (3).csv" ):
    df_shopify = pd.read_csv(productcsv)
    df_shopify.sort_values(["Title"], ascending=True, inplace=True)
    df_shopify.reset_index(drop = True,inplace=True)
    return (df_shopify)

def shopify_merge(df_swdk,df_shopify):
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

def xe_rates():
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=SGD'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,"html.parser")
    ratedata = soup.find_all('p',class_="sc-1c293993-1 fxoXHw")
    for each in ratedata:
        each = str(each)
        holder1 = re.split(">",each)
        holder21 = re.split("<",holder1[1])
        holder22 = re.split("<",holder1[2])
        rates = holder21[0]+holder22[0]
    return (rates)

def sv6_main(filename = ""):
    swdk_name = swdk_sv6()
    shpfy_name = shopify_sv6(filename) #include error handling here
    tnt_rh,tnt_singles = tnt_sv6()
    simplemerge = sv6_merge(swdk_name, tnt_rh, tnt_singles)
    finalmerge,changelog = shopify_merge(simplemerge, shpfy_name)
    dttm = datetime.now()
    filename = f"SV6 Shopify English {dttm.strftime('%y%m%d')}.csv"
    finalmerge.to_csv(filename,index=False)
    changelog.to_csv("Changelog.csv",index = False)
    print("SV6 completed")

if __name__ == "__main__":
    sv6_main()
