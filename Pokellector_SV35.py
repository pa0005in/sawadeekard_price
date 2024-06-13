import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def SV35_main():
    page = requests.get('https://www.pokellector.com/Scarlet-Violet-151-Expansion/')
    soup = BeautifulSoup(page.content,"html.parser")

    plaque = soup.find_all(class_= "plaque")
    namelist = []
    IDlist = []
    pattern1 = r"<div class="
    pattern2 = r'"plaque">'
    pattern3 = r'#\d+ - '
    pattern35 = r' - '
    pattern4 = r'</div>'
    for line in plaque:
        line = str(line)
        line = re.sub(pattern1,'',line)
        line = re.sub(pattern2,'',line)
        ID = re.match(pattern3,line)
        if ID:
            ID = ID.group(0)
            ID = re.sub(pattern35,'', ID)
            IDlist.append(ID)
        line = re.sub(pattern3,'',line)
        line = re.sub(pattern4,'',line)
        namelist.append(str(line))
    dict_df = {'ID':IDlist,'Name':namelist}
    dfa = pd.DataFrame(data=dict_df)
    return dfa

if __name__ == "__main__":
    SV35 = SV35_main()