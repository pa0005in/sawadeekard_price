# Scrape to Update:

## Description:
"Scrape to Update" is a Python script designed to streamline the process of maintaining accurate and competitive prices for Pokémon cards in your Shopify store.  
The script scrapes the latest card prices from specified websites and automatically updates a Shopify-compatible CSV file, ready for upload.  
This ensures your store always reflects current market values, enhancing your inventory management and customer satisfaction.  

![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/48f93e33-c817-4d44-bbbb-33b65d7d7372)

The script uses Python's library such as Pandas, Regular Expression, requests and BeautifulSoup4 to scrape, search and update the CSV file.  

## Scripts  
__Menu display.py__  
This main script contains an object oriented controller as menu, with each set called upon as a class.  
The script can be used after cloning in any software with Python interpreter.  
There is an option to not use the Shopify CSV file update feature and a simple CSV file will be generated containing ID, Name and Price.  
In order to use the Shopify CSV file update feature, it must be included into the same folder as the script.  

__Pokellector_Namegenerator.py (additional)__  
This additional script scrapes the list of names provided from the website Pokellector.com.  
The script can be used after cloning in any software with Python interpreter.  
The script will generate a CSV file containing ID and Name, and multiples will be created for cards with Reverse Holo option.  
In order to use the script, copy and paste the link directly from the webpage bar and include the last card within the set.  

## Requirements
Any python environment with interpreter can run the script.  

However, certain libraries have to be installed beforehand.  

__BeautifulSoup4__
```
pip install beautifulsoup4
```

__requests__
```
pip install requests
```

__Regular Expression__
```
pip install regex
```

## Features
### Menu
The main script is designed using Object Oriented Programming with a simple menu design.  
  
This is the initial options to choose between English and Japanese sets.  
![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/72353abc-20fd-47a6-829a-e3a026acd8ee)  
  
If option 2 was chosen, options for English sets will be listed.  
![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/e033194b-07f0-49fe-bb7e-2345a5326cf4)  
  
As of the current design, you can choose the options by typing the option number on the left when prompted.  
In this scenario, "00" is the option to run all of the listed set consecutively.  
Once you have chosen the sets, another prompt will ask if the CSV file for the chosen set exists.  
![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/dae4aa21-a881-47d3-aa0a-3054b0f5a402)  
If the CSV file does not exist, a simple CSV file containing the ID, Name and USD price will be generated as demo instead.  
Once all options are entered, the program will run starting.  

### Shopify CSV file update
The main script will look for the CSV within the same folder to read and update.  
Once the Shopify CSV file has been found, the script will match the scraped data with the corresponding entry within the Shopify data and update accordingly.  
When the update has been commpleted, a new CSV file will be generated with the name "xxxx_english/japanese Shopify yy:mm:dd" (e.g. SV04_english Shopify 240601").
  
A changelog will also be generated with 3 columns \["Before","Change","After"\] with the name "Changelog xxxx_english/japanese".  
![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/9ca1bc29-981d-4b3a-9d86-64a9ff633585)  
The changelog records the prices changed within the CSV file to let the user be aware of the price changes.  
The user can then change the updated CSV file if he is not satisfied with the price change.  

## Future Roadmap  
__1) Inserting older series such as Sword and Shield Series__  
  This series has a few sets with additional cards known separately as Galarian Gallery (GG) or Trainer Gallery (TG).  
  To properly identify and include them into the set list during scraping.  

__2) Holo Energy with no ID number tagged__  
  Troll and Toad did not provide ID number in the names of specific Energy cards when it should be included.  
  Alternatives will be considered on how to include them into the set list.  
  
## Past Issues (Resolved)
__1) The website may change its format due to inventory audit, out of stock or minor mistakes.__  
  Future updates will include checks or more error exception to ensure the script is still able to run or alternatives are included.  
  Current issues encountered:  
  Inclusive of Promo cards (Fixed in Version 1.4)  
  ![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/704bc55f-bfcb-43e5-8f60-65e8b2d41e3e)  
  Separate version of card ID in SV3.5 (Fixed for SV3.5 in Version 1.4)  
  ![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/9181c5da-5b3b-46a4-8d21-cdbdf15391d8)  
  Duplicated entries from website  
  ![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/98d154c8-785c-407b-8974-50b36b37f89c)  
  Inventory audit  
  ![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/4485c1f1-1ddb-4622-9e26-02c32485ce05)  
  Galar Gallery (#GG0x) and Trainer Gallery (#TG0x) cannot be read by the script  
  ![image](https://github.com/pa0005in/sawadeekard_price/assets/142402904/a0da95e0-7ac4-4826-b1a7-336d002d9bf4)  
  __Resolved in Version 2.0__  
  Current solution will remove the repeated entry upon detection by checking for the same ID and Title.  
  The removed entry will be declared and printed out to let the user know that a repeated entry was detected.  
  For items that do not have a price due to inventory audit, the price will remain as per previous pricing.  
  
__2) The codes for each series is an individual class.__  
  Future version can simplify the entire code to a single parent to simplify the code for checking and running.  
  ___Resolved in Version 2.0__  
  Currently all Scarlet Violet Series will be able to use the same parent code with minor changes to url, number of pages for each series and string containing the set name to replace.  

## Acknowledgements  
This script was just a passion project after learning how to do webscraping through Python using BeautifulSoup4.  
I would like to thank my mentors for the guidance on using OOP to create a controller and to use BS4.  
