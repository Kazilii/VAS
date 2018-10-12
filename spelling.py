from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import speech_recognition as sr
import json

openjson = open("Excel Speech Recognition-7425f397ccea.json")

jsonfile = json.load(openjson)
creds = {}
testing = json.dumps(creds)

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    print("Waiting for voice command.")
    audio = r.listen(source)
print("Voice command received, processing...")
#print(r.recognize_google_cloud(audio_data=audio, credentials_json=testing))
#response = r.recognize_google_cloud(audio, credentials_json=testing)
response = r.recognize_google(audio)
print(response)
#response = input("Inventory Entry: ")

choices = ["Absolute Vodka", "Makers Mark", "Fireball Cinnamon Whisky"]
fuzzyresponse = process.extract(response, choices, limit=1)

print(fuzzyresponse)

def refuzzy(fuzz):
    regex = r"\[\(\'((\w+)? ?-?_?)+\'\, \d+\)\]"

    matches = re.finditer(regex, str(fuzz))

    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        return match.group(groupNum)

result = refuzzy(fuzzyresponse)

print(result)
