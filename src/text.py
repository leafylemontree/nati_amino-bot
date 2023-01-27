import json

text = None 

def reload():
    with open("data/text.json", "r") as textFile:
        global text
        text = json.load(textFile)
        print("Texto cargado")
    return

reload()
