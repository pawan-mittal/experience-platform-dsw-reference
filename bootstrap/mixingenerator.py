
#pip install jsonschema
import requests
import yaml
from utils import setup_logger
from dictor import dictor
import copy
import json
import jsonschema
from genson import SchemaBuilder

LOGGER = setup_logger(__name__)
FILE_PATH = "../datasets/retail/XDM0.9.9.9/"
CONTENT_TYPE = "application/json"

# Read the json data 
# # Getting dictionary
with open(FILE_PATH + "input.json", 'r') as jsonFile:
    datastore = json.load(jsonFile)
    jsonFile.close()

#print ("JSON Data", datastore)

builder = SchemaBuilder(schema_uri=None)
#builder.add_object({"hi": "there"})
builder.add_object(datastore)
print ("Generated Schema: ", builder.to_schema())
with open(FILE_PATH + "genson-schema-" + "input.json", 'w') as outfile:
        json.dump(builder.to_schema(), outfile)
        
# Set the tenant id
#for key in list(datastore):
    #print ("key, ", key)

if __name__ == "__main__":
    LOGGER.info("Generating Mixins - JSON")
        