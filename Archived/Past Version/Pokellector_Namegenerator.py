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
    
    iconset = soup.find_all(class_="icon set")
    for each in iconset:
        each = str(each)
        holder1 = each.split('"/>')
        holder2 = holder1[1].split('</h1')
        seriesname = holder2[0]

    plaque = soup.find_all(class_= "plaque")
    namelist = []
    IDlist = []
    pattern1 = r"<div class="
    pattern2 = r'"plaque">'
    pattern3 = r'#\d+ - '
    pattern35 = r' - '
    pattern4 = r'</div>'
    for line in plaque:
        line = str(line) #string conversion from tag
        #changing tag
        line = re.sub(pattern1,'',line) 
        line = re.sub(pattern2,'',line)
        #matching ID with "#<digit> - " format
        ID = re.match(pattern3,line)
        if ID:
            ID = ID.group(0) #returning the matched string which is the actual ID
            ID = re.sub(pattern35,'', ID)
            IDlist.append(ID)
        line = re.sub(pattern3,'',line)
        line = re.sub(pattern4,'',line)
        namelist.append(str(line))
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