import tkinter
from tkinter import *
from tkinter import ttk
from Dijkstra import Dijkstra
import csv
import json


class Interface:

    def __init__(self):
        self.confirmBTN = None
        self.window = Tk()
        self.window.geometry("500x300")
        self.window.title("Dijkstra - Accueil")
        self.frm = ttk.Frame(self.window, padding=10)
        self.frm.grid()
        self.currentMap = {"A": {}}
        self.point = None
        self.string = tkinter.StringVar(self.window)
        ttk.Button(self.frm, text="New Map", command=self.newMap).grid(column=0, row=1)
        ttk.Button(self.frm, text="Import", command=self.Import1).grid(column=1, row=1)
        ttk.Button(self.frm, text="Quit", command=self.window.destroy).grid(column=0, row=2)
        self.name = None
        self.way = None
        self.dist = None
        self.trip = None
        self.point2 = None
        self.string2 = tkinter.StringVar(self.window)
        self.onewayStreet = tkinter.BooleanVar(self.window)
        self.onWayStreetCheck = None
        self.file = None
        self.file_name = None

    def Import1(self):
        self.clearPage()
        self.file_name = ttk.Entry()
        self.file_name.grid()
        ttk.Button(self.frm, text="Select", command=self.Import2).grid(column=3, row=2)


    def Import2(self):
        self.currentMap = {}

        with open(self.file_name.get() + ".csv", "r") as file:
            reader = csv.DictReader(file)
            for line in reader:
                value = "{ways}".format(ways=line["Ways"])
                json_acceptable_string = value.replace("'", "\"")
                self.currentMap["{point}".format(point=line["Point_Name"])] = json.loads(json_acceptable_string)
        self.file_name.destroy()
        self.newMap()


    def newMap(self):
        self.window.title("Dijkstra - New Map")
        self.clearPage()
        self.point = ttk.OptionMenu(self.window, self.string, list(self.currentMap.keys())[0], *self.currentMap.keys(), command=self.selected)
        self.point.grid(column=1, row=0)
        ttk.Button(self.frm, text="Add", command=self.Add).grid(column=0, row=0)
        ttk.Button(self.frm, text="Add Ways", command=self.AddWays).grid(column=0, row=3)
        ttk.Button(self.frm, text="remove Ways", command=self.RemoveWays).grid(column=1, row=3)
        ttk.Button(self.frm, text="Start", command=self.start).grid(column=2, row=0)
        ttk.Button(self.frm, text="Remove", command=self.removePoint).grid(column=1, row=0)

    def Add(self):
        self.pointName = ttk.Entry()
        self.pointName.grid(column=2, row=0)
        self.confirmBTN = ttk.Button(self.frm, text="confirm", command=self.confirm)
        self.confirmBTN.grid(column=0, row=0)

    def confirm(self):
        self.currentMap[self.pointName.get()] = {}
        self.point.destroy()
        self.point = ttk.OptionMenu(self.frm, self.string, list(self.currentMap.keys())[0], *self.currentMap.keys(), command=self.selected)
        self.point.grid(column=3, row=0)
        self.pointName.destroy()
        self.confirmBTN.destroy()
        self.confirmBTN = None
        print(self.currentMap)

    def selected(self, *args):
        if self.name is not None:
            self.name.destroy()
            self.way.destroy()
            self.dist.destroy()
        self.name = ttk.Label(self.frm, text=self.string.get())
        self.name.grid(column=0, row=1)
        destination = ""
        dist = ""
        for i in self.currentMap.get(self.string.get()).keys():
            destination += "\n" + i
            dist += "\n" + str(self.currentMap.get(self.string.get()).get(i))
        self.way = ttk.Label(self.frm, text=destination)
        self.way.grid(column=1, row=1)
        self.dist = ttk.Label(self.frm, text=dist)
        self.dist.grid(column=2, row=1)

    def clearPage(self):
        for widget in self.frm.winfo_children():
            widget.destroy()

    def AddWays(self):
        self.trip = ttk.Entry()
        self.trip.grid(column=2, row=3)
        self.point2 = ttk.OptionMenu(self.frm, self.string2, list(self.currentMap.keys())[0], *self.currentMap.keys())
        self.point2.grid(column=1, row=3)
        self.confirmBTN = ttk.Button(self.frm, text="confirm", command=self.confirmWays)
        self.confirmBTN.grid(column=0, row=3)
        self.onWayStreetCheck = ttk.Checkbutton(self.frm, text="One Way Street", variable=self.onewayStreet, onvalue=True, offvalue=False)
        self.onWayStreetCheck.grid(column=4, row=3)

    def confirmWays(self):
        self.currentMap.get(self.string.get())[self.string2.get()] = int(self.trip.get())
        if self.onewayStreet.get() is False:
            self.currentMap.get(self.string2.get())[self.string.get()] = int(self.trip.get())

        self.confirmBTN.destroy()
        self.trip.destroy()
        self.point2.destroy()
        self.onWayStreetCheck.destroy()

    def RemoveWays(self):
        self.point2 = ttk.OptionMenu(self.frm, self.string2, list(self.currentMap.keys())[0], *self.currentMap.keys(), command=self.selected)
        self.point2.grid(column=1, row=3)
        self.confirmBTN = ttk.Button(self.frm, text="confirm", command=self.delConfirm)
        self.confirmBTN.grid(column=0, row=3)

    def delConfirm(self):
        del self.currentMap.get(self.string.get())[self.string2.get()]
        del self.currentMap.get(self.string2.get())[self.string.get()]
        self.confirmBTN.destroy()
        self.point2.destroy()

    def removePoint(self):
        del self.currentMap[self.string.get()]
        for i in self.currentMap.keys():
            del self.currentMap.get(i)[self.string.get()]
        self.point.destroy()
        self.point = ttk.OptionMenu(self.frm, self.string, list(self.currentMap.keys())[0], *self.currentMap.keys(),command=self.selected)

    def start(self):
        self.clearPage()
        ttk.Label(self.frm, text="starting point").grid(column=0, row=0)
        ttk.Label(self.frm, text="ending point").grid(column=0, row=1)
        self.point2 = ttk.OptionMenu(self.frm, self.string2, list(self.currentMap.keys())[0], *self.currentMap.keys())
        self.point2.grid(column=1, row=1)
        self.point = ttk.OptionMenu(self.frm, self.string, list(self.currentMap.keys())[0], *self.currentMap.keys())
        self.point.grid(column=1, row=0)
        self.confirmBTN = ttk.Button(self.frm, text="confirm", command=self.launch)
        self.confirmBTN.grid(column=2, row=0)

    def launch(self):
        self.clearPage()
        dj = Dijkstra(map=self.currentMap, startPoint=self.string.get(), endPoint=self.string2.get())
        dj.Dijkstra()
        ttk.Label(self.frm, text=f"Le chemin le plus court est {dj.road} avec une distance de {dj.dist}").grid()
        ttk.Button(self.frm, text="Save", command=self.save1).grid()

    def save1(self):
        self.clearPage()
        self.file_name = ttk.Entry()
        self.file_name.grid()
        ttk.Button(self.frm, text="Confirm", command=self.save2).grid(column=3, row=2)

    def save2(self):
        with open(self.file_name.get() + ".csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Point_Name", "Ways"])
            for i in self.currentMap.keys():
                writer.writerow([i, self.currentMap[i]])
            file.close()
            self.window.destroy()

    def run(self):
        self.window.mainloop()

i = Interface()
i.run()