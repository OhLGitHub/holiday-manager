# FOR TOM OR YIHUA: My code runs, but I was not able to complete all requirements. My sincerest apologies. I tried.

# HolidayManager
# Lindsey Oh

# Import
from datetime import datetime
import json
from pprint import pprint
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import types
import copy

# RUBRIC: Can see classes created with meaningful properties and method names.
# RUBRIC: Uses classes and are creating instances for using their classes.

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    """
    This is a class for Holidays.
    """
    def __init__(self,name,date): # Date must be input as a string in the format 'Jan 01, 2022'
        self.__name = name
        self.__date = datetime.strptime(date, "%b %d, %Y").date()
    
    def __str__ (self):
        return f'{self.__name} ({self.__date})' # String Method was implemented. You can print an object with the string representation.
    
    def HolidayDict(self):
        return {'name':self.__name,'date':self.__date}
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container: where you store your holidays (ask Tom)
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    """
    This is a class for the list of Holidays.
    """
    def __init__(self):
        self.innerHolidays = []

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if isinstance(holidayObj, Holiday):
            # Use innerHolidays.append(holidayObj) to add holiday
            self.innerHolidays.append(holidayObj.HolidayDict())
            # print to the user that you added a holiday
            print(f'{holidayObj} has been added.')
        else:
            print(f'{holidayObj} is not a Holiday Object.')

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for dict in self.innerHolidays:
            if (list(dict.values())[0] == HolidayName) and (list(dict.values())[1] == datetime.strptime(Date, "%b %d, %Y").date()):
                # Return Holiday
                print(f'{HolidayName} is in the list.')
            else:
                print("Error: Enter the holiday name as a string, the holiday date as a string in the format 'Jan 01, 2020'")

    def removeHoliday(self, HolidayName, Date): # HolidayName must be a string; Date must be a string in the format 'Jan 01, 2020'
        # Find Holiday in innerHolidays by searching the name and date combination.
        counter = 0
        for innerHoldict in self.innerHolidays:
            if (innerHoldict['name'] == HolidayName) and (innerHoldict['date'] == datetime.strptime(Date, "%b %d, %Y").date()):
                # remove the Holiday from innerHolidays
                del self.innerHolidays[counter]
                # inform user you deleted the holiday
                print(f'{HolidayName} has been removed.')
                break
            counter += 1

    def read_json(self, filelocation): # filelocation example: 'holidays.json'
        # Read in things from json file location
        with open(filelocation,'r') as jsonfile:
            data = json.load(jsonfile)
            # pprint(data)
        # Use addHoliday function to add holidays to inner list
            for holdict in data['holidays']:
                holdict['date'] = datetime.strptime(holdict['date'], "%Y-%m-%d").date()
                self.innerHolidays.append(holdict)
        # print(HolidayList().innerHolidays)

    def save_to_json(self, filelocation): # filelocatione example: 'outputjson.json'
        jsoninnerH = copy.deepcopy(self.innerHolidays)
        for innerdict in jsoninnerH:
            innerdict['date'] = innerdict['date'].strftime('%Y-%m-%d')
        # Write out json file to selected file.
        json_object = json.dumps(jsoninnerH, indent=4)
        with open(filelocation,'w') as output:
            output.write(json_object)
        
    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        def getHTML(url):
            response = requests.get(url) # variable that is making a GET request to the website at url
            return response.text
        
        for year in range(2020,2023):
            html = getHTML(f'https://www.timeanddate.com/calendar/print.html?year={year}&country=1&cols=3&hol=33554809&df=1') # get the data using getHTML function
            soup = BeautifulSoup(html, 'html.parser') # store Beautiful Soup oject, pass in HTML object, parse
            timeanddate = []
            for column in soup.find_all('td'):
                timeanddate.append(column.text)
            holidays_only = timeanddate[-239:-1]
            dates_only = holidays_only[::2]
            names_only = holidays_only[1::2]
            fulldates_only = [d + f', {year}' for d in dates_only]
            formatted_dates = [datetime.strptime(ds, "%b %d, %Y").date() for ds in fulldates_only]
            for (n,d) in zip(names_only,formatted_dates):
                kvp = {'name':n, 'date':d}
                # Check to see if name and date of holiday is in innerHolidays array
                if kvp in self.innerHolidays:
                    pass
                # Add non-duplicates to innerHolidays
                else:
                    self.innerHolidays.append(kvp)
                # Handle any exceptions.     

    def numHolidays(self):
        return len(self.innerHolidays) # Return the total number of holidays in innerHolidays
    
    # def filter_holidays_by_week(year, week_number):
    #     # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
    #     filter(lambda weeknumber: weeknumber == week_number, HolidayList().innerHolidays)
    #     # Week number is part of the the Datetime object
    #     # Cast filter results as list
    #     # return your holidays

    # def displayHolidaysInWeek(holidayList):
    #     # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
    #     # Output formated holidays in the week. 
    #     # * Remember to use the holiday __str__ method.

    # def getWeather(weekNum):
    #     # Convert weekNum to range between two days
    #     # Use Try / Except to catch problems
    #     # Query API for weather in that week range
    #     # Format weather information and return weather string.

    # def viewCurrentWeek():
    #     # Use the Datetime Module to look up current week and year
    #     # Use your filter_holidays_by_week function to get the list of holidays 
    #     # for the current week/year
    #     # Use your displayHolidaysInWeek function to display the holidays in the week
    #     # Ask user if they want to get the weather
    #     # If yes, use your getWeather function and display results



def main():
    # Initialize HolidayList Object
    HolListObj = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    HolListObj.read_json('holidays.json')
    # Scrape additional holidays using your HolidayList scrapeHolidays function.
    HolListObj.scrapeHolidays()
    # Create while loop for user to keep working with HolidayManager
    is_running = True
    no_changes = False
    while is_running == True:
        print(f'''
Holiday Manager
===================
There are {HolListObj.numHolidays()} holidays stored in the system.
        ''')
        # Display User Menu
        print(f''' 
Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit
        ''')
        # Get user input and check for errors
        choice = str(input('Type 1 to Add, 2 to Remove, 3 to Save, 4 to View, 5 to Exit: ')).strip() # strip spaces from user input
        if choice == '1':
            print(f'''
Add a Holiday
=============
Holiday date must be in the format 'Jan 01, 2020'
        ''')
            add_namestring = str(input('Name: ')).strip() # strip spaces from user input
            add_datestring = str(input('Date: ')).strip() # strip spaces from user input
            if isinstance(add_namestring, str) and isinstance(add_datestring, str):
                HolListObj.addHoliday(Holiday(add_namestring,add_datestring))
                continue
            else: 
                print('Error: you did not follow directions.')
                continue
        elif choice == '2':
            print(f'''
Remove a Holiday
================
Holiday date must be in the format 'Jan 01, 2020'
        ''')
            remove_namestring = str(input('Name: ')).strip() # strip spaces from user input
            remove_datestring = str(input('Date: ')).strip() # strip spaces from user input
            if isinstance(remove_namestring, str) and isinstance(remove_datestring, str):
                HolListObj.removeHoliday(remove_namestring,remove_datestring)
                continue
            else:
                print('Error: you did not follow directions.')
                continue
        elif choice == '3':
            print(f'''
Saving Holiday List
====================
        ''')
            save_changes = str(input('Are you sure you want to save your changes? [y/n]: ')).lower().strip() # lowercase, strip spaces from user input
            if save_changes == 'y':
                HolListObj.save_to_json('outputjson.json')
                print('''
Success:
Your changes have been saved.
                ''')
                continue
            elif save_changes == 'n':
                continue
            else:
                print('Error: you did not follow directions.')
                continue
        elif choice == '4':
            print(f'''
View Holidays
=================
        ''')
            pprint(HolListObj.innerHolidays)
            continue
        elif choice == '5':
            if no_changes == True:
                print('''
Exit
=====
                ''')
                exit_nochanges = str(input('Are you sure you want to exit? [y/n]: ')).lower().strip() # lowercase, strip spaces from user input
                if exit_nochanges == 'y':
                    print('''
Goodbye!
                    ''')
                    is_running = False
                elif exit_nochanges == 'n':
                    continue
                else:
                    print('Error: you did not follow directions.')
                    continue
            else:
                print('''
Exit
=====
Your changes will be lost.
                ''')
                exit_changes = str(input('Are you sure you want to exit? [y/n]: ')).lower().strip() # lowercase, strip spaces from user input
                if exit_changes == 'y':
                    print('''
Goodbye!
                    ''')
                    is_running = False
                elif exit_changes == 'n':
                    continue
                else:
                    print('Error: you did not follow directions.')
                    continue
        else:
            print('Error: you did not follow directions.')
            continue
        is_running = False

    # 6. Run appropriate method from the HolidayList object depending on what the user input is  ---> holidayList.addHoliday()
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.