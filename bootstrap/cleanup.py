import requests
import json
from utils import setup_logger, http_request

LOGGER = setup_logger(__name__)

def cleanup(schema_title, create_schema_url, class_title, create_class_url, mixin_title, create_mixin_url, headers):
    LOGGER.info("<--------- Clean up --------->")
    headers["Accept"] = "application/vnd.adobe.xed-full+json"
    delete_item(schema_title, create_schema_url, headers)
    delete_item(class_title, create_class_url, headers)
    delete_item(mixin_title, create_mixin_url, headers)

    return True

def delete_item(title, url, headers):
    LOGGER.info("<--------- delete_item --------->")
    get_url = url + "?property=title==" + title
    res_text = http_request("get", get_url, headers)
    results = json.loads(res_text)["results"]
    if len(results) == 0:
        LOGGER.debug("No aep item found with title = %s", title)
    else: 
        for result in results:
            itemId  = result["meta:altId"] # _tenantid.schemas.cb4c0bab66a387c031b8a571291e4a30
            LOGGER.debug("delete itemId = %s", itemId)
            existing_item_url = url + "/" + itemId
            headers["Accept"] = "application/vnd.adobe.xed+json"
            http_request("delete", existing_item_url, headers)        