from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import time
import string
import requests
import shutil
import os
from driver_builder import DriverBuilder

## Configurations
download_location = r"/Users/mayank.gupta/Moneygen/Downloads"
data_file_location = r"/Users/mayank.gupta/Moneygen/DataFiles"
sleep_duration = 3

### Load the chrome webdriver
driver = DriverBuilder().get_driver(download_location, headless=True)

### Get the web page using driver for BANKNIFTY
driver.get("https://nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying=BANKNIFTY&instrument=FUTIDX&type=-&strike=-&expiry=25JUL2019")
time.sleep(sleep_duration)

### Select 'Options' as instrument type
instrument_type_element = driver.find_element_by_id("instruments")
instrument_selector = Select(instrument_type_element)
## Index is always index + 1 because 0 index corresponds to 'Select...'
instrument_selector.select_by_index(2)
time.sleep(sleep_duration)

### Get expiry dates of all available contracts
expiry_dates_element = driver.find_element_by_id("expiryDates")
expiry_dates = expiry_dates_element.text.split('\n')[2:].copy()
time.sleep(sleep_duration)

### Select expiry dates and populate the strike price list
def getStrikePrices():
    date_price_dict = dict()
    expiry_dates_selector = Select(expiry_dates_element)
    for index in range(len(expiry_dates)):
        print('Getting strike prices for: ', expiry_dates[index], ', having index: ', index)
        indexer = index + 1
        date_price_dict[expiry_dates[index]] = dict()

        ## Select expiry for a contract
        expiry_dates_selector.select_by_index(indexer)
        time.sleep(sleep_duration)

        ## Selecting 'Call' option to populate 'Strike Price' list
        Select(driver.find_element_by_id("optionType")).select_by_index(1)
        time.sleep(sleep_duration)

        ## Populating strike prices for Call option of selected date
        strike_price_element = driver.find_element_by_id('strikePrices')
        date_price_dict[expiry_dates[index]]['Call'] = strike_price_element.text.split('\n')[2:].copy()
        print('Length of strike price list for ', expiry_dates[index], 'Call option: ', len(date_price_dict[expiry_dates[index]]['Call']))
        time.sleep(sleep_duration)

        ## Selecting 'Put' option to populate 'Strike Price' list
        Select(driver.find_element_by_id("optionType")).select_by_index(2)
        time.sleep(sleep_duration)

        ## Populating strike prices for Put option of selected date
        strike_price_element = driver.find_element_by_id('strikePrices')
        date_price_dict[expiry_dates[index]]['Put'] = strike_price_element.text.split('\n')[2:].copy()
        print('Length of strike price list for ', expiry_dates[index], 'Put option: ', len(date_price_dict[expiry_dates[index]]['Put']))
        time.sleep(sleep_duration)
    return date_price_dict

try:
    date_price_dict = getStrikePrices()
except:
    print('Exception occured, trying again')
    time.sleep(sleep_duration + 10)
    date_price_dict = getStrikePrices()


month_mapper = {
"JAN":"-01-",
"FEB":"-02-",
"MAR":"-03-",
"APR":"-04-",
"MAY":"-05-",
"JUN":"-06-",
"JUL":"-07-",
"AUG":"-08-",
"SEP":"-09-",
"OCT":"-10-",
"NOV":"-11-",
"DEC":"-12-"
}

expiry_dates_mapper = dict()
## Change month name to month number
for index, date in enumerate(expiry_dates):
    month_name = expiry_dates[index][2:5]
    month_number = month_mapper[month_name]
    expiry_dates_mapper[expiry_dates[index]] = expiry_dates[index].replace(month_name, month_number)

for old_key, new_key in zip(expiry_dates_mapper.keys(), expiry_dates_mapper.values()):
    date_price_dict[new_key] = date_price_dict.pop(old_key)

# Get historical data for All contracts -> All Strike Prices
driver.get('https://www.nseindia.com/products/content/derivatives/equities/historical_fo.htm')


Select(driver.find_element_by_id('instrumentType')).select_by_index(3) ## Select `Index Options`
time.sleep(sleep_duration)
Select(driver.find_element_by_id('symbol')).select_by_index(4) ## Select `BANK NIFTY`
time.sleep(sleep_duration)
Select(driver.find_element_by_id('dateRange')).select_by_index(6) ## Select `BANK NIFTY`
time.sleep(sleep_duration)
Select(driver.find_element_by_id('year')).select_by_index(5) ## Select `BANK NIFTY`
time.sleep(sleep_duration)

expiry_date_element = driver.find_element_by_id('expiryDate') ## Get expiryDates on website
expiry_date_list = expiry_date_element.text.replace(' ','').split('\n') ## Remove white spaces and split by newline

## Skip dates 
skip_list = list()

try:
    ## For Call options
    for index, item in enumerate(expiry_date_list):
        print(item)
        if item in skip_list:
            print('Skipped item: ', item)
            continue
        if item in list(expiry_dates_mapper.values()):
            print('Inside if: ', item)
            Select(expiry_date_element).select_by_index(index)
            Select(driver.find_element_by_id("optionType")).select_by_index(1)
            time.sleep(sleep_duration)
            for strike_price in date_price_dict[item]['Call']:
                driver.find_element_by_id('strikePrice').clear()
                driver.find_element_by_id('strikePrice').send_keys(int(strike_price.split('.')[0]))
                
                time.sleep(sleep_duration)
                try:
                    driver.find_element_by_id('getButton').click()
                    download_link = WebDriverWait(driver, sleep_duration+20).until(EC.presence_of_element_located((By.LINK_TEXT, "Download file in csv format")))
                    download_link.click()
                except:
                    print('Exception occured, waiting and trying again')
                    driver.find_element_by_id('getButton').click()
                    download_link = WebDriverWait(driver, sleep_duration+20).until(EC.presence_of_element_located((By.LINK_TEXT, "Download file in csv format")))
                    time.sleep(sleep_duration+10)
                    download_link.click()
                time.sleep(sleep_duration)
                try:
                    filename = os.listdir(download_location)[0]
                except:
                    print("Index error occured, waiting for a file to appear in directory")
                    ## There might be a glitch due to which 'Download' link doesn't get clicked
                    download_link.click()
                    time.sleep(sleep_duration + 10)
                    filename = os.listdir(download_location)[0]
                destination_filename = item + '_' + 'Call' + '_' + strike_price.split('.')[0] + '.csv'
                shutil.move(os.path.join(download_location,filename),os.path.join(data_file_location+'/Call', destination_filename))
            skip_list.append(item)

except:
    open('skip_list.txt', 'w+').write(str(skip_list))

skip_list = list()

try:
    # For Put options
    for index, item in enumerate(expiry_date_list):
        print(item)
        if item in skip_list:
            print('Skipped item: ', item)
            continue
        if item in list(expiry_dates_mapper.values()):
            print('Inside if: ', item)
            Select(expiry_date_element).select_by_index(index)
            Select(driver.find_element_by_id("optionType")).select_by_index(2)
            time.sleep(sleep_duration)
            for strike_price in date_price_dict[item]['Put']:
                driver.find_element_by_id('strikePrice').clear()
                driver.find_element_by_id('strikePrice').send_keys(int(strike_price.split('.')[0]))
                driver.find_element_by_id('getButton').click()
                time.sleep(sleep_duration)
                try:
                    download_link = WebDriverWait(driver, sleep_duration+20).until(EC.presence_of_element_located((By.LINK_TEXT, "Download file in csv format")))
                    download_link.click()
                except:
                    print('Exception occured, waiting and trying again')
                    driver.find_element_by_id('getButton').click()
                    download_link = WebDriverWait(driver, sleep_duration+20).until(EC.presence_of_element_located((By.LINK_TEXT, "Download file in csv format")))
                    download_link.click()
                time.sleep(sleep_duration)
                try:
                    filename = os.listdir(download_location)[0]
                except:
                    print("Index error occured, waiting for a file to appear in directory")
                    ## There might be a glitch due to which 'Download' link doesn't get clicked
                    download_link.click()
                    time.sleep(sleep_duration + 10)
                    filename = os.listdir(download_location)[0]
                destination_filename = item + '_' + 'Put' + '_' + strike_price.split('.')[0] + '.csv'
                shutil.move(os.path.join(download_location,filename),os.path.join(data_file_location+'/Call', destination_filename))
            skip_list.append(item)
except:
    open('skip_list.txt', 'w+').write(str(skip_list))

driver.close()

# Append dataframe to respective Date-StrikePrice combo
dataframe_dict = dict()

def process_data_files(data_directory: str, option_type: str, dataframe_dict: dict):
    
    files_path = os.path.join(data_directory, option_type)
    
    for file in os.listdir(files_path):
#         print('Processing file:', file)
        filename_split = file.split('_')
        expiry_date = filename_split[0]
        strike_price = filename_split[2].split('.')[0]

        if expiry_date not in dataframe_dict.keys():
            dataframe_dict[expiry_date] = dict()

        if option_type not in dataframe_dict[expiry_date].keys():
            dataframe_dict[expiry_date][option_type] = dict()

        dataframe_dict[expiry_date][option_type][strike_price] = pd.read_csv(os.path.join(files_path, file))
        
    return dataframe_dict

dataframe_dict = process_data_files('DataFiles','Put',dict())
dataframe_dict = process_data_files('DataFiles','Call',dataframe_dict)
dataframe_dict_copy = dataframe_dict.copy()

## Remove dataframes with 0 in all ohlc data
def remove_strike_prices_with_only_zero_values(dataframe_dictionary: dict, option_type: str):
    dataframe_dict = dataframe_dictionary.copy()
    for expiry_date in list(dataframe_dict.keys()):
#         print("Expiry date:", expiry_date)
        for strike_price in list(dataframe_dict[expiry_date][option_type].keys()):
#             print("Strike Price:", strike_price)
            if dataframe_dict[expiry_date][option_type][strike_price]['Open'].sum() == 0:
                del dataframe_dict[expiry_date][option_type][strike_price]
    return dataframe_dict

dataframe_non_zero_put = remove_strike_prices_with_only_zero_values(dataframe_dict_copy, 'Put')
dataframe_non_zero_all = remove_strike_prices_with_only_zero_values(dataframe_non_zero_put, 'Call')


## Filter OHLC data in all dataframes
def filter_ohlc_data(dataframe_dictionary: dict, option_type: str):
    dataframe_dict = dataframe_dictionary.copy()
    for expiry_date in list(dataframe_dict.keys()):
#         print("Expiry date:", expiry_date)
        for strike_price in list(dataframe_dict[expiry_date][option_type].keys()):
#             print("Strike Price:", strike_price)
            dataframe_dict[expiry_date][option_type][strike_price] = dataframe_dict[expiry_date][option_type][strike_price][ohlc]
    return dataframe_dict

dataframe_ohlc_put = filter_ohlc_data(dataframe_non_zero_all, 'Put')
dataframe_ohlc_all = filter_ohlc_data(dataframe_ohlc_put, 'Call')

## Get profitable stocks from OHLC
## Criteria can be: Open, High, Low, Close
def list_profitable_stocks(dataframe_dictionary: dict, option_type: str, criteria: str): 
    profit_list = list()
    return_string = ''
    dataframe_dict = dataframe_dictionary.copy()
    for expiry_date in list(dataframe_dict.keys()):
#         print("Expiry date:", expiry_date)
        for strike_price in list(dataframe_dict[expiry_date][option_type].keys()):
#             print("Strike Price:", strike_price)
            df = dataframe_dict[expiry_date][option_type][strike_price]
            df = df[df[criteria] != 0]
            profit_loss_df = df - df.shift(1)
            profit_loss_value = profit_loss_df[criteria].sum()
            if profit_loss_value > 0:
                profit_list.append(str('Profit in: '+ expiry_date + ' ' + option_type + ' ' + strike_price + ' ' + "with value: "+ ' ' + profit_loss_value))
                for item in profit_list:
                    return_string = item + '\n' + return_string
#                 print('Profit in:', expiry_date, option_type, strike_price, "with value: ", profit_loss_value)
    return return_string

dataframe_profitable_put = list_profitable_stocks(dataframe_ohlc_all, 'Put', 'Open')
dataframe_profitable_call = list_profitable_stocks(dataframe_ohlc_all, 'Call', 'Open')

slack_hook = 'https://hooks.slack.com/services/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'
requests.post(slack_hook,str(dataframe_profitable_put))
requests.post(slack_hook,str(dataframe_profitable_call))
