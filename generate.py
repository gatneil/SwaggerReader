import requests
import sys
import json

url = "https://raw.githubusercontent.com/Azure/azure-rest-api-specs/master/specification/compute/resource-manager/Microsoft.Compute/stable/2018-06-01/compute.json"

r = requests.get(url)
if r.status_code != 200:
    print("Could not get swagger file")
    sys.exit()

j = r.json()

def get_full_def(ref_key):
    res = {}
    def_key = ref_key.split('/')[2]
    if "allOf" in j["definitions"][def_key]:
        res = {}
        for individual in j["definitions"][def_key]["allOf"]:
            tmp = get_full_def(individual["$ref"])
            for item in tmp:
                res[item] = tmp[item]

    if "properties" in j["definitions"][def_key]:
        for prop in j["definitions"][def_key]["properties"]:
            if "type" not in j["definitions"][def_key]["properties"][prop]:
                res[prop] = get_full_def(j["definitions"][def_key]["properties"][prop]["$ref"])
            elif j["definitions"][def_key]["properties"][prop]["type"] == "array":
                if "$ref" in j["definitions"][def_key]["properties"][prop]["items"]:
                    res[prop] = [get_full_def(j["definitions"][def_key]["properties"][prop]["items"]["$ref"])]
                else:
                    res[prop] = [j["definitions"][def_key]["properties"][prop]["items"]["type"]]
            else:
                res[prop] = j["definitions"][def_key]["properties"][prop]["type"]

    return res

def print_with_overline(s, u):
    l = len(s)
    a = [u for x in range(0, l)]
    print("".join(a))
    print(s)


def print_with_underline(s, u):
    l = len(s)
    a = [u for x in range(0, l)]
    print(s)
    print("".join(a))

paths = j["paths"]
for path in paths:
    for verb in paths[path]:
        print_with_overline(verb + " " + path, "=")

        for parameter in paths[path][verb]["parameters"]:
            if "in" not in parameter:
                continue

            if parameter["in"] == "body":
                print("")
                print_with_underline("Request Body", "-")
                res = get_full_def(parameter["schema"]["$ref"])
                print(json.dumps(res, indent=2))
                
        print("")
        print_with_underline("Responses", "-")
        for response in paths[path][verb]["responses"]:
            print(response)
            if "schema" in paths[path][verb]["responses"][response]:
                if "type" in paths[path][verb]["responses"][response]["schema"]:
                    if paths[path][verb]["responses"][response]["schema"]["type"] == "array":
                        # (*** TODO ***) what does it even mean for the response to be an array? JSON doesn't have [] as the outermost element
                        res = [get_full_def(paths[path][verb]["responses"][response]["schema"]["items"]["$ref"])]
                else:
                    res = get_full_def(paths[path][verb]["responses"][response]["schema"]["$ref"])
                    print(json.dumps(res, indent=2))
                    print("")

        print("")



print(get_full_def("#/definitions/VirtualMachineExtensionImage"))
