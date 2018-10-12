from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
import speech_recognition as sr
import json

openjson = open("Excel Speech Recognition-7425f397ccea.json")

jsonfile = json.load(openjson)

creds = {
  "type": "service_account",
  "project_id": "excel-speech-recognition",
  "private_key_id": "7425f397ccea37a7bb61a34dc3ed6737fe6398c7",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCn1aHnvp8ImUkX\nAcLzyrUU+0Ho7Jfr7O5NTpWHYnNnpaM78MScNNY9BKNVnNMqHQPa9bPJEwOhsroD\np1m9KxHCMssx/ZkCgOeLEEB9jwmZTAV2PLiAjt3y4TxUrk/TrS/L4HmJFDAjSkWL\nLZVEH8lGMQh9ECHxmK2o5oHASu6M+pz0oGVxv8GrsIHbmsQH2i2gEg3hZPUflE30\nd9yeHyB/OFV+b4CBbCI6U7RdumP73R/DCnvdYtotsK8wIjfx+pHp8S1+BqFlS+fa\nMNsv+5cyCz/4SSxcMUzTj2hJAGZspNMogOhs9NL0L/D7cJ9T6F0teCf4fdawq4Yg\nW6DRxSSfAgMBAAECggEABLibxvyed7JSSsEN3VKv95rtPgsdeISiKMjRdOrjdNfv\n5X6erpAS/4VYWHm1vAQi7hfuncHY1hsAOb58ZdFkq8Ik0pfogcLr/Dli4KEK07+T\nxVr1HOYBh6W4nAF4VUEDcvuYqTeeXOc9FSqUn9z1TkcqKG4xJS4yXoNVb7XJw2uw\nkqls8BAYYxezavUCbEMcSHSEFjkadJXAOycr0CjhA+Tma0RzRaSD+2Y2r0yE5JWR\nKEEbQUVB5UfYXv+4hENw9jc9j3rQVraOaTy7SyNFeC710r2ctfBw70BfDRZ90/ba\nWKPAl4qqbm3wzswclW5ZXF14iok4sRphv0xhYN6zAQKBgQDbYZtTmyUpw3KsnyoJ\nJJL9V70sZhxNn80GDlGy7c+z5AYCmTdvBzJrPMEtF0coJef3Ini5CKC0M1wCjQd1\nsXmnuGkoT9N+6uOBCQfpwfyejLT515LNbkOrD9qQPEd+90zHc6ZfNauPpQnlQRyz\nCqVjPiLtLvHJkCweGGXuWGjgHwKBgQDD2WCuzDGa/d1C0cCNPOtVTJS4SzXlk9a4\nZFuAIIux0dZcnHHczrGBKQTR9YKx7gAjFpXiT2DFw1uxlXSRsFmte8uc+DtJvY7z\nlFrVI1thJalZv8V0G7a0pXc4cNLA9SSWAtzmzA6LujBOqzZNJaEXDXsBHJCl/6j5\npqnPs9krgQKBgDbN53O3ak1Imjkted7W2DGZ3ZRd3ew2Y42Dvj0o055o9Gdpx0Nh\nVOMdRlTxX8FT1uMSJX5z/VGHExFAEgEA2RdhJkP/zSIDo9n0W5m18FnbZMqVZAMV\n7KmrSDqIFIRPW0roRUO7sKQt4o72+ShxHGfyed8uvxBPh/XsumoUg/6ZAoGBAIAV\nsYqAFs0jzEn//esg9VPi8ryYy5Xqmxoa4FCqeFICRyxoUHs1Xpd3KSTbaO9PFR3d\njobknQiZnGVGtmb1q6Cu/toY6kVuyIf69XDBX+joBZqhtdQar+Hy+UabWupBKP1G\nwAvdVoIBcchxZuELhBAci96NPPijfHJRkms5VwWBAoGAY+y+6Wj1DgrsVfkDHA3A\nfVJ3tKKhfXT2GN3mn0ZIG9F47WClUsewx5y3EG0dTFISpwrh6S2CLSH4j1z5rM0v\nrORGKm3KrWwY9o+3B4S7oPEBEqqTktYIPJi4UJ/sqLF+wWH4HVntvyZ7k6ZqKioP\ngz39daFA6HznX/nIXIrLFn0=\n-----END PRIVATE KEY-----\n",
  "client_email": "kazilii-testing@excel-speech-recognition.iam.gserviceaccount.com",
  "client_id": "114817235352355753650",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kazilii-testing%40excel-speech-recognition.iam.gserviceaccount.com"
}
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