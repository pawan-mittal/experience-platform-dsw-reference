'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2019 Adobe Systems Incorporated
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Adobe Systems Incorporated and its suppliers,
 * if any.  The intellectual and technical concepts contained
 * herein are proprietary to Adobe Systems Incorporated and its
 * suppliers and are protected by all applicable intellectual property
 * laws, including trade secret and copyright laws.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
'''

import requests
import json
from utils import setup_logger, http_request

LOGGER = setup_logger(__name__)
CONTENT_TYPE = "application/json"


def get_tenant_id(tenant_id_url, headers):
    """
    Get TenantId by making a GET call to "/data/foundation/schemaregistry/stats"
    :param tenant_id_url - url
    :param headers - headers
    :return - tenant id

    """

    res_text = http_request("get", tenant_id_url, headers)
    tenant_id = "_" + json.loads(res_text)["tenantId"]
    LOGGER.debug("tenant_id = %s", tenant_id)
    return tenant_id


def get_class_id(create_class_url, headers, class_title, data, reset_demo):
    """
    Get the classId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/classes"
    :param create_class_url:  url
    :param headers: headers
    :param class_title: class title
    :param data: post request data
    :return: class url
    """
    try:
        # Set the class title and description
        data['title'] = class_title   
        data['description'] = class_title
        headers["Content-type"] = CONTENT_TYPE
        res_text = http_request("POST", create_class_url, headers, json.dumps(data))
        class_id = json.loads(res_text)["$id"]
        LOGGER.debug("class_id = %s", class_id)
        
        return class_id

    except requests.exceptions.HTTPError as http_err:
        http_error_json_msg = u'%s' % (http_err)
        error_json = json.loads(http_error_json_msg)
        if(reset_demo == "True" and error_json["status"] == 400) :
            id_param = get_id_from_errordetail(error_json)
            existing_class_id = create_class_url + "/" + id_param
            print ("Deleting class with id ", existing_class_id)
            http_request("delete", existing_class_id, headers)

            return get_class_id(create_class_url, headers, class_title, data, reset_demo)
            
def get_mixin_id(create_mixin_url, headers, mixin_title, data, class_id, tenant_id, mixin_definition_title, reset_demo):
    """
    Get the mixinId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/mixins"

    :param create_mixin_url: url
    :param headers: headers
    :param mixin_title: mixin title
    :param data: post request data
    :param class_id: class url
    :param tenant_id: tenant id in the org
    :param mixin_definition_title: mixin definition title to set the url
    :return: mixin url
    """

    try:
        # Set the title and description
        data['title'] = mixin_title
        data['description'] = mixin_title
        # Set the class id
        data['meta:intendedToExtend'][0] = class_id

        # Set the tenant id
        for key in list(data["definitions"]):
            data["definitions"][mixin_definition_title] = data["definitions"][key]
            for nested_key in list(data["definitions"][key]["properties"]):
                data["definitions"][key]["properties"][tenant_id] = data["definitions"][key]["properties"][nested_key]
                del data["definitions"][key]["properties"][nested_key]
            del data["definitions"][key]
        # Set the reference url
        data["allOf"][0]["$ref"] = "#/definitions/" + mixin_definition_title
        headers["Content-type"] = CONTENT_TYPE
        print ("mixin data : ", data)
        res_text = http_request("post", create_mixin_url, headers, json.dumps(data))
        mixin_id = json.loads(res_text)["$id"]
        LOGGER.debug("mixin_id = %s", mixin_id)
        return mixin_id

    except requests.exceptions.HTTPError as http_err:
        http_error_json_msg = u'%s' % (http_err)
        error_json = json.loads(http_error_json_msg)
        if(reset_demo == "True" and error_json["status"] == 400) :
            id_param = get_id_from_errordetail(error_json)
            existing_mixin_id = create_mixin_url + "/" + id_param
            print ("Deleting mixin with id ", existing_mixin_id)
            http_request("delete", existing_mixin_id, headers)

            return get_mixin_id(create_mixin_url, headers, mixin_title, data, class_id, tenant_id, mixin_definition_title, reset_demo)

def get_schema_id(create_schema_url, headers, schema_title, class_id, mixin_id, data, reset_demo):
    """
    Get the schemaId by making a POST REQUEST to "/data/foundation/schemaregistry/tenant/schemas"

    :param create_schema_url: url
    :param headers: headers
    :param schema_title: schema title
    :param class_id: class_url
    :param mixin_id: mixin_url
    :param data: post request data
    :return: schema_url
    """
    try:
        # Set the title and description
        data['title'] = schema_title
        data['description'] = schema_title
        # Set the mixin id
        data['meta:extends'][0] = mixin_id
        data["allOf"][0]["$ref"] = mixin_id
        # Set the class id
        data['meta:extends'][1] = class_id
        data["allOf"][1]["$ref"] = class_id

        headers["Content-type"] = CONTENT_TYPE
        res_text = http_request("post", create_schema_url, headers, json.dumps(data))
        schema_id = json.loads(res_text)["$id"]
        LOGGER.debug("schema_id = %s", schema_id)
        return schema_id

    except requests.exceptions.HTTPError as http_err:
        http_error_json_msg = u'%s' % (http_err)
        error_json = json.loads(http_error_json_msg)
        if(reset_demo == "True" and error_json["status"] == 400) :
            id_param = get_id_from_errordetail(error_json)
            existing_schema_id = create_schema_url + "/" + id_param
            print ("Deleting schema with id ", existing_schema_id)
            http_request("delete", existing_schema_id, headers)

            return get_schema_id(create_schema_url, headers, schema_title, class_id, mixin_id, data, reset_demo)

def get_id_from_errordetail(error_json):
    """
    :param error_json : json data
    {
        "type": "/placeholder/type/uri",
        "status": 400,
        "title": "BadRequestError",
        "detail": "Title must be unique. An object https://ns.adobe.com/salesvelocity/classes/f412489610bf750ad40b30e0b7804a13 already exists with the same title."
    }
    """
    detail = error_json['detail']
    startIndex = detail.find("https://ns.adobe.com")
    if(startIndex != -1):
        detail = detail[startIndex:]
        endIndex = detail.find(" ")
        detail = detail[0: endIndex]
        detail = detail.replace("https://ns.adobe.com/", "")
        detail = detail.replace("/", ".")

        return "_" + detail