import time
import pandas as pd
import numpy as np
import calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city not in ['chicago', 'new york', 'washington']:
            print('Please type a correct city.')
        else:
            break

    while True:
        time_filter = input('Would you like to filter the data by month, day, or not at all? type \'none\' for no filter.\n').lower()
        if time_filter not in ['month', 'day', 'none']:
            print('Please pick one of the choices.')
        elif time_filter == 'none':
            month = 'all'
            day = 'all'
            break
        elif time_filter == 'month':
            # get user input for month (all, january, february, ... , june)
            while True:
                month = input('Which month - January, February, March, April, May, or June?\n').lower()
                if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                    print('Please type a correct month.')
                else:
                    break
            day = 'all'
            break
        elif time_filter == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
                if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    print('Please type a correct day.')
                else:
                    break
            month = 'all'
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # find the most popular month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', calendar.month_name[popular_month])

    # display the most common day of week
    # find the most popular day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Day of Week:', popular_day)

    # display the most common start hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # find the most popular start station
    popular_start = df['Start Station'].mode()[0]

    print('Most Popular Start Station:', popular_start)

    # display most commonly used end station
    # find the most popular end station
    popular_end = df['End Station'].mode()[0]

    print('Most Popular End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    # find the most popular combination of start station and end station
    popular_start_end = (df['Start Station'] + ' || ' + df['End Station']).mode()[0]

    print('Most Popular Combination of Start Station and End Station:', popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    formatted_ttt = datetime.timedelta(seconds = int(total_travel_time))
    print('Total Travel Time:', formatted_ttt)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    formatted_att = datetime.timedelta(seconds = int(avg_travel_time))
    print('Average Travel Time:', formatted_att)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        print('')
        user_genders = df['Gender'].value_counts()
        print(user_genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('')
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest Year of Birth:', int(earliest_birth))
        print('Most Recent Year of Birth:', int(most_recent_birth))
        print('Most Common Year of Birth:', int(most_common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Asks user if they want to view raw data. Loop until user input anything other than 'yes'

    Returns:
        5 lines of raw data
    """

    i = 0
    while True:
        restart = input('\nWould you like to see 5 lines of raw data? Enter yes to continue.\n')
        if restart.lower() != 'yes':
            print('-'*40)
            break
        else:
            print(df.iloc[i:i+5])
            i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes to continue.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
