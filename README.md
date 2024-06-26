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
The main script 
