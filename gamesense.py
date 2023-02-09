import psutil
import serial
import time

arduino = serial.Serial('COM6', 115200, timeout=.1)
l = ["Beat Saber.exe", "Terraria.exe","Borderlands2.exe","GRB_UPP.exe","RainbowSix.exe","Risk of Rain 2.exe","VRChat.exe","Vacation Simulator.exe","ShooterGame.exe","ActingLessons.exe","Krautscape.exe"]
s = 0
i = 0
length = len(l) - 1
count = 0

def gamesense():
    global i
   # print(l[i])
    if l[i] in (p.name() for p in psutil.process_iter()):
        print(l[i]," Running")
        arduino.write(b"1")
        data = arduino.readline()[:-2]  # the last bit gets rid of the new-line chars
        if data:
            print(data)
        global s
        s = 1
        global count
        
        while l[i] in (p.name() for p in psutil.process_iter()):
            time.sleep(1)
            count += 1
       # i = 0

    else:
        if i < length:
            i += 1
        else:
            if i == length:
                i = 0

        data = arduino.readline()[:-2]
        if data:
            print(data)
        if s == 1:
            s = 0
            arduino.write(b"0")
            print("Time in Game: ",count, " seconds")


while True:
    gamesense()

