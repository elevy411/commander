import csv
from time import sleep

home = Cell(1,1)
masterControl = True
coreCategories = ['Creature','Sorcery','Instant','Artifact','Enchantment','Planeswalker','Land','Total']
categories = list(coreCategories)
colors = 'aqua black blue fuchsia gray green lime maroon navy olive purple red silver teal white yellow'.upper().split(' ')

class button:
  def __init__(self,name,(x,y),cellColor,color='Black',func=None):
    self.name = Cell(x,y).name
    self.location = (x,y)
    self.function = func
    temp = Cell(x,y)
    temp.value = name
    temp.copy_format_from(Cell("A1"))  
    temp.font.bold = True
    temp.font.color = color
    if cellColor != 'None':
      temp.color = cellColor
    active_cell(home)
  def addFunction(self,func):
  	self.function = func

def hello():
	print 'Hello World!\n'
	active_cell(home)
	af()

def resetCounts():
	global categories
	for cell in Cell('O8').vertical_range:
		row = cell.row
		ref = Cell('P{}'.format(row))
		ref.value = 0

def resetCategories():
	global categories,coreCategories
	for cell in Cell('O8').vertical_range:
		row = cell.row
		sec = Cell('P{}'.format(row))
		cell.clear()
		sec.clear()
	categories = list(coreCategories)
	makeCategories()
	recount()

deckDic = {}
def updateDic(cell,valToAdd = None, value = True):
	global deckDic
	if cell.value not in deckDic.values() and cell.value != None:
		deckDic[cell.value] = {}
		deckDic[cell.value]['Count'] = 1
	if valToAdd != None:
		deckDic[cell.value][valToAdd] = value	

def printDic():
	global deckDic
	for key in deckDic:
		print 'deckDic[{}] :'.format(key)
		for key2 in deckDic[key]:
			print '[{}] = {}'.format(key2,deckDic[key][key2])
	active_cell(home)

def toTxtFile():
	global deckDic
	textFile = open('{}.txt'.format(active_sheet()),'w')
	listToWriteFrom = []
	for key in deckDic:
		hashList = ''
		for key2 in deckDic[key]:
			if key2 != 'Count':
				hashList += '#{} '.format(key2)
		formattedString = '{} {}\n'.format(key,hashList)
		listToWriteFrom.append(formattedString)
	for x in sorted(listToWriteFrom):
		textFile.write("1 {}".format(x))
	textFile.close()
	active_cell(home)

def recount():
	global categories,deckDic
	resetCounts()
	for letter in 'ABCDEFGHIJKL':
		for cell in Cell('{}6'.format(letter)).vertical_range:
			refRow = 8
			i = 0
			updateDic(cell)
			while i < len(categories):
				refCell = Cell('O{}'.format(refRow))
				countCell = Cell('P{}'.format(refRow))
				if cell.color == refCell.color:
					countCell.value = countCell.value + 1
					updateDic(cell,refCell.value)
					updateDic(cell,Cell('{}5'.format(letter)).value)
				if refCell.value == 'Total':
					countCell.value = len(deckDic)
				refRow += 1
				i += 1
		refRow = 8
	active_cell(home)
	af()

def clean():
	global masterControl,deckDic
	deckDic = {}
	clear_sheet()
	makeStage()
	active_cell(home)

def stop(): 
	global masterControl
	masterControl = False
	sleep(0.5)
	active_cell(home)

''' Make the Buttons'''
cells = []
def makeButtons():
	global cells
	recountCell = button('Recount',(1,3),'Green')
	cleanCell = button("Clean",(1,4),'Red')
	stopCell = button("Stop",(1,5),'Yellow')
	addCategoryCell = button("AddCategory",(1,6),"Aqua")
	resetCategoriesCell = button("ResetCategories",(1,7),"Red")
	toTxtFileCell = button("ToTxtFile",(1,8),"Green")

	cells.append(recountCell)
	cells.append(cleanCell)
	cells.append(stopCell)
	cells.append(addCategoryCell)
	cells.append(resetCategoriesCell)
	cells.append(toTxtFileCell)

	recountCell.addFunction(recount)
	cleanCell.addFunction(clean)
	stopCell.addFunction(stop)
	addCategoryCell.addFunction(addCategory)
	resetCategoriesCell.addFunction(resetCategories)
	toTxtFileCell.addFunction(toTxtFile)

	# comment this out in hidden
	printDicCell = button("PrintDic",(1,9),"Yellow")
	cells.append(printDicCell)
	printDicCell.addFunction(printDic)


''''''

def format(cell,color=None,alignment=None,font=None):
	cell.font.bold = True
	cell.font.color = 'Black'
	if color != None:
		cell.color = color
	if alignment != None:
		cell.alignment = alignment
	if font != None:
		cell.font.color = font

def makeCmc():
	tableStart = 'ABCDEFGHIJKL'
	row = 5
	for i,letter in enumerate(tableStart):
		ref = Cell('{}{}'.format(letter,row)) 
		if letter != 'L':
			ref.value = 'CMC{}'.format(i)
		else:
			ref.value = 'CMC 11+ or X'
		format(ref,'Black','center','white')		

def makeTable(): 
	tableStart = 'NOPQR'
	x = 5
	while x <= 38:
		if x == 5 or x == 38:
			for letter in tableStart:
				Cell('{}{}'.format(letter,x)).color = 'Yellow'
		else:
			rest = 'NR'
			for letter in rest:
				Cell('{}{}'.format(letter,x)).color = 'Yellow'
		x += 1

	Cell('O6').value = 'Category'
	Cell('P6').value = 'Count'
	
	merge_range(CellRange("O5:Q5"))
	Cell('O5').value = 'Stats Table'
	
	format(Cell('O5'),'black','center','white')
	
	format(Cell('O6'))
	format(Cell('P6'))
	active_cell(home)


def makeCategories():
	global categories,colors
	row = 8
	for cat in categories:
		ref = Cell('O{}'.format(row)) 
		ref.value = cat
		if cat != 'Total':
			format(ref,colors[row-8],'left','white')
		else:
			format(ref,1060,'left','white')
		row += 1
	resetCounts()
	af()
	active_cell(home)

def addCategory():
	global categories
	Cell('F2').value = "Insert Category in Cell G2 -->"
	Cell('F3').value = "Then Press Enter!"
	active_cell('G2')
	af()
	done = False
	count = 0
	while not done:
		if active_cell() == Cell('G3'):
			done = True
			if not Cell('G2').is_empty():
				categories[len(categories)-1]=Cell('G2').value
				categories.append('Total')
				Cell('F2').clear()
				Cell('F3').clear()
				Cell('G2').clear()
				makeCategories()
		count += 1
		if count > 100000:
			done = True
			Cell('F2').clear()
			Cell('F3').clear()
			Cell('G2').clear()
			makeCategories()

def makeStage():
	clear_sheet()
	home.value = 'Running'
	makeButtons()
	makeTable()
	makeCmc()
	makeCategories()
	af()

def af():
	autofit()

def main():
	global masterControl,cells
	masterControl = True
	makeStage()
	while masterControl:
		for cell in cells: 
			if cell.name == active_cell().name:
				cell.function()
	home.clear()
	active_cell(home)

if __name__ == '__main__':
	main()