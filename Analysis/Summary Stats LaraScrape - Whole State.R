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

# Check NA
sum(is.na(results2$Org_year))     # 1,685,435 values not NA
sum(is.na(results2$Inact_year))   # 1,269,518 values active
sum(is.na(results2$Recent_Rept))  # 819,403 values active


XLIM <- c(1975,2019)

# Density Chart of Inactive Vs Org Date + and -
ggplot(results2) + 
  geom_density(aes(x = Inact_year, y = -..density..),alpha = 0.5, fill = 'red') +
  geom_density(aes(x = Org_year, y = ..density..),alpha = 0.5, fill = 'green') +
  coord_cartesian(xlim= XLIM)+
  ggtitle('MI Business Creation & Completion \n 1985 - 2015') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Year of Organization \n or Inactivation') +
  theme_economist()

# Density Chart of Inactive Vs Org Date overlaid
ggplot(results2) + 
  geom_density(aes(x = Inact_year),alpha = 0.5, fill = 'red') +
  geom_density(aes(x = Org_year),alpha = 0.5, fill = 'green') +
  coord_cartesian(xlim= XLIM)+
  ggtitle('MI Business Creation & Completion \n 1985 - 2015') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Year of Organization \n or Inactivation') +
  theme_economist()

XLIM2 <- c(1930,2019)
# Density Chart of Inactive Vs Org Date overlaid 2
ggplot(results2) + 
  geom_density(aes(x = Inact_year),alpha = 0.5, fill = 'red') +
  geom_density(aes(x = Org_year),alpha = 0.5, fill = 'green') +
  coord_cartesian(xlim= XLIM2)+
  ggtitle('MI Business Creation & Completion \n 1930 - 2015') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Year of Organization \n or Inactivation') +
  theme_economist()

XLIM3 <- c(2005,2019)
# Density Chart of Inactive Vs Org Date overlaid 2
ggplot(results2) + 
  geom_density(aes(x = Inact_year),alpha = 0.5, fill = 'red') +
  geom_density(aes(x = Org_year),alpha = 0.5, fill = 'green') +
  coord_cartesian(xlim= XLIM3)+
  ggtitle('MI Business Creation & Completion \n 2005 - 2015') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Year of Organization \n or Inactivation') +
  theme_economist()

# Density of last annual report 1985 to 2015
ggplot(results2) + 
  geom_density(aes(x = Recent_Rept),alpha = 0.8, fill = 'grey') +
  coord_cartesian(xlim= XLIM)+
  ggtitle('Last Report received by LARA \n 1985 - 2015') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Last year submitted report') +
  theme_economist()

XLIM4 <- c(1985,2019)
# Density of last annual report 1985 to 2019
ggplot(results2) + 
  geom_density(aes(x = Recent_Rept),alpha = 0.8, fill = 'grey') +
  coord_cartesian(xlim= XLIM4)+
  ggtitle('Last Report received by LARA \n 1985 - 2019') +# for the main title
  ylab('Density') +# for the x axis label
  xlab('Last year submitted report') +
  theme_economist()
