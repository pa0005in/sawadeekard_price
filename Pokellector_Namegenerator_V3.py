#Version 1
#Created and able to run list to scrape list
#===========================================================
#Version 2
#ID changed to 3 digits format e.g. 1 -> 001, 24 -> 024
#ID changed to include setcount e.g. 001 -> 001/145
#Included query for setcount
#Included rh split for all cards in setcount (before AR)
#===========================================================
#Version 3
#Edited to account for sets less than 100 (e.g. xxx/064) done
#Adjusted Capitalization for "Non-Foil", "Reverse Holo" and "Foil" done
#Adjusted Naming convention following SV4.5 from Sawadeekard website E.g [ENG] SV05 Temporal Forces: 186/162 Iron Leaves ex [Grass] [UR - Ultra Rare] (Foil)

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def SV35_main():
    url = input("Please type the pokellector link (including https://): ")
    urlflag = False
    while urlflag == False:
        try:
            page = requests.get(url)
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
            setcountholder = int(setcount)
            setcountflag = True
        except:
            print("\nThis one cannot be the set count lah please...\n")
            print("How big is the set in this series: ")
            setcount = input("e.g. xxx/135 -> type 135, xxx/162 -> type 162\n")

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
        if re.search("ex<",line) or IDcounter > setcount: #only 1 set for ex
            #matching ID with "#<digit> - " format
            ID = re.match(pattern3,line)
            if ID:
                ID = ID.group(0) #returning the matched string which is the actual ID
                ID = re.sub(pattern35,'', ID)
                ID = re.sub("#", '',ID)
                IDlist.append(ID.zfill(3)+"/"+str(setcount))
            line = re.sub(pattern3,'',line)
            line = re.sub(pattern4,'',line)
            namelist.append(str(line))
            IDcounter += 1
        else:
            # matching ID with "#<digit> - " format
            ID = re.match(pattern3, line)
            if ID:
                ID = ID.group(0)  # returning the matched string which is the actual ID
                ID = re.sub(pattern35, '', ID)
                ID = re.sub("#", '', ID)
                IDlist.append(ID.zfill(3) + "/" + str(setcount))
                IDlist.append(ID.zfill(3) + "/" + str(setcount))# append twice for rh and non-foil
            line = re.sub(pattern3, '', line)
            line = re.sub(pattern4, '', line)
            namelist.append(str(line) + " (Non-Foil)")
            namelist.append(str(line) + " (Reverse Holo)")
            IDcounter += 1
    dict_df = {'ID':IDlist,'Name':namelist}
    dfa = pd.DataFrame(data=dict_df)
    return (dfa,seriesname)

if __name__ == "__main__":
    SV35,filename = SV35_main()
    filename = filename +".csv"
    print(f"\n{filename}\n")
    print(SV35)
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