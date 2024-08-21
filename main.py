import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import os
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile

# Function to download, extract, and clean up the dataset
def download_and_prepare_data():
    # Initialize Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Set paths and dataset
    dataset = 'rohanrao/formula-1-world-championship-1950-2020'
    download_path = './formula-1-world-championship-1950-2020.zip'
    extract_path = './f1_data'
    
    # Check if the data is already extracted
    if not os.path.exists(extract_path):
        try:
            # Download the dataset
            print('Downloading dataset...')
            api.dataset_download_files(dataset, path='.', unzip=False)
            
            # Extract the zip file
            print('Extracting dataset...')
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            # Remove the zip file after extraction
            print('Cleaning up...')
            os.remove(download_path)
            
        except Exception as e:
            print(f"An error occurred: {e}")
    
    return extract_path


# get wins per driver in a given year
def wins_per_driver_for_season(year, extract_path):
    races = pd.read_csv(os.path.join(extract_path, 'races.csv'))

    if year not in races.year.unique():
        print('Year not found')
        return  
    
    # load other data
    drivers = pd.read_csv(os.path.join(extract_path, 'drivers.csv'))
    results = pd.read_csv(os.path.join(extract_path, 'results.csv'))
    

    # prepare races data
    races = races.drop(columns=['time', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'round' ,'sprint_time', 'circuitId' ,'date', 'name'])
    races = races[races['year'] == year]
    races = races.drop(columns=['year'])

    # prepare results data
    results = results.drop(columns=['number', 'grid', 'positionText','points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId'])
    winners = results[results['positionOrder'] == 1]
    winners = winners.drop(columns=['positionOrder', 'position', 'constructorId'])

    # join races and their winners
    race_winners = pd.merge(races, winners, on='raceId')

    # prepare drivers data
    drivers = drivers.drop(columns=['number', 'code', 'url', 'nationality', 'dob', 'driverRef'])

    # join driver names to ids
    race_winners = pd.merge(race_winners, drivers, on='driverId')

    # count wins per driver
    wins_per_driver = race_winners.groupby(['driverId', 'forename', 'surname']).size().reset_index(name='wins')
    wins_per_driver = wins_per_driver.sort_values(by='wins', ascending=False)

    # visualize wins per driver
    plt.figure(figsize=(20, 10))
    plt.bar(wins_per_driver['forename'] + ' ' + wins_per_driver['surname'], wins_per_driver['wins'], color='skyblue')
    plt.title(f'Wins per driver in {year} season' , fontdict={'fontsize': 20, 'fontweight': 'bold'}, y=1.05)
    plt.xlabel('Driver name', fontsize=15)
    # make the y values integers, plt doesn't include the max value automatically
    plt.yticks(range(0, wins_per_driver['wins'].max() + 1, 1))

    plt.ylabel('Number of wins', fontsize=15)

    plt.show()

# get the number of races per month in a given year
def num_races_per_month_for_season(year, extract_path):
    # check if year is valid
    races = pd.read_csv(os.path.join(extract_path, 'races.csv'))
    
    if year not in races['year'].unique():
        print('Year not found')
        return
    
    # prepare races data
    races = races[races['year'] == year]
    races = races.drop(columns=['year', 'time', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'round' ,'sprint_time', 'circuitId'])

    # Extract month from the date
    races['date'] = pd.to_datetime(races['date'])
    races['month'] = races['date'].dt.month

    # Count the number of races per month  and name the column 'number'
    races_per_month = races.groupby('month').size().reset_index(name='number')

    # turn the month number into month name using calendar lib
    races_per_month['month'] = races_per_month['month'].apply(lambda x: calendar.month_abbr[x])

    # create a bar chart with x-axis month name and y-axis the number of races 
    plt.figure(figsize=(20, 10))
    plt.bar(races_per_month['month'], races_per_month['number'], color='skyblue')
    
    plt.title(f'Number of Races per Month in {year}', fontdict={'fontsize': 20, 'fontweight': 'bold'}, y=1.05)
    plt.xlabel('Month', fontsize=15)
    plt.ylabel('Number of Races', fontsize=15)

    # make the y values integers, because plt converts then to floats when plotting
    plt.yticks(range(0, races_per_month['number'].max() + 1, 1))
    plt.show()


# create a pie chart of nationality distribution given a year
def nationality_representation_for_season(year, extract_path):
    # check if year is valid
    races = pd.read_csv(os.path.join(extract_path, 'races.csv'))
    if year not in races.year.unique():
        print('Year not found')
        return
    
    # prepare drivers data
    drivers = pd.read_csv(os.path.join(extract_path, 'drivers.csv'))
    drivers = drivers.drop(columns=['number', 'code', 'url', 'dob', 'driverRef'])

    # load other data
    results = pd.read_csv(os.path.join(extract_path, 'results.csv'))
    
    # filter races in the given year
    races_in_year = races[races['year'] == year]

    # merge with results to get driverIds
    results_in_year = pd.merge(races_in_year, results, on='raceId')

    # get unique driverIds for the races in the given year
    driver_ids_in_year = results_in_year['driverId'].unique()

    # filter drivers who participated in the given year
    drivers_in_year = drivers[drivers['driverId'].isin(driver_ids_in_year)]    

    # get nationality distribution
    nationality_distribution = drivers_in_year['nationality'].value_counts().reset_index()
    nationality_distribution.columns = ['nationality', 'count']
    nationality_distribution = nationality_distribution.sort_values(by='count', ascending=False)
    
    # create a pie chart
    plt.figure(figsize=(10, 10))

    custom_colors = plt.cm.plasma(np.linspace(0, 1, len(nationality_distribution['nationality'])))
    # random shuffle the colors
    # np.random.shuffle(custom_colors)

    # reverse the colors
    custom_colors = custom_colors[::-1]

    
    plt.pie(nationality_distribution['count'], labels=nationality_distribution['nationality'], autopct='%1.1f%%', colors=custom_colors)
    plt.title(f'Nationality Distribution of F1 Drivers in {year} Season', fontdict={'fontsize': 20, 'fontweight': 'bold'}, y=1.05)
    plt.show()
    

def main():
    extract_path = download_and_prepare_data()
    wins_per_driver_for_season(2018, extract_path)
    num_races_per_month_for_season(2022, extract_path)
    nationality_representation_for_season(2023, extract_path)


main()

