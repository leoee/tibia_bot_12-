import json
import logging
import random
import os
import threading
import pyautogui
import pyscreenshot as ImageGrab
import sys
import time
import tkinter as tk
from tkinter import *
from pynput.mouse import Listener as MouseListener
from pynput import mouse

configIndex = 0
P1 = 0
P2 = 0
firstTime = False
shouldListener = False

path = os.getcwd()
def returnListPointsBar():
	file = open("config_screen.txt", "r")
	contents = file.read()
	list = []
	indexPrevious = 0
	indexNext = 0
	for i in range (16):
		value = ""
		indexPrevious = contents.index('"', indexNext + 1)
		indexNext = contents.index('"', indexPrevious + 1)
		for x in range(indexPrevious + 1, indexNext):
			value += contents[x]
		list.append(value)
	return list

def checkConfigScreen():
	im=pyautogui.screenshot()
	im = im.crop((int(P1[0]), int(P1[1]), int(P2[0]), int(P2[1])))
	im.show()
	popupmsg('Please, confirm if the following points are valids\n P1' + str(P1) + ', P2' + str(P2))

def on_move(x, y):
	global firstTime
	if (firstTime == False):
		return False

def on_click(x, y, button, pressed):
	global shouldListener
	if pressed:
		if (button == mouse.Button.right and shouldListener):
			shouldListener = False
			checkConfigScreen()
			return False
		else:
			global configIndex, P1, P2
			if (configIndex == 0):
				P1 = [x, y]
				configIndex = 1
			elif (configIndex == 1):
				P2 = [x, y]
				configIndex = 0

with MouseListener(on_move=on_move, on_click=on_click) as listener:
	listener.join()

class Concur(threading.Thread):
	def __init__(self):
		super(Concur, self).__init__()
		self.iterations = 0
		self.master = None
		self.daemon = True
		self.paused = True
		self.state = threading.Condition()

	def setMaster(self, master):
		self.master = master

	def run(self):
		self.resume()
		while True:
			with self.state:
				if self.paused:
					self.state.wait()
			controller(self)
			time.sleep(.1)
			self.iterations += 1

	def resume(self):
		with self.state:
			self.paused = False
			self.state.notify()

	def pause(self):
		with self.state:
			self.paused = True


def changeGeneratorToList(vector_life, vector_mana):
	for i in range(0, 10):
		vector_life[i] = list(vector_life[i])
		vector_mana[i] = list(vector_mana[i])

def configHeal(master, currentLife, currentMana):
	valueTotalMana = concur.master["totalMana"].get()
	valueTotalLife = concur.master["totalLife"].get()
	keyLife90 = concur.master["keyPressCure90"].get().lower()
	keyLife70 = concur.master["keyPressCure70"].get().lower()
	keyLife50 = concur.master["keyPressCure50"].get().lower()
	manaPercentForHeal = concur.master["manaPercent"].get()
	manaPercentForTrain = concur.master["manaPercentForTrain"].get()
	keyPressMana = concur.master["keyPressCureMana"].get().lower()
	keyPressTrainMana = concur.master["keyPressTrainMana"].get().lower()
	
	if (valueTotalLife.isdigit() == False or valueTotalMana.isdigit() == False):
		return

	if (currentLife > int(valueTotalLife)):
		valueTotalLife = currentLife
		concur.master["totalLife"].delete(0, END)
		concur.master["totalLife"].insert(0, str(currentLife))

	if (currentMana > int(valueTotalMana)):
		valueTotalMana = currentMana
		concur.master["totalMana"].delete(0, END)
		concur.master["totalMana"].insert(0, str(currentMana))

	currentLifePercent = (float(currentLife/int(valueTotalLife)) * 100)
	currentManaPercent = (float(currentMana/int(valueTotalMana)) * 100)

	if (currentLifePercent <= 50 and keyLife50 != " "):
		pyautogui.press(keyLife50)
	elif (currentLifePercent <= 70 and keyLife70 != " "):
		pyautogui.press(keyLife70)
	elif (currentLifePercent <= 90 and keyLife90 != " "):
		pyautogui.press(keyLife90)
	
	if (manaPercentForHeal.isdigit() == False and manaPercentForTrain.isdigit() == False):
		return

	if (manaPercentForHeal.isdigit() and currentManaPercent <= int(manaPercentForHeal) and keyPressMana != " "):
		pyautogui.press(keyPressMana)

	if (manaPercentForTrain.isdigit() and currentManaPercent > int(manaPercentForTrain) and keyPressTrainMana != " "):
		pyautogui.press(keyPressTrainMana)

def confirmIsTarget(image):
	left = pyautogui.locateAll(path + '/images/left.png', image, grayscale=True, confidence=.85)
	right = pyautogui.locateAll(path + '/images/right.png', image, grayscale=True, confidence=.85)
	top = pyautogui.locateAll(path + '/images/top.png', image, grayscale=True, confidence=.85)
	bottom = pyautogui.locateAll(path + '/images/bottom.png', image, grayscale=True, confidence=.85)
		
	if (left != None and right != None and top != None and bottom != None):
		return True

	return False

def identifyNumbers(imgLife, imgMana, vector_life, vector_mana):
	for x in range(0, 10):
		vector_life[x] =  pyautogui.locateAll(path + '/images/' + str(x) + '.png', imgLife, grayscale=True, confidence=.90)
		vector_mana[x] =  pyautogui.locateAll(path + '/images/' + str(x) + '.png', imgMana, grayscale=True, confidence=.90)

def convertNumbersToString(validIndex, vector, currentValue):
	while(validIndex):
		max = 2000
		indexRemoved = 0
		insideIndexRemove = 0
		for value in vector:
			if (vector[value] != None):
				for valueIntoItem in vector[value]:
					if (max > valueIntoItem[0]):
						indexRemoved = value
						insideIndexRemove = valueIntoItem
						max = valueIntoItem[0]
		if (insideIndexRemove != 0):
			vector[indexRemoved].remove(insideIndexRemove)
		currentValue += str(indexRemoved)
		validIndex -= 1
	return currentValue
def useSpell(spell):
	pyautogui.write(spell)
	pyautogui.press('enter')
	pyautogui.write(spell)
	pyautogui.press('enter')
	pyautogui.write(spell)
	pyautogui.press('enter')


def activeCharacter():
	direction = random.randint(0, 4)
	if (direction == 1):
		pyautogui.hotkey('ctrl', 'up')
	elif (direction == 2):
		pyautogui.hotkey('ctrl', 'right')
	elif(direction == 3):
		pyautogui.hotkey('ctrl', 'down')
	else:
		pyautogui.hotkey('ctrl', 'left')


def controller(concur):
	FLAG_TIME_ANTI_IDLE = 0
	FLAG_TIME_AUTO_SPELL = 0
	FLAG_TIME_AUTO_UTAMO = 0
	time.sleep(1)
	while (True):
		FLAG_TIME_AUTO_SPELL += 1
		FLAG_TIME_ANTI_IDLE += 1
		FLAG_TIME_AUTO_UTAMO += 1
		if (concur.paused == True):
			break
		time.sleep(0.2)
		im=pyautogui.screenshot()
		life = im
		mana = im
		food = im
		isTarget = im
		listPoints = returnListPointsBar()
		life = life.crop((int(listPoints[0]), int(listPoints[1]), int(listPoints[2]), int(listPoints[3])))
		mana = mana.crop((int(listPoints[4]), int(listPoints[5]), int(listPoints[6]), int(listPoints[7])))
		food = food.crop((int(listPoints[8]), int(listPoints[9]), int(listPoints[10]), int(listPoints[11])))
		#isTarget = isTarget.crop((int(listPoints[12]), int(listPoints[13]), int(listPoints[14]), int(listPoints[15])))
		
		screenBot = pyautogui.locateAll('images/bot.png', im, grayscale=True, confidence=.70)
		lstScreen = list(screenBot)
		if (len(lstScreen) != 0):
			continue
		vector_life = {}
		vector_mana = {}
		
		hasHungry = pyautogui.locateAll(path + '/images/food.png', food, grayscale=True, confidence=.75)
		lstHasHungry = list(hasHungry)
		hasSpeed = pyautogui.locateAll(path + '/images/speed.png', food, grayscale=True, confidence=.75)
		lstHasSpeed = list(hasSpeed)
		hasUtamo = pyautogui.locateAll(path + '/images/utamo.png', food, grayscale=True, confidence=.75)
		listHasUtamo = list(hasUtamo)
		hasUtito = pyautogui.locateAll(path + '/images/utamo.png', food, grayscale=True, confidence=.75)
		listHasUtito = list(hasUtito)
		
		identifyNumbers(life, mana, vector_life, vector_mana)
		validIndexLife = 0
		validIndexMana = 0
		lifeValue = ""
		manaValue = ""
				
		changeGeneratorToList(vector_life, vector_mana)
		
		for i in range(0, 10):
			validIndexLife += (sum(x is not None for x in vector_life[i]))
			validIndexMana += (sum(x is not None for x in vector_mana[i]))
			
		if (validIndexLife == validIndexMana and validIndexMana == 0):
			continue;
		
		mustEatFood = concur.master["eatFood"].get()
		keyPressEatFood = concur.master["keyPressFood"].get().lower()
		mustUseAutoSpell = concur.master["autoSpell"].get()
		keyAutoSpell = concur.master["keyAutoSpell"].get().lower()
		timeAutoSpell = concur.master["timeAutoSpell"].get()
		mustUseHur = concur.master["autoRun"].get()
		spellHur = concur.master["spellHur"].get().lower()
		mustUseUtamo = concur.master["autoUtamo"].get()
		keyAutoUtamo = concur.master["keyUtamoVita"].get().lower()
		mustUseUtito= concur.master["autoUtito"].get()
		keyAutoUtito = concur.master["keyUtito"].get().lower()
		isAntiIdleOn= concur.master["antiIdle"].get()
				
		lifeValue = convertNumbersToString(validIndexLife, vector_life, lifeValue)
		manaValue = convertNumbersToString(validIndexMana, vector_mana, manaValue)

		configHeal(master, int(lifeValue), int(manaValue))

		if (len(lstHasHungry) != 0 and mustEatFood):
			pyautogui.press(keyPressEatFood)

		if (len(lstHasSpeed) == 0 and mustUseHur and spellHur != " "):
			pyautogui.press(spellHur)

		if (len(listHasUtamo) == 0 and keyAutoUtamo != "" and mustUseUtamo or (190 * 5) <= (FLAG_TIME_AUTO_UTAMO)):
			pyautogui.press(keyAutoUtamo)
			FLAG_TIME_AUTO_UTAMO = 0

		elif (len(listHasUtito) == 0 and mustUseUtito and keyAutoUtito != " "):
			pyautogui.press(keyAutoUtito)

		elif (mustUseAutoSpell and keyAutoSpell != " " and timeAutoSpell * 5 <= FLAG_TIME_AUTO_SPELL):
			pyautogui.press(keyAutoSpell)
			FLAG_TIME_AUTO_SPELL = 0

		elif (isAntiIdleOn and (60 * 5) < FLAG_TIME_ANTI_IDLE):
			activeCharacter()
			FLAG_TIME_ANTI_IDLE = 0

		master.title('Tibia Bot - Running - Life: ' + str(lifeValue) + ' // Mana: ' + str(manaValue))

def popupmsg(msg):
	popup = tk.Tk()
	popup.wm_title("Warning")
	label = ttk.Label(popup, text=msg, font=("Verdana", 8))
	label.pack(side="top", fill="x", pady=10)
	B2 = ttk.Button(popup, text="Ok", command = popup.destroy)
	B2.pack()
	popup.mainloop()

def stopBot(concur, master):
	children_widgets = master.winfo_children()
	for child_widget in children_widgets:
		if child_widget.winfo_class() == 'Button':
			if (str(child_widget) == ".!button4"):
				child_widget.configure(bg="red")
			elif (str(child_widget) == ".!button3"):
				child_widget.configure(bg="green")
	master.title('TibiaBot - Stopped')
	concur.pause()

def loadConfig(a, b):
	print(a.get())
	print(b.get())
	
def startBot(concur, master):
	children_widgets = master.winfo_children()
	for child_widget in children_widgets:
		if child_widget.winfo_class() == 'Button':
			if (str(child_widget) == ".!button4"):
				child_widget.configure(bg="green")
			elif (str(child_widget) == ".!button3"):
				child_widget.configure(bg="red")
	valueTotalMana = concur.master["totalMana"].get()
	valueTotalLife = concur.master["totalLife"].get()
	
	if (valueTotalLife.isdigit() == False or valueTotalMana.isdigit() == False):
		popupmsg('Configure Total Life and Total Mana')
	else:
		concur.resume()
		master.title('TibiaBot - Running')

def confirmFieldsAreBeSeeing(master, itemsFromScreen):
	children_widgets = master.winfo_children()
	valueLife = itemsFromScreen["totalLife"].get()
	valueMana = itemsFromScreen["totalMana"].get()
	im=pyautogui.screenshot()
	life = im
	mana = im
	list = returnListPointsBar()
	life = life.crop((int(list[0]), int(list[1]), int(list[2]), int(list[3])))
	mana = mana.crop((int(list[4]), int(list[5]), int(list[6]), int(list[7])))
	vector_life = {}
	vector_mana = {}
		
	identifyNumbers(life, mana, vector_life, vector_mana)
			
	validIndexLife = 0
	validIndexMana = 0
	lifeValue = ""
	manaValue = ""
	
	changeGeneratorToList(vector_life, vector_mana)
	
	for i in range(0, 10):
		validIndexLife += (sum(x is not None for x in vector_life[i]))
		validIndexMana += (sum(x is not None for x in vector_mana[i]))

	lifeValue = convertNumbersToString(validIndexLife, vector_life, lifeValue)
	manaValue = convertNumbersToString(validIndexMana, vector_mana, manaValue)

	if (valueLife == "" or valueMana == ""):
		popupmsg('Set total life and total mana')
	if (validIndexLife != len(valueLife)):
		popupmsg('Length total life does not match with your length from life bar.\n'+
					'If your total life is right, please change your Life Bar points into config_screen.\n'+
					'Your life is ' + str(valueLife) + ' but the bot identify ' + str(lifeValue))
		return
	elif (validIndexMana != len(valueMana)):
		popupmsg('Length total mana does not match with your length from mana bar.\n'+
					'If your total mana is right, please change your Life Mana points into config_screen.\n'+
					'Your mana is ' + str(valueMana) + ' but the bot identify ' + str(manaValue))
		return
	else:
		for child_widget in children_widgets:
			if child_widget.winfo_class() == 'Button':
				if (str(child_widget) == ".!button2"):
					child_widget.configure(bg="green")
	master.title('Tibia Bot - Life: ' + str(lifeValue) + ' // Mana: ' + str(manaValue))


def configScreen():
	global shouldListener
	shouldListener = True
	listener.run()

def createSreen(concur):
	fKeys = ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 
			'F9', 'F10', 'F11', 'F12', 'HOME', 'INSERT', 'DEL')
			
	tk.Label(master, 
			 text="Total Life").grid(row = 0)
	tk.Label(master, 
			 text="Total Mana").grid(row = 1)
	tk.Label(master, 
			 text="Time(s)").grid(row=5, column = 8)

	totalLife = tk.Entry(master, width=7)
	totalMana = tk.Entry(master, width=7)
	timeAutoSpell = tk.Entry(master, width=7)
	
	totalLife.grid(row=0, column=1)
	totalMana.grid(row=1, column=1)
	timeAutoSpell.grid(row=5, column = 9)

	autoUtamo = IntVar()
	Checkbutton(master, text="Auto Utamo Vita", variable=autoUtamo).grid(row=0, column = 6, sticky=W)

	autoUtitoTempo = IntVar()
	Checkbutton(master, text="Auto Utito Tempo", variable=autoUtitoTempo).grid(row=1, column = 6, sticky=W)

	autoAntiIdle = IntVar()
	Checkbutton(master, text="Anti Idle", variable=autoAntiIdle).grid(row=2, column = 6, sticky=W)

	eatFood = IntVar()
	Checkbutton(master, text="Eat Food", variable=eatFood).grid(row=3, column = 6, sticky=W)
	
	autoRun = IntVar()
	Checkbutton(master, text="Auto Run", variable=autoRun).grid(row=4, column = 6, sticky=W)

	autoSpell = IntVar()
	Checkbutton(master, text="Auto Spell", variable=autoSpell).grid(row=5, column = 6, sticky=W)

	textUtamoVita = StringVar()
	keyUtamoVita = ttk.Combobox(master, width = 6, textvariable = textUtamoVita)

	keyUtamoVita['values'] = fKeys
	  
	keyUtamoVita.grid(row = 0, column = 7, sticky=W) 
	keyUtamoVita.current()	

	textUtitoTempo = StringVar()
	keyUtitoTempo = ttk.Combobox(master, width = 6, textvariable = textUtitoTempo)

	keyUtitoTempo['values'] = fKeys
	  
	keyUtitoTempo.grid(row = 1, column = 7, sticky=W) 
	keyUtitoTempo.current()

	textHur = StringVar()
	keyPressRun = ttk.Combobox(master, width = 6, textvariable = textHur)

	keyPressRun['values'] = fKeys
	  
	keyPressRun.grid(row = 4, column = 7, sticky=W) 
	keyPressRun.current()	
	
	boxAutoSpell = StringVar()
	keyAutoSpell = ttk.Combobox(master, width = 6, textvariable = boxAutoSpell)
	
	keyAutoSpell['values'] = fKeys 
	  
	keyAutoSpell.grid(row = 5, column = 7, sticky=W) 
	keyAutoSpell.current() 

	keyPressFood = StringVar()
	keyChoosen = ttk.Combobox(master, width = 6, textvariable = keyPressFood)
	
	keyChoosen['values'] = fKeys
	  
	keyChoosen.grid(row = 3, column = 7, sticky=W) 
	keyChoosen.current()

	tk.Label(master, 
			text="Life 90%").grid(row = 3)
			
	keyPressCure90 = StringVar()
	keyChoosenCure90 = ttk.Combobox(master, width = 6, textvariable = keyPressCure90)
	
	keyChoosenCure90['values'] = fKeys
	  
	keyChoosenCure90.grid(row = 3, column = 1, sticky=W) 
	keyChoosenCure90.current()
	
	tk.Label(master, 
			text="Life 70%").grid(row = 4, column = 0)
			
	keyPressCure70 = StringVar()
	keyChoosenCure70 = ttk.Combobox(master, width = 6, textvariable = keyPressCure70) 

	keyChoosenCure70['values'] = fKeys
	  
	keyChoosenCure70.grid(row = 4, column = 1, sticky=W) 
	keyChoosenCure70.current()

	tk.Label(master, 
			text="Life 50%").grid(row = 5, column = 0)
			
	keyPressCure50 = StringVar()
	keyChoosenCure50 = ttk.Combobox(master, width = 6, textvariable = keyPressCure50) 

	keyChoosenCure50['values'] =  fKeys
	  
	keyChoosenCure50.grid(row = 5, column = 1, sticky=W) 
	keyChoosenCure50.current()
	
	tk.Label(master, 
		text="When Mana <").grid(row = 6, column = 0, sticky=W)
	
	manaPercent = tk.Entry(master, width=6)	
	manaPercent.grid(row=6, column=1, sticky=W)
	
	tk.Label(master, 
		text="% use").grid(row = 6, column = 2, sticky=W)	
	keyPressCureMana = StringVar()
	keyPressCureMana = ttk.Combobox(master, width = 6, textvariable = keyPressCureMana) 
	  
	keyPressCureMana['values'] =  fKeys
	  
	keyPressCureMana.grid(row = 6, column = 3) 
	keyPressCureMana.current()

	tk.Label(master, 
		text="When Mana >").grid(row = 7, column = 0, sticky=W)
	
	manaPercentForTrain = tk.Entry(master, width=6)	
	manaPercentForTrain.grid(row=7, column=1, sticky=W)
	
	tk.Label(master, 
		text="% use").grid(row = 7, column = 2, sticky=E)	
	keyPressTrainMana = StringVar()
	keyPressTrainMana = ttk.Combobox(master, width = 6, textvariable = keyPressTrainMana) 
	  
	keyPressTrainMana['values'] =  fKeys
	  
	keyPressTrainMana.grid(row = 7, column = 3) 
	keyPressTrainMana.current()
			
	itemsFromScreen = {
		"keyPressCure90": keyChoosenCure90,
		"keyPressCure70": keyChoosenCure70,
		"keyPressCure50": keyChoosenCure50,
		"manaPercent": manaPercent,
		"manaPercentForTrain": manaPercentForTrain, 
		"keyPressCureMana": keyPressCureMana,
		"keyPressTrainMana": keyPressTrainMana,
		"eatFood": eatFood,
		"keyPressFood": keyPressFood,
		"totalLife": totalLife,
		"totalMana": totalMana,
		"autoRun": autoRun,
		"spellHur": keyPressRun,
		"autoSpell": boxAutoSpell,
		"keyAutoSpell": keyAutoSpell,
		"timeAutoSpell": timeAutoSpell,
		"autoUtamo": autoUtamo,
		"keyUtamoVita": keyUtamoVita,
		"autoUtito": autoUtitoTempo,
		"keyUtito": keyUtitoTempo,
		"antiIdle": autoAntiIdle
	}

	concur.setMaster(itemsFromScreen)

	tk.Button(master, 
			  text='Config Screen',
			  activebackground='green',
			  command=lambda: configScreen()).grid(row=0, 
										column=4, 
										sticky=W, 
										pady=4)
	tk.Button(master, 
			  text='Check Config Screen',
			  bg='red',
			  command = lambda: confirmFieldsAreBeSeeing(master, itemsFromScreen)).grid(row=0, 
										column=3, 
										sticky=E, 
										pady=4,
										padx=4)

	tk.Button(master, 
			  text='Stop', command = lambda: stopBot(concur, master)).grid(row=8, 
														   column=2, 
														   sticky=tk.W, 
														   pady=4)

	tk.Button(master, 
			  text='Start', command = lambda: startBot(concur, master)).grid(row=8, 
														   column=1, 
														   sticky=tk.W, 
														   pady=4)


if __name__ == '__main__':
	firstTime = True
	master = tk.Tk()
	master.geometry("720x270")
	master.resizable(False, False)
	master.title('TibiaBot - Stopped')

	concur = Concur()
	createSreen(concur)
	concur.start()
	concur.pause()


	tk.mainloop()
	