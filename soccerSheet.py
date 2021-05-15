# ~~~~~~~~~~~~~~~~~~~~~~~~~~   Importing Packages    ~~~~~~~~~~~~~~~~~~~~~~~~~~
try:
    from googlesearch import search
    import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    
    import requests
    import time
    import numpy as np
    import datetime
    import pandas as pd
except ImportError:
    print("Import Error")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~   Finding URLs    ~~~~~~~~~~~~~~~~~~~~~~~~~~
def findID(name):
    query = "WhoScored.com"
    teamIDs = []
    for i in name:
        httpsLink = [j for j in search(query+i, num=1, stop=1, pause=1)][0]
        teamIDs += [httpsLink] #gets relevant team https to whoscored.com
        print(httpsLink)
    return teamIDs

# ~~~~~~~~~~~~~~~~~~~~~~~~~~   Finding Elements    ~~~~~~~~~~~~~~~~~~~~~~~~~~

#               ~~~~~~~~~~~~~~~~~~ Finished ~~~~~~~~~~~~~~~~~~~~~~~~
    
def find_shots(browserElement):
    WebDriverWait(browserElement, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="team-squad-stats-options"]/li[5]/a'))).click()
    WebDriverWait(browserElement, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subcategory"]'))).click()
    WebDriverWait(browserElement, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subcategory"]/option[3]'))).click()
    time.sleep(10)
    #multiple selections in this pathway
    shots_on_target = browserElement.find_elements_by_class_name('shotOnTarget')
    shots_on_target_values = [i.text for i in shots_on_target[1:]]#first element is title string and we use float to make sure we can sum later
    
    total_shots = browserElement.find_elements_by_class_name('shotsTotal')
    total_shots_values = [i.text for i in total_shots[1:]]#first element is title string and we use float to make sure we can sum later
    
    players = []
    for i in range(1,len(total_shots)):
        playing = browserElement.find_elements(By.XPATH, '//*[@id="player-table-statistics-body"]/tr['+str(i)+']/td[1]/a')
        players += [(playing[-1].text).split("\n")[1]]
    return [shots_on_target_values,total_shots_values, players]
    
def find_fouls(browserElement):
    WebDriverWait(browserElement, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]'))).click()
    WebDriverWait(browserElement, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]/optgroup[1]/option[3]'))).click()
    time.sleep(5)
    #multiple selections in this pathway
    fouls_committed = browserElement.find_elements_by_class_name('foulCommitted')
    fouls_committed_values = [i.text for i in fouls_committed[1:]] #first element is title string and we use float to make sure we can sum later
    
    fouls_given = browserElement.find_elements_by_class_name('foulGiven')
    fouls_given_values = [i.text for i in fouls_given[1:]]#first element is title string and we use float to make sure we can sum later
    
    time_played = browserElement.find_elements_by_class_name('minsPlayed')
    time_played_values = [i.text for i in time_played[1:]]#first element is title string and we use float to make sure we can sum later
    indexing = [1 if i =='Mins' else 0 for i in time_played_values]
    time_played_values = [i for i in time_played_values[indexing.index(1)+1:]]
    
    return [fouls_committed_values,fouls_given_values,time_played_values]

def find_cards(browserElement):
    WebDriverWait(browserElement, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]/optgroup[1]/option[4]'))).click()
    time.sleep(5)
    yellows = browserElement.find_elements_by_class_name('yellowCard')
    indexing = [1 if i.text=='Yellow' else 0 for i in yellows]
    yellow_card_values = [i.text for i in yellows[indexing.index(1)+1:]]
    
    reds = browserElement.find_elements_by_class_name('redCard')
    indexing = [1 if i.text=='Red' else 0 for i in reds]
    red_card_values = [i.text for i in reds[indexing.index(1)+1:]]

    return [yellow_card_values,red_card_values]

#               ~~~~~~~~~~~~~~~~~~ Unfinished ~~~~~~~~~~~~~~~~~~~~~~~~

def find_number_of_leagues(browserElement):
    class_name = 'tournament-link iconize iconize-icon-left'
    table_element = browserElement.find_elements_by_class_name(class_name)
    table_names = [i.text for i in table_element]
    league_number = len(table_names)
    return league_number

def last_five_games(browserElement):
    table = browserElement.find_element_by_id('team-fixtures-summary')
    team_Goals = table.find_element_by_id
    return table.page_source
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~   Running the Driver    ~~~~~~~~~~~~~~~~~~~~~~~~~~

def generateExcel(df,name):
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=True, header=True):
        ws.append(r)
    wb.save(name + "sheet.xlsx")
    
def runChromeWhoScored(url,name):
    # start web browser
    browser=webdriver.Chrome()

    # get source code
    browser.get(url)
    time.sleep(2)
    
    #pull each desired variable with the functions above
    shots = find_shots(browser)
    time.sleep(np.random.rand()*10) #need to wait a little in case it raises concern
    foul = find_fouls(browser)
    time.sleep(np.random.rand()*10) #need to wait a little in case it raises concern
    cards = find_cards(browser)
    
    #get the output ready
    on_target = shots[0]
    total = shots[1]
    
    fouls = foul[0]
    fouled = foul[1]
    
    yellow_cards = cards[0]
    red_cards = cards[1]
    
    player = shots[2]
    minsPlayed = foul[2]
    
    print(player, minsPlayed, len(player), len(minsPlayed), len(on_target))
    df = pd.DataFrame({'Players':player, 'Shots On Target per Game':on_target, 'Total Shots per Game':total, 'Fouls per Game':fouls, 'Fouled per Game':fouled, 'Yellow Cards per Game':yellow_cards, 'Red Cards per Game':red_cards, 'Mins Played Total':minsPlayed})
    
    # close web browser
    print(df)
    generateExcel(df,name)
    browser.close()
    return 'Done'


'''name = ['PSG','Arsenal']
for i in range(len(name)):'''

name = ['Arsenal']
print(runChromeWhoScored(findID(name)[0],name[0]))


