import json

with open(r"D:\Max Research\Franka-Max\knowledgegraph\knowledge.json", "rb") as jsonFile:
    data = json.load(jsonFile)
    product = data["service"]["smart phone"][0]["definition"][0]["product"]
    pcb = data["service"]["smart phone"][0]["definition"][1]["PCB"]
    fuses = data["service"]["smart phone"][0]["definition"][2]["fuses"]
    house = data["service"]["smart phone"][0]["definition"][3]["house"]
    cover = data["service"]["smart phone"][0]["definition"][4]["cover"]
    lab = data["service"]["smart phone"][0]["definition"][5]["lab"]
    process = data["service"]["smart phone"][0]["definition"][6]["process"]

    PCBtoFuses = data["service"]["smart phone"][1]["relationship"][0]["PCBtoFuses"]
    PCBtoHouse = data["service"]["smart phone"][1]["relationship"][1]["PCBtoHouse"]
    HousetoCover = data["service"]["smart phone"][1]["relationship"][2]["HousetoCover"]
    FusestoHouse = data["service"]["smart phone"][1]["relationship"][3]["FusestoHouse"]
    FusestoCover = data["service"]["smart phone"][1]["relationship"][4]["FusestoCover"]
    PCBtoCover = data["service"]["smart phone"][1]["relationship"][5]["PCBtoCover"]

    print(product)
    print(pcb)
    print(fuses)
    print(house)
    print(cover)
    print(lab)
    print(PCBtoFuses)
    print(PCBtoHouse)
    print(HousetoCover)
    print(FusestoHouse)
    print(FusestoCover)
    print(PCBtoCover)