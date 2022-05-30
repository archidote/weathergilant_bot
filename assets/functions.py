import requests
from datetime import datetime
from datetime import timezone
    
def windAlert(data) : 
    if (data > 10 and data < 20) :
        return "Slow 🟢"
    elif (data >= 20 and data < 30) :
        return "Medium 🟡"
    elif (data >= 30 and data < 40) :
        return "High 🟠"
    elif (data > 40) :
        return "Critical 🔴"
    else : 
        return "Very slow 🔵"

def indiceUV(data) :
    if (data >= 1 and data < 3) :
        return ""+str(data)+" Risk : Low 🟢"
    elif (data >= 3 and data <= 5) :        
        return ""+str(data)+" Risk : Moderate 🟡"
    elif (data >= 6 and data <= 7) :        
        return ""+str(data)+" Risk : High 🟠"
    elif (data >= 8 and data <= 10) :        
        return ""+str(data)+" Risk : Very High 🔴"
    elif (data >= 11) :        
        return ""+str(data)+" Risk : Extremly High 🟤"

def isDay(data) : 
    if (data == 1) : 
        return "🏙️"
    else :
        return "🌃"

def pollutionNO2(data) :
    data = round(data,1)
    if (data < 40) :
        risk = ""+str(data)+" Risk : Low 🟢"
        indexpollutionNO2 = 1
        return [risk,indexpollutionNO2]
    elif (data < 90) :        
        risk = ""+str(data)+" Risk : Moderate 🟡"
        indexpollutionNO2 = 2
        return [risk,indexpollutionNO2]
    elif (data < 120) :        
        risk = ""+str(data)+" Risk : High 🟠"
        indexpollutionNO2 = 3
        return [risk,indexpollutionNO2]
    elif (data < 230) :        
        risk = ""+str(data)+" Risk : Very high 🔴"
        indexpollutionNO2 = 4
        return [risk,indexpollutionNO2]
    elif (data < 340):    
        risk = ""+str(data)+" Risk : Exceptionally high 🟤"
        indexpollutionNO2 = 5
        return [risk,indexpollutionNO2]
    else:    
        risk = ""+str(data)+" Risk : Extremly high 🟣" 
        indexpollutionNO2 = 6
        return [risk,indexpollutionNO2]

def pollutionO3(data) :
    data = round(data,1)
    if (data < 50) :
        risk = ""+str(data)+" Risk : Low 🟢"
        indexpollution03 = 1
        return [risk,indexpollution03]
    elif (data < 100) :        
        risk = ""+str(data)+" Risk : Moderate 🟡"
        indexpollution03 = 2
        return [risk,indexpollution03]
    elif (data < 130) :        
        risk = ""+str(data)+" Risk : High 🟠"
        indexpollution03 = 3
        return [risk,indexpollution03]
    elif (data < 240) :        
        risk = ""+str(data)+" Risk : Very high 🔴"
        indexpollution03 = 4
        return [risk,indexpollution03]
    elif (data < 380):    
        risk = ""+str(data)+" Risk : Exceptionally high 🟤"
        indexpollution03 = 5
        return [risk,indexpollution03]
    else:    
        risk = ""+str(data)+" Risk : Extremly high 🟣"  
        indexpollution03 = 6
        return [risk,indexpollution03]


def pollutionPM10(data) : 
    data = round(data,1)
    if (data < 20) :
        risk = ""+str(data)+" Risk : Low 🟢"
        indexpollutionPM10 = 1 
        return [risk,indexpollutionPM10]
    elif (data < 40) :        
        risk = ""+str(data)+" Risk : Moderate 🟡"
        indexpollutionPM10 = 2 
        return [risk,indexpollutionPM10]
    elif (data < 50) :        
        risk = ""+str(data)+" Risk : High 🟠"
        indexpollutionPM10 = 3 
        return [risk,indexpollutionPM10]
    elif (data < 100) :        
        risk = ""+str(data)+" Risk : Very high 🔴"
        indexpollutionPM10 = 4 
        return [risk,indexpollutionPM10]
    elif (data < 150):    
        risk = ""+str(data)+" Risk : Exceptionally high 🟤"
        indexpollutionPM10 = 5 
        return [risk,indexpollutionPM10]
    else:    
        risk = ""+str(data)+" Risk : Extremly high 🟣" 
        indexpollutionPM10 = 6 
        return [risk,indexpollutionPM10]

def pollutionPM2_5(data) : # Value index x 2 because pm2_5 are more dangerous than pm10
    data = round(data,1)
    if (data < 10) :
        risk = ""+str(data)+" Risk : Low 🟢"
        indexpollutionPM2_5 = 2 
        return [risk,indexpollutionPM2_5]
    elif (data < 20) :        
        risk = ""+str(data)+" Risk : Moderate 🟡"
        indexpollutionPM2_5 = 4 
        return [risk,indexpollutionPM2_5]
    elif (data < 25) :        
        risk = ""+str(data)+" Risk : High 🟠"
        indexpollutionPM2_5 = 6 
        return [risk,indexpollutionPM2_5]
    elif (data < 50) :        
        risk = ""+str(data)+" Risk : Very high 🔴"
        indexpollutionPM2_5 = 8
        return [risk,indexpollutionPM2_5]
    elif (data < 75):    
        risk = ""+str(data)+" Risk : Exceptionally high 🟤"
        indexpollutionPM2_5 = 10
        return [risk,indexpollutionPM2_5]
    else:    
        risk = ""+str(data)+" Risk : Extremly high 🟣" 
        indexpollutionPM2_5 = 12
        return [risk,indexpollutionPM2_5]

def pollutionSO2(data) :
    data = round(data,1)
    if (data < 100) :
        risk = ""+str(data)+" Risk : Low 🟢"
        indexpollutionSO2 = 1
        return [risk,indexpollutionSO2]
    elif (data < 200) :        
        risk = ""+str(data)+" Risk : Moderate 🟡"
        indexpollutionSO2 = 2
        return [risk,indexpollutionSO2]
    elif (data < 350) :        
        risk = ""+str(data)+" Risk : High 🟠"
        indexpollutionSO2 = 3
        return [risk,indexpollutionSO2]
    elif (data < 500) :        
        risk = ""+str(data)+" Risk : Very high 🔴"
        indexpollutionSO2 = 4
        return [risk,indexpollutionSO2]
    elif (data < 750):    
        risk = ""+str(data)+" Risk : Exceptionally high 🟤"
        indexpollutionSO2 = 5
        return [risk,indexpollutionSO2]
    else:    
        risk = ""+str(data)+" Risk : Extremly high 🟣" 
        indexpollutionSO2 = 6
        return [risk,indexpollutionSO2]

def avgPollution(PpollutionNO2,PpollutionO3,PpollutionPM10,PpollutionPM2_5, PpollutionSO2):
    a = pollutionNO2(PpollutionNO2)
    b = pollutionO3(PpollutionO3)
    c = pollutionPM10(PpollutionPM10)
    d = pollutionPM2_5(PpollutionPM2_5)
    e = pollutionSO2(PpollutionSO2)
    # print (a[1],b[1],c[1],d[1],e[1])
    total = a[1] + b[1] + c[1] + d[1] + e[1]
    avg = total / 6
    avg = round(avg,1)
    # print (total)
    # print (avg)
    if (avg < 1.5 ) :
        return " "+str(avg)+"/6 Low 🟢"
    elif (avg < 2) : 
        return " "+str(avg)+"/6 Medium 🟡"
    elif (avg < 3 ) : 
        return " "+str(avg)+"/6 High 🔴"
    elif (avg < 5) : 
        return " "+str(avg)+"/6 Very High 🟤"
    else :
        return " "+str(avg)+"/6 Extremly High 🟣"

def visibility(data) : # in miles
    if (data > 5) :
        return "Good 🟢"
    elif (data > 2 or data < 5) :        
        return "Medium 🟡"
    elif (data < 2 or data > 0.5) :        
        return "Bad 🟠"
    else : # < 0.5 miles
        return "Very bad 🔴"

def allergiesAVG(data) :
    if (data == 0) :
        return "No allergies 🔵"
    elif (data == 1) :        
        return "Risk : Slow 🟢"
    elif (data == 2) :        
        return "Risk : Medium 🟡"
    elif (data == 3) :        
        return "Risk : High 🟠"
    elif (data == 4) :        
        return "Risk : Very High 🔴"
    else :
        return "Risk : Extremly High 🟤"

def checkIfFrenchlocationExist(locationCode) :
    locationCode = str(locationCode)    
    url = "https://geo.api.gouv.fr/departements/"+locationCode+""
    resp = requests.get(url=url)
    data = resp.json()
    
def dateFormat(unformatedDate) : 
    d = datetime.fromisoformat(unformatedDate).astimezone(timezone.utc)
    return d.strftime('%Y-%m-%d %H:%M:%S') # English !