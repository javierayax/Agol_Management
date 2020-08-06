# publish services
# imports
import arcpy

# variables
aprx_path = r"C:\jescudero\Esri\AM\aprx\data_grid.aprx"
service = "Grilla"

# environments
arcpy.env.overwriteOutput = 1

# Identify map and aprx
aprx = arcpy.mp.ArcGISProject(aprx_path)
map = aprx.listMaps()[0]

# Get the properties of the service
ssd = map.getWebLayerSharingDraft("HOSTING_SERVER", "FEATURE", "Grilla")
ssd.summary = "Grilla de coca"
ssd.description = u'Grilla de coca para el proceso de interpretación'
ssd.tags = u'Coca, Interpretación'
ssd.portalFolder = 'Datos'
ssd.overwriteExistingService = True

# Export service definition draft
draft = r"{0}\{1}.sddraft".format(aprx.homeFolder, service)
ssd.exportToSDDraft(draft)

# Export service definition data
definition = r"{0}\{1}.sd".format(aprx.homeFolder, service)
arcpy.StageService_server(draft, definition)

# Upload service definition
arcpy.UploadServiceDefinition_server(definition, "My Hosted Services")

# End

