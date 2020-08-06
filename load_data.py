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

# End
