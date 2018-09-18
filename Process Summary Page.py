###                     ###
###                     ###
###   Lara business     ###
###      scrape         ###
###                     ###
###                     ###

# By Sean Tobin, MPP. 

# This is meant to replicate the public information as supplied by the Michigan Department of Licensing and Regulatory Affairs. 
#Load it into a database and have fun. I'm building a longitudinal spatial model. There is no warranty with this script. 

import requests, os, time
from bs4 import BeautifulSoup as bs

import pandas as pd

#Add your own Dir here
#os.chdir('')

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

import requests, os, time
from bs4 import BeautifulSoup as bs

import pandas as pd

os.chdir('C:\\Users\\Sean\\Desktop\\Forecasting')

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

blank_df = pd.DataFrame([],columns = Column_IDs).to_csv('Lara_records_Ordered.csv')

for page in range(800000000,900000000):
    page_ID = pageCompare(page)
    
    if page_ID is not None:
        
        foo = page_parse(page_ID)
        
        df = pd.DataFrame(foo, index = [foo['MainContent_lblIDNumberHeader']],columns = Column_IDs)
        
        with open('Lara_records_Ordered.csv', 'a') as f:
            df.to_csv(f, header=False)
        time.sleep(.25) # Added cause manners count
        
    time.sleep(1) # Added cause manners count
    
