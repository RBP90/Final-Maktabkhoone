import mysql.connector
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
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
query = 'SELECT * FROM bama'
cursor.execute(query)
results = cursor.fetchall()
df = pd.DataFrame(results, columns=["Name", "Year", "Kilometers", "City", "Price"])

le_name = LabelEncoder()
le_city = LabelEncoder()

df['Name'] = le_name.fit_transform(df['Name'])
df['City'] = le_city.fit_transform(df['City'])
df['Year'] = df.apply(lambda row: row['Year'] if row['Year'] >= 1900 else solar_to_georgian(row['Year'], 1, 1), axis=1)

#print(df)

x = []
y = []
for index, row in df.iterrows():
    x.append([row['Name'], row['Year'], row['Kilometers'], row['City']])
    y.append(row['Price'])
clf = tree.DecisionTreeRegressor()
clf = clf.fit(x, np.ravel(y))

name = input("Name: ")
encoded_name = le_name.transform([name])[0]

year = int(input("Year: "))
if year >= 1900:
    input_year = year
else:
    input_year = solar_to_georgian(year, 1, 1)

kilometers = int(input("Kilometers: "))
city = input("city: ")
encoded_city = le_city.transform([city])[0]

input_values = [[encoded_name, input_year, kilometers, encoded_city]]
#print (input_values)

prediction = clf.predict(input_values)
print("Predicted price:", prediction[0])