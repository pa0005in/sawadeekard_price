# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:53:21 2024

@author: khin_
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

url = input("Please type the bulbapedia link (including https://): \n")
urlflag = False
while urlflag == False:
    try:
        page = requests.get(url)
        urlflag = True
    except:
        print("Just copy and paste the website from browser please...\n")
        url = input("Please type the bulbapedia link (including https://): ")
setcode = input("What is the code for this set: e.g. SV3.5 or SWSH11\n")
soup = BeautifulSoup(page.content,"html.parser")

data = soup.find_all("table",class_="roundy")
tbl_round = []
jap={}
eng={}
raw_data ={}
df_dict = {}
setnameen = ""
setnamejp = ""
tablename = ""

def myfunc(e):
    return len(e)

for each in data:
    if re.search("Rarity",str(each)):
        if re.search("Additional Cards",str(each)):
            pass
        else:
            tbl_round.append(str(each))
    
tbl_round.sort(key=len,reverse = True)

if len(tbl_round) == 2:
    if re.search("Illustration Rare",tbl_round[0]):
        eng[0] = tbl_round[0]
        jap[0] = tbl_round[1]
    elif re.search("AR", tbl_round[0]):
        jap[0] = tbl_round[0]
        eng[0] = tbl_round[1]
elif len(tbl_round) >2:
    for i in range(len(tbl_round)):
        if re.search("AR",tbl_round[i]):
            if len(jap)==0:
                jap[0]=tbl_round[i]
            elif len(jap)>0:
                jap[1]=tbl_round[i]
        if re.search("Illustration Rare",tbl_round[i]):
            eng[0]=tbl_round[i]
                
df_merged = pd.DataFrame(columns=['ID', 'Mark','Name', 'Type','Rarity'])
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
        #re.search ('ex') and re.search ('Basic' and 'Energy') is for pokemon and energy cards respectively
        #therefore not required to have the check for I, St, Su and PT types
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
                if new_row['Type'] == 'I':
                    new_row['Type'] = 'Item'
                elif new_row['Type'] == 'St':
                    new_row['Type'] = 'Stadium'
                elif new_row['Type'] == 'Su':
                    new_row['Type'] = 'Support'
                elif new_row['Type'] == 'PT':
                    new_row['Type'] = 'Pokemon Tool'
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
                if new_row['Type'] == 'I':
                    new_row['Type'] = 'Item'
                elif new_row['Type'] == 'St':
                    new_row['Type'] = 'Stadium'
                elif new_row['Type'] == 'Su':
                    new_row['Type'] = 'Support'
                elif new_row['Type'] == 'PT':
                    new_row['Type'] = 'Pokemon Tool'
                new_row = pd.DataFrame(new_row, index=[0])
                df_merged = pd.concat([df_merged, new_row], ignore_index=True)                    
    finallist = []
    for i in range(len(df_merged)):
        if df_merged.iloc[i,4] == 'Common':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [C - Common] (Non-foil)")
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [C - Common] (Reverse Holo)")
        elif df_merged.iloc[i,4] == 'Uncommon':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [U - Uncommon] (Non-foil)")
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [U - Uncommon] (Reverse Holo)")
        elif df_merged.iloc[i,4] == 'Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [R - Rare] (Foil)")
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [R - Rare] (Reverse Holo)")
        elif df_merged.iloc[i,4] == 'Double Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [RR - Double Rare] (Foil)")
        elif df_merged.iloc[i, 4] == 'ACE SPEC Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i, 0]} {df_merged.iloc[i, 2]} [{df_merged.iloc[i, 3]}] [AS - ACE SPEC] (Foil)")
        elif df_merged.iloc[i,4] == 'Shiny Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [SR - Shiny Rare] (Foil)")
        elif df_merged.iloc[i,4] == 'Ultra Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [UR - Ultra Rare] (Foil)")
        elif df_merged.iloc[i,4] == 'Illustration Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [IR - Illustration Rare] (Foil)")
        elif df_merged.iloc[i,4] == 'Special Illustration Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [SIR - Special Illustration Rare] (Foil)")
        elif df_merged.iloc[i,4] == 'Hyper Rare':
            finallist.append(f"[ENG] Pokemon {setcode} {tablename}: {df_merged.iloc[i,0]} {df_merged.iloc[i,2]} [{df_merged.iloc[i,3]}] [HR - Hyper Rare] (Foil)")
        
    final_df = pd.DataFrame(data = finallist,columns = ['Name'])
    df_dict[tablename]=final_df

# choiceflag = False
# while choiceflag == False:
#     choice = input("Do you want the Japanese sets as well? (Y/N) ")
#     if choice.upper() == "Y" or choice.upper() == "YES" or choice.upper() == "YE" or re.match("YES", choice.upper()):
#         choiceflag = True
#         choice = 'Y'
#         print("JITPUN LANG LESGO")
#     elif choice.upper() == "N" or choice.upper() == "NO" or re.match("NO", choice.upper()):
#         print("OK no Japanese today!")
#         choiceflag = True
#         choice = 'N'
#     else:
#         print("Can read instructions not...") 

choice = 'N' #remove japanese set function first

if choice == 'Y':
    df_merged = pd.DataFrame(columns=['ID', 'Mark','Name', 'Type','Rarity'])
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
    
for each in df_dict:
    df_dict[each].to_csv(f"{each}.csv",index = False)