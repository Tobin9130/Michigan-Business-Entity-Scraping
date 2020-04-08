library(DBI)
library(ggplot2)
library(ggthemes)

# Using one Dir higher as we're still building
setwd('C:/Users/Sean Tobin/Documents/Data backups')

con <- dbConnect(RSQLite::SQLite(), "___LaraScrape___.sqlite")

# Get list of tables
dbListTables(con)

# get list of fields in table
dbListFields(con, "LaraBusinessClean")
#dbListFields(con, "LaraOfficers")

QUERY <- "SELECT 
            EntityType,
            ID_Number,
            Org_year,
            MostRecentAnnualReportYear as Recent_Rept,
            Inact_year
          FROM LaraBusinessClean;"

# Different Querying method
results2 <- dbGetQuery(con, QUERY)

# Disconnect from DB
dbDisconnect(con)

# getiing data
head(results2)

# Convert character vector to numeric vector
results2$Org_year <- as.numeric(results2$Org_year)
results2$Inact_year <- as.numeric(results2$Inact_year)
results2$Recent_Rept <- as.numeric(results2$Recent_Rept)
results2$ID_Number <- as.numeric(results2$ID_Number)

# Check NA
sum(is.na(results2$Org_year))     # 1,685,435 values not NA
sum(is.na(results2$Inact_year))   # 1,269,518 values active
sum(is.na(results2$Recent_Rept))  # 819,403 values active
sum(is.na(results2$ID_Number))    # 1,685,437 values active

# Test Correlations between Org Year and ID_Number
cor(results2$ID_Number, results2$Org_year, use = 'complete.obs')

my_scatter <- ggplot(results2, aes(x=ID_Number, y=Org_year, color=EntityType)) + 
  geom_point()  
  #legend.position = "none"

# Get just Legend

my_scatter
