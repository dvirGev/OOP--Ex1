import sys
from CallForElevator import CallForElevator
from Building import Building
from Elevators import Elevators
import csv
import random
import subprocess
counter = 0
# for run: python Ex1.py input\Ex1_Buildings\B2.json input\Ex1_Calls\Calls_a.csv myOutput.csv

#read the input names from the terminal else put defalt names
def inputs():
    if len(sys.argv) == 4:
        di = {
            "buildingName": sys.argv[1],
            "callsName": sys.argv[2],
            "outputName": sys.argv[3]
        }
    else:
        di = {
            "buildingName": "input\Ex1_Buildings\B2.json",
            "callsName": "input\Ex1_Calls\Calls_a.csv",
            "outputName": "out.csv"
        }
    return di

#read the csv input to list "calls"
def readCalls(file_name):
    calls = []
    with open(file_name) as fp:
        data = csv.reader(fp)
        for k in data:
            if (int(k[2]) < building.minFloor or int(k[2]) > building.maxFloor) or (int(k[3]) < building.minFloor and int(k[3]) > building.maxFloor):
                raise Exception("the call doesnt freat")
                
            calls.append(CallForElevator(k))
    return calls

#write the list "calls" to a csv file
def writeCalls():
    dataCalls = []
    for k in calls:
        dataCalls.append(k.__dict__.values())
    with open(myinput["outputName"], 'w', newline="") as fu:
        csvwriter = csv.writer(fu)
        csvwriter.writerows(dataCalls)

#retrun the most preferable elevators
def candidateElevators(call):
    global counter
    temp = []
    if call.type == 1:
        for e in building.elevators:
            if e.state == call.type and e.currentFloor < call.src:
                temp.append(e)
    elif call.type == -1:
        for e in building.elevators:
            if e.state == call.type and e.currentFloor > call.src:
                temp.append(e)
    for e in building.elevators:
        if e.destList.empty():
            temp.append(e)
    if len(temp) == 0:
        if call.type == 1:
            for e in building.elevators:
                if e.state == 1:
                    temp.append(e)
        elif call.type == -1:
            for e in building.elevators:
                if e.state == -1:
                    temp.append(e)
    if len(temp) == 0:
        for e in building.elevators:
            if e.state == call.type:
                temp.append(e)
    if len(temp) == 0:
        while True:
            counter = counter % len(building.elevators)
            if building.elevators[counter].state != call.type:
                break
        temp.append(building.elevators[counter])
        counter += 1
    return temp

#calculate the time that add to elevator from the call
def calculateTime(elev: Elevators, src: int) -> float:
    distance = abs(elev.currentFloor - src)
    time = (distance / elev.speed) + elev.openTime + elev.closeTime + elev.startTime + elev.stopTime
    return time

#put elevator to all the calls
def allocateAnElevator(call):
    temp = []
    temp = candidateElevators(call)
    relevant = calculateTime(temp[0], call.src)
    elev = temp[0]
    for e in temp:
        min = calculateTime(e, call.src)
        if relevant > min:
            relevant = min
            elev = e
    elev.destList.put(call.src)
    elev.destList.put(call.dest)
    elev.state = call.type

    call.elevator = elev.id

#move the elevators such the tester evry secound
def cmd(time: int):
    for e in building.elevators:
        if e.state == 1 and e.startTime <= time:
            e.currentFloor += e.speed
            if e.currentFloor >= e.dest:
                e.currntFloor = e.updetDest()
                e.startTime = time + e.stopTime
        elif e.state == -1 and e.startTime <= time:
            e.currentFloor -= e.speed
            if e.currentFloor <= e.dest:
                e.currntFloor = e.updetDest()
                e.startTime = time + e.stopTime
        if e.destList.empty():
            e.dest = 0

#the "brain" of the code
def algorithm():
    index = 0
    endTime = int(calls[-1].time) + 2
    for time in range(endTime):
        cmd(time)
        while int(calls[index].time) + 1 == time:
            allocateAnElevator(calls[index])
            index += 1
            if index == len(calls):
                break
#run the tester with the new output  
def runTester():
    subprocess.Popen(["powershell.exe", "java -jar lib\Ex1_checker_V1.2_obf.jar 207296989,209530583 " +
                     myinput["buildingName"] + "  " + myinput["outputName"] + "  outputFormTEster.log"])

#main
if __name__ == "__main__":
    myinput = inputs()
    building = Building(myinput["buildingName"])
    calls = readCalls(myinput["callsName"])
    algorithm()
    writeCalls()
    runTester()
