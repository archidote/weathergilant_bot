import requests
from assets.functions import * 

def allergies(location) :
    
    try : 
        checkIfFrenchlocationExist(location)
    except : 
        return "Wrong location code (FR) !"

    url = "https://www.pollens.fr/risks/thea/counties/"+location+""

    resp = requests.get(url=url)
    data = resp.json() # Check the JSON Response Content documentation below

    # print (data)

    allergies="Allergies : \n"
    allergies+="France - "+data["countyName"]+" - "+data["countyNumber"]+"\n\n"
    
    for i in range(19):
        allergies+=""+str(data["risks"][i]["pollenName"])+" : "+str(data["risks"][i]["level"])+"/5 - "+allergiesAVG(data["risks"][i]["level"])+"\n"
    allergies+="-"
        
    return allergies