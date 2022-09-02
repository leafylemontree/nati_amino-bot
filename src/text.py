import json

text = None 

def reload():
    global text
    with open("data/text.json", "r") as textFile:
        text = json.load(textFile)
        print("Texto cargado")
    return

reload()
