# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 22:49:17 2023

@author: khin_
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def tnt_sv35():
    pricelist = []
    namelist = []
    IDlist = []
    for i in range(1, 4):
        url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-151/19702?Keywords=&page-no=' + str(i)
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
    df_sv35_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
    df_sv35_rh.sort_values(["ID"], ascending=True, inplace=True)
    df_sv35_rh.reset_index(drop=True, inplace=True)

    pricelist = []
    namelist = []
    IDlist = []
    promocounter = 0
    for i in range(1, 5):
            url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-151/19701?Keywords=&page-no=' + str(i)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find_all('div', class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
            for each in price:
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
            name = soup.find_all('a', class_="card-text")
            for each in name:
                each = str(each)
                if re.search("Promo", each):  # promo cards were added
                    promocounter += 1
                else:
                    nameholder1 = re.split(">", each)
                    nameholder2 = re.split("<", nameholder1[1])
                    nameholder3 = re.split("-", nameholder2[0])
                    namelist.append(nameholder3[0].strip())
                    IDlist.append(nameholder3[1].strip())
    print(f"Number of price is {len(pricelist)}, ID is {len(IDlist)} and name is {len(namelist)}.")
    df_sv35_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
    df_sv35_singles.sort_values(["ID"], ascending=True, inplace=True)
    df_sv35_singles.reset_index(drop=True, inplace=True)
    return df_sv35_rh, df_sv35_singles

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


if __name__ == "__main__":
    rh,singles = tnt_sv35()
