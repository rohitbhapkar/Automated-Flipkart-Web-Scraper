#-----------Automated Flipkart Web scraper----------
# -------Code By : Rohit Bhapkar ------------

#Read the readme for necessary installations

#Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# create instance from chrome webdriver
os.environ['PATH'] += r'C:\Users\Rohit Bhapkar\Desktop\Testing\Flipkart login automation'
driver = webdriver.Chrome()


pwd = "" #Enter password for login
mobile_number = 123456789  #Enter your own mobile number but should be registered on flipkart

#function for logging in the website
def login():
    driver.get('https://www.flipkart.com/account/login?ret=/') #login Url
    number = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[1]/input')
    number.send_keys(mobile_number)

    password = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[2]/input')
    password.send_keys(pwd)
    
    submit = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div[2]/div/form/div[4]/button')
    submit.click()

    time.sleep(3)

#function to search for the laptops 
def search_laptops():
    laptop = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input')
    laptop.send_keys("laptops")
    
    laptop_search = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/button')
    laptop_search.click()

# function to scrape data 
def scrape_info():
    link = 'https://www.flipkart.com/search?q=tv&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_8_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_8_0_na_na_na&as-pos=8&as-type=TRENDING&suggestionId=tv&requestId=9c9fa553-b7e5-454b-a65b-bbb7a9c74a29'
    page = requests.get(link)

    #name of product
    soup = bs(page.content, 'html.parser')
    name=soup.find('div',class_="_4rR01T")
    print(name.text)

    ##get rating of a product
    rating=soup.find('div',class_="_3LWZlK")
    print('\n')
    print(rating.text)

    #get other details and specifications of the product
    specification=soup.find('div',class_="fMghEO")
    print(specification)
    specification.text

    #get price of the product
    price=soup.find('div',class_='_30jeq3 _1_WHN1')
    print(price)
    price.text

    products=[]              #List to store the name of the product
    prices=[]                #List to store price of the product
    ratings = []
    apps = []                #List to store supported apps                
    os = []                  #List to store operating system
    hd = []                  #List to store resolution
    sound = []               #List to store sound output

    for data in soup.findAll('div',class_='_3pLy-c row'):
        names=data.find('div', attrs={'class':'_4rR01T'})
        price=data.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
        rating=data.find('div', attrs={'class':'_3LWZlK'})
        specification = data.find('div', attrs={'class':'fMghEO'})
        
        for each in specification:
            col=each.find_all('li', attrs={'class':'rgWa7D'})
            app =col[0].text
            os_ = col[1].text
            hd_ = col[2].text
            sound_ = col[3].text

        products.append(names.text) # Add product name to list
        prices.append(price.text) # Add price to list
        apps.append(app)# Add supported apps specifications to list
        os.append(os_) # Add operating system specifications to list
        hd.append(hd_) # Add resolution specifications to list
        sound.append(sound_) # Add sound specifications to list

    #printing the length of list
    print(len(products))
    print(len(prices))
    print(len(apps))
    print(len(sound))
    print(len(os))
    print(len(hd))

    # Convert to dataframe and store in csv
    df=pd.DataFrame({'Product Name':products,'Supported_apps':apps,'sound_system':sound,'OS':os,"Resolution":hd,'Price':prices})
    df.to_csv('products.csv', index=False, encoding='utf-8')

#main driver of program
if __name__ == '__main__':
    login()
    search_laptops()
    scrape_info()

    driver.quit()
