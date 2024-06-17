import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def SV6_main():
    pricelist = []
    namelist = []
    IDlist = []
    datalist = []
    for i in range(1,4):
        url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19895?Keywords=&page-no='+str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content,"html.parser")
        price = soup.find_all('div',class_="product-col col-12 p-0 my-1 mx-sm-1 mw-100")
        for each in price:
            each = str(each)
            priceholder0 = re.split("col-2 text-center p-1",each)
            priceholder1 = re.split(">",priceholder0[3])
            priceholder2 = re.split("<",priceholder1[1])
            priceholder3 = priceholder2[0].replace("$","")
            priceholder3 = priceholder3.strip()
            pricelist.append(priceholder3)
        name = soup.find_all('a',class_="card-text")
        for each in name:
            each = str(each)
            nameholder1 = re.split(">",each)
            nameholder2 = re.split("<",nameholder1[1])
            nameholder3 = re.split("- ",nameholder2[0])
            namelist.append(nameholder3[0].strip())
            IDlist.append(nameholder3[1].strip())
    return namelist,IDlist
        #     if re.search("button",each):
        #         pass
        #     elif re.search("Price",each):
        #         pass
        #     elif re.search("Quantity",each):
        #         pass
        #     else:
        #         each = each.replace('<div class="col-2 text-center p-1">',"")
        #         each = each.replace('</div>',"")
        #         pricelist.append(each)
        # name = soup.find_all('a',class_="card-text")
        # for each in name:
        #     each = str(each)
        #     nameholder1 = re.split(">",each)
        #     nameholder2 = re.split("<",nameholder1[1])
        #     nameholder3 = re.split("- ",nameholder2[0])
        #     namelist.append(nameholder3[0].strip())
        #     IDlist.append(nameholder3[1].strip())
    # df_sv6_rh = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
    # df_sv6_rh.sort_values(["ID"], ascending=True, inplace=True)
    # df_sv6_rh.reset_index(drop = True,inplace=True)
    
    # pricelist = []
    # namelist = []
    # IDlist = []
    # for i in range(1,5):
    #     url = 'https://www.trollandtoad.com/pokemon/scarlet-violet-temporal-forces/19897'+str(i)
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content,"html.parser")
    #     price = soup.find_all('div',class_="col-2 text-center p-1")
    #     for each in price:
    #         each = str(each)
    #         if re.search("button",each):
    #             pass
    #         elif re.search("Price",each):
    #             pass
    #         elif re.search("Quantity",each):
    #             pass
    #         else:
    #             each = each.replace('<div class="col-2 text-center p-1">',"")
    #             each = each.replace('</div>',"")
    #             pricelist.append(each)
    #     name = soup.find_all('a',class_="card-text")
    #     for each in name:
    #         each = str(each)
    #         nameholder1 = re.split(">",each)
    #         nameholder2 = re.split("<",nameholder1[1])
    #         nameholder3 = re.split("- ",nameholder2[0])
    #         namelist.append(nameholder3[0].strip())
    #         IDlist.append(nameholder3[1].strip())
    # df_sv6_singles = pd.DataFrame({"ID": IDlist, "Name": namelist, "Price in USD": pricelist})
    # df_sv6_singles.sort_values(["ID"], ascending=True, inplace=True)
    # df_sv6_singles.reset_index(drop = True,inplace=True)
    # return(df_sv6_rh,df_sv6_singles)

if __name__ == "__main__":
    # tnt_rh,tnt_singles = 
    name,ID = SV6_main()
    # b = pickle.dumps(a)
    # c = pickle.loads(b)