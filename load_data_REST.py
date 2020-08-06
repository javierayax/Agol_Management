#  Load data
# imports
from initial_config import *
import pandas as pd
from urllib import parse
import requests
import json

# variables
csv = r"C:\jescudero\Esri\AM\data\erradicacion_06_08.csv"
url = "https://services2.arcgis.com/0K7cILuuyNUzfzjA/arcgis/rest/services/ErradicacionCoca/FeatureServer/0/addFeatures"

# Read data
names = ["nombredepartamento", "nombremunicipio", 'hectareas', 'grupoarmado', "latitud", "longitud"]
df = pd.read_csv(csv, sep=",", usecols=[13, 14, 21, 31, 43, 44], names=names, skiprows=1)

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
data = {"features": json.dumps(adds)}
params = {"f": "json", "token": token}
with requests.post(url, data=data, params=params, verify=False) as response:
    if response.status_code == 200:
        result = json.loads(response.content)
        print(result)

# End
