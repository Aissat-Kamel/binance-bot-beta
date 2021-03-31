import datetime as dt
from database import Status
import time
from os import system

def time_now():
    time = dt.datetime.now()
    time = time.strftime("%H:%M:%S    //   %d-%m-%Y") #10:42:30   //   01-03-2021
    return time

two_stat = ["ON", "OFF"]

while True:
    try:
        system("cls")
        stat = Status.find_status(collection = "Status")
        user_stat = input("Bot now is "+stat+". You can control the bot by [ON, OFF] commands! \n")
        if user_stat.upper() in two_stat:
            if user_stat.upper() == "ON":
                Status.save_status(collection = "Status", status = user_stat.upper(), time = time_now())
                with open("log.txt", "a") as log_file:
                    log_file.write("System is activated at : "+time_now()+"\n")

            elif user_stat.upper() == "OFF":
                Status.save_status(collection = "Status", status = user_stat.upper(), time = time_now())
                with open("log.txt", "a") as log_file:
                    log_file.write("System is disactivated at : "+time_now()+"\n")


        else:
            print("Incorrect command!")
            user_stat = input("Bot now is "+stat+". You can control the bot by [ON, OFF] commands! \n")
    except:
        pass
