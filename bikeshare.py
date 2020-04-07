import time
import string
import pandas as pd
import numpy as np
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_input(validValues):
    
    # Asks user for input and checks input for correct input values.
    
    valid = False
    value = input('>')
    value = value.lower()
    while not valid:
        if value in map(str.lower, validValues):
            valid = True
        else:
            print('Please enter a correct value!')
            print(*validValues, sep = ", ")
            value = input('>')
    return value

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cities = ['Chicago', 'New York', 'Washington']
    filterValues = ['Month', 'Day', 'Both', 'None']
    months = ['January', 'February', 'March', 'April', 'May', 'June']            
    days = ['1', '2', '3', '4', '5', '6', '7']
    
    
    print('What city do you want to look into ? Chicago, New York or Washington?')
    city = get_valid_input(cities)
   
    # TO DO: get user input for month (all, january, february, ... , june)
    
    print('Do you want to filter the data by Month, Day, Both or not at all? Type "None" for no time filter!')
    filter = get_valid_input(filterValues)
    
    if filter == 'month':
        print('Which month? January, February, March, April, May or June?')
        month = get_valid_input(months)
        day = 'all'
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    elif filter == 'day':
        print('Which day? Monday(1), Tuesday(2), ..., ? Please enter number!')
        day = int(get_valid_input(days))-1
        month = 'all'
        
    elif filter == 'both':
        print('Which month? January, February, March, April, May or June?')
        month = get_valid_input(months)
        print('Which day? Monday(1), Tuesday(2), ..., ? Please enter number!')
        day = int(get_valid_input(days))-1
    
    elif filter == 'none':
        month = 'all'
        day = 'all'
        
    else:
        return -1
    
    if month !='all': 
        month = [element.lower() for element in months].index(month) + 1
    

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    if city == 'chicago':
        filename = 'chicago.csv'
    elif city == 'new York':
        filename = 'new_york_city.csv'
    elif city == 'washington':
        filename = 'washington.csv'
    else:
        return -1
   
    df = pd.read_csv(filename)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    if month != 'all':
        df = df[df['Start Time'].dt.month == month]

    if day != 'all':
        df = df[df['Start Time'].dt.weekday == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
        
    df['Start Month'] = df['Start Time'].dt.month_name()
    month_count = df['Start Month'].value_counts()
    print("The most common month is", month_count.index[0], ".")
    
    # TO DO: display the most common day of week

    df['Start Day'] = df['Start Time'].dt.day_name()
    day_count = df['Start Day'].value_counts()
    print("The most common day is", day_count.index[0], ".")

    # TO DO: display the most common start hour

    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print("The most common start hour is between", popular_hour, "-", popular_hour+1, ".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    start_station_count = df['Start Station'].value_counts()
    print("The most common start station is", start_station_count.index[0], ".")


    # TO DO: display most commonly used end station

    end_station_count = df['End Station'].value_counts()
    print("The most common end station is", end_station_count.index[0], ".")

    # TO DO: display most frequent combination of start station and end station trip

    route_count = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'})
    popular_route = route_count.sort_values(by=['count'], ascending=False).iloc[0]
    print("The most common route is from", popular_route['Start Station'], "to", popular_route['End Station'],".")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    df['Trip Duration'] = (df['End Time'] - df['Start Time'])
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was:', total_travel_time)
    
    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time was:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_type_count = df['User Type'].value_counts()
    print('The number of rentals per user type:')
    print(user_type_count.to_string())

    # TO DO: Display counts of gender
    
    if 'Gender' in df.columns:
    
        gender_type_count = df['Gender'].value_counts()
        print('\nThe number of rental per gender:')
        print(gender_type_count.to_string())
    
    else:
    
        print('\nNo data about gender available.\n')
        
    # TO DO: Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        
        youngest_user = df['Birth Year'].max()
        common_user = df['Birth Year'].mode()[0]
        oldest_user = df['Birth Year'].min()
        print('\nThe youngest user was born', int(youngest_user))
        print('The most common user was born', int(common_user))
        print('The oldest user was born', int(oldest_user))
    
    else:
        
        print('\nNo data about age available.\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
   
    # Raw data is displayed upon request by the user in this manner: 
    #  - Script prompts the user if they want to see 5 lines of raw data, 
    #  - display that data if the answer is 'yes', 
    #  - and continue these prompts and displays until the user says 'no'.

    count = 0
    raw_data = input('\nDo you want to see the raw data? Enter yes or no.\n')
    if raw_data.lower() == 'yes':
        while True: 
            print(df.iloc[count*5:count*5+5])
            count += 1 
            more = input('\nWould you like to view more? Enter yes or no.\n')
            if more.lower() != 'yes':
                break
    return
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)  
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
