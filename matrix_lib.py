#!/usr/bin/python
#matrix_libs.py
###USAGE### matrix_libs.py ; sms=N ; $#=0
import math
import prgm_lib
getchar=prgm_lib.getch
cls=prgm_lib.cls

def dot_product(v1, v2):
	ans = 0
	for x in range(len(v1)):
		ans += v1[x]*v2[x]
	return ans	
	
def nth_column(n, matrix):
	rows = len(matrix)
	col = []
	for r in range(rows):
		col.append(matrix[r][n])
	return col

def matrix_multiply(left, right):
	output = []
	for row in left:
		newrow = []
		for col in range(len(row)):
			rcol = nth_column(col, right)
			newrow.append(dot_product(row, rcol))
		output.append(newrow)
	return output
	
def scalar_multiple(matrix, const):
	for r in range(len(matrix)):
		for c in range(len(matrix[r])):
			matrix[r][c] = matrix[r][c] * const
	return matrix
	
def matrix_addition(left, right):
	output = []
	for r in range(len(left)):
		newrow = []
		for c in range(len(left[r])):
			newrow.append(left[r][c] + right[r][c])
		output.append(newrow)
	return output

def try_get_value(replace, p_key):
	if p_key in replace.keys():
		return replace[p_key]
	else:
		return p_key

###output a 2D-matrix###
def opg(matrix,pad=' ',replace={}):
	for r in range(len(matrix)):
		line = ''
		for c in range(len(matrix[r])):
			line = line + str(try_get_value(replace, str(matrix[r][c]))) + pad
		print line

def read_in_grid_p(xval,yval,return_str=True):
	mtrx=[]
	temp_l=[]
	str1=''
	for y in range(yval):
		temp_l=[]
		for x in range(xval):
			print 'What is the value of the grid at ('+str(x)+','+str(y)+')? (1-part of board, 0-otherwise)'
			new=raw_input()
			str1=str1+str(new)
			temp_l.append(new)			
		mtrx.append(temp_l)
	if return_str:
		return str1
	else:
		return mtrx

def read_in_grid_i(xval,yval,return_str=True,one_char=True):
	mtrx=[]
	temp_l=[]
	strings=[]
	str1=''
#	iter0=range(yval)
	y=0
	x=0
	while y<yval:
#		iter1=range(xval)
		fail=0
		while x<xval:
			cls()
			print 'Grid entering mode. the \'_\' is the position that you are currently entering.'
			print 'If you make a mistake, press \'b\' to go back.'
			if strings!=[]:
				for str0 in strings:
					print str0
			print str1 + '_'
			if one_char:
				new_ch=getchar()
			else:
				new_ch=raw_input()
			if (new_ch=='b' or new_ch=='B') and (not (x==0 and y==0)):
				str1=str1[:-1]
				temp_l=temp_l[:-1]
				x=x-1
			else:
				str1=str1+new_ch
				temp_l.append(new_ch)
				x=x+1
			if x==-1:
				x=xval+1
				y=y-1
				fail=1
		if fail==0:
			strings.append(str1)
			mtrx.append(temp_l)
			temp_l=[]
			str1=''
			y=y+1
			x=0
		else:
			temp_l=mtrx.pop()
			temp_l.pop()
			str1=strings.pop()
			str1=str1[:-1]
			x=xval-1
	one_string=''
	for str0 in strings:
		one_string=one_string+str0
	if return_str:
		return one_string
	else:
		return mtrx


def init_grid(x0,y0,fill):
	matrix=[]
	temp_l=[]
	for y in range(y0):
		for x in range(x0):
			temp_l.append(fill)
		matrix.append(temp_l)
		temp_l=[]
	return matrix

def coor_split(num,xmax):
	x1=int(num) % xmax
	y1=int(num) / xmax
	return [x1,y1]

def coor_splice(x,y,xmax):
	if (x >= xmax) or (x < 0):
		return -1
	else:
		return y*xmax + x

def contiguous_subset_p(pos0,xmax,others,no_diags=True):
	connections=[]
#	pos0=coor_splice(x0,y0,xmax)
	change=0
	for k in range(len(others)):
		pos1=others[k]
		if is_adjacent(pos0,pos1,xmax,no_diags):
			connections.append(1)
			change=change+1
		else:
			connections.append(0)
	if change==0:
		return connections
	else:
		current=0
		while change!=0:
			current=current+1
			change=0
			for c in range(len(others)):
				t=connections[c]
				if t==current:
					pos1=others[c]
					for k in range(len(others)):
						cr=others[k]
						if is_adjacent(pos1,cr,xmax,no_diags) and connections[k]==0:
							connections[k]=current+1
							change=change+1
	return connections

def contiguous_subset_c(x0,y0,xmax,others,no_diags=True):
	connections=[]
	pos0=coor_splice(x0,y0,xmax)
	change=0
	for k in range(len(others)):
		cr=others[k]
		if is_adjacent(pos0,coor_splice(cr[0],cr[1],xmax),xmax,no_diags):
			connections.append(1)
			change=change+1
		else:
			connections.append(0)
	if change==0:
		return connections
	else:
		current=0
		while change!=0:
			current=current+1
			change=0
			for c in range(len(others)):
				t=connections[c]
				if t==current:
					pos1=coor_splice(others[c][0],others[c][1],xmax)
					for k in range(len(others)):
						cr=others[k]
						if is_adjacent(pos1,coor_splice(cr[0],cr[1],xmax),xmax,no_diags) and connections[k]==0:
							connections[k]=current+1
							change=change+1
	return connections

def sep_cs(all_pos,xmax,no_diags=True):
	pos0=all_pos[0]
	rest=all_pos[1:]
	c_list=contiguous_subset_p(pos0,xmax,rest,no_diags)
	temp_lst=[]
	temp_lst.append(pos0)
	re_do=[]
	subsets=[]
	for k in range(len(c_list)):
		con=c_list[k]
		if con!=0:
			temp_lst.append(rest[k])
		else:
			re_do.append(rest[k])
	subsets.append(temp_lst)
	if re_do!=[]:
		new_list=sep_cs(re_do,xmax,no_diags)
		subsets=subsets+new_list
	return subsets

def is_adjacent(a,b,gridx=4,strict=False,dx=-7,dy=-7):
	x1=int(a) % gridx
	y1=int(a) / gridx
	x2=int(b) % gridx
	y2=int(b) / gridx
	if strict==False:
		if (abs(x2-x1) <= 1) and (abs(y2-y1) <= 1) and (a!=b):
			return True
		else:
			return False
	if strict==True:
		if (dx==-7) and (dy==-7):
			if (abs(x2-x1) <= 1) and (abs(y2-y1) <= 1) and (a!=b) and (abs(x2-x1) + abs(y2-y1) < 2):
				return True
			else:
				return False
		else:
			if (abs(x2-x1)==dx) and (abs(y2-y1)==dy):
				return True
			else:
				return False

###row operations needed for solving the system of equations###
def row_ops(matrix, flag, col, row1, row2=-1):
	c=0
	if flag==1:
		val1=matrix[row1][row1]
		while (c<col):
			matrix[row1][c]=matrix[row1][c] / val1
			c=c+1			
	else:
		val1=matrix[row2][row1]
		while (c<col):
			matrix[row2][c]=math.fsum([matrix[row2][c], -1*(val1 * matrix[row1][c])])
			c=c+1
	return matrix

###main algorithm for solving the system of equations###
def soles(matrix, cols, rows):
	q=0
	while (q<rows):
		matrix=row_ops(matrix, 1, cols, q)
		qq=0
		while (qq<rows):
			if (qq!=q):
				matrix=row_ops(matrix, 2, cols, q, qq)
			qq=qq+1
#			print
#			print q,qq
#			opg(matrix)
		q=q+1
	return matrix
