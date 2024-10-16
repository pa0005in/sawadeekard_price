# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:53:21 2024

@author: khin_
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

url = "https://bulbapedia.bulbagarden.net/wiki/Stellar_Crown_(TCG)"
url2 = "https://bulbapedia.bulbagarden.net/wiki/Shrouded_Fable_(TCG)"
url3 = "https://bulbapedia.bulbagarden.net/wiki/Paldean_Fates_(TCG)"
page = requests.get(url3)
soup = BeautifulSoup(page.content, 'html.parser')

data = soup.find_all("table",class_="roundy")#, attrs = {"class":"roundy", "style":"float:left; background:#342F80; border: 3px solid #00E5E7"})
asdf = []
raw_data ={}
df_dict = {}
df_merged = pd.DataFrame(columns=['ID', 'Mark','Name', 'Type','Rarity'])
setnameen = ""
setnamejp = ""
tablename = ""

def myfunc(e):
    return len(e)

for each in data:
    each = str(each)
    # if re.search('align="center"', each):
    #     pass
    if re.search("(TCG)",each) and re.search("background:#FFFFFF",each):
        holder=each.split("<tr>")
        asdf.append(holder)
        del_ctr = 0
    
        for i in range (len(holder)):
            if re.search('text-align:left; color',holder[i-del_ctr]):
                print(holder[i-del_ctr] + "wtf")
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
            asdf.append(holder[i].split('title='))
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