import time,pandas as pd,numpy as np,seaborn as sns,matplotlib.pyplot as plt

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
        #store data in user_input, then store into city variable if valid
        user_input=input("Which city data are you interested in? (Chicago,New York City,Washington): ").lower()
        if user_input in cities:
            city=user_input
            break
        else:
            print("Invalid city: Please try again.")


    # get user input for month (all, january, february, ... , june)
    months=['january','february','march','april','may','june']
    while True:
        #store user input into month variable, if invalid will keep asking user for input until valid
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
    """
    Displays statistics on the most frequent times of travel.
    Using the filtered dataframe, df, from load_data the following statistics are printed out.
    -month with highest use of bike share
    -most popular day to use bike share
    -most common starting hour
    -hour of day with most uses of bikeshare 
    """

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
    """
    Displays statistics on the most popular stations and trip.
    Takes the filtered dataframe, df, from load_data and prints following statistics:
    -most popular starting station
    -most popular ending station
    -most popular combination of start/end stations

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_startingstation=df['Start Station'].mode()[0]
    print("The most frequented station to start biking from is: {}.".format(most_common_startingstation))
    # display most commonly used end station
    most_common_endstation=df['End Station'].mode()[0]
    print("The most frequented ending station is {}.".format(most_common_endstation))

    # display most frequent combination of start station and end station trip
    
    trip_combination_frequencies=df.groupby(['Start Station','End Station']).size()#get frequency table of trip combinations
    most_common_trip=trip_combination_frequencies.idxmax() #find most popular trip combination 
   
    print("Most popular trip starts and ends respectively at: {}".format(most_common_trip))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("The total travel time is: {:.2f} days".format(total_travel_time/(3600*24)))#Convert time to days, 2 decimal place 

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("The average travel time is {:.2f} minutes for each trip".format(mean_travel_time/60))#convert to minutes, 2 decimal place

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=df['User Type'].value_counts()
    print("The distribution of user types are:\n {} \n".format(user_types))

    if city!='washington':  #washington has no gender/birthyear column
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

def tripduration_usertype(df):
    """
    Compute the average trip duration based on each user type

    """
    print('\nCalculating Trip duration based on user type...\n')
    start_time = time.time()

    dur_by_user=df.groupby('User Type')['Trip Duration'].mean()
    dur_by_user_min=(dur_by_user/60).round(2)   # average trip duration in minutes by user type, to 2 dp
    print("Average trip duration by user type:\n{}".format(dur_by_user_min))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def tripduration_genderbirth(df):
    """
    Compute average trip duration based on gender/birth year
    Does not apply for washington since no gender/birth year data available
    """
    print('\nCalculating Trip duration based on gender and birth year\n')
    start_time = time.time()

    #trip duration by gender
    dur_by_gender=df.groupby('Gender')['Trip Duration'].mean()
    dur_by_gender_min=(dur_by_gender/60).round(2) #average trip duration in minutes by gender, to 2 dp
    print("Average trip duration by gender:\n{}".format(dur_by_gender_min))

    #longest trip duration by birth year
    dur_by_birth_max=df.groupby('Birth Year')['Trip Duration'].mean().max()
    dur_idx_max=df.groupby('Birth Year')['Trip Duration'].mean().idxmax()
    dur_by_birth_max_minutes=(dur_by_birth_max/60).round(2)
    #shortest trip by birth year
    dur_by_birth_min=df.groupby('Birth Year')['Trip Duration'].mean().min()
    dur_idx_min=df.groupby('Birth Year')['Trip Duration'].mean().idxmin()
    dur_by_birth_min_minutes=(dur_by_birth_min/60).round(2)

    print("Average trip duration by birth year:\nUsers born in {:.0f} spend the most time on a trip, averaging {:.2f} minutes\nUsers born in {:.0f} spend the least time on a trip, averaging: {:.2f} minutes".format(dur_idx_max,dur_by_birth_max_minutes,dur_idx_min,dur_by_birth_min_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters() #get user input in order to filter data
        df = load_data(city, month, day) #load data and return df that is filtered based on user input

        time_stats(df) #print out stats on most frequent times of travel
        station_stats(df) #print out stats on most frequented stations
        trip_duration_stats(df) #print out stats on trip total time and average trip time
        user_stats(df,city) #print out stats on users
        tripduration_usertype(df)
        if city!='washington': #washington has no gender/birth data
            tripduration_genderbirth(df)
        print("city: {}, month: {}, day: {}".format(city,month,day))
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
