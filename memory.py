#Memory (grafisk ver)
#Sandra Liljeqvist
#2011-12-08

import random
import tkinter
from tkinter import *
        

#"Kortleken" med de ord som kommer användas
class CardDeck:

    #Konstruktor för CardDeck
    #
    #@param sideLen - Spelplanens sidlängd
    def __init__(self,sideLen):
        self.sideLen = sideLen

    #Läser in alla ord från filen memory.txt och placerar i listan self.allWords
    def read(self):

        file = open("memory.txt","r")
        line = file.readline()
        self.allWords = []
        while line !="":
            part = line.split("\n")
            self.allWords.append(part[0])
            line = file.readline()
        file.close()

    #Slumpar fram så många ord som ska användas och sparar dem i self.words
    def random(self):
        random.shuffle(self.allWords)
        self.words = self.allWords[:int(pow(self.sideLen,2)/2)]

    #Dubblerar och blandar orden
    def dubble(self):
        self.words = self.words*2
        random.shuffle(self.words)

    #Skapar en lista med card-objekt
    def createCards(self):
        self.cards = []
        for i in self.words:
            self.cards.append(Card(i,False))
        

#Kortet
class Card:

    #Konstruktor för Card
    #
    #@param word - Det ord kortet tillägnats
    #@param up - Om kortet är upp- eller nedvänt
    def __init__(self,word,up):
        self.word = word
        self.up = up

    #Utskrift för card
    #@return - returnerar kortets ord om kortet är uppvänt
    def __str__(self):
        if self.up == True:
            return self.word
        else:
            return ""
   
#Det grafiska
class Application:

    #Konstruktor för Application
    #
    #@param root - huvuvdfönstret
    def __init__(self, root):
        self.root = root
        self.countClicks = 0
        self.indexToCompare = []
        self.trials = 0
        self.pairs = 0
        self.text = False

        #Skapar huvudfönstret och container
        self.root.title("Sandras python-memory")
        tkinter.Frame(self.root, width=500, height=450).pack()

        self.setLevel()

    #Radioknappar med val av nivå/brädstorlek
    def setLevel(self):

        self.var = StringVar()
        self.txt = tkinter.Label(self.root, textvariable=self.var).place(x=0, y=0)
        self.var.set("Välj nivå")
                                      
        self.varRadio = IntVar()
        self.radiobuttons = []
        for i in range(3):
            self.radiobuttons.append(Radiobutton (self.root, text="Nivå "+str(i+1), variable=self.varRadio, value=(i+1)*2, command=self.start))
            self.radiobuttons[i].pack(anchor = W)

    #Sätter spelbrädets storlek (dvs värdet på sideLen) startar igång programmet och kontrollerar att filen är korrekt
    def start(self):
        self.sideLen = self.varRadio.get()

        self.c = CardDeck(self.sideLen)
        OK1 = True
        try:
            self.c.read()
        except IOError:
            text = self.var.get()
            self.var.set("Filen finns ej")
            OK1 = False

        if OK1 == True:
            if len(self.c.allWords) < pow(self.sideLen,2)/2:
                text = self.var.get()
                self.var.set("Filen innehåller för få ord")
            else:
                self.c.random()
                self.c.dubble()
                self.c.createCards()
                self.printBoard()

    #Skapar ett spelbräde med knappar
    #
    #@param sideLen - Spelplanens sidlängd
    def printBoard(self):
        xvar=10
        yvar=70
        self.buttons = []
        cardCount = 0
        for i in range(self.sideLen):
            for j in range(self.sideLen):

                cmd = lambda index=cardCount: self.click(index)               
                self.buttons.append(tkinter.Button(self.root, command=cmd, text=self.c.cards[cardCount], width="6"))
                self.buttons[cardCount].place(x=xvar, y=yvar)
                
                xvar=xvar+80
                cardCount += 1
            xvar=10
            yvar=yvar+60

        #Tar bort text och radioknappar
        text = self.var.get()
        self.var.set("")
        
        for i in range(len(self.radiobuttons)):
            self.radiobuttons[i].pack_forget()

    #Vänder upp kortet efter klickning
    #
    #@param index - Index för det valda kortet
    #countClicks - Räknar klickningar så vi vet när två är uppvända
    #indexToCompare - Sparar index för de uppvända korten
    #text - Om True så är text utskriven
    def click(self,index):
        #Kontrollerar att kortet inte redan är uppvänt
        if self.c.cards[index].up == False:

            #Vänder kortet
            self.c.cards[index].up = True
            self.buttons[index].config(text=self.c.cards[index])
            self.countClicks += 1

            #Tar bort eventuell tidigare utskriven text
            if self.text == True:
                text = self.var.get()
                self.var.set("")
                self.text = False

            #Uppdaterar knapparna
            if len(self.indexToCompare) == 2:
                self.buttons[self.indexToCompare[0]].config(text=self.c.cards[self.indexToCompare[0]])
                self.buttons[self.indexToCompare[1]].config(text=self.c.cards[self.indexToCompare[1]])
                self.indexToCompare = []
    
            #Sparar index i listan indexToCompare och ser till att kort jämförs om två är uppvända                       
            if self.countClicks == 2:
                self.countClicks = 0
                self.indexToCompare.append(index)
                self.compare()
            else:
                self.indexToCompare.append(index)
                self.text = True
                
        else:
            text = self.var.get()
            self.var.set("Kortet är redan uppvänt")

    #Orden jämförs och vänds ner om de är olika
    #
    #self.trials - Räknar antalet försök att hitta par
    def compare(self):
        self.trials += 1
        if self.c.cards[self.indexToCompare[0]].word == self.c.cards[self.indexToCompare[1]].word:
            text = self.var.get()
            self.var.set("Du hittade ett par!")
            self.text = True
            
            self.indexToCompare = []
            self.countPairs()
        else:
            self.c.cards[self.indexToCompare[0]].up = False
            self.c.cards[self.indexToCompare[1]].up = False

    #Räknar antalet par och upptäcker eventuell vinst
    def countPairs(self):
        self.pairs += 1
        if self.pairs == pow(self.sideLen,2)/2:
            text = self.var.get()
            self.var.set("DU VANN!\nDu klarade spelet på "+str(self.trials)+" försök")
            self.newGameButton = tkinter.Button(self.root, command=self.newGame, text="Spela igen?", width="12")
            self.newGameButton.pack()

    #Nollställer och startar nytt spel
    def newGame(self):
        text = self.var.get()
        self.var.set("")
        self.text = False
        self.newGameButton.destroy()
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        self.trials = 0
        self.pairs = 0
        self.text = False
        self.setLevel()


#Huvudprogram
root = tkinter.Tk()
Application(root)
root.mainloop()
