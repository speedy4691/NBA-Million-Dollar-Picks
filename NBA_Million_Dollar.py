import streamlit as st
#with st.echo():
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.by import By
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

j=0
i=0

@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
         options=options,
    )

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = get_driver()
@st.cache_resource
def get_data():
    driver.get('https://www.sportsline.com/nba/odds/')
    teams = driver.find_elements(By.XPATH, '//div[@data-testid="Team-name"]')
    odds = driver.find_elements(By.XPATH, '//span[@class="primary"]')
    payout = driver.find_elements(By.XPATH, '//span[@class="secondary"]')
    date = driver.find_elements(By.XPATH,"//div[@class='date']")
    teams = [element.text for element in teams]
    odds = [element.text for element in odds]
    payout = [element.text for element in payout]
    date = [element.text for element in date]
    driver.quit()
    # print(teams)
    # print(odds)
    # print(payout)
    Money_Line=[]
    Line=[]
    Over_Under=[]
    for i in range(0,len(odds),3):
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
            date[j]=date[j][0:5]
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
        Bets.append("$0")


    data={'Teams': teams, 'Date': game_date, 'Money Line': Money_Line, 'Line': Line, 'Over/Under': Over_Under, "Chase": Bets, "Cole": Bets, "Fletch": Bets}
    return pd.DataFrame(data)
df=get_data()
#df = pd.DataFrame(data)

st.title('NBA Million Dollar Picks')
st.write("### Enter Your Picks Here")
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(editable=True)
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    editable=True
)
updated_df = pd.DataFrame(grid_response['data'])

st.write("### Daily Bets")
st.dataframe(updated_df)
    
#st.code(driver.page_source)
