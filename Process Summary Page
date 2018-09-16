# Production Script

import requests, os
from bs4 import BeautifulSoup as bs

import pandas as pd

#os.chdir() ## Make sure to enter the directory you want the program to populate the csv in

def pageCompare(ID):
    # Goal here is to plug this function into a loop for the range to copy records of all businesses 
    # available through the business entity search portal.
    
    baseLink = 'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?ID='
    
    response = requests.get(baseLink + str(ID))
    soup = bs(response.text, 'lxml')
    message = soup.find(id = "MainContent_lblMessage")
    
    if message is None:
        return soup

def page_parse(page):
    
    catch = dict.fromkeys(Column_IDs, [])
    
    for ID in Column_IDs:
        catch[ID]= page.find(id=ID)
        try:
            catch[ID] = catch[ID].get_text()
        except:
            pass
    return catch

Column_IDs = [
    'MainContent_lblEntityName',
    'MainContent_lblIDNumberHeader',
    'MainContent_lblEntityType',
    'MainContent_lblOrganisationDate',
    'MainContent_lblTerm',
    'MainContent_lblMostRecentAnnualReportYear',
    'MainContent_lblTerm',
    'MainContent_lblInactiveDateLabel',
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
# Little bit of sampling done by me suggests that all IDs are in this 8mil to 9mil range. 

blank_df = pd.DataFrame([],columns = Column_IDs).to_csv('Lara_records_2.csv')

for page in range(800000000,900000000):
    page_ID = pageCompare(page)
    
    if page_ID is not None:
            #page_IDs = [x for x in good_IDs if x is not None] # dont' like this it is HACKY
        
        foo = page_parse(page_ID)
        
        #output = {}
    
        #for k in foo[0].keys():
         #   output[k] = [x[k] for x in foo]
        
        df = pd.DataFrame(foo, index = [foo['MainContent_lblIDNumberHeader']])
    
        with open('Lara_records_2.csv', 'a') as f:
            df.to_csv(f, header=False)
