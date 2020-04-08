library(DBI)


# Using one Dir higher as we're still building
setwd('C:/Users/stob1/Desktop/Incremental Detroit/Data projects/Lara_Scrape')

# Create an ephemeral in-memory RSQLite database
# Connect to dummy db
con <- dbConnect(RSQLite::SQLite(), "LaraScrape.sqlite")



# Read Table  - DONT DO IT ON A BIG TABLE - use a query
#dbReadTable(con, "ParcelDetail")

# SEND QUERY & FETCH RESULTS:

# example is large
res <- dbSendQuery(con, "SELECT 
                   count(distinct EntityName)
                   FROM LaraBusiness;")
# went fairly quick?
results1 <- dbFetch(res)

# Comes out as DataFrame
class(results1)

# getiing data
head(results1)

# Clear the result
dbClearResult(res)

# Disconnect from the database
dbDisconnect(con)

################################################### Better method???

library(DBI)

# Using one Dir higher as we're still building
setwd('C:/Users/stob1/Desktop/Incremental Detroit/Data projects')

con <- dbConnect(RSQLite::SQLite(), "LaraScrape.sqlite")

# Get list of tables
dbListTables(con)

# get list of fields in table
dbListFields(con, "LaraBusiness")
dbListFields(con, "LaraOfficers")

# Detroit Metro Zip Codes
ZipCodes <- c(48201,48202,48203,48204,48205,48206,48207,48208,
              48209,48210,48211,48212,48213,48214,48215,48216,
              48217,48218,48219,48220,48221,48222,48223,48224,
              48225,48226,48227,48228,48229,48230,48231,48232,
              48233,48234,48235,48236,48237,48238,48239,48240,
              48242,48243,48244,48255,48260,48264,48265,48266,
              48267,48268,48269,48272,48275,48277,48278,48279,
              48288)

QUERY <- "SELECT 
          EntityType,
          OrganisationDate,
          InactiveDate,
          MostRecentAnnualReportYear
          FROM LaraBusiness
          Where ResidentZip in (48201,48202,48203,48204,48205,48206,48207,48208,
              48209,48210,48211,48212,48213,48214,48215,48216,
              48217,48218,48219,48220,48221,48222,48223,48224,
              48225,48226,48227,48228,48229,48230,48231,48232,
              48233,48234,48235,48236,48237,48238,48239,48240,
              48242,48243,48244,48255,48260,48264,48265,48266,
              48267,48268,48269,48272,48275,48277,48278,48279,
              48288);"

# Different Querying method
results2 <- dbGetQuery(con, QUERY)

# getiing data
head(results2)

results2$OrganisationDate <- as.Date(results2$OrganisationDate,"%d/%m/%Y")
results2$InactiveDate <- as.Date(results2$InactiveDate,"%d/%m/%Y")
results2$MostRecentAnnualReportYear <- as.numeric(results2$MostRecentAnnualReportYear)


hist(results2$MostRecentAnnualReportYear)

str(results2)

library(ggplot2)
library(reshape2)

results <- data.frame(c(results2$OrganisationDate,results2$InactiveDate))
results <- melt(results)

head(results)

ggplot(results2) + 
  geom_density(aes(x = InactiveDate),alpha = 0.25, fill = 'red') +
  geom_density(aes(x=OrganisationDate),alpha = 0.25, fill = 'green') +
  ggtitle('SE MI Business Creation & Completion') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Date of Organization or Inactivation') +
  theme_classic()



ggplot(results,aes(x=value, fill=variable)) + geom_density(alpha=0.25)
ggplot(data,aes(x=value, fill=variable)) + geom_histogram(alpha=0.25)
ggplot(data,aes(x=variable, y=value, fill=variable)) + geom_boxplot()
































QUERY2 <- "SELECT 
EntityName,
EntityType,
OrganisationDate,
InactiveDate,
ResidentZip
FROM LaraBusiness
;"

# Different Querying method
results <- dbGetQuery(con, QUERY2)

# getiing data
head(results)

unique(results$EntityType, incomparables = FALSE)