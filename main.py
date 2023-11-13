import pandas as pd
import matplotlib.pyplot as plt

# load data
drivers = pd.read_csv('./data/full/drivers.csv')
results = pd.read_csv('./data/full/results.csv')
races = pd.read_csv('./data/full/races.csv')

# prepare races data
races = races.drop(columns=['time', 'url', 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 'quali_date', 'quali_time', 'sprint_date', 'round' ,'sprint_time', 'circuitId' ,'date', 'name'])
races_2018 = races[races['year'] == 2018]
races_2018 = races_2018.drop(columns=['year'])

# prepare results data
results = results.drop(columns=['number', 'grid', 'positionText','points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId'])
winners = results[results['positionOrder'] == 1]
winners = winners.drop(columns=['positionOrder', 'position', 'constructorId'])

# join races and their winners
race_winners_2018 = pd.merge(races_2018, winners, on='raceId')

# prepare drivers data
drivers = drivers.drop(columns=['number', 'code', 'url', 'nationality', 'dob', 'driverRef'])

# join driver names to ids
race_winners_2018 = pd.merge(race_winners_2018, drivers, on='driverId')

# count wins per driver
wins_per_driver = race_winners_2018.groupby(['driverId', 'forename', 'surname']).size().reset_index(name='wins')
wins_per_driver = wins_per_driver.sort_values(by='wins', ascending=False)

# visualize wins per driver
plt.figure(figsize=(20, 10))
plt.bar(wins_per_driver['forename'] + ' ' + wins_per_driver['surname'], wins_per_driver['wins'], color='skyblue')
plt.title('Wins per driver in F1 2018 season', fontdict={'fontsize': 20, 'fontweight': 'bold'}, y=1.05)
plt.xlabel('Driver name', fontsize=15)
plt.ylabel('Number of wins', fontsize=15)

plt.show()