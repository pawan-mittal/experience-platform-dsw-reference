#pip install jsonschema
from utils import setup_logger
import json
from genson import SchemaBuilder

LOGGER = setup_logger(__name__)

def make_aep_compatible(json_schema_str):
        json_schema_str = json_schema_str.replace('"type": "null"', '"type": "string"')
        json_schema_str = json_schema_str.replace('@', '')

        return json_schema_str

def gen_mixin_schema_from_json_data(raw_data_file, raw_data_mixin_schema_file):
    # Read the json data 
    # Getting dictionary
    with open(raw_data_file, 'r') as jsonFile:
        datastore = json.load(jsonFile)
        jsonFile.close()
    
    builder = SchemaBuilder(schema_uri = None)
    #builder.add_object({"hi": "there"})
    builder.add_object(datastore)
    LOGGER.info("Mixin json schema generated successfully.")
    #LOGGER.info("Schema: %s" , builder.to_schema())

    # Make generated schema AEP Compatible
    json_schema_str = builder.to_json(indent=2)
    json_schema_str = make_aep_compatible(json_schema_str)

    with open(raw_data_mixin_schema_file, 'w') as outfile:
        #json.dump(builder.to_schema(), outfile)
        outfile.write(json_schema_str)
        outfile.close()

    return json_schema_str

if __name__ == "__main__":
    LOGGER.info("<--------- Generating Mixins --------->")
    FILE_PATH = "../datasets/retail/XDM0.9.9.9/"
    gen_mixin_schema_from_json_data(FILE_PATH + "13724.json", FILE_PATH + "13724-mixin-schema.json")
        