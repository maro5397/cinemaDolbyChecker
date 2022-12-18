import os
import json
import logging

logging.basicConfig(filename='../info.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s [%(filename)s]: %(name)s %(funcName)20s - Message: %(message)s')

jsonfile = os.path.join("../", 'settings.json')
with open(jsonfile, 'r') as f:
    values = json.loads(f.read())
 
def getJsonValue(key):
        try:
            return values[key]
        except KeyError:
            error_msg = "Set the {} environment variable".format(key)
            raise KeyError(error_msg)

if __name__ == "__main__":
    print(getJsonValue("discordkey"))
