import json
from configure import Config

cfg = Config()

def update_service(text):
    with open(cfg.dialogue, "r") as jsonFile:
        data = json.load(jsonFile)
        data[0]["service"] = text
    jsonFile.close()
    with open(cfg.dialogue, "w") as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()

def update_mir(internet, system, task):
    with open(cfg.dialogue, "r") as jsonFile:
        data = json.load(jsonFile)
        data[0]["mir_internet"] = internet
        data[0]["mir_system"] = system
        data[0]["mir_task"] = task
    jsonFile.close()
    with open(cfg.dialogue, "w") as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()

def update_max(text):
    with open(cfg.dialogue, "r") as jsonFile:
        data = json.load(jsonFile)
        data[0]["Max"] = text
    jsonFile.close()
    with open(cfg.dialogue, "w") as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()


def update_user(text):
    with open(cfg.dialogue, "r") as jsonFile:
        data = json.load(jsonFile)
        data[0]["User"] = text
    jsonFile.close()
    with open(cfg.dialogue, "w") as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()


def update_franka(internet, system, task):
    with open(cfg.dialogue, "r") as jsonFile:
        data = json.load(jsonFile)
        data[0]["franka_internet"] = internet
        data[0]["franka_system"] = system
        data[0]["franka_task"] = task
    jsonFile.close()
    with open(cfg.dialogue, "w") as jsonFile:
        json.dump(data, jsonFile)
    jsonFile.close()