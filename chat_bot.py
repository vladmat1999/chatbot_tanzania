from fbchat import log, Client
import matplotlib.pyplot as plt
import fbchat
import time
import strings
import threading
import json
from dateutil.parser import parse as parseDate
import datetime
from datetime import timedelta 


database=[]
appointments=[]

answers = strings.answers

{"uid": "",
      "Name": "",
      "Weight": 0,
      "Height": 0,
      "BloodType": "",
      "Wheelchair": "",
      "MedicalNotes": "",
      "CurrentStep": 0,
      "CurrentFunction": ""
    }

{
    "uid": "",
    "date": "",
    "hospital": ""
}

message=""
client=fbchat.Client
language=0
swahili=strings.swahili
english=[]
currentApp = 2
thisSession=True

def getAllSubstrings(input_string, l=3):
  length = len(input_string)
  return [input_string[i:j+1] for i in range(0,length) for j in range(i+l-1,length)]

def messageIn(lista):
    global message
    a=getAllSubstrings(message)
    for x in a:
        if x in lista:
            return True
    return False

def getById(author_id):
    for x in database:
        if x["uid"] == author_id:
            return x
    return None

def getAppById(appId):
    for x in appointments:
        if x["appId"] == appId:
            return x
    return None

def sendMessage(message, author_id):
    global client
    client.send(fbchat.Message(text=message), int(author_id))

def detectLanguage(author_id):
    global language
    if message.upper() in swahili and language != 1:
        language = 1
        sendMessage(answers["changeLang"][1], author_id)
        getById(author_id)["CurrentStep"]-=1
        if(getById(author_id)["CurrentStep"] < -1):
            getById(author_id)["CurrentStep"] = -1
    elif language != 0:
        language = 0
        sendMessage(answers["changeLang"][0], author_id)
        getById(author_id)["CurrentStep"]-=1
        if(getById(author_id)["CurrentStep"] < -1):
            getById(author_id)["CurrentStep"] = -1

def saveData():
    global database, appointments
    with open("database.json","w") as f:
        json.dump(database, f)
    with open("appointments.json","w") as f:
        json.dump(appointments, f)

def instructionMessage(numberSMS, author_id):
    sendMessage(answers["instVer"][language],author_id)
    sendMessage(numberSMS,author_id)
    sendMessage(answers["freeCharge"][language],author_id)
    sendMessage(answers["notVerified"][language],author_id)

def checkIfReal(companyName):
    for x in strings.checkAuthenticity:
        if companyName.upper() == x[0].upper():
            return x[1]
    return -1

def register(author_id):
    print("database")
    user = getById(author_id)

    if(user == None):
        a={"uid": author_id,
        "Name": "",
        "Weight": 0,
        "Height": 0,
        "BloodType": "",
        "Wheelchair": "",
        "MedicalNotes": "",
        "CurrentStep": 1,
        "CurrentFunction": ""
        }
        database.append(a)
        print(database)
        print(message)
        print(answers["greeting"][language])
        sendMessage(answers["greeting"][language], author_id)
        sendMessage(answers["getName"][language], author_id)

    elif user["CurrentStep"] == 1:
        user["CurrentStep"] = 2
        user["Name"] = message
        sendMessage(answers["greeting2"][language] + user["Name"], author_id)
        sendMessage(answers["weight"][language], author_id)
    
    elif user["CurrentStep"] == 2:
        user["CurrentStep"] = 3
        s = [int(x) for x in message.split() if x.isdigit()]
        weight = 0
        for x in s:
            weight = weight*10 + x
        user["Weight"] = weight
        sendMessage(answers["height"][language], author_id)
        print(database)
    
    elif user["CurrentStep"] == 3:
        user["CurrentStep"] = 4
        s = [int(x) for x in message.split() if x.isdigit()]
        height = 0
        for x in s:
            height = height*10 + x
        user["Height"] = height
        sendMessage(answers["bloodtype"][language], author_id)
        print(database)

    elif user["CurrentStep"] == 4:
        user["CurrentStep"] = 5
        s = message.split()
        x=""
        for x in s:
            if x.upper() in ["AII","A2"]:
                x="A2"
                break
            
            elif x.upper() in ["BIII", "B3"]:
                x="B3"
                break

            elif x.upper() in ["ABIV", "AB4"]:
                x="AB4"
                break

            elif x.upper() in ["OI", "O1"]:
                x="O1"
                break

            else:
                x=""

        if(x == ""):
            user["CurrentStep"] = 4
            sendMessage(answers["default"][language], author_id)
        else:
            user["BloodType"] = x
            sendMessage(answers["wheelchair"][language], author_id)
            print(database)

    elif user["CurrentStep"] == 5:
        user["CurrentStep"] = 6
        response=""
        for x in getAllSubstrings(message.upper(),2):
            if x in ["YES"]:
                response="YES"
                break
            elif x in ["NO"]:
                response="NO"
                break
            else:
                user["CurrentStep"] = 5
                sendMessage(answers["afirmativeQuestion"][language], author_id)
                response=""
            
        if(response == ""):
            user["CurrentStep"] = 5
        else:
            user["Wheelchair"] = response
            sendMessage(answers["medicalNotes"][language], author_id)
            print(database)

    elif user["CurrentStep"] == 6:
        user["CurrentStep"] = -1
        user["MedicalNotes"] = message
        sendMessage(answers["configSuccess"][language], author_id)
        print(database)



def appointment(author_id):
    user = getById(author_id)
    if(user["CurrentFunction"][0:3] != "app"):
        user["CurrentFunction"] = "app0"
        sendMessage("Would you like to make an appointment?", author_id)
        print(database)
    
    elif(user["CurrentFunction"][0:3] == "app"):
        print(database)
        if(int(user["CurrentFunction"][3:]) == 0):
            print(database)
            for x in getAllSubstrings(message.upper(),2):
                response = ""
                if x in ["YES"]:
                    response="YES"
                    break
                elif x in ["NO"]:
                    response="NO"
                    break
            
            if response.upper() == "YES":
                user["CurrentFunction"] = "app1"
                sendMessage("Please enter the date and time of your appointment",author_id)
            
            elif response.upper() =="NO":
                user["CurrentFunction"]=""
                sendMessage("Ok then!", author_id)
                print(database)

            else:
                sendMessage(answers["afirmativeQuestion"][language], author_id)

        elif(int(user["CurrentFunction"][3:]) == 1):
            global currentApp
            currentApp+=1
            user["CurrentFunction"] = "app" + str(currentApp)
            appDate = parseDate(message)
            appDateString = appDate.strftime("%Y-%m-%d %H:%M:%S")
            appointment={
                     "uid": author_id,
                     "appId": currentApp,
                     "date": appDateString,
                     "hospital": ""
                    }

            appointments.append(appointment)
            sendMessage("Where will the appointment take place?", author_id)
            print(appointments)

        elif(int(user["CurrentFunction"][3:]) > 1):
            appId = int(user["CurrentFunction"][3:])
            user["CurrentFunction"] = ""
            appointment=getAppById(appId)
            appointment["hospital"] = message
            sendMessage("Your appointment has been made on " + appointment["date"] + " for " + appointment["hospital"],author_id)
            print(appointment)

def diagnosticate(author_id):
    user = getById(author_id)
    if(user["CurrentFunction"][0:3] != "dig"):
        user["CurrentFunction"] = "dig0"
        sendMessage(answers["healthProblem"][language], author_id)
        print(database)
    
    elif(user["CurrentFunction"][0:3] == "dig"):
        print(database)
        if(int(user["CurrentFunction"][3]) == 0):
            print(database)
            for x in getAllSubstrings(message.upper(),2):
                response = ""
                if x in ["YES"]:
                    response="YES"
                    break
                elif x in ["NO"]:
                    response="NO"
                    break
            
            if response.upper() == "NO":
                user["CurrentFunction"] = ""
                sendMessage("Ok then!",author_id)
            
            elif response.upper() =="YES":
                user["CurrentFunction"]="dig2"
                sendMessage("Which type of health problem is it ?", author_id)
                print(database)

            else:
                sendMessage(answers["afirmativeQuestion"][language], author_id)

        elif(int(user["CurrentFunction"][3]) == 2):
            for x in getAllSubstrings(message.upper(),3):
                response = ""
                if x in ["FEVER"]:
                    response="FEVER"
                    break
                elif x in ["COLD"]:
                    response="COLD"
                    break
                elif x in ["PAIN"]:
                    response="PAIN"
                    break
                elif x in ["THROAT"]:
                    response="COLD"
                    break
                elif x in ["BLUE"]:
                    response="PUKE"
                    break
                elif x in ["PUKE"]:
                    response="PUKE"
                    break
                elif x in ["THROWED UP"]:
                    response="PUKE"
                    break
                elif x in ["WEAK"]:
                    response="WEAK"
                    break
                elif x in ["DIZZY"]:
                    response="WEAK"
                    break
                elif x in ["CHILLS"]:
                    response="COLD"
                    break
            if response == "PAIN":
                user["CurrentFunction"]="dig3"
                sendMessage("Where do you feel the pain ?",author_id)
            elif response == "FEVER":
                user["CurrentFunction"]="dig4"
                sendMessage("Have you had any infections recently ?",author_id)
            elif response == "COLD":
                user["CurrentFunction"]=""
                sendMessage("Go to the closest pharmacy",author_id)
                sendMessage("Tell the pharmacist for how long have you experienced this symptoms",author_id)
                sendMessage("It's not a big deal, with some medicine you will be allright",author_id)
                print(database)
            elif response == "PUKE":
                user["CurrentFunction"]="dig5"
                sendMessage("Did you eat something bad ?",author_id)
            elif response == "WEAK":
                user["CurrentFunction"]="dig6"
                sendMessage("Did you get to sleep in the last 24 hours ?",author_id)
            else:
                sendMessage("I don't what to do in this case, but I know someone who does",author_id)
                appointment(author_id)
        elif(int(user["CurrentFunction"][3]) == 3):
                print(database)
        elif(int(user["CurrentFunction"][3]) == 4):
            for x in getAllSubstrings(message.upper(),2):
                response = ""
                if x in ["YES"]:
                    response="YES"
                    break
                elif x in ["NO"]:
                    response="NO"
                    break
            
            if response.upper() == "YES":
                user["CurrentFunction"] == "dig7"
                sendMessage("Did you finished your treatment ?",author_id)
            
            elif response.upper() =="NO":
                user["CurrentFunction"]=""
                sendMessage("The most likely cause of a fever is an infection. I recommend seeing an internal medicine doctor. ", author_id)
                appointment(author_id)
                print(database)
        
        elif(int(user["CurrentFunction"][3]) == 5):
            for x in getAllSubstrings(message.upper(),2):
                response = ""
                if x in ["YES"]:
                    response="YES"
                    break
                elif x in ["NO"]:
                    response="NO"
                    break
            
            if response.upper() == "YES":
                user["CurrentFunction"] == ""
                sendMessage("Here's an article for your issue",author_id)
                sendMessage("https://www.healthline.com/health/blue-lips",author_id)
            
            elif response.upper() =="NO":
                user["CurrentFunction"]=""
                sendMessage("The most common cause is a cyanosis. I recommend seeing an internal medicine doctor. ", author_id)
                appointment(author_id)
                print(database)


def checkAuth(author_id):
    user = getById(author_id)
    if(user["CurrentFunction"][0:3] != "aut"):
        user["CurrentFunction"] = "aut0"
        sendMessage("Would you like to check your medicine?", author_id)
        print(database)

    elif(user["CurrentFunction"][0:3] == "aut"):
        print(database)
        if(int(user["CurrentFunction"][3]) == 0):
            print(database)
            for x in getAllSubstrings(message.upper(),2):
                response = ""
                if x in ["YES"]:
                    response="YES"
                    break
                elif x in ["NO"]:
                    response="NO"
                    break
            
            if response.upper() == "YES":
                user["CurrentFunction"] = "aut1"
                sendMessage("What is your firm name?",author_id)
            
            elif response.upper() =="NO":
                user["CurrentFunction"]=""
                sendMessage("Ok then!", author_id)
                print(database)

            else:
                sendMessage(answers["afirmativeQuestion"][language], author_id)

        elif(int(user["CurrentFunction"][3]) == 1):
                user["CurrentFunction"] = ""
                print("aut1")
                if(message.upper() in strings.firmNames):
                    print("In firm names")
                    number = checkIfReal(message)
                    if(number != -1):
                        print("in number")
                        instructionMessage(number, author_id)
                else:
                    user["CurrentFunction"] = "aut1"
                    sendMessage("I'm sorry, but your company is not on my list",author_id)
                

            


class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        global message

        user=getById(author_id)

        if(self.uid != author_id):
            message = message_object.text

            detectLanguage(author_id)

            print("Self uid")

            thisSession = False

            if(user is not None):
                if(user["CurrentStep"] != -1):
                    register(author_id)
                    saveData()
                else:
                    if(user["CurrentFunction"][0:3] == "app"):
                         appointment(author_id)
                         thisSession = True

                    if(user["CurrentFunction"][0:3] == "aut"):
                        checkAuth(author_id)
                        thisSession = True

                    if(user["CurrentFunction"][0:3] == "dig"):
                        diagnosticate(author_id)
                        thisSession = True
    
                    for x in message.upper().split():
                        if x in [answers["doctor"][language],answers["appointment"][language]]:
                            appointment(author_id)
                            thisSession = True
                        elif x in ["MEDICINE","DRUG"]:
                            checkAuth(author_id)
                            thisSession = True
                        elif x in ["SICK","BAD","FEELING","FELT","FEEL"]:
                            diagnosticate(author_id)
                        elif x in ["HELLO","HI"]:
                            sendMessage("Hey " + getById(author_id)["Name"], author_id)
                            getById(author_id)["CurrentFunction"] = "hlo"
                            thisSession = True
                        elif x in ["HELP","URGENT"]:
                            sendMessage("Let me call an ambulance for you", author_id)
                            getById(author_id)["CurrentFunction"] = "hlo"
                            thisSession = True

                    if(getById(author_id)["CurrentFunction"] == "hlo"):
                        getById(author_id)["CurrentFunction"] = ""

                    if(getById(author_id)["CurrentFunction"] == "" and not thisSession):
                        sendMessage(answers["default"][language],author_id)


            saveData()

            if(user == None):
                print("author None")
                register(author_id)




























'''
def getAllSubstrings(input_string):
  length = len(input_string)
  return [input_string[i:j+1] for i in range(length) for j in range(i,length)]


def getDic(authorId):
    for x in lista:
        if x["Id"] == authorId:
            return x
    return None

def getIndex(authorId):
    for x in range(0,len(lista)):
        if lista[x]["Id"]==authorId:
            return x
    return None



















step=0
lista=[]
reminders=[]
monthlyBudgetSpoofed1=[x+1 for x in range(30)]
monthlyBudgetSpoofed2=[1479, 1376, 1694, 1441, 1590, 1534, 1523, 1553, 1500, 1241, 1256, 1333, 1463, 1376, 1491, 1674, 1372, 1454, 1309, 1610, 1352, 1346, 1453, 1616, 1295, 1390, 1466, 1612, 1472, 1201]
reminderId=0
regCompleted=True
goToRemainderJob=False

class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        message = fbchat.models.Message(text=None, mentions=None, emoji_size=None, sticker=None, attachments=None)

        text = message_object.text
        print(text)

        substrings = getAllSubstrings(text)

        global step, regCompleted, goToRemainderJob, reminderId
        understand=0
        temp=""

        if author_id != self.uid:
            if True:
                uid=author_id
                author_id = self.uid

                print(uid)

                print(regCompleted)

                name = getName(uid)

                print(name)

                if "BYE" in text.upper():
                    message.text = "It was nice talking to you"
                    self.send(message, thread_id=thread_id, thread_type=thread_type)

                if "MONTHLY BUDGET" in text.upper():
                        plt.axes()
                        plt.ylim([0, 2000])
                        plt.plot(monthlyBudgetSpoofed1,monthlyBudgetSpoofed2)
                        plt.savefig("img.png")
                        self.sendLocalFiles("C://Users//Vlad//AppData//Local//Programs//Python//Python35//img.png",None, thread_id=thread_id, thread_type=thread_type)
                       

                if(name!=None and regCompleted==True):
                    for x in substrings:
                        if x.upper() in ["HELLO","HI","GOOD MORNING","HEY","ALOHA"]:
                            message.text = "Hello, " + name + ", what can I do for you today?"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)

                    if goToRemainderJob:
                        goToRemainderJob=False;
                        op=0
                        if "SUB" in text.upper():
                            op=-1;
                        if "ADD" in text.upper():
                            op=1;
                        if op!=0:
                            s = [int(x) for x in text if x.isdigit()];
                            a=0;
                            for x in s:
                                a=a*10+x
                        for x in reminders:
                            if x["ReminderId"]==reminderId:
                                for y in lista:
                                    if y["Id"]==x["Id"]:
                                        y["Buget"]=y["Buget"]+op*a
                                        if(op==-1):
                                            tm=x["Time"]
                                            message.text = "Okay then, I will substract  " + str(a) + " from your account each day at " + tm + " o'clock"
                                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                                        if(op==1):
                                            tm=x["Time"]
                                            message.text = "Okay the, I will add " + str(a) + " to your account each day at " + tm + " o'clock"
                                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            
                    if "Set".upper() in text.upper() or "Reminder".upper() in text.upper():
                        reminderId+=1
                        if "DAILY" in text.upper():
                            timeList=[int(s) for s in text if s.isdigit()]
                            h=timeList[0]*10+timeList[1];
                            m=timeList[2]*10+timeList[3];
                            remainderMessage = text.split("to ")[1];
                            remainderMessage.capitalize()
                            print(str(h) + ":" + str(m));
                            message.text = "Reminder set for " + str(h) + ":" + str(m)
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            time.sleep(1)
                            reminders.append({
                                "Id":uid,
                                "ReminderId":reminderId,
                                "Message":remainderMessage,
                                "Operation":"",
                                "Interval":24*60*60,
                                "Time":str(h) + ":" + str(m)
                                })
                            print(reminders)
                            goToRemainderJob=True;
                            message.text = "Do you want the reminder to do any operations?"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)

                    if "GO OUT" in text.upper():
                        a=getDic(uid)
                        if a["Buget"]-a["MandatoryCost"]-a["FoodMonth"] > 0:
                            message.text = "It seems like you have enough money to go out and party!!!"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                        else:
                            message.text = "I highly advise that you stay home this week"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)

                         
                else:
                     regCompleted=False
                     if(step==7):
                        if True:
                            author_id=self.uid
                            s = [int(x) for x in text.split() if x.isdigit()];
                            a=0;
                            for x in s:
                                a=a*10+x
                                
                            lista[0]["FoodMonth"]=a*4
                            message.text="Great, that's all I need to know for now!"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            time.sleep(1)
                            message.text="Let me take care from here"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            step=0
                            understand=1
                            regCompleted=True
                            
                     if(step==6):
                        if True:
                            author_id=self.uid
                            s = [int(x) for x in text.split() if x.isdigit()];
                            a=0;
                            for x in s:
                                a=a*10+x
                                
                            lista[getIndex(uid)]["MandatoryCost"]=a
                            message.text="Last but not least, how much do you spend on food each week?"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            step=7
                            understand=1

                    
                     if(step==5):
                        if True:
                            author_id=self.uid
                            a=0
                            a = [int(s) for s in text.split() if s.isdigit()][0];
                            lista[getIndex(uid)]["OutCounter"] = a
                            message.text = "Not bad!"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            time.sleep(1)
                            message.text = "Now I need to know what's your monthly maintanance"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            step=6
                            understand=1

                    
                     if(step==4):
                        if True:
                            author_id=self.uid
                            s = filter(str.isdigit, text);
                            a=0;
                            for x in s:
                                a=a*10+int(x)

                            lista[getIndex(uid)]["Income"]=a
                            message_object.text = "Alright, I'll keep track of that"
                            self.send(message_object, thread_id=thread_id, thread_type=thread_type)
                            time.sleep(1)
                            message.text = "How often do you go out?"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            step=5
                            understand=1
                    
                     if(step==3):
                        if True:
                            author_id=self.uid
                            s = filter(str.isdigit, text);
                            a=0;
                            for x in s:
                                a=a*10+int(x)
                            print(getIndex(uid))
                            print(uid)
                            print(lista)
                            lista[getIndex(uid)]["Buget"]=a
                            temp="Okay, " +getName(uid)+"! I've set your budget to be " + str(a) + "."
                            message.text = temp
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            time.sleep(1)
                            message.text = "What's your monthly income?"
                            self.send(message, thread_id=thread_id, thread_type=thread_type)
                            print(lista)
                            step=4
                            understand=1

                    
                     if(step==2):
                        print(text)
                        if(text.upper() not in "Great!".upper() and text not in "What's your name?"):
                            if True:
                                author_id=self.uid
                                lista.append({
                                    "Id":uid,
                                    "Name":text,
                                    "Buget":0,
                                    "Income":0,
                                    "OutCounter":0,
                                    "MandatoryCost":0,
                                    "Spent":0,
                                    "FoodMonth":0
                                    })
                                temp="Nice to meet you, " + getName(uid) + " !"
                                message.text = "Nice to meet you, " + getName(uid) + " !"
                                self.send(message, thread_id=thread_id, thread_type=thread_type)
                                time.sleep(1)
                                message.text = "Can you please tell me your budget?"
                                self.send(message, thread_id=thread_id, thread_type=thread_type)
                                step=3
                                understand=1


                     if(step==1):
                        print(text)
                        if "ye".upper() in text.upper():
                            if True:
                                author_id = self.uid
                                message.text = "Great!"
                                self.send(message, thread_id=thread_id, thread_type=thread_type)
                                time.sleep(1)
                                message.text = "What's your name?"
                                self.send(message, thread_id=thread_id, thread_type=thread_type)
                                step=2
                                understand=1

                     if(step==0):
                        if True:
                            step=-1
                            for x in substrings:
                                if x.upper() in ["HELLO","HI","GOOD MORNING","HEY","ALOHA"]:                             
                                    message.text = "Hi, my name is BudgetBuddy and I am here to help you do better things with your money. Shall we start?"
                                    self.send(message, thread_id=thread_id, thread_type=thread_type)
                                    step=1
                                    undestand=1
                                    print(step)      


client = EchoBot("budget_buddy@yahoo.com", "uddy1234")
client.listen()
'''

if __name__ == "__main__":
    with open("database.json","r") as f:
        database = json.load(f)
    with open("appointments.json","r") as f:
        appointments= json.load(f)

    appointments.sort(key = lambda x: x["appId"], reverse = True)

    currentApp = appointments[0]["appId"] + 1

    appointments.append({
                     "uid": "100002228934335",
                     "appId": currentApp,
                     "date": (datetime.datetime.now() + timedelta(minutes = 121)).strftime("%Y-%m-%d %H:%M:%S"),
                     "hospital": "afffsdf"
    })


    client = EchoBot("medhelp19@gmail.com","Parola111")
    client.listen()

    
    
