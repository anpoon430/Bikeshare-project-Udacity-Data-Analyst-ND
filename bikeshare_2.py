import time,pandas as pd,numpy as np

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
    cities={'chicago','new york city','washington'}
    while True:
        user_input=input("Which city data are you interested in? (Chicago,New York City,Washington): ").lower()
        if user_input in cities:
            city=user_input
            break
        else:
            print("Invalid city: Please try again.")


    # get user input for month (all, january, february, ... , june)
    months=['january','february','march','april','may','june']
    while True:
        month=input("Which month's data do you want to filter by?(January to June available) Or type 'all' to show all months: ").lower()
        if month in months:
            break
        elif month=='all':
            break
        else:
            print("Invalid month: Please try again.")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while True:
        day=input("Which day of the week are you interested in? Or type 'all' to show all days of the week: ").lower()
        if day in days:
            break
        elif day=='all':
            break
        else:
            print("Invalid day of the week: Please try again")

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['months']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name

    if month!='all':
        months=['january','february','march','april','may','june']
        month=months.index(month)+1
        df=df[df['months']==month]

    if day!='all':
        df=df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    months=['january','february','march','april','may','june']
    most_common_month=df['months'].mode()[0]-1 #index of months starts at 0 so need to subtract 1
    print("People use bikeshare most frequently in {}.".format(months[most_common_month]))
    # display the most common day of week
    most_common_day=df['day_of_week'].mode()[0]
    print("{} is the most popular day of the week to use bikeshare".format(most_common_day))

    # display the most common start hour
    df['hours']=df['Start Time'].dt.hour
    most_common_startinghour=df['hours'].mode()[0]
    print("Most popular hour of the day to use bikeshare is: {}.".format(most_common_startinghour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_startingstation=df['Start Station'].mode()[0]
    print("The most frequent station to start biking from is: {}.".format(most_common_startingstation))
    # display most commonly used end station
    most_common_endstation=df['End Station'].mode()[0]
    print("The most frequent destination is {}.".format(most_common_endstation))

    # display most frequent combination of start station and end station trip
    
    trip_combination_frequencies=df.groupby(['Start Station','End Station']).size()
    most_common_trip=trip_combination_frequencies.idxmax()
   
    print("Most common trip: {}".format(most_common_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("The total travel time is: {:.2f} days".format(total_travel_time/(3600*24)))

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("The average travel time is {:.2f} minutes for each trip".format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print("The distribution of user types are:\n {} \n".format(user_types))


    # Display counts of gender
    gender=df['Gender'].value_counts()
    print("The genders of users:\n {}\n".format(gender))

    # Display earliest, most recent, and most common year of birth
    min_birth=df['Birth Year'].min()
    latest_birth=df['Birth Year'].max()
    common_birth=df['Birth Year'].mode()[0]
    print("Earliest birth year of users was: {:.0f}\nMost recent birth year of users was: {:.0f}\nMost common birth year was {:.0f}".format(min_birth,latest_birth,common_birth))

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
        print("city: {}, month: {}, day: {}".format(city,month,day))
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
