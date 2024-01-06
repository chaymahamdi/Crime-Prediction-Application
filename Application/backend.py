import numpy as np
import pandas as pd
import requests
import joblib

point_de_terminaison = 'https://locatenyc.io/arcgis/rest/services/locateNYC/v1/GeocodeServer/reverseGeocode?location='
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImdoYXppWFgiLCJleHBpcmVzIjoxMDAyMjk1Mjc4Mjc1ODgsInBlcm1pc3Npb25zIjoiYmFzaWMiLCJpYXQiOjE2NDA4MTI1MjcsImV4cCI6MTAwMjI5NTI3ODI3fQ.v1f9Frhjc6orvvqj-2yEUKHD2BdSVTKhgdn0xmPrPc8" 
model = joblib.load(r"D:\Downloads\xgboost.joblib")  
types_des_crimes = {0: 'Violation', 1: "Délit", 2: "Crime"}
crime = open(r"D:\Downloads\newyorkcrime_app\categories_des_crimes\crime.txt", "r").read()  
delit = open(r"D:\Downloads\newyorkcrime_app\categories_des_crimes\délit.txt", "r").read() 
violation = open(r"D:\Downloads\newyorkcrime_app\categories_des_crimes\violation.txt", "r").read()  
def create_custom_df(hour, month, day, latitude, longitude, place, vic_age, vic_race, vic_sex):
    hour = int(hour) if int(hour) < 24 else 0
    api_data = None
    try:
        api_data = requests.get(f'{api_endpoint}{longitude},{latitude}&distance=1000&token={api_token}').json()['address']
        pct, boro = int(api_data["policePrecinct"]), api_data["Borough"]
        boro = boro.upper()
    except Exception as e:
        print(e)
    month = int(month)
    day = int(day)
    in_park = 1 if place == "Dans un parc" else 0
    in_public = 1 if place == "Dans un logement public" else 0
    in_station = 1 if place == "Dans une station" else 0

    columns = np.array(['HEURE_EVENEMENT', 'ADDR_PCT_CD', 'mois', 'jour', 'Latitude', 'Longitude', 'DANS_UN_PARC',
                        'DANS_UN_LOGEMENT_PUBLIC', 'DANS_UNE_STATION', 'BORO_NM_BRONX', 'BORO_NM_BROOKLYN',
                        'BORO_NM_MANHATTAN', 'BORO_NM_QUEENS', 'BORO_NM_STATEN ISLAND', 'BORO_NM_UNKNOWN',
                        'VIC_AGE_GROUP_18-24', 'VIC_AGE_GROUP_25-44', 'VIC_AGE_GROUP_45-64', 'VIC_AGE_GROUP_65+',
                        'VIC_AGE_GROUP_<18', 'VIC_AGE_GROUP_UNKNOWN', 'VIC_RACE_AMERICAN INDIAN/ALASKAN NATIVE',
                        'VIC_RACE_ASIAN / PACIFIC ISLANDER', 'VIC_RACE_BLACK', 'VIC_RACE_BLACK HISPANIC',
                        'VIC_RACE_OTHER', 'VIC_RACE_UNKNOWN', 'VIC_RACE_WHITE', 'VIC_RACE_WHITE HISPANIC', 'VIC_SEX_D',
                        'VIC_SEX_E', 'VIC_SEX_F', 'VIC_SEX_M', 'VIC_SEX_U'])

    data = [[hour, 114 if api_data is None else pct, month, day, latitude, longitude, in_park, in_public,
             in_station, 0 if api_data is None else 1 if boro == "BRONX" else 0,
             0 if api_data is None else 1 if boro == "BROOKLYN" else 0,
             0 if api_data is None else 1 if boro == "MANHATTAN" else 0,
             0 if api_data is None else 1 if boro == "QUEENS" else 0,
             0 if api_data is None else 1 if boro == "STATEN ISLAND" else 0,
             1 if api_data is None else 1 if boro not in ("BRONX", "BROOKLYN", "MANHATTAN", "QUEENS", "STATEN ISLAND") else 0,
             1 if vic_age in range(18, 25) else 0, 1 if vic_age in range(25, 45) else 0,
             1 if vic_age in range(45, 65) else 0, 1 if vic_age >= 65 else 0,
             1 if vic_age < 18 else 0, 0, 1 if vic_race == "AMERICAN INDIAN/ALASKAN NATIVE" else 0,
             1 if vic_race == "ASIATIQUE / ÎLIEN DU PACIFIQUE" else 0,
             1 if vic_race == "NOIRE" else 0, 1 if vic_race == "HISPANIQUE NOIRE" else 0,
             1 if vic_race == "AUTRE" else 0, 1 if vic_race == "INCONNU" else 0,
             1 if vic_race == "BLANCHE" else 0, 1 if vic_race == "HISPANIQUE BLANCHE" else 0,
             0, 0, 1 if vic_sex == "Femme" else 0, 1 if vic_sex == "Homme" else 0, 0]]

    df = pd.DataFrame(data, columns=columns)
    return df.values

def predict_custom(data):
    pred = model.predict(data)[0]
    if pred == 0:
        return types_des_crimes[pred], violation
    elif pred == 1:
        return types_des_crimes[pred], delit
    else:
        return types_des_crimes[pred], crime
