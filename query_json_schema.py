# -*- coding: utf-8 -*-
import json

def get_type_for_key_path(schema: dict, key_path: str) -> str: 
    '''
       Given a valid json schema https://json-schema.org/specification.html
       and a key path, returns the type of the property
    '''
    tokens = key_path.split(".")
    current = schema["properties"]
    prop = None
    definitions = schema["definitions"]
    pos = 0
    
    while pos <= len(tokens) - 1:
        t = tokens[pos]
        
        if t in current:
            prop = current[t]
            
            if "$ref" in prop:
                ref = prop["$ref"][14:]
                prop = definitions[ref]
                current = prop["properties"]
        else:
            return None
        pos += 1

        
    return prop["type"]

def main():
    schema = json.loads('''{
      "$id": "https://example.com/nested-schema.json",
      "title": "nested-schema",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "required": [
        "EmploymentInformation",
        "EmployeePartyID",
        "Age"
      ],
      "properties": {
        "EmployeePartyID": {
          "type": "string",
          "minLength": 1,
          "maxLength": 3
        },
        "EmploymentInformation": {
          "$ref": "#/definitions/EmploymentInformation"
        },
        "Age": {
          "type": "integer",
          "minimum": 16,
          "maximum": 80
        }
      },
      "definitions": {
        "EmploymentInformation": {
          "type": "object",
          "required": [
            "OriginalHireDate"
          ],
          "properties": {
            "OriginalHireDate": {
              "type": "string",
              "format": "date"
            },
            "Beneficiary": {
              "$ref": "#/definitions/DependantInformation"
            }
          }
        },
        "DependantInformation": {
          "type": "object",
          "required": [
            "Name"
          ],
          "properties": {
            "Name": {
              "type": "string",
              "minLength": 5
            }
          }
        }
      },
      "description": "nested-schema"
    }''')
    
    assert(get_type_for_key_path(schema, "Age") == "integer")
    assert(get_type_for_key_path(schema, "EmploymentInformation.OriginalHireDate") == "string")
    assert(get_type_for_key_path(schema, "EmploymentInformation.Beneficiary.Name") == "string")
    assert(get_type_for_key_path(schema, "foo.bar") == None)
    
if __name__ == "main":
    main()