import mysql.connector
from sklearn import tree
import pandas as pd
import numpy as np
import datetime

def solar_to_georgian(year, month, day):
    gregorian_date = datetime.date.fromisocalendar(year + 621, month, day)

    gregorian_year = gregorian_date.year

    return gregorian_year

cnx = mysql.connector.connect(user='root', password='reza6678232',
                              host='127.0.0.1',
                              database='maktab')

cursor = cnx.cursor()
car_brand = input('Car Name: ')
query = f"SELECT * FROM bama WHERE Name = '{car_brand}'"
cursor.execute(query)
results = cursor.fetchall()
df = pd.DataFrame(results, columns=["Name", "Year", "Kilometers", "City", "Price"])
df['Year'] = df.apply(lambda row: row['Year'] if row['Year'] >= 1900 else solar_to_georgian(row['Year'], 1, 1), axis=1)

#print(df)

x = []
y = []
for index, row in df.iterrows():
    x.append([row['Year'], row['Kilometers']])
    y.append(row['Price'])
clf = tree.DecisionTreeRegressor()
clf = clf.fit(x, np.ravel(y))


year = int(input("Year: "))
if year >= 1900:
    input_year = year
else:
    input_year = solar_to_georgian(year, 1, 1)

kilometers = int(input("Kilometers: "))

input_values = [[input_year, kilometers]]
#print (input_values)

prediction = clf.predict(input_values)
print("Predicted price:", prediction[0])