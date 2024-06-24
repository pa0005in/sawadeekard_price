# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 22:49:17 2023

@author: khin_
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


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
    swdk = swdk_sv6()
