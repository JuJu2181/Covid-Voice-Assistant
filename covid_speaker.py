#for voice assistant
import pyttsx3
import speech_recognition as sr
import pytz

#for web scrapping
import requests
from bs4 import BeautifulSoup
import json



URL = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?#countries"
try:
    result = requests.get(URL)
except:
    print("Unable to go online. Check your internet connection and try again")
    exit()

#using beautiful soup object to get elements of table 
soup = BeautifulSoup(result.text, 'lxml')
table = soup.find("table",id="main_table_countries_today")
header = [heading.text.replace("#","S.N.").replace(",Other", "").replace('Tot\xa0Cases/1M pop','TotCases/1M pop').replace('Tests/\n1M pop\n','Tests/1M pop') for heading in table.find_all('th')]
tablerows = [row for row in table.find_all('tr')]
table_data = table.tbody.find_all("tr") 

#writing the results of web scrapping on json file
results = [{header[index]:cell.text for index,cell in enumerate(row.find_all('td'))}for row in tablerows]

#to extract the country names from table
OLD_LIST = []
for i in range(len(table_data)):
    try:
        key = table_data[i].find_all("a",href= True)[0].string
    except:
        key = table_data[i].find_all("td")[0].string
    OLD_LIST.append(key)
OLD_LIST = OLD_LIST[8:]
OLD_LIST.append('world')
COUNTRY_LIST = []
for country in OLD_LIST:
    COUNTRY_LIST.append(country.lower())

#functions to get details
#checking empty is required as empty string is recieved which is not spoken during output
def checkForEmpty(data):
    if data == "":
        data = 0
    return data    

#filtering to remove '+' from the newest datas
def filterString(data):
    if "+" in data:
        data= data.replace("+", "")
    return data    

def getAllCountryDetails(country):
    for i in results:
        if "Country" in i:
            if i["Country"] == country:
                speak(f'Following Details have been obtained for {country}')
                print(i)
           
def getCases(country = "World",caseType = "total"):
    for i in results:
        if "Country" in i:
            if i["Country"] == country:
                if caseType == 'total':
                    total_cases = i['TotalCases']
                    total_cases = checkForEmpty(total_cases)
                    print(f'Total Cases for {country} is {total_cases}')
                    speak(f'According to the latest update Total Cases for {country} is {total_cases}')
                elif caseType == 'new':
                    new_cases = i['NewCases']
                    new_cases = checkForEmpty(new_cases)
                    new_cases = filterString(new_cases)
                    print(f'New Cases for {country} is {new_cases}')
                    speak(f'New Cases for {country} is {new_cases}')
                elif caseType == 'active':
                    active_cases = i['ActiveCases']
                    active_cases = checkForEmpty(active_cases)
                    print(f'Active Cases for {country} is {active_cases}')
                    speak(f'Active Cases for {country} is {active_cases}')
                elif caseType == 'serious':
                    serious_cases = i['Serious,Critical']
                    serious_cases = checkForEmpty(serious_cases)
                    print(f'Serious Cases for {country} is {serious_cases}')
                    speak(f'Serious Cases for {country} is {serious_cases}')
                                  
def getDeaths(country = "World",deathType = "total"):
    for i in results:
        if "Country" in i:
            if i["Country"] == country:
                if deathType == 'total':
                    total_deaths = i['TotalDeaths']
                    total_deaths = checkForEmpty(total_deaths)
                    print(f'Total Deaths for {country} is {total_deaths}')
                    speak(f'So far {total_deaths} people have died in {country}')
                elif deathType == 'new':
                    new_deaths = i['NewDeaths']
                    new_deaths = checkForEmpty(new_deaths)
                    new_deaths = filterString(new_deaths)
                    print(f'New Deaths for {country} is {new_deaths}')
                    speak(f'Based on latest update {new_deaths} deaths have been recorded today in {country}')                   

def getRecoveries(country = "World",recoveredType = "total"):
    for i in results:
        if "Country" in i:
            if i["Country"] == country:
                if recoveredType == 'total':
                    total_recoveries = i['TotalRecovered']
                    total_recoveries = checkForEmpty(total_recoveries)
                    print(f'Total Recoveries for {country} is {total_recoveries}')
                    speak(f'So far {total_recoveries} people have recovered in {country}')
                elif recoveredType == 'new':
                    new_recoveries = i['NewRecovered']
                    new_recoveries = checkForEmpty(new_recoveries)
                    new_recoveries = filterString(new_recoveries)
                    print(f'New Recoveries for {country} is {new_recoveries}')
                    speak(f'{new_recoveries} people have recovered today in {country}')

def getTests(country):
    for i in results:
        if "Country" in i:
            if i["Country"] == country:
                total_tests = i['TotalTests']
                total_tests = checkForEmpty(total_tests)
                #In the table I scrapped tests performed in the world was empty 
                if country == "World" and total_tests == 0:
                    speak(f'Sorry the total tests performed in the world has not been recorded yet')
                    print('No data found for world')
                else:
                    speak(f'According to latest update The total tests performed in {country} so far is {total_tests}')  
                    print(f'The total tests performed in {country} so far is {total_tests}') 

def getCountry():
    speak("Which Country's details do you want to know?")
    print("Listening to user . . .")
    country_answer = get_audio()
    nation = None
    for country in COUNTRY_LIST:
        #print(country)  
        
        if country in country_answer:
           # print(country)
            country = country.capitalize()
            if (country == 'Usa' or country == 'Uk' or country == 'uae' or country == 'drc' or country == 'car'):
                country = country.upper()

            print(f'User : {country_answer}')
            nation = country
    if (nation == None):
        speak("No Such Country Data Found")     
    return nation             




#These functions use pyttsx3 and sr:
def speak(text):
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')
    engine.setProperty('voice',sound[1].id)
    engine.say(text)
    engine.runAndWait()

count = 0
def get_audio():
    global count
    if (count > 10):      #if exception is recieved more than 10 times automatically close the system
        speak("System is closing as the user seems to be offline")
        exit()

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        speech = ""

        try:
            speech = recognizer.recognize_google(audio)
            print(speech)
        except Exception:
            speak("Sorry I didn't hear you. Can you please repeat what you were saying?")
            print("Exception: Input not recieved by assistant")  #raise exception if no input  
            count += 1    #we increase count everytime we recieve exceptions
    return speech.lower()


#the assistant will respond if any of these starting phrases are said
STARTING_PHRASES = ["assistant", "hey robo","wake up","hello bot"]
print("Starting the Covid-19 Stats Updater")

while True:  #main loop
    print('Listening . . .')
    text = get_audio()
    print(f'User : {text}')
    for phrase in STARTING_PHRASES:
        if text.count(phrase) > 0:
            speak("Hello I am Covid-19 Stats updater. How may I help you?")

            while True:
                print("Listening to user . . .")
                text = get_audio()
                print(f'User : {text}')
                UPDATE_PHRASE = "update"
                if UPDATE_PHRASE in text:
                    speak("Updating the data in local file")
                    with open('covid.json', 'w') as f:
                        json.dump(results[8:], f)     #first 8 data are null so removing them
                    print('Data updated sucessfully')
                    speak("Data updated sucessfully")

                #Assistant will get details if any of these phrases are mentioned  
                READING_PHRASES = ["read", "get", 'tell', "fetch"]
                for phrase in READING_PHRASES:
                    if phrase in text:
                        country = getCountry()
                        if(country):    
                            speak("Country Data Noted")
                            speak(f'What do you want to know about {country} ?')
                            print("Listening to user . . .")
                            query = get_audio()
                            print(f'User : {query}')
                            if "case" in query:
                                speak("What type of case do you want to know about?")
                                print("Listening to user . . .")
                                answer = get_audio()
                                print(f'User : {answer}')
                                speak('Fetching data')
                                if "new" in answer:
                                    getCases(country, 'new')
                                elif "active" in answer:
                                    getCases(country, 'active')
                                elif "serious" in answer:
                                    getCases(country, 'serious')
                                else:
                                    speak(f"Getting all details about total cases of {country}")
                                    getCases(country, 'total')
                                speak("Data fetched Successfully")
                                    

                            elif "death" in query or "died" in query or "lost" in query:
                                speak("Do you want to know about the newest deaths?")
                                print("Listening to user . . .")
                                answer = get_audio()
                                print(f'User : {answer}')
                                speak('Fetching Data')
                                if 'yes' in answer:
                                    getDeaths(country, 'new')
                                else:
                                    speak(f'Fetching the total deaths for {country}')
                                    getDeaths(country)
                                speak("Data Fetched Successfully")    

                            elif "recover" in query or "save" in query or "recoveries" in query:
                                speak("Do you want to know about the latest recoveries?")
                                print("Listening to user . . .")
                                answer = get_audio()
                                print(f'User : {answer}')
                                speak('Fetching Data')
                                if 'yes' in answer:
                                    getRecoveries(country, 'new')
                                else:
                                    speak(f'Fetching the total recovered data for {country}')
                                    getRecoveries(country)
                                speak('Data Fetched Successfully')               

                            elif "test" in query :
                                speak("Fetching Data")
                                getTests(country)   
                                speak("Data fetched successfully") 
                            
                            else:
                                speak(f"Getting all the data for {country}")
                                getAllCountryDetails(country)
              
                    

               #Spelling sleeping phrases will exit the process
                SLEEPING_PHRASES = ["sleep","end","bye"] 
                for phrase in SLEEPING_PHRASES:
                    if phrase in text:
                        speak("Goodbye See you later")
                        print('Stopping Assistant')
                        exit()     