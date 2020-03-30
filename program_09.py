#!/bin/env python
# add your header here
#This script creates a series of data quality checks for the 'DataQualityChecking.txt' file
#Checks include replacing defined no data (-999) with NAN, removal of gross errors as commented, swapping max and min air
#Temp as commented, and subtracting max and min air range as commented
#Script outputs replaced values cumulative, scatterplots per wind, precip, and air temp checks, failed data, and changed value count totals
#Created by Aaron Etienne (aetienne93 Github and aetienne Purdue uname) on 3/27/20

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=['1. No Data', '2. Gross Error', '3. Swapped', '4. Range Fail'], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # add your code here
    #Replace all values of -999 with NAN
    
    #Precip, temp, wind speed 
    for i in range (0,len(DataDF)-1):
       for j in range(0,3):
           if DataDF.iloc[i,j] == -999:
               DataDF.iloc[i,j]= np.nan
               

    ReplacedValuesDF.iloc[0,0]=DataDF['Precip'].isna().sum()
    ReplacedValuesDF.iloc[0,1]=DataDF['Max Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,2]=DataDF['Min Temp'].isna().sum()
    ReplacedValuesDF.iloc[0,3]=DataDF['Wind Speed'].isna().sum()

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # add your code here
    #(GEC = gross error check)
    
    #precipitation GEC 
    for i in range (0,len(DataDF)-1):
           if (DataDF.iloc[i,0]<0) or (DataDF.iloc[i,0]> 25):
               DataDF.iloc[i,0]= np.nan
        
    #temperature GEC
    #Min temp 
    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i,2]< (-25):
               DataDF.iloc[i,2]= np.nan
               
    #MaxTemp 
    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i, 1] > (35):
               DataDF.iloc[i,1]= np.nan
               
    #Wind Speed GEC           
    for i in range (0,len(DataDF)-1):
           if (DataDF.iloc[i, 3]< 0) or (DataDF.iloc[i, 3]> 10):
               DataDF.iloc[i,0]= np.nan

    ReplacedValuesDF.iloc[0,0]=DataDF['Precip'].isna().sum() - ReplacedValuesDF.iloc[0,0]
    ReplacedValuesDF.iloc[0,1]=DataDF['Max Temp'].isna().sum() - ReplacedValuesDF.iloc[0,1]
    ReplacedValuesDF.iloc[0,2]=DataDF['Min Temp'].isna().sum() - ReplacedValuesDF.iloc[0,2]
    ReplacedValuesDF.iloc[0,3]=DataDF['Wind Speed'].isna().sum() - ReplacedValuesDF.iloc[0,3]

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    # add your code here
    '''
    # create function for number of days whenmax air temp is less than min air temp
       
    T_cum= len(DataDF.loc[DataDF['Max Temp'] < DataDF['Min Temp']])
   
    # swao the values where max temp is less than min temp 
    DataDF.loc[DataDF['Max Temp']<DataDF['Min Temp'],['Max Temp','Min Temp']]= DataDF.loc[ DataDF['Max Temp']<DataDF['Min Temp'],['Min Temp','Max Temp']].values 
   
    # create a running total of the replaced data 
    ReplacedValuesDF.loc["3. Swapped"]=[0, T_cum, T_cum, 0]

    return( DataDF, ReplacedValuesDF )
    '''
    
   
    # create function for number of days when max air temp is less than min air temp
       
    ReplacedValuesDF.iloc[2,1]=(DataDF['Min Temp']> DataDF['Max Temp']).sum()
    ReplacedValuesDF.iloc[2,2]=(DataDF['Min Temp']> DataDF['Max Temp']).sum()
    
    # swap the values where max temp is less than min temp
    for i in range (0,len(DataDF)-1):
           if DataDF.iloc[i,1] < DataDF.iloc[i,2]:
               T_swap=DataDF.iloc[i,2]
               DataDF.iloc[i,2]= DataDF.iloc[i,1]
               DataDF.iloc[i,1]=T_swap
     # create a running total of the replaced data          
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # add your code here
    
    # find the number of days when max air temp minus min air temp is greater than or equal to 25 degrees celcius (outliers)
       
    Tdays_cum= len(DataDF.loc[(DataDF['Max Temp'] - DataDF['Min Temp']>=25)])
   
    # replace values in which max temp minus min temp is greater than or equal to 25 degrees c with an NAN value 
    DataDF.loc[(DataDF['Max Temp']-DataDF['Min Temp']>=25),['Max Temp','Min Temp']]= np.nan
    
    # total ampount (cumulative) data values that are replaced with NAN
    ReplacedValuesDF.loc["4. Range"]=[0, Tdays_cum, Tdays_cum, 0]

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    plt.plot(ReplacedValuesDF)
    plt.savefig('repval.png')

##################################################################
    # Plot each dataset before and after correction has been made.
    #Use a single set of axis for each variable, and
    # Original data provided before data quality check
    # define column names
##################################################################
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open original CSV file to plot before and after comparision 
    Org_DF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    Org_DF = Org_DF.set_index('Date')
    
    # create scatter plot of before and after data checking for precipitation
    plt.scatter(DataDF.index, Org_DF['Precip'],color = 'red',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Precip'],color = 'midnightblue', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel('Precipitation (mm)')
    plt.xticks(rotation=20)
    plt.legend(loc='lower left')
    plt.savefig('precip_fix.png')
    plt.close()
    
    # create scatter plot of before and after data checking max air temp 
    plt.scatter(DataDF.index, Org_DF['Max Temp'],color = 'red',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Max Temp'],color = 'aqua', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Max Air Temperature (°C)")
    plt.xticks(rotation=20)
    plt.legend(loc='lower left')
    plt.savefig('max_temp_fix.png')
    plt.close()
  
    # create scatter plot of before and after data checking min air temp 
    plt.scatter(DataDF.index, Org_DF['Min Temp'],color = 'red' ,label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Min Temp'],color = 'green', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Min Air Temperature (°C)")
    plt.xticks(rotation=20)
    plt.legend(loc='lower left')
    plt.savefig('min_temp_fix.png')
    plt.close()
  
    # create scatter plot of before and after data checking wind speed  
    plt.scatter(DataDF.index, Org_DF['Wind Speed'],color = 'red',label = 'Before Data Quality Check' )
    plt.plot(DataDF.index, DataDF['Wind Speed'],color = 'blue', label = 'After Data Quality Check')
    plt.xlabel('Date (1915-1916)')
    plt.ylabel("Wind Speed (m/s)")
    plt.xticks(rotation=20)
    plt.legend(loc='upper right')
    plt.savefig('wind_fix.png')
    plt.close() 

    #export data quality check (DQC) data frame (DF) to text file
    DataDF.to_csv('after_DQC.txt', header=False, index='Date', sep = ' ')
    
    #export DF showing failed checks to text file 
    ReplacedValuesDF.to_csv('failed_checks.txt', header=True, index=True, sep = '\t')

    
