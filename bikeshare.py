import time
import pandas as pd
import numpy as np
import calendar
# Additional change 1

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city, month, day = '', 0, ''
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input('What city would you like to analyze data for? \n')
        city = city.lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    while month > 7 or month < 1:
        try:
            month = int(input('What month would you like to analyze? (Please enter month number or 7 for all)\n'))
        except:
            print('Please enter a valid number!')
    if month == 7:
        month = 'all'
    else:
        month = calendar.month_name[month]
        month = month.lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    while day not in weekdays:
        day = input('What day of the week would you like to analyze? (Please capitalize day or use "all" for all)\n')

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    most_common_month = calendar.month_name[most_common_month]
    print("The most common month is " + str(most_common_month))
    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day is " + str(most_common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is " + str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print("The most common start station is " + str(most_common_start))

    # TO DO: display most commonly used end station
    most_common_end = df['End Station'].mode()[0]
    print("The most common end station is " + str(most_common_end))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("The most common combination of start and end stations is \n")
    print(most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is " + str(total_time))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The mean travel time is " + str(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("The earliest birth year is : ")
        print(int(earliest))
        print("The most recent birth year is : ")
        print(int(most_recent))
        print("The most common birth year is : ")
        print(int(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        counter, counter_2 = 0, 5
        raw_data = "Y"
        while raw_data == "Y":
            raw_data = input("Would you like to see 5 lines of raw data? ('Y' or 'N')\n")
            raw_data = raw_data.upper()
            if raw_data == "Y":
                print(df.iloc[counter:counter_2])
                counter += 5
                counter_2 += 5
            if raw_data == "N":
                break
            else:
                print("Please enter Y or N!")
                raw_data = "Y"

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
