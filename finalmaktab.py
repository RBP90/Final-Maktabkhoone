import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector
import os
password = os.environ.get('MYSQL_PASSWORD')

cnx = mysql.connector.connect(user='root', password=password,
                              host='127.0.0.1',
                              database='maktab')

cursor = cnx.cursor()

driver = webdriver.Chrome()
driver.get("https://bama.ir/car?price=1&mileage=1")

for i in range(1, 100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

brands = soup.find_all('p' , attrs={'class' : 'bama-ad__title'})
details = soup.find_all('div' , attrs={'class' : 'bama-ad__detail-row'})
addresses = soup.find_all('div' , attrs={'class' : 'bama-ad__address'})
prices = soup.find_all('div' , attrs={'class': 'bama-ad__price-holder'})

for brand, detail , address , price in zip(brands,details,addresses,prices):
    gheymat = int(re.sub(r'\s+' , '' , price.text).strip().replace(',', ''))
    name = re.sub(r'\s+' , '' , brand.text).strip()
    area = re.sub(r'\s+' , '' , address.text).strip()
    city = area.split('/')
    info = re.sub(r'\s+' , '' , detail.text).strip()
    info1 = re.findall(r'(\d{4})(\d+\,\d{3})' , info)
    if len(info1) >= 1:
        year1 , kilometers = info1[0]
        year = int(year1)
        kilometers = int(kilometers.replace(',', ''))
    #print (gheymat , name , city[0] , year , kilometers)

    query = 'INSERT IGNORE INTO bama (Name, Year, Kilometers, City, Price) VALUES (%s, %s, %s, %s, %s)'
    values = (name, year, kilometers, city[0], gheymat)
    cursor.execute(query , values)
cnx.commit()

cnx.close()
