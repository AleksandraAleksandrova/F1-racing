import pandas as pd
import matplotlib.pyplot as plt
import calendar

# get wins per driver in a given year
def wins_per_driver_for_season(year):
    races = pd.read_csv('./data/full/races.csv')

    if year not in races.year.unique():
        print('Year not found')
        return  
    
    # load other data
    drivers = pd.read_csv('./data/full/drivers.csv')
    results = pd.read_csv('./data/full/results.csv')
    

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

    
def races_calendar_for_season(year):
    # check if year is valid
    races = pd.read_csv('./data/full/races.csv')
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


wins_per_driver_for_season(2022)
races_calendar_for_season(2022)