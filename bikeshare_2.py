#The structure of my code is heavily based on the template provided in this course.
#The function 'load_data' was constructed with help from Practice Solution #3 in this module.
import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city_accepted_inputs = ('chicago', 'new york city', 'washington')

    while True:
        city_input = str(input('Which city would you like to see data for? Chicago, New York City, or Washington?').lower())
        if city_input in city_accepted_inputs:
            city = city_input
            break
        else:
            print('Your chosen city has been entered incorrectly. Please try again.')

    # get user input for month (all, january, february, ... , june)
    month_accepted_inputs = ('all', 'january', 'february', 'march', 'april', 'may', 'june')

    while True:
        month_input = str(input('Which month would you like to see data for? Enter "all" to view data for all months or enter the full name of a month from January to June.').lower())
        if month_input in month_accepted_inputs:
            month = month_input
            break
        else:
            print('Your chosen month has been entered incorrectly. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_accepted_inputs = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday')

    while True:
        day_input = str(input('Which day would you like to see data for? Enter "all" to view data for all days or the full name of a particular day.').lower())
        if day_input in day_accepted_inputs:
            day = day_input
            break
        else:
            print('Your chosen day has been entered incorrectly. Please try again.')

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
    df['hour'] = df['Start Time'].dt.hour #Not sure if this goes here. This section is for city, day, month not hour. If code crashes move into time_stats section above popular_hour.

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
    popular_month = df['month'].mode()[0]
    print('Most common month to use bikeshare:', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week to use bikeshare:', popular_day)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour to start trip:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #count Start Stations then display max
    start_station_count = df.groupby(['Start Station'])['Start Station'].count()
    start_station_count_sort = start_station_count.sort_values()
    print('Most popular start station:', start_station_count_sort.tail(1))
    #make the display of this a little more elegant ie. Most popular station: x \n Count: x

    # display most commonly used end station
    #count End Stations then display max
    end_station_count = df.groupby(['End Station'])['End Station'].count()
    end_station_count_sort = end_station_count.sort_values()
    print('Most popular end station:', end_station_count_sort.tail(1))

    # display most frequent combination of start station and end station trip
    #join start and end station into one column. Count these columns then display start and end station using a split.
    df['trip'] = 'Start Station: ' + df['Start Station'] + ' End Station: ' + df['End Station']
    trip_count = df.groupby(['trip'])['trip'].count()
    trip_count_sort = trip_count.sort_values()
    print('Most popular trip:', trip_count_sort.tail(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #sum trip duration column. Answer default is in seconds.
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time/3600, 'hours.')

    # display mean travel time
    #mean of trip duration. Answer default is in seconds
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, 'minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_type_stats(df):
    """Displays statistics on bikeshare user type."""

    print('\nCalculating User Type Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #count different user types
    user_type_count = df.groupby(['User Type'])['User Type'].count()
    print(user_type_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def other_user_stats(df):
    """Displays gender and birth year statistics on bikeshare users."""

    print('\nCalculating Other User Stats...\n')
    start_time = time.time()

    # Display counts of gender
    #count genders and account for NaN entries and if city is washington display data not available

    df['Gender'].fillna('Not Specified', inplace=True) #check data type. Maybe this is whu groupby not working?
    gender_count = df.groupby(['Gender'])['Gender'].count()
    print(gender_count)

    #gender_count = fill_na_gender.groupby(['Gender'])['Gender'].count()


    # Display earliest, most recent, and most common year of birth
    # min max and mode of birth year column and account for NaN entries and if city is washington display data not available
    df['Birth Year'].dropna(axis=0, inplace=True)
    birth_year_min = df['Birth Year'].min()
    birth_year_max = df['Birth Year'].max()
    birth_year_mode = df['Birth Year'].mode()
    print('Earliest birth year:', birth_year_min)
    print('Most recent birth year:', birth_year_max)
    print('Most common birth year:', birth_year_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_type_stats(df)

        if city != 'washington':
            other_user_stats(df)
        else:
            print('\nSorry, birth year and gender data are unavailable for Washington.\n')

        raw_data_input = input('Would you like to view 5 rows of raw data? Enter yes or no.').lower()
        start_loc = 0
        while raw_data_input == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            raw_data_input = input('Would you like to see another 5 rows of raw data?').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
