#!/usr/bin/python
#level_editor_3d.py
###USAGE### level_editor.py -f <file_name> [-e]; sms=N ; $#=1
import sys
import PythonLibraries.matrix_lib as matrix_lib
import PythonLibraries.prgm_lib as prgm_lib
try_get_value = matrix_lib.try_get_value
import xml.etree.ElementTree as ET
re_mk=prgm_lib.flag_re_mk

BACKGROUND = 0
FOREGROUND = 1
MAX_COLS = 50
MAX_ROWS = 20

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def get_row_range(num_rows,row_pos):
	if num_rows <= MAX_ROWS:
		return range(num_rows)
	else:
		if row_pos >= (num_rows - MAX_ROWS):
			 return range(num_rows - MAX_ROWS, num_rows)
		else:
			return range(row_pos, row_pos + MAX_ROWS)
			
def get_col_range(num_cols,col_pos):
	if num_cols <= MAX_COLS:
		return range(num_cols)
	else:
		if col_pos >= (num_cols - MAX_COLS):
			 return range(num_cols - MAX_COLS, num_cols)
		else:
			return range(col_pos, col_pos + MAX_COLS)

def opg_underline(matrix,pad=' ',replace={}, xpos = -1, ypos = -1, layer = 1):
	matrix = matrix[layer]
	mod = ''
	if layer == 0:
		mod = bcolors.BLUE
	for r in get_row_range(len(matrix),ypos):
		line = ''
		for c in get_col_range(len(matrix[r]),xpos):
			if ypos == r and xpos == c:
				line = line + mod + bcolors.UNDERLINE + str(try_get_value(replace, str(matrix[r][c]))) + bcolors.ENDC + mod + pad + bcolors.ENDC
			else:
				line = line + mod + str(try_get_value(replace, str(matrix[r][c]))) + pad + bcolors.ENDC
		print line
	row_range = get_row_range(len(matrix),ypos)
	col_range = get_col_range(len(matrix[0]),xpos)
	print "Showing rows " + str(row_range[0]) + " to " + str(row_range[-1]) + " of " + str(len(matrix))
	print "Showing cols " + str(col_range[0]) + " to " + str(col_range[-1]) + " of " + str(len(matrix[0]))
	
def make_reverse_dict(in_dict):
	out_dict = {}
	for key in in_dict.keys():
		out_dict[in_dict[key]] = key
	return out_dict
	
class WorldObject:
	def __init__(self,name,xpos,ypos):
		self.x = xpos
		self.typename = name
		self.y = ypos
		
	def get_name(self):
		return self.typename
		
	def get_x(self):
		return self.x
		
	def get_y(self):
		return self.y

	
def level_xml_import(file_name, default = "  "):
	tree = ET.parse(file_name)
	root = tree.getroot()	# XnaContent
	asset = root[0]
	object_list = []
	for item in asset:
		name = item.find('type').text
		x = int(item.find('xPosition').text)
		y = int(item.find('yPosition').text)
		object_list += [WorldObject(name,x,y)]
	xmax = 0
	ymax = 0
	for obj in object_list:
		if obj.get_x() > xmax:
			xmax = obj.get_x()
		if obj.get_y() > ymax:
			ymax = obj.get_y()
	foreground = matrix_lib.init_grid(xmax+1,ymax+1,default)
	background = matrix_lib.init_grid(xmax+1,ymax+1,default)
	for obj in object_list:
		if obj.get_name() in background_objects:
			background[obj.get_y()][obj.get_x()] = obj.get_name()
		else:
			foreground[obj.get_y()][obj.get_x()] = obj.get_name()
	return [background, foreground]
			

def level_xml_export(matrix, file_name, default = "  "):
	indent = "  "
	FILE = open(file_name, 'w')
	FILE.write("<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n")
	FILE.write("<XnaContent>\n")
	FILE.write("  <Asset Type=\"WorldObjectLibrary.WorldObject[]\">\n")
	for layer in range(len(matrix)):
		for y in range(len(matrix[layer])):
			for x in range(len(matrix[layer][y])):
				if matrix[layer][y][x] != default:
					FILE.write(indent * 2 + "<Item>\n")
					FILE.write(indent * 3 + "<type>" + matrix[layer][y][x] + "</type>\n")
					FILE.write(indent * 3 + "<xPosition>" + str(x) + "</xPosition>\n")
					FILE.write(indent * 3 + "<yPosition>" + str(y) + "</yPosition>\n")
					FILE.write(indent * 2 + "</Item>\n")
	FILE.write("  </Asset>\n")
	FILE.write("</XnaContent>\n")	
	FILE.close()

def level_replace(matrix, replace):
	for layer in range(len(matrix)):
		for y in range(len(matrix[layer])):
			for x in range(len(matrix[layer][y])):
				if matrix[layer][y][x] in replace.keys():
					matrix[layer][y][x] = replace[matrix[layer][y][x]]
	return matrix

def level_edit(matrix, default = "  "):
	xpos = 0
	ypos = 0
	layer = 1
	num_layers = 2
	y_length = len(matrix[BACKGROUND])
	x_length = len(matrix[BACKGROUND][0])
	ch = ''
	arrow = 0
	while ch != 'q':
		prgm_lib.cls()
		print "Below, is the level so far."
		print "press 'q' to quit level editing."
		print "use the arrow keys to traverse the level."
		print "press enter to edit a cell."
		print "press 'a' or 'd' to add or delete rows or columns."
		print "press 'b' or 'f' to switch to the background or foreground."
		print "\nactive layer: (" + str(xpos) + "," + str(ypos) + ") (col,row)"
		opg_underline(matrix, ',',{}, xpos, ypos, layer)
		print "other layer:"
		opg_underline(matrix, ',',{}, xpos, ypos, (layer + 1) % 2)
		if ch == '':
			ch = prgm_lib.getch()
		if ch == '\x1b':
			ch = prgm_lib.getch()
			if ch == '[':
				ch = prgm_lib.getch()
				if ch == 'A':	#up arrow
					arrow = 1
				elif ch == 'B':	#down arrow
					arrow = 2
				elif ch == 'D':	#left arrow
					arrow = 3
				elif ch == 'C':	#right arrow
					arrow = 4
				else:
					arrow = 0
				ch = ''
			elif ch == '\x1b':
				pass
			else:
				ch = ''
		elif ch == '\n' or ch == '\r':
			print "please type what should go into this box of the matrix."
			val = prgm_lib.get_str()
			matrix[layer][ypos][xpos] = val
			ch = ''
		elif ch == 'q' or ch == '\x1b':
			pass
		elif ch == 'd':
			print "delete key pressed. do you wish to delete a 'r'ow or 'c'olumn?"
			ch = prgm_lib.getch()
			if ch == 'r':
				if y_length > 1:
					matrix[BACKGROUND] = matrix[BACKGROUND][0:ypos] + matrix[BACKGROUND][ypos+1:]
					matrix[FOREGROUND] = matrix[FOREGROUND][0:ypos] + matrix[FOREGROUND][ypos+1:]
					y_length -= 1
					if ypos > y_length - 1:
						ypos = y_length - 1
				else:
					print "you cannot delete the only row!!"
			elif ch == 'c':
				if x_length > 1:
					for y in range(len(matrix[BACKGROUND])):
						matrix[BACKGROUND][y] = matrix[BACKGROUND][y][0:xpos] + matrix[BACKGROUND][y][xpos+1:]
						matrix[FOREGROUND][y] = matrix[FOREGROUND][y][0:xpos] + matrix[FOREGROUND][y][xpos+1:]
					x_length -= 1
					if xpos > x_length - 1:
						xpos = x_length - 1
				else:
					print "you cannot delete the only column!!"
			else:
				ch = ''
		elif ch == 'a':
			print "add key pressed. do you wish to add a 'r'ow or 'c'olumn?"
			ch = prgm_lib.getch()
			if ch == 'r':
				row1 = [default for x in range(len(matrix[BACKGROUND][0]))]
				row2 = [default for x in range(len(matrix[BACKGROUND][0]))]
				matrix[BACKGROUND] = matrix[BACKGROUND][0:ypos+1] + [row1] + matrix[BACKGROUND][ypos+1:]
				matrix[FOREGROUND] = matrix[FOREGROUND][0:ypos+1] + [row2] + matrix[FOREGROUND][ypos+1:]
				y_length += 1
			elif ch == 'c':
				for y in range(len(matrix[BACKGROUND])):
					matrix[BACKGROUND][y] = matrix[BACKGROUND][y][0:xpos+1] + [default] + matrix[BACKGROUND][y][xpos+1:]
					matrix[FOREGROUND][y] = matrix[FOREGROUND][y][0:xpos+1] + [default] + matrix[FOREGROUND][y][xpos+1:]
				x_length += 1
			else:
				ch = ''
		elif ch == 'f':
			layer = FOREGROUND
			ch = ''
		elif ch == 'b':
			layer = BACKGROUND
			ch = ''
		else:
			ch = ''

		if arrow == 1:		#up arrow
			if ypos > 0:
				ypos -= 1
			else:
				row1 = [default for x in range(len(matrix[BACKGROUND][0]))]
				row2 = [default for x in range(len(matrix[BACKGROUND][0]))]
				matrix[BACKGROUND] = [row1] + matrix[BACKGROUND]
				matrix[FOREGROUND] = [row2] + matrix[FOREGROUND]
				y_length += 1
		elif arrow == 2:	#down arrow
			if ypos < y_length - 1:
				ypos += 1
			else:
				row1 = [default for x in range(len(matrix[BACKGROUND][0]))]
				row2 = [default for x in range(len(matrix[BACKGROUND][0]))]
				matrix[BACKGROUND] = matrix[BACKGROUND] + [row1]
				matrix[FOREGROUND] = matrix[FOREGROUND] + [row2]
				y_length += 1
				ypos += 1
		elif arrow == 3:	#left arrow
			if xpos > 0:
				xpos -= 1
			else:
				for x in range(len(matrix[BACKGROUND])):
					matrix[BACKGROUND][x] = [default] + matrix[BACKGROUND][x]
					matrix[FOREGROUND][x] = [default] + matrix[FOREGROUND][x]
				x_length += 1
		elif arrow == 4:	#right arrow
			if xpos < x_length - 1:
				xpos += 1
			else:
				for x in range(len(matrix[BACKGROUND])):
					matrix[BACKGROUND][x] = matrix[BACKGROUND][x] + [default]
					matrix[FOREGROUND][x] = matrix[FOREGROUND][x] + [default]
				x_length += 1
				xpos += 1
		arrow = 0
	return matrix
		
mario_mappings = {"up":"UpwardGreenPipe", "mm":"Mario", "ci":"CoinItem", "fi":"FireFlowerItem", "mi":"MushroomItem", "oi":"OneUpItem", "si":"StarItem", "ge":"Goomba", "ke":"Koopa", "bb":"BrickBlock", "fb":"FloorBlock", "hb":"HiddenBlock", "qb":"QuestionBlock", "wb":"WallBlock", "tt":"TripleTree", "st":"SingleTree", "tc":"TripleCloud", "sc":"SingleCloud", "bh":"BigHill", "sh":"SmallHill", "sp":"UpwardGreenSectionPipe", "MQ":"MushroomQuestionBlock", "OH":"OneUpHiddenBlock", "CB":"CoinBrickBlock", "SH":"StarHiddenBlock", "lp":"LeftGreenPipe", "ff":"Flagpole"}

background_objects = ["tt", "TripleTree", "st", "SingleTree", "tc", "TripleCloud", "sc", "SingleCloud", "bh", "BigHill", "sh", "SmallHill"]

arg_nums = [1,0]
regexs = [re_mk('file'),re_mk('edit')]			
o_args = prgm_lib.arg_flag_ordering(sys.argv,arg_nums,regexs)
xml_file = ''
edit = False

if str(o_args[0]) != "None":
	xml_file = str(o_args[0])
else:
	print "Please pass a file_name to export to."
	raise SystemExit
if str(o_args[1]) != "None":
	edit = True
	
if edit:
	level = level_xml_import(xml_file)
	level = level_replace(level, make_reverse_dict(mario_mappings))
else:
	level = [[["  "]],[["  "]]]
level = level_edit(level)
level = level_replace(level, mario_mappings)
level_xml_export(level, xml_file)



