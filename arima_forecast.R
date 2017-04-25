# this will install any required packages on the fly
list.of.packages <- c("zoo", "forecast", "dplyr", "tidyr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(zoo, warn.conflicts = F)
library(forecast, warn.conflicts = F)
library(dplyr, warn.conflicts = F)
library(tidyr, warn.conflicts = F)

data <- read.csv("/Users/samhainsworth/Google Drive/HCV Agent Model/Data/LGA_Summary_TS.csv")

make_dates <- function(num_quarts){
  # Build the time series data frame
  dates <- as.data.frame(seq(as.Date("2016-01-01"), as.Date("2017-12-01"), by="month" ))
  colnames(dates) <- "Date"
  # put into quarters
  quarterly <- dates %>%
    mutate(Quarter = as.yearqtr(Date, format = "%Y-%m-%d") )
  # remove excess dates by slicing
  quarterly <- as.data.frame(unique(quarterly$Quarter)[1:num_quarts])
  quarterly <- as.data.frame(quarterly[rep(seq_len(nrow(quarterly)), times =545), ])
  colnames(quarterly) <- "Date"

  return(quarterly)
}


forecast_all_lgas <- function(data, num_quarts){
  # get arima forecasts for the next 2 years = 8 time steps
  dates <- make_dates(num_quarts)
  # convert to time series
  data.ts <- with(data, tapply(LGACount, LGACode, FUN=ts, start = c(2010, 1), end = c(2015, 4), frequency = 4))
  # run arima
  result <- lapply(data.ts, auto.arima)
  # forecast
  pred <- lapply(result, FUN = forecast, h = num_quarts )
  preds <- as.data.frame(sapply(pred, "[", 4 ))
  # convert to long form
  preds <- preds %>%
    tidyr::gather(LGACode, Forecast, X10050.mean:X99399.mean)
  # if forecasts negative, change to 0
  preds$Forecast[preds$Forecast < 0] <- 0

  preds$LGACode <- gsub("\\.mean","", preds$LGACode)
  preds$LGACode <- gsub("^X","", preds$LGACode)

  new <- cbind(dates, preds)
  new$Quarter <- rep(seq(1,8, by = 1), times = length(unique(preds$LGACode)))
  return(new)

}

# get arguments from Python
myArgs <- commandArgs(trailingOnly = TRUE)
# convert to numeric
args <- as.numeric(myArgs)

result <- forecast_all_lgas(data, 8)
# date for python
result$DateMonth <- as.yearmon(result$Date)
colnames(result) <- c("Date", "LGACode", "Forecast", "Quarter", "DateMonth")
#
write.csv(result, file = "/Users/samhainsworth/Google Drive/HCV Agent Model/Data/arima forecasts by LGA.csv", row.names = F)

# 
