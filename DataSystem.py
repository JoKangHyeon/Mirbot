#_*_ coding: utf-8 _*_
import pickle
import os.path
data = {}

dataFile = "data.dat"

def setData(userID, key, value):
    loadData()
    if userID not in data:
        data[userID] = {}
    data[userID][key]=value

def getData(userID, key):
    loadData()
    if userID not in data:
        data[userID] = {}
    if key not in data[userID]:
        return None
    return data[userID][key]

def getValue(userID) : 
    loadData()
    if userID not in data:
        data[userID] = {}
    if "value" not in data[userID]:
        data[userID]["value"] = {}
    return data[userID]["value"]

def setValue(userID,key,value):
    loadData()
    if userID not in data:
        data[userID] = {}
    if "value" not in data[userID]:
        data[userID]["value"] = {}
    data[userID]["value"][key]=value
    saveData()

def removeValue(userID, key):
    loadData()
    if userID not in data:
        data[userID] = {}
    if "value" not in data[userID]:
        data[userID]["value"] = {}
    if key in data[userID]["value"]:
        data[userID]["value"].pop(key)
        saveData()
        return True
    else:
        return False

def saveData():
    with open(dataFile,"wb") as f:
        pickle.dump(data,f)

def loadData():
    global data
    if not os.path.isfile(dataFile):
        saveData()
    with open(dataFile,"rb") as f:
        data = pickle.load(f)
