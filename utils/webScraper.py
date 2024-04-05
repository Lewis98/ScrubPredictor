import requests
import json
import csv

from datetime import datetime, timedelta


def parseDate(dateStr):

    dateArr = dateStr.split('-')

    return datetime(
        int(dateArr[0]),
        int(dateArr[1]),
        int(dateArr[2])
    )

def avg(arr):
    if (len(arr) == 0):
        return 0
    return sum(arr) / len(arr)

def processData(rawData):
    data = json.loads(rawData)

    day = data['date']
    weekday = data['a_day']

    glider_flights = 0
    g_tows = 0
    g_winches = 0

    other_flights = 0

    g_durations = []
    o_durations = []

    g_crosscountry = 0
    o_crosscountry = 0

    for flight in data['flights']:
        fType = (data['devices'][flight['device']])['aircraft_type']
        

        duration = flight['duration']

        if fType == 1:

            glider_flights += 1
            if duration is None: 
                g_crosscountry += 1
            else:
                g_durations.append(flight['duration'])


            if flight['tow'] is not None:
                g_tows += 1
            else:
                g_winches += 1

        else:

            other_flights += 1
            if duration is None: 
                o_crosscountry += 1
            else:
                o_durations.append(flight['duration'])

    return f"{day},{weekday},{glider_flights},{avg(g_durations)},{g_crosscountry},{g_tows},{g_winches},{other_flights},{avg(o_durations)},{o_crosscountry}\n"




if __name__ == "__main__":
    print('Select date range start (Format : YYYY-MM-DD)')
    startDate = parseDate(input())

    print('Select date range end (Format : YYYY-MM-DD)')
    endDate = parseDate(input())

    dateFilter = {0,1,2,3,4,5,6} # Wednesday, Saturday, Sunday

    day = startDate
    dateRangeSize = (endDate - startDate).days
    processed = 0
    reportOn = 15

    fname = 'csvOutput.csv'

    with open(fname, 'w', newline='') as csvFile:

        csvFile.write("Day,Weekday,Glider flights,Avg Duration,Cross Countrys,Tows,Winches,Other Flights,Avg Duration,Cross Country\n")

        while day <= endDate:
            if (day.weekday() in dateFilter):
                rawData = requests.get(f"https://flightbook.glidernet.org/api/logbook/GB-0411/{day.strftime('%Y-%m-%d')}")
                csvOut = processData(rawData.text)
                csvFile.write(csvOut)
        
                processed += 1
                if processed % reportOn == 0:
                    print(f"Processed {processed}/{dateRangeSize}")

            day += timedelta(days=1)
        print(f"Processed {processed}/{dateRangeSize}")
