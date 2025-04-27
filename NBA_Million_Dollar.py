from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import streamlit as st
#from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

options = Options()
options.headless = True
i=0
j=0
#References the latest version of chromedriver to use 
driver = webdriver.Firefox(options=options)

#driver = webdriver.Chrome('C:\Python\Python310\Web Scrape\chromedriver.exe')
driver.get('https://www.sportsline.com/nba/odds/')
teams = driver.find_elements(By.XPATH, '//div[@data-testid="Team-name"]')
teams = [element.text for element in teams]
odds = driver.find_elements(By.XPATH, '//span[@class="primary"]')
odds = [element.text for element in odds]
payout = driver.find_elements(By.XPATH, '//span[@class="secondary"]')
payout = [element.text for element in payout]
date = driver.find_elements(By.XPATH,"//p[@class='sc-753a78ea-0 sc-753a78ea-1 hvAzLq emdlKR']")
date = [element.text for element in date]
# print(teams)
# print(odds)
# print(payout)
#
driver.quit()
Money_Line=[]
Line=[]
Over_Under=[]
for i in range(0,len(odds),6):
    a=odds[i]
    b=odds[i+1]
    c=odds[i+2]
    Money_Line.append(a)
    Line.append(b)
    Over_Under.append(c)
game_date=[]
for i in range(0,2*len(date),1):
    remainder=i%2
    if remainder==0:
        date[j]=date[j][0:6]
        game_date.append(date[j])
    else:
        game_date.append(date[j])
        j=j+1    
for i in range(len(Over_Under)):
    Over_Under[i]=Over_Under[i][1:]
# print(teams)
# print((game_date))
# print(Money_Line)
# print(Line)
# print(Over_Under)


Bets=[]
for i in range(len(Over_Under)):
     Bets.append("no")


data={'Teams': teams, 'Date': game_date, 'Money Line': Money_Line, 'Line': Line, 'Over/Under': Over_Under, "Chase": Bets, "Cole": Bets, "Fletch": Bets}
df = pd.DataFrame(data)

st.title('NBA Million Dollar Picks')
st.dataframe(df)
