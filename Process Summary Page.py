###                     ###
###                     ###
###   Lara business     ###
###      scrape         ###
###                     ###
###                     ###

# This is meant to replicate the public information as supplied by Michigan's Licensing and Regulatory Agency. 


import requests, os, time
from bs4 import BeautifulSoup as bs

import pandas as pd

## os.chdir('')

def pageCompare(ID):
    # Goal here is to plug this function into a loop for the range described above to copy records of all businesses 
    # available through this portal.
    
    baseLink = 'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?ID='
    
    response = requests.get(baseLink + str(ID))
    soup = bs(response.text, 'lxml')
    message = soup.find(id = "MainContent_lblMessage")
    
    if message is None:
        return soup

def page_parse(page):
    
    # create empty dict with needed keys(columns)
    catch = dict.fromkeys(Column_IDs, [])
    
    for ID in Column_IDs:
        catch[ID]= page.find(id=ID)
        try:
            catch[ID] = catch[ID].get_text()
        except:
            pass
    return catch

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

blank_df = pd.DataFrame([],columns = Column_IDs).to_csv('Lara_records_Ordered.csv')
blank_df2 = pd.DataFrame([],columns = ['Title', 'Name', 'Address', 'CorpID']).to_csv('Lara_officers_Ordered.csv')


for page in range(800000000,900000000):
    page_ID = pageCompare(page)
    
    if page_ID is not None:
        
        foo = page_parse(page_ID)
        
        if page_ID.find(id = 'MainContent_grdOfficers') is not None:
            Officer_parse(page_ID)
        
        df = pd.DataFrame(foo, index = [foo['MainContent_lblIDNumberHeader']],columns = Column_IDs)
        
        with open('Lara_records_Ordered.csv', 'a') as f:
            df.to_csv(f, header=False)
        time.sleep(.25) # Added cause manners count. Embedded only where we are actually saving info.
    
