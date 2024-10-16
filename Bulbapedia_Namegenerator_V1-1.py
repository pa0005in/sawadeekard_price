# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:53:21 2024

@author: khin_
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

url1 = "https://bulbapedia.bulbagarden.net/wiki/Stellar_Crown_(TCG)"
url2 = "https://bulbapedia.bulbagarden.net/wiki/Scarlet_%26_Violet_(TCG)"
url3 = "https://bulbapedia.bulbagarden.net/wiki/Paldean_Fates_(TCG)"
page1 = requests.get(url1)
page2 = requests.get(url2)
page3 = requests.get(url3)
soup1 = BeautifulSoup(page1.content, 'html.parser')
soup2 = BeautifulSoup(page2.content, 'html.parser')
soup3 = BeautifulSoup(page3.content, 'html.parser')

data1 = soup1.find_all("table",class_="roundy")#, attrs = {"class":"roundy", "style":"float:left; background:#342F80; border: 3px solid #00E5E7"})
data2 = soup2.find_all("table",class_="roundy")
data3 = soup3.find_all("table",class_="roundy")
asdf1 = []
asdf2 = []
asdf3 = []
jap={}
eng={}
raw_data ={}
df_dict = {}
df_merged = pd.DataFrame(columns=['ID', 'Mark','Name', 'Type','Rarity'])
setnameen = ""
setnamejp = ""
tablename = ""

def myfunc(e):
    return len(e)

for each in data1:
    if re.search("Rarity",str(each)):
        if re.search("Additional Cards",str(each)):
            pass
        else:
            asdf1.append(str(each))
    
for each in data2:
    if re.search("Rarity",str(each)):
        if re.search("Additional Cards",str(each)):
            pass
        else:
            asdf2.append(str(each))
    
for each in data3:
    if re.search("Rarity",str(each)):
        if re.search("Additional Cards",str(each)):
            pass
        else:
            asdf3.append(str(each))

asdf1.sort(key=len,reverse = True)
asdf2.sort(key=len,reverse = True)
asdf3.sort(key=len,reverse = True)

dfdf = asdf3

if len(dfdf) == 2:
    if re.search("Illustration Rare",dfdf[0]):
        eng[0] = dfdf[0]
        jap[0] = dfdf[1]
    elif re.search("AR", dfdf[0]):
        jap[0] = dfdf[0]
        eng[0] = dfdf[1]
elif len(dfdf) >2:
    for i in range(len(dfdf)):
        if re.search("AR",dfdf[i]):
            if len(jap)==0:
                jap[0]=dfdf[i]
            elif len(jap)>0:
                jap[1]=dfdf[i]
        if re.search("Illustration Rare",dfdf[i]):
            eng[0]=dfdf[i]
                

for each in eng:
    place = eng[each]
    # if re.search('align="center"', each):
    #     pass
    holder=place.split("<tr>")
    del_ctr = 0
    holderlist = []
   
    for i in range (len(holder)):
        if re.search('text-align:left; color',holder[i-del_ctr]):
            # print(holder[i-del_ctr] + "wtf")
            tablename = holder[i-del_ctr].split("<b>")[1].split("</b>")[0]
            del holder[i-del_ctr]
            del_ctr += 1
        elif re.search("background:#FFFFFF",holder[i-del_ctr]):
            pass
        else:
            del holder[i-del_ctr]
            del_ctr += 1
    
    print(tablename)
    raw_data[tablename]=holder
    
    for i in range(len(holder)):
        holderlist.append(holder[i].split('title='))
        if re.search('"ex"',holder[i]):
            new_row = {
                'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                'Mark':holder[i].split('title=')[1].split('"')[1],
                'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                'Type':holder[i].split('title=')[4].split('"')[1],
                'Rarity':holder[i].split('title=')[5].split('"')[1]
                }
            new_row = pd.DataFrame(new_row, index=[0])
            df_merged = pd.concat([df_merged, new_row], ignore_index=True)
        else:
            try:
                new_row = {
                    'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                    'Mark':holder[i].split('title=')[1].split('"')[1],
                    'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                    'Type':holder[i].split('title=')[3].split('"')[1],
                    'Rarity':holder[i].split('title=')[4].split('"')[1]
                    }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
            except:
                if re.search("Basic",holder[i]) and re.search("Energy", holder[i]):
                    new_row = {
                        'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                        'Mark':"-",
                        'Name':holder[i].split('title=')[1].split('">')[1].split('</')[0].strip(),
                        'Type':holder[i].split('title=')[2].split('"')[1].strip(),
                        'Rarity':holder[i].split('title=')[3].split('"')[1]
                        }
                else:
                    new_row = {
                        'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                        'Mark':holder[i].split('title=')[1].split('"')[1],
                        'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                        'Type':holder[i].split('title=')[2].split(';">')[1].split("</th>")[0].strip(),
                        'Rarity':holder[i].split('title=')[3].split('"')[1]
                        }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)                    
    df_dict[tablename]=df_merged
    
for each in jap:
    place = jap[each]
    # if re.search('align="center"', each):
    #     pass
    holder=place.split("<tr>")
    del_ctr = 0
    holderlist = []
   
    for i in range (len(holder)):
        if re.search('text-align:left; color',holder[i-del_ctr]):
            # print(holder[i-del_ctr] + "wtf")
            tablename = holder[i-del_ctr].split("<b>")[1].split("</b>")[0]
            del holder[i-del_ctr]
            del_ctr += 1
        elif re.search("background:#FFFFFF",holder[i-del_ctr]):
            pass
        else:
            del holder[i-del_ctr]
            del_ctr += 1
    
    print(tablename)
    raw_data[tablename]=holder
    
    for i in range(len(holder)):
        holderlist.append(holder[i].split('title='))
        if re.search('"ex"',holder[i]):
            new_row = {
                'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                'Mark':holder[i].split('title=')[1].split('"')[1],
                'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                'Type':holder[i].split('title=')[4].split('"')[1],
                'Rarity':holder[i].split('title=')[5].split('"')[1]
                }
            new_row = pd.DataFrame(new_row, index=[0])
            df_merged = pd.concat([df_merged, new_row], ignore_index=True)
        else:
            try:
                new_row = {
                    'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                    'Mark':holder[i].split('title=')[1].split('"')[1],
                    'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                    'Type':holder[i].split('title=')[3].split('"')[1],
                    'Rarity':holder[i].split('title=')[4].split('"')[1]
                    }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)
            except:
                if re.search("Basic",holder[i]) and re.search("Energy", holder[i]):
                    new_row = {
                        'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                        'Mark':"-",
                        'Name':holder[i].split('title=')[1].split('">')[1].split('</')[0].strip(),
                        'Type':holder[i].split('title=')[2].split('"')[1].strip(),
                        'Rarity':holder[i].split('title=')[3].split('"')[1]
                        }
                else:
                    new_row = {
                        'ID':holder[i].split('title=')[0].split('</td>')[0].split('FF">')[1].strip(),
                        'Mark':holder[i].split('title=')[1].split('"')[1],
                        'Name':holder[i].split('title=')[2].split('"')[1].split(f'({tablename}')[0].strip(),
                        'Type':holder[i].split('title=')[2].split(';">')[1].split("</th>")[0].strip(),
                        'Rarity':holder[i].split('title=')[3].split('"')[1]
                        }
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)                    
    df_dict[tablename]=df_merged