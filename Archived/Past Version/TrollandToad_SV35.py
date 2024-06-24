import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def SV35_main():
    fulllist = []
    for i in range(1,4):
        url = 'https://www.trollandtoad.com/scarlet-violet-151-reverse-holo-singles/19702?Keywords=&page-no='+str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        parsedlist = soup.find_all(class_="row position-relative align-center py-2 m-auto")
        for each in parsedlist:
            fulllist.append(each)
    print(len(fulllist))

if __name__ == "__main__":
    SV35_main()