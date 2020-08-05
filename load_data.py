#  Load data
# imports
from initial_config import *
import pandas as pd

# variables
csv = r"C:\jescudero\Esri\AM\data\erradicacion_05_08.csv"

# Read data
names = ["nombredepartamento", "nombremunicipio", 'hectareas', 'grupoarmado', "latitud", "longitud"]
df = pd.read_csv(csv, sep=",", usecols=[13, 14, 21, 31, 43, 44], names=names, skiprows=1)


# ----------- Method one: With ArcGIS Python API --------------
# ArcGIS imports
from arcgis.gis import GIS
from arcgis.features import GeoAccessor

# Connect to gis
gis = GIS(agol_url, agol_user, agol_password)

# Prepare data
df_xy = GeoAccessor.from_xy(df, "longitud", "latitud", sr=4326)
fs = df_xy.spatial.to_featureset()

# Append data
erradicacion_id = "9bc352654401432ca046825fd35f8fc1"
erradicacion_item = gis.content.get(erradicacion_id)
result = erradicacion_item.layers[0].edit_features(adds=fs)

print(result)


# Method two: With REST (Without ArcGIS Python API)
# Imports
from urllib import parse
import requests
import json

# Authenticate
values = {'username': agol_user, 'password': agol_password, 'referer': 'https://www.arcgis.com', 'f': 'json'}
params = parse.urlencode(values).encode('ascii')
token = None
with requests.post("https://arcgis.com/sharing/rest/generateToken", params=params,  verify=False) as response:
    if response.status_code == 200:
        result = json.loads(response.content)
        if 'token' in result:
            token = result['token']
print(token)

# Prepare data
adds = []
for i, row in df.iterrows():
    depto = row["nombredepartamento"]
    mpio = row["nombremunicipio"]
    x = row["longitud"]
    y = row["latitud"]
    atts = {'nombredepartamento': depto, 'nombremunicipio': mpio}
    geom = {'x': x, 'y': y}
    newFeature = {"attributes": atts, "geometry": geom}
    adds.append(newFeature)

# Append data
url = "https://services2.arcgis.com/0K7cILuuyNUzfzjA/arcgis/rest/services/ErradicacionCoca/FeatureServer/0/addFeatures"
data = {"features": json.dumps(adds)}
params = {"f": "json", "token": token}
with requests.post(url, data=data, params=params, verify=False) as response:
    if response.status_code == 200:
        result = json.loads(response.content)
        print(result)



