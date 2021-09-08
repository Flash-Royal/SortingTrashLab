from tkinter import Tk, Canvas, Button, Label, Entry, messagebox
import random, math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

Interval = 1000
blinkInterval = 200
MaxCapacityOfTrash = 10000
MaxCapacityOfSortTrash = 5000

flag = 0
buffer = 0
iters = 0

massiv = [[0.0,0.0]]
profitTable = [ ['','','',''] for i in range(10) ]

totalIncome = 0   #доходы
totalExpense = 0  #расходы
totalProfit = 0   #прибыль

currentIncome = 0   #текущие доходы
currentExpense = 0  #текущие расходы
currentProfit = 0   #текущая прибыль

class Trash():
    def __init__(self):
        global MaxCapacityOfTrash

        self.glassTrash = 0
        self.dangerousTrash = 0
        self.plasticTrash = 0
        self.summaryTrash = self.glassTrash + self.dangerousTrash + self.plasticTrash

    def addTrash(self):
        num = 1000
        if (self.summaryTrash + num) < MaxCapacityOfTrash:
            summary = int(num / 4)
            glass = summary + random.randint(0,summary)
            plastic = summary + random.randint(0,summary)
            self.glassTrash = self.glassTrash + glass
            self.plasticTrash = self.plasticTrash + plastic
            self.dangerousTrash = self.dangerousTrash + num - glass - plastic
            self.summaryTrash = self.glassTrash + self.dangerousTrash + self.plasticTrash
        else:
            if self.summaryTrash < MaxCapacityOfTrash:
                summary = int((MaxCapacityOfTrash-self.summaryTrash)/4)
                glass = summary + random.randint(0,summary)
                plastic = summary + random.randint(0,summary)
                self.glassTrash = self.glassTrash + glass
                self.plasticTrash = self.plasticTrash + plastic
                self.dangerousTrash = self.dangerousTrash + num - glass - plastic
                self.summaryTrash = self.glassTrash + self.dangerousTrash + self.plasticTrash

class Graph():
    def __init__(self):
        self.fig = plt.figure(figsize = (7,4),frameon = False)
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        self.tableFig = plt.figure(figsize = (8,4),frameon = False)
        self.tableFig.patch.set_facecolor('snow')
        self.tableFig.patch.set_visible(False)
        self.ax2 = self.tableFig.add_subplot()

    def drawGraph(self, massiv):
        xs = []
        ys = []
        for line in massiv[:len(massiv) - 1]:
            xs.append(line[0])
            ys.append(line[1])

        self.ax1.clear()
        self.ax1.plot(xs, ys)

        self.ax1.set_xlabel('Days')
        self.ax1.set_ylabel('Profit')
        self.ax1.set_title('Profit over time graph')

        self.fig.canvas.draw()

    def drawTable(self, massiv):
        self.ax2.clear()
        self.ax2.table(cellText = massiv[::-1],
                  colLabels = ['День','Доход(р)','Расход(р)','Общая прибыль(р)'],
                  loc='center',
                  bbox=[0, 0, 1.1, 1.1],
                  colWidths = [0.6, 0.6, 0.6, 0.6],
                  )
        self.ax2.axis('off')
        self.ax2.axis('tight')
        self.tableFig.canvas.draw()

class Field():
    def __init__(self,tk):
        self.graph = Graph()

        self.canGraph = Canvas(tk, width = 780, height = 600)
        self.canGraph.place(x = 800, y = 305)
        self.canvasGraph = FigureCanvasTkAgg(self.graph.fig, self.canGraph)
        self.canvasGraph.get_tk_widget().config(bg = 'snow')
        self.canvasGraph.get_tk_widget().grid(column=0,row=0)

        self.canTable = Canvas(window, width = 300, height = 600)
        self.canTable.place(x = 0, y = 305)
        self.canvasTable = FigureCanvasTkAgg(self.graph.tableFig, self.canTable)
        self.canvasTable.get_tk_widget().config(bg = 'snow')
        self.canvasTable.get_tk_widget().grid(column=0, row=0, sticky='nsew')

        self.trashSortCanvas = Canvas(tk, width = 1000, height = 305, bg = "snow", highlightthickness = 0)
        self.trashSortCanvas.place(x = 500, y = 0)

        self.trashSummaryBox = self.trashSortCanvas.create_rectangle(10, 30, 100, 270)
        self.trashSummaryText = Label(self.trashSortCanvas, text = "Accepting Trash", bg = "snow")
        self.trashSummaryText.place(x = 10, y = 5)

        self.glassTrashBox = self.trashSortCanvas.create_rectangle(150, 30, 350, 90)
        self.glassTrashText = Label(self.trashSortCanvas, text = "Glass Trash", bg = "snow")
        self.glassTrashText.place(x = 220, y = 5)

        self.plasticTrashBox = self.trashSortCanvas.create_rectangle(150, 120, 350, 180)
        self.plasticTrashText = Label(self.trashSortCanvas, text = "Plastic Trash", bg = "snow")
        self.plasticTrashText.place(x = 217, y = 95)

        self.dangerousTrashBox = self.trashSortCanvas.create_rectangle(150, 210, 350, 270)
        self.dangerousTrashText = Label(self.trashSortCanvas, text = "Dangerous Trash", bg = "snow")
        self.dangerousTrashText.place(x = 207, y = 185)

        self.acceptingTrashToGlass = self.trashSortCanvas.create_oval(110, 45, 140, 75)
        self.acceptingTrashToPlastic = self.trashSortCanvas.create_oval(110, 135, 140, 165)
        self.acceptingTrashToDangerous = self.trashSortCanvas.create_oval(110, 225, 140, 255)

        self.massivBox = []

    def fillBox(self, box, percent):
        k = 0
        coordsBox = self.trashSortCanvas.coords(box)
        if len(self.massivBox) == 0:
            fillingBox = self.trashSortCanvas.create_rectangle(coordsBox[0],coordsBox[3],coordsBox[2],coordsBox[3], fill = "black")
            self.massivBox.append(fillingBox)

        for i in range(len(self.massivBox)):
            coordsFillingBox = self.trashSortCanvas.coords(self.massivBox[i])
            if coordsFillingBox[0] == coordsBox[0] and coordsFillingBox[3] == coordsBox[3]:
                j = i
                k = 1
                break

        if k == 0:
            fillingBox = self.trashSortCanvas.create_rectangle(coordsBox[0],coordsBox[3],coordsBox[2],coordsBox[3], fill = "black")
            self.massivBox.append(fillingBox)
        else:
            height = percent * (coordsBox[3] - coordsBox[1]) / 100 # учитывает высоту заполнения относительно высоты самого прямоугольника
            coordsBox[1] = coordsBox[3] - height #изменяем координату y левого верхнего угла прямоугольника, оставляя все остальные координаты неизменными
            self.trashSortCanvas.coords(self.massivBox[j],coordsBox) #

    def changeObjectColor(self,color,object):
        self.trashSortCanvas.itemconfig(object, fill = color)

    def blinkArrow(self, arrows, color):
        global Interval, blinkInterval
        for arrow in arrows:
            interval = 0
            for i in range(round(Interval/blinkInterval)):
                if i % 2:
                    self.trashSortCanvas.after(interval, self.changeObjectColor, color, arrow)
                else:
                    self.trashSortCanvas.after(interval, self.changeObjectColor, 'white', arrow)
                interval += blinkInterval
            self.trashSortCanvas.after(Interval, self.changeObjectColor, 'white', arrow)

class SortAndClearTrash():
    def __init__(self,tk):
        self.trash = Trash()
        self.draw = Field(tk)
        self.num = 1000

        self.glassTrash = 0
        self.dangerousTrash = 0
        self.plasticTrash = 0


        self.trashAddButtonCanvas = Canvas(tk, width = 150, height = 10, bg = "snow", highlightthickness = 0)
        self.trashAddButtonCanvas.place(x = 350, y = 135)

        self.trashAddButton =  Button(self.trashAddButtonCanvas, text = "fetch 1000 kg trash", width = 20, height = 2, bg = "lightcyan",foreground = "black")
        self.trashAddButton.pack(side = "left")
        self.trashAddButton.bind(sequence = "<Button-1>", func = self.addTrash)

        self.glassTrashDelButtonCanvas = Canvas(self.draw.trashSortCanvas, width = 150, height = 10, bg = "snow", highlightthickness = 0)
        self.glassTrashDelButtonCanvas.place(x = 400, y = 40)

        self.glassTrashDelButton = Button(self.glassTrashDelButtonCanvas, text = "export glass trash", width = 20, height = 2, bg = "lightcyan",foreground = "black")
        self.glassTrashDelButton.pack(side = "left")
        self.glassTrashDelButton.bind(sequence = "<Button-1>", func = self.delGlassTrash)

        self.plasticTrashDelButtonCanvas = Canvas(self.draw.trashSortCanvas, width = 150, height = 10, bg = "snow", highlightthickness = 0)
        self.plasticTrashDelButtonCanvas.place(x = 400, y = 130)

        self.plasticTrashDelButton = Button(self.plasticTrashDelButtonCanvas, text = "export plastic trash", width = 20, height = 2, bg = "lightcyan",foreground = "black")
        self.plasticTrashDelButton.pack(side = "left")
        self.plasticTrashDelButton.bind(sequence = "<Button-1>", func = self.delPlasticTrash)

        self.dangerousTrashDelButtonCanvas = Canvas(self.draw.trashSortCanvas, width = 150, height = 10, bg = "snow", highlightthickness = 0)
        self.dangerousTrashDelButtonCanvas.place(x = 400, y = 220)

        self.dangerousTrashDelButton = Button(self.dangerousTrashDelButtonCanvas, text = "export dangerous trash", width = 20, height = 2, bg = "lightcyan",foreground = "black")
        self.dangerousTrashDelButton.pack(side = "left")
        self.dangerousTrashDelButton.bind(sequence = "<Button-1>", func = self.delDangerousTrash)

        self.canStopSystemButton = Canvas(tk, width = 200, height = 300, bg = "snow", highlightthickness = 0)
        self.canStopSystemButton.place(x = 100, y = 70)

        self.stopSystemButton = Button(self.canStopSystemButton, text = 'Stop \nSystem', width = 20, height = 10, bg = "red",foreground = "white")
        self.stopSystemButton.pack(side = 'bottom')
        self.stopSystemButton.bind(sequence="<Button-1>", func = self.makeError)

        self.totalProfitText = Label(self.draw.trashSortCanvas, text = "Общая прибыль = 0р.", font=("arial", 18), bg="snow", anchor = "w", width=30)
        self.totalProfitText.place(x = 600, y = 130)


    def addTrash(self, event):
        self.trash.addTrash()
        self.draw.fillBox(self.draw.trashSummaryBox, math.floor(self.trash.summaryTrash / MaxCapacityOfTrash * 100))

    def sortGlassTrash(self):
        num = self.num / 4
        if (self.trash.glassTrash > num and (self.glassTrash + num) < MaxCapacityOfSortTrash):
            self.trash.glassTrash = self.trash.glassTrash - num
            self.trash.summaryTrash = self.trash.summaryTrash - num
            self.glassTrash = self.glassTrash + num
        else:
            if (self.trash.glassTrash > 0 and (self.glassTrash + self.trash.glassTrash) < MaxCapacityOfSortTrash):
                self.glassTrash = self.glassTrash + self.trash.glassTrash
                self.trash.summaryTrash = self.trash.summaryTrash - self.trash.glassTrash
                self.trash.glassTrash = 0
        self.draw.fillBox(self.draw.glassTrashBox, math.floor(self.glassTrash / MaxCapacityOfSortTrash * 100))

    def sortPlasticTrash(self):
        num = self.num / 4
        if (self.trash.plasticTrash > num and (self.plasticTrash + num) < MaxCapacityOfSortTrash):
            self.trash.plasticTrash = self.trash.plasticTrash - num
            self.trash.summaryTrash = self.trash.summaryTrash - num
            self.plasticTrash = self.plasticTrash + num
        else:
            if (self.trash.plasticTrash > 0 and (self.plasticTrash + self.trash.plasticTrash) < MaxCapacityOfSortTrash):
                self.plasticTrash = self.plasticTrash + self.trash.plasticTrash
                self.trash.summaryTrash = self.trash.summaryTrash - self.trash.plasticTrash
                self.trash.plasticTrash = 0
        self.draw.fillBox(self.draw.plasticTrashBox, math.floor(self.plasticTrash / MaxCapacityOfSortTrash * 100))

    def sortDangerousTrash(self):
        num = self.num / 4
        if (self.trash.dangerousTrash > num and (self.dangerousTrash + num) < MaxCapacityOfSortTrash):
            self.trash.dangerousTrash = self.trash.dangerousTrash - num
            self.trash.summaryTrash = self.trash.summaryTrash - num
            self.dangerousTrash = self.dangerousTrash + num
        else:
            if (self.trash.dangerousTrash > 0 and (self.dangerousTrash + self.trash.dangerousTrash) < MaxCapacityOfSortTrash):
                self.dangerousTrash = self.dangerousTrash + self.trash.dangerousTrash
                self.trash.summaryTrash = self.trash.summaryTrash - self.trash.dangerousTrash
                self.trash.dangerousTrash = 0
        self.draw.fillBox(self.draw.dangerousTrashBox, math.floor(self.dangerousTrash / MaxCapacityOfSortTrash * 100))

    def sortTrash(self):
        global currentProfit, currentExpense, currentIncome
        if self.trash.glassTrash != 0 and self.trash.plasticTrash != 0 and self.trash.dangerousTrash:
            self.draw.blinkArrow([self.draw.acceptingTrashToGlass, self.draw.acceptingTrashToPlastic, self.draw.acceptingTrashToDangerous], "green")
        self.sortGlassTrash()
        self.sortPlasticTrash()
        self.sortDangerousTrash()
        currentExpense = 1000
        currentProfit = -currentExpense
        currentIncome = 0
        self.draw.fillBox(self.draw.trashSummaryBox, math.floor(self.trash.summaryTrash / MaxCapacityOfTrash * 100))

    def delGlassTrash(self, event):
        global flag, buffer
        buffer = self.glassTrash
        self.glassTrash = 0
        self.draw.fillBox(self.draw.glassTrashBox, 0)
        flag = 2
        flag1 = 1

    def delPlasticTrash(self, event):
        global flag, buffer
        buffer = self.plasticTrash
        self.plasticTrash = 0
        self.draw.fillBox(self.draw.plasticTrashBox, 0)
        flag = 2

    def delDangerousTrash(self, event):
        global flag, buffer
        buffer = self.dangerousTrash
        self.dangerousTrash = 0
        self.draw.fillBox(self.draw.dangerousTrashBox, 0)
        flag = 2


    def makeError(self, event):
        global flag
        flag = 1

    def syserror(self):
            global flag
            messagebox.showerror(
                "System malfunction",
                "Press OK to fix system (500$)")
            flag = 0

    def progress(self):
        global flag, massiv, profitTable, Interval, totalIncome, totalExpense, totalProfit, currentIncome, currentProfit, currentExpense, iters
        if flag == 1:
            self.syserror()
            currentExpense += 500
            currentIncome = 0
            currentProfit -= currentExpense
            totalIncome += currentIncome
            totalExpense += currentExpense
            totalProfit += currentProfit
            profitTable.append([iters, currentIncome, currentExpense, totalProfit])
            self.draw.trashSortCanvas.after(Interval, self.progress)
        elif flag == 2:
            flag = 0
            currentIncome = 5 * buffer
            currentProfit = currentIncome
            currentExpense = 0
            totalIncome += currentIncome
            totalExpense += currentExpense
            totalProfit += currentProfit
            profitTable.append([iters, currentIncome, currentExpense, totalProfit])
            self.draw.trashSortCanvas.after(Interval, self.progress)
        else:
            self.sortTrash()
            totalIncome += currentIncome
            totalExpense += currentExpense
            totalProfit += currentProfit
            profitTable.append([iters, currentIncome, currentExpense, totalProfit])
            iters += 1
            self.draw.trashSortCanvas.after(Interval, self.progress)

        massiv.append([iters, totalProfit])


        if len(massiv) > 15:               #максимальный размер массива
            del massiv[0]
        if len(profitTable) > 10:       #максимальный размер таблицы
            del profitTable[0]

        self.draw.graph.drawGraph(massiv)
        self.draw.graph.drawTable(profitTable)

        self.totalProfitText.config(text = 'Общая прибыль = ' + str(totalProfit) + 'р.')

window = Tk()
window["bg"] = "snow"
window.resizable(0, 0)


field = SortAndClearTrash(window)
field.progress()
# field.draw.trashSortCanvas.after(0, field.progress)
window.geometry('1480x720')
window.mainloop()
