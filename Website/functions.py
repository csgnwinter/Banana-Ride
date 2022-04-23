import requests, json
from datetime import datetime
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

# API token
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjg0OTMsInVzZXJfaWQiOjg0OTMsImVtYWlsIjoibGltd2VpamllOTk5QGhvdG1haWwuY29tIiwiZm9yZXZlciI6ZmFsc2UsImlzcyI6Imh0dHA6XC9cL29tMi5kZmUub25lbWFwLnNnXC9hcGlcL3YyXC91c2VyXC9zZXNzaW9uIiwiaWF0IjoxNjQ5NDAyNDc1LCJleHAiOjE2NDk4MzQ0NzUsIm5iZiI6MTY0OTQwMjQ3NSwianRpIjoiMjRkY2QyMGI0Yzg3ZTFhMTBhNmJhZWU0ZjdlZjQ5NTEifQ.dCN_1GYpGxPBsNqdV8rpEORsi21avngbBkd5Lx8jfGE'

# Gets the coordiantes when input postal code
def mapSearch(location):
    # Using requests get 
    url = f'https://developers.onemap.sg/commonapi/search?searchVal={location}&returnGeom=Y&getAddrDetails=Y&pageNum=1'
    r = requests.get(url)
    data = json.loads(r.text)
    if data["found"] != 0:
        lat = data['results'][0]['LATITUDE']
        long = data['results'][0]['LONGTITUDE']
        return lat, long
    else:
        return "No results", "No results"

# Calculation of distance between two nodes
def nodeDistance(node1_lat, node1_long, node2_lat, node2_long):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(node1_lat)
    lon1 = radians(node1_long)
    lat2 = radians(node2_lat)
    lon2 = radians(node2_long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Pre-defined forumla to get the distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def distancePricing(distance):
    base_price = 5.99                                               # Defining a base price of our ride booking
    distance_price = (0.5 * distance)*base_price + base_price       # Some predefined formula to calculate our price
    return distance_price                                           # Returning the data


def surge():
    now = datetime.now()                                            # Get the current time
    current_time = now.strftime("%H:%M:%S")                         # Format the current time
    if "07:30:00" <= current_time < "09:30:00" or "17:30:00" <= current_time < "19:30:00":
        price_surge = 1.7       # If the current time falls within this range, set price surge to 1.7
    elif "09:30:00" <= current_time < "12:00:00" or "19:30:00" <= current_time < "21:30:00":
        price_surge = 1.5       # If the current time falls within this range, set price surge to 1.7
    elif "12:00:00" <= current_time < "17:30:00" or "21:30:00" <= current_time < "00:00:00":
        price_surge = 1.2       # If the current time falls within this range, set price surge to 1.7
    else:
        price_surge = 1         # If the current time does not fall within any of these range, set price surge to 1.7
    return price_surge          # Return the value of price_surge


def matching_panda(carType, num_seats, customer_lat, customer_long):
    df = pd.read_csv("Website/driver.csv")
    driverLocation = [None]*2
    # initialize variables, we'll take the first driver as closest and closest distance will be the max distance possible
    closest_driver = 0
    closest_distance = 999999

    # looping through the dataframe of drivers
    for i in range(len(df)):
        driver_seats = int(df.loc[i, "num_seats"])
        driver_booked = int(df.loc[i, "isBooked"])
        driver_carType = df.loc[i, "car_type"]

        # Check if driver seats and car are the same and if it's booked or not
        if driver_seats == num_seats and driver_booked == 0 and driver_carType == carType:
            driver_lat = float(df.loc[i, "current_lat"])
            driver_long = float(df.loc[i, "current_long"])

            # Using routing algorithm to calculate the total distance between customer and driver
            total_distance = nodeDistance(customer_lat, customer_long, driver_lat, driver_long)

            # if its closer (lesser) than previous driver, we'll assign new closest driver
            if total_distance < closest_distance:
                driverLocation[0] = driver_lat
                driverLocation[1] = driver_long
                closest_driver = i
                closest_distance = total_distance

    df.at[closest_driver, "isBooked"] = 1
    return driverLocation
