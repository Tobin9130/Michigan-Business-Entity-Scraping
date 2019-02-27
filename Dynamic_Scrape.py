
import os, time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd

# I put the chrome drive in the Selenium module's directory on my local machine. 
path = '' # Path to where you put the driver of choice, I used chrome.

driver = webdriver.Chrome(path)

def pageCompare(ID):
    # Goal here is to plug this function into a loop for the range described above to copy records of all businesses 
    # available through this portal.
    
    # With adding the dynamic setup, I think this would be the best opportunity to grab all of the filings pages and potential assumed names pages. 
    
    baseLink = 'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?ID='
    
    driver.get(baseLink+ID)
    soup = bs(driver.page_source, 'lxml')
    message = soup.find(id = "MainContent_lblMessage")
    filings_button = driver.find_element_by_id('MainContent_btnViewFilings')
    filings_button.click()
    filing_soup = bs(driver.page_source, 'lxml')
    
    if message is None:
        return soup, filing_soup

def page_parse(page):
    # create empty dict with needed keys(columns)
    # append to main page csv
    
    catch = dict.fromkeys(Column_IDs, [])
    
    for ID in Column_IDs:
        catch[ID]= page.find(id=ID)
        try:
            catch[ID] = catch[ID].get_text()
        except:
            pass
    df = pd.DataFrame(catch, index = [catch['MainContent_lblIDNumberHeader']],columns = Column_IDs)
    
    with open('Lara_records_Ordered.csv', 'a') as f:
        df.to_csv(f, header=False)

def Officer_parse(page):
    # builds a separate table for officers
    
    # Grabs the html table - if it's there
    tble = page.find(id = 'MainContent_grdOfficers')#'MainContent_tblOfficers') # MainContent_grdOfficers grid #
    
    rows = []
    for x in tble.find_all('tr'):
        cell =[cell.get_text() for cell in x.find_all('td')]
        rows.append(cell)
    
    # purge any empty rows
    rows = [x for x in rows if len(x) > 0]
    
    # put records into DF
    df = pd.DataFrame.from_records(rows, columns = ['Title', 'Name', 'Address'])
    
    # Add Corp ID to every row in this DF
    ID = page.find(id='MainContent_lblIDNumberHeader').get_text()
    df['CorpID'] = ID
    
    with open('Lara_officers_Ordered.csv', 'a') as f:
            df.to_csv(f, header=False)    


Column_IDs = [
    'MainContent_lblEntityName',
    'MainContent_lblIDNumberHeader',
    'MainContent_lblEntityType',
    'MainContent_lblOrganisationDate',
    'MainContent_lblTerm',
    'MainContent_lblMostRecentAnnualReportYear',
    'MainContent_lblTerm',
    'MainContent_lblInactiveDate',
    'MainContent_tdRevivalDateText',
    'MainContent_tdInactiveDate',
    'MainContent_lblMostRecentAnnualReportWithOfficersAndDirectors',
    'MainContent_lblResidentAgentName',
    'MainContent_lblResidentStreet',
    'MainContent_lblaptsuiteother',
    'MainContent_lblResidentCity',
    'MainContent_lblResidentState',
    'MainContent_lblResidentZip',
    'MainContent_trConfPrinciple',
    'MainContent_lblPrincipleStreet',
    'MainContent_lblaptsuiteotherlblpricipal',
    'MainContent_lblPrincipleCity',
    'MainContent_lblPrincipleState',
    'MainContent_lblPrincipleZip',
    'MainContent_lblActsFormedUnder',
    'MainContent_lblSum',
    'MainContent_txtComments'
]

# Ok here is the meat and potatoes
pd.DataFrame([],columns = Column_IDs).to_csv('Lara_records_Ordered.csv')
pd.DataFrame([],columns = ['Title', 'Name', 'Address', 'CorpID']).to_csv('Lara_officers_Ordered.csv')

Begin = 800000001

while Begin <= 800001000:
    # Set the begin at the ID we want to start at then rename that ID after every connection failure
    
    try:
        
        for page in range(Begin,800001000):
            page_ID, filings_page = pageCompare(str(page))
            
            if page_ID is not None:
                
                foo = page_parse(page_ID)
                
                if page_ID.find(id = 'MainContent_grdOfficers') is not None:
                    Officer_parse(page_ID)
                
                time.sleep(.25) # Added cause manners count. Embedded only where we are actually saving info.
        
    except:
        print('It failed')
        break
    
    if Begin == pd.read_csv('Lara_records_Ordered.csv').tail(1)['MainContent_lblIDNumberHeader'].item():
        # looks like due to my using of range and while in conjunction, there is an overlap where the two loops begin and end. This will generate som DUPLICATE entries to look into purging.
        
        print('Broke on index check')
        break
    else:
        Begin = pd.read_csv('Lara_records_Ordered.csv').tail(1)['MainContent_lblIDNumberHeader'].item()
    print(Begin)
