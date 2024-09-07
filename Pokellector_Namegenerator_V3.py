#Version 1
#Created and able to run list to scrape list
#===========================================================
#Version 2
#ID changed to 3 digits format e.g. 1 -> 001, 24 -> 024
#ID changed to include setcount e.g. 001 -> 001/145
#Included query for setcount
#Included rh split for all cards in setcount (before AR)
#===========================================================
#Version 2-1
#Edited to account for sets less than 100 (e.g. xxx/064) done
#Adjusted Capitalization for "Non-Foil", "Reverse Holo" and "Foil" done
#
#To do:
#Adjusted Naming convention following SV4.5 from Sawadeekard website E.g [ENG] SV05 Temporal Forces: 186/162 Iron Leaves ex [Grass] [UR - Ultra Rare] (Foil)
#============================================================
#Version 3 [UPDATE]
#To obtain information through multi webscraping #Test for time

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

def SV35_main():
    url = input("Please type the pokellector link (including https://): ")
    if url[-1] != "/":
        url = url + "/"
        print(url)
    urlflag = False
    while urlflag == False:
        try:
            page = requests.get(url)
            if re.search("/jp.",url):
                engorjap = "[JAP]"
            else:
                engorjap = "[ENG]"
            urlflag = True
        except:
            print("Just copy and paste the website from browser please...\n")
            url = input("Please type the pokellector link (including https://): ")
    soup = BeautifulSoup(page.content,"html.parser")

    print("How big is the set in this series: ")
    setcount = input("e.g. xxx/135 -> type 135, xxx/162 -> type 162\n")
    setcountflag = False
    while setcountflag == False:
        try:
            #Added this to check if input is int
            setcountint = int(setcount)
            setcountflag = True
        except:
            print("\nThis one cannot be the set count lah please...\n")
            print("How big is the set in this series: ")
            setcount = input("e.g. xxx/135 -> type 135, xxx/162 -> type 162\n")

    print("What code would you like to use: ")
    setcode = input("e.g. SV4.5 -> type SV4.5, SWSH09 -> type SWSH09\n")

    timestart = time.time()
    iconset = soup.find_all(class_="icon set")
    for each in iconset:
        each = str(each)
        holder1 = each.split('"/>')
        holder2 = holder1[1].split('</h1')
        seriesname = holder2[0]

    plaque = soup.find_all(class_= "plaque")
    namelist = []
    IDlist = []
    IDcounter = 1
    pattern1 = r"<div class="
    pattern2 = r'"plaque">'
    pattern3 = r'#\d+ - '
    pattern35 = r' - '
    pattern4 = r'</div>'
    for line in plaque:
        line = str(line) #string conversion from tag
        if re.search("ex<",line) == True:
            print(line)
        #changing tag
        line = re.sub(pattern1,'',line) 
        line = re.sub(pattern2,'',line)
        ID = re.match(pattern3, line)
        if ID:
            ID = ID.group(0)  # returning the matched string which is the actual ID
            ID = re.sub(pattern35, '', ID)
            ID = re.sub("#", '', ID)
            #IDlist.append(ID.zfill(3) + "/" + setcount.zfill(3))
        line = re.sub(pattern3, '', line)
        line = re.sub(pattern4, '', line)
        rarity, rh = singlecardinfo(url,line,IDcounter)
        if rarity == "Common":
            rarityplus = "[C - Common]"
            foilstatus = ["(Non-Foil)","(Reverse Holo)"]
        elif rarity == "Uncommon":
            rarityplus = "[U - Uncommon]"
            foilstatus = ["(Non-Foil)", "(Reverse Holo)"]
        elif rarity == "Double Rare":
            rarityplus = "[RR - Double Rare]"
            foilstatus = ["(Foil)"]
        elif rarity == "Illustration Rare":
            rarityplus = "[IR - Illustration Rare]"
            foilstatus = ["(Foil)"]
        elif rarity == "Ultra Rare":
            rarityplus = "[UR - Ultra Rare]"
            foilstatus = ["(Foil)"]
        elif rarity == "Special Illustration Rare":
            rarityplus = "[SIR - Special Illustration Rare]"
            foilstatus = ["(Foil)"]
        elif rarity == "Hyper Rare":
            rarityplus = "[HR - Hyper Rare]"
            foilstatus = ["(Foil)"]
        for i in range(len(foilstatus)):
            fullname = engorjap +" Pokemon " + setcode + f" {seriesname}: " + rarityplus + foilstatus[i]
            namelist.append(fullname)
            IDlist.append(ID.zfill(3) + "/" + setcount.zfill(3))
        IDcounter += 1
#        if re.search("ex<",line) or IDcounter > setcountint: #only 1 set for ex
#            #matching ID with "#<digit> - " format
#            ID = re.match(pattern3,line)
#            if ID:
#                ID = ID.group(0) #returning the matched string which is the actual ID
#                ID = re.sub(pattern35,'', ID)
#                ID = re.sub("#", '',ID)
#                IDlist.append(ID.zfill(3)+"/"+setcount.zfill(3))
#            line = re.sub(pattern3,'',line)
#            line = re.sub(pattern4,'',line)
#            namelist.append(str(line))
#            IDcounter += 1
#        else:
#            # matching ID with "#<digit> - " format
#            ID = re.match(pattern3, line)
#            if ID:
#                ID = ID.group(0)  # returning the matched string which is the actual ID
#                ID = re.sub(pattern35, '', ID)
#               ID = re.sub("#", '', ID)
#                IDlist.append(ID.zfill(3) + "/" + str(setcount))
#                IDlist.append(ID.zfill(3) + "/" + str(setcount))# append twice for rh and non-foil
#            line = re.sub(pattern3, '', line)
#            line = re.sub(pattern4, '', line)
#            namelist.append(str(line) + " (Non-Foil)")
#            namelist.append(str(line) + " (Reverse Holo)")
#            IDcounter += 1
    dict_df = {'ID':IDlist,'Name':namelist}
    dfa = pd.DataFrame(data=dict_df)
    timeend = time.time()
    timetaken = timeend - timestart
    filename = setcode + "_" + seriesname + ".csv"
    return (dfa,filename,timetaken)

def singlecardinfo(url, name, ID):
    rhflag = False
    urlcard = re.sub(' ', '-', name)
    urlcard = re.sub("'", "", urlcard)
    urlcard = url + urlcard + '-Card-' + str(ID)
    page = requests.get(urlcard)
    soup = BeautifulSoup(page.content,"html.parser")
    rare = soup.find_all("div",class_="infoblurb")
    for each in rare:
        each0 = str(each)
        each1 = each0.split("</div>")
        each2 = each1[0].split("</strong>")
        rarity = each2[1].strip()
    rh = soup.find_all("h1")
    for each in rh:
        each = str(each)
        if re.search("Alternate Versions of this Card",each):
            rhflag = True
    return (rarity, rhflag)

if __name__ == "__main__":
    SV35,filename,time = SV35_main()
    print(f"\n{filename}\n")
    #pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(SV35)
    print(f"Time take is {time} seconds.")
#    print(SV35.iloc[1])
#    print(SV35.iloc[111])
    choiceflag = False
    while choiceflag == False:
        choice = input("Do you want this as csv file (Y/N): ")
        if choice.upper() == "Y" or choice.upper() == "YES" or choice.upper() == "YE" or re.match("YES", choice.upper()):
            SV35.to_csv(filename, index=False)
            choiceflag = True
            print("Ho liao...")
        elif choice.upper() == "N" or choice.upper() == "NO" or re.match("NO", choice.upper()):
            print("Okay lor....")
            choiceflag = True
        else:
            print("Can read instructions not...")