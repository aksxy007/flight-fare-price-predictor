import streamlit as st
import pickle
import sklearn
import pandas as pd
import datetime
import geopy
from geopy import Nominatim
from geopy.distance import great_circle


class MakeMapOfPlaces(dict):
    def __init__(self):
        self = dict()

    def add(self, key, lat, long):
        self[key] = [lat, long]


Map = MakeMapOfPlaces()

Airlines_dict = pickle.load(open("Airlines.pkl", "rb"))
Airlines = pd.DataFrame(Airlines_dict)
model = pickle.load(open("flight_fare.pkl", "rb"))
Stoppages = pickle.load(open("Stoppages.pkl", "rb"))

st.title('Flight Fare Predictor')
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)
journey_date = st.date_input('Journey Date', today)
# return_date = st.date_input('Return Date', tomorrow)
# if journey_date > return_date:
#     st.error('Return date must fall after Journey date.')

t = datetime.datetime.now()
departureTime = datetime.time(t.hour, t.minute)
dept_Time = st.time_input('Departure Time', departureTime)
arrivalTime = datetime.time(t.hour, t.minute)
arrival_Time = st.time_input('Arrival Time', departureTime)

# if arrival_Time.hour <= dept_Time.hour:
#     st.error('Departure Time  must be before Arrival date.')

selected_source = st.selectbox(
    "From",
    ("Delhi", "Bangalore", "Chennai", "Kolkata", "Mumbai"))
selected_Destination = st.selectbox(
    "To",
    ("Bangalore", "Delhi", "Chennai", "Kolkata", "Kochi", "Hyderabad"))

if selected_source == selected_Destination:
    st.error('Error: Change Either Source or Destination to see Results.')

stops = st.selectbox(
    "Total stops",
    ("Non stop", "1", "2", "3", "4")
)


# def getstops(count):
#     while int(stops) != count:
#         count += 1
#     if count == int(stops):
#         return

if stops != 'Non stop':
    intermediateStops = []
    # count = 0
    # intermediateStops = st.multiselect(
    #     "Intermediate Stops",
    #     Stoppages
    # )

    columns = st.columns(int(stops))
    for i, col in enumerate(columns):
        text = f"Intermediate Stop {i+1}"
        with col:
            intermediateStops.append(st.selectbox(
                text,
                Stoppages
            )
            )
    # st.write("Stoppages:", intermediateStops)

selected_airline = st.selectbox(
    "Airlines",
    Airlines[0].values)


def makeroute():
    route = []
    if stops != 'Non stops':
        route.append(selected_source)
        for i in intermediateStops:
            print(i)
            route.append(i)
        route.append(selected_Destination)

    return route



def getDistance(route):
    loc = Nominatim(user_agent="GetLoc")
    distance = 0
    if len(route) != 0:
        for i in range(0, len(route) - 1):
            getLoc = loc.geocode(route[i])
            lat = getLoc.latitude
            long = getLoc.longitude
            Map.add(selected_source, lat, long)

            getLoc = loc.geocode(route[i + 1])
            lat = getLoc.latitude
            long = getLoc.longitude
            Map.add(selected_Destination, lat, long)

            start = (Map.get(selected_source)[0], Map.get(selected_source)[1])
            stop = (Map.get(selected_Destination)[0], Map.get(selected_Destination)[1])
            # print(start)
            # print(stop)
            distance += great_circle(start, stop).km
    else:
        getLoc = loc.geocode(selected_source)
        lat = getLoc.latitude
        long = getLoc.longitude
        Map.add(selected_source, lat, long)

        getLoc = loc.geocode(selected_Destination)
        lat = getLoc.latitude
        long = getLoc.longitude
        Map.add(selected_Destination, lat, long)
        distance = 0
        start = (Map.get(selected_source)[0], Map.get(selected_source)[1])
        stop = (Map.get(selected_Destination)[0], Map.get(selected_Destination)[1])
        # print(start)
        # print(stop)
        distance += (great_circle(start, stop).km)

    return distance


def pricePredict():
    if stops != 'Non stop':
        flightRoute = makeroute()

    Journey_day = int(pd.to_datetime(journey_date, format="%Y/%m/%d").day)
    Journey_month = int(pd.to_datetime(journey_date, format="%Y/%m/%d").month)
    # print(Journey_day, Journey_month)
    day_of_week_number = pd.to_datetime(journey_date, format="%Y/%m/%d").dayofweek

    Dept_hour = dept_Time.hour
    Dept_min = dept_Time.minute
    # print(Dept_hour, Dept_min)

    Arrival_hour = arrival_Time.hour
    Arrival_min = arrival_Time.minute

    duration_hour = abs(Arrival_hour - Dept_hour)
    duration_min = abs(Arrival_min - Dept_min)

    if duration_hour == 0:
        duration_hour = 24

    Duration_in_minutes = int(duration_hour * 60 + duration_min)
    print(Duration_in_minutes)

    Total_stops = stops
    if Total_stops == "Non stop":
        Total_stops = 0
    print(Total_stops)

    airline = selected_airline
    if (airline == 'Jet Airways'):
        Jet_Airways = 1
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'IndiGo'):
        Jet_Airways = 0
        IndiGo = 1
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Air India'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 1
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Multiple carriers'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 1
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'SpiceJet'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 1
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Vistara'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 1
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'GoAir'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 1
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Multiple carriers Premium economy'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 1
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Jet Airways Business'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 1
        Vistara_Premium_economy = 0
        Trujet = 0

    elif (airline == 'Vistara Premium economy'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 1
        Trujet = 0

    elif (airline == 'Trujet'):
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 1

    else:
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0

    # print(Jet_Airways,
    #     IndiGo,
    #     Air_India,
    #     Multiple_carriers,
    #     SpiceJet,
    #     Vistara,
    #     GoAir,
    #     Multiple_carriers_Premium_economy,
    #     Jet_Airways_Business,
    #     Vistara_Premium_economy,
    #     Trujet)

    Source = selected_source
    if (Source == 'Delhi'):
        s_Delhi = 1
        s_Kolkata = 0
        s_Mumbai = 0
        s_Chennai = 0

    elif (Source == 'Kolkata'):
        s_Delhi = 0
        s_Kolkata = 1
        s_Mumbai = 0
        s_Chennai = 0

    elif (Source == 'Mumbai'):
        s_Delhi = 0
        s_Kolkata = 0
        s_Mumbai = 1
        s_Chennai = 0

    elif (Source == 'Chennai'):
        s_Delhi = 0
        s_Kolkata = 0
        s_Mumbai = 0
        s_Chennai = 1

    else:
        s_Delhi = 0
        s_Kolkata = 0
        s_Mumbai = 0
        s_Chennai = 0
    #
    # print(s_Delhi,
    #     s_Kolkata,
    #     s_Mumbai,
    #     s_Chennai)

    # Destination
    # Banglore = 0 (not in column)
    Source = selected_Destination
    if (Source == 'Kochi'):
        d_Kochi = 1
        d_Delhi = 0
        d_Hyderabad = 0
        d_Kolkata = 0

    elif (Source == 'Delhi'):
        d_Kochi = 0
        d_Delhi = 1
        d_Hyderabad = 0
        d_Kolkata = 0

    elif (Source == 'Hyderabad'):
        d_Kochi = 0
        d_Delhi = 0
        d_Hyderabad = 1
        d_Kolkata = 0

    elif (Source == 'Kolkata'):
        d_Kochi = 0
        d_Delhi = 0
        d_Hyderabad = 0
        d_Kolkata = 1

    else:
        d_Kochi = 0
        d_Delhi = 0
        d_Hyderabad = 0
        d_Kolkata = 0

    # print(
    #     d_Kochi,
    #     d_Delhi,
    #     d_Hyderabad,
    #     d_Kolkata
    # )
    # Distance= 1234.2344

    Distance = getDistance(flightRoute)
    # print(Distance)

    prediction = model.predict([[
        Total_stops,
        Journey_day,
        Journey_month,
        day_of_week_number,
        Distance,
        Dept_hour,
        Dept_min,
        Arrival_hour,
        Arrival_min,
        Duration_in_minutes,
        Air_India,
        GoAir,
        IndiGo,
        Jet_Airways,
        Jet_Airways_Business,
        Multiple_carriers,
        Multiple_carriers_Premium_economy,
        SpiceJet,
        Trujet,
        Vistara,
        Vistara_Premium_economy,
        s_Chennai,
        s_Delhi,
        s_Kolkata,
        s_Mumbai,
        d_Kochi,
        d_Delhi,
        d_Hyderabad,
        d_Kolkata,
    ]])

    PredictedPrice = round(prediction[0], 2)

    return Distance, PredictedPrice


if st.button("Calculate Price"):
    # price = 0
    Distance, price = pricePredict()
    distanceText = f'<p style="font-family:sans-serif; color:White; font-size: 15px;">The Journey is: {round(Distance, 3)} KM </p>'
    priceText = f'<p style="font-family:sans-serif; color:White; font-size: 20px;">The Flight will cost you: Rs {price} </p>'
    st.markdown(priceText, unsafe_allow_html=True)
    st.markdown(distanceText, unsafe_allow_html=True)
