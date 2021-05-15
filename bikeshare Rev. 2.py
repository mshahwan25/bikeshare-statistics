# Rev.2: __main__ function is added
import pandas as pd
import numpy as np
import time

# the followings dictionaries are used as raw data for further selection inputs by users.
citydata = {'Chicago': 'Chicago.csv', 'New York': 'new_york_city.csv', 'Washington':'washington.csv'}
monthslist = { 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'All':13}
monthslistinverted = {1: 'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 13:'All'}
dayslist = { 'Sat':5 , 'Sun':6, 'Mon':0,'Tue':1, 'Wed':2, 'Thu':3, 'Fri':4, 'All':7}
dayslistinverted={0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}

# this function is used to handle raw input by user.
def checkinput (listofinputs, msg):
    print ('-'*50)
    print ('Options are: ', list(listofinputs.keys()))
    inputname = input(msg+'from the above list :')
    while True:
        if inputname not in listofinputs:
            inputname = input('Not valid input, '+ msg + ', Or enter exit to skip: ')
            if inputname == 'exit':
                print ('Thank you, See you later...')
                break
        else:
            print ('You chose ', inputname)
            return(inputname)
            print('-'*50)
            break
 
# this function is used for time statistics
def time_stats(dfrm):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    commonday =dayslistinverted[dfrm['Day'].mode().loc[0]]
    commonmonth = monthslistinverted[dfrm['Month'].mode().loc[0]]
    commonhour = dfrm['Hour'].mode().loc[0]
    # display the most common month   
    print ('Most common month: ', commonmonth)
    # display the most common day of week
    print ('Most common day: ',commonday)
    # display the most common start hour
    print ('Most common hour: ', commonhour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

# this function is used for duration statistics
def trip_duration_stats(dfrm):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = dfrm['Trip Duration'].sum()
    # display mean travel time
    mean_travel_time = dfrm['Trip Duration'].mean()
    print('Total Travel Time in Sec: ', total_travel_time)
    print('Mean Travel Time in Sec: ', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

# this function is used for station statistics
def station_stats(dfrm):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = dfrm['Start Station'].mode().loc[0]
    # display most commonly used end station
    common_end_station = dfrm['End Station'].mode().loc[0] 
    # display most frequent combination of start station and end station trip
    common_frequent_stations = dfrm['StartEndStation'].mode().loc[0]
    print('Most common used start station: ', common_start_station)
    print('Most common used end station: ', common_end_station)
    print('Most frequent stations combinations: ', common_frequent_stations)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

# this function is used for user stats statisticsf
def user_stats(dfrm,cityname):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ('Counts of user types: \n', dfrm['User Type'].value_counts())

    if cityname == 'Washington':
        print ("Sorry, we don't have data regarding gender & birth year for Washington city")
    else:
        print ('Counts of user genders: \n', dfrm['Gender'].value_counts())
        print ('Earliest birth year: ', dfrm['Birth Year'].min())
        print ('Most recent birth year: ', dfrm['Birth Year'].max())
        print ('Most common year: ', dfrm['Birth Year'].mode().loc[0])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def rawdata (dfrm):
    ans = checkinput({'y':'y', 'n':'n'}, "Would you like to check first 5 lines of raw data before computing statistics? ")
    if ans == 'y':
        print (dfrm)
    

def main():
    while True:
        print ("Hello, Let's explain som of US bikeshare data --- Kindly follow the following instructions carefully")
        city = checkinput(citydata, 'Choose a city name to analyze ')
        if city == None:
            break
        else:
            month = checkinput(monthslist, 'Choose a filter month ')
            if month == None:
                break
            else:    
                day = checkinput(dayslist, 'Choose a day filter ')
                if day == None:
                    break
                else: 
                    ans = checkinput({'y':'y', 'n':'n'}, "Would you like to check raw data before computing statistics? ")
                    if ans == None:
                        break
                    else:
                        # main calculations starts execution after proper selection of (city, month, day) filters
                        print ('Filter city:',city,'-','Filter month:',month,'-','Filter day:',day)
                        df = pd.read_csv(citydata[city])
                        df['Start Time'] = pd.to_datetime(df['Start Time'])
                        df['Month'] = df['Start Time'].dt.month
                        df['Day']=df['Start Time'].dt.weekday
                        df['Hour']=df['Start Time'].dt.hour
                        df['StartEndStation'] = df['Start Station']+ " To " + df['End Station']
                    
                        # clear month filter if filter is 'All'
                        if monthslist[month] != 13:
                            df = df.loc[df['Month']==monthslist[month]]
                        # clear day filter if filter is 'All'
                        if dayslist[day] != 7:
                            df = df.loc[df['Day']==dayslist[day]]
                        # perform main calculations
                        if ans == 'y':
                            print (df)
                        time_stats(df)
                        trip_duration_stats(df) 
                        station_stats(df) 
                        user_stats(df,city)
                    
                        # repeat the whole program calculations if needed
                        repeat = checkinput({'y':'y', 'n':'n'}, 'Do you want to restart analyzing? [y/n] ')
                        if repeat == 'n':
                            print ('Thank you, See you later...')
                            break

if __name__ == '__main__':
    main()