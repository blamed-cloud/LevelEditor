#!/usr/bin/python
#prgm_lib.py
###USAGE### prgm_lib.py ; sms=N ; $#=0
import re

def memo(f):
    "Memoize function f."
    table = {}
    def fmemo(*args):
        if args not in table:
            table[args] = f(*args)
        return table[args]
    fmemo.memo = table
    return fmemo

def reverse(data):
	for index in range(len(data)-1, -1, -1):
		yield data[index]

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def get_keypress():
	pass

def get_int(quiet=False):
	unf=True
	while unf:
		if not quiet:
			print 'Enter an integer: ',
		response=raw_input()
		char_lst=[l for l in str(response)]
		fail=0
		if len(char_lst) != 0:
			if char_lst[0]=='-':
				char_lst=char_lst[1:]
			for l in char_lst:
				if not re.search('[0123456789]',l,re.I):
					fail=1
					if not quiet:
						print 'That was not an integer. Please try again.'
					break
			if fail==0:
				unf=False
	return int(response)
	
def get_int_escape_codes(escape_codes, quiet=False):
	unf=True
	while unf:
		if not quiet:
			print 'Enter an integer: ',
		response=raw_input()
		if response in escape_codes:
			return response
		char_lst=[l for l in str(response)]
		if len(char_lst) != 0:
			fail=0
			if char_lst[0]=='-':
				char_lst=char_lst[1:]
			for l in char_lst:
				if not re.search('[0123456789]',l,re.I):
					fail=1
					if not quiet:
						print 'That was not an integer. Please try again.'
					break
			if fail==0:
				unf=False
	return int(response)

def get_num(quiet=False):
	unf=True
	while unf:
		if not quiet:
			print 'Enter a number: ',
		response=raw_input()
		char_lst=[l for l in str(response)]
		fail=0
		decimal=0
		if char_lst[0]=='-':
			char_lst=char_lst[1:]
		for l in char_lst:
			if not re.search('[0123456789]',l,re.I):
				if (l!='.') or (l=='.' and decimal==1):
					fail=1
					if not quiet:
						print 'That was not a valid number. Please try again.'
					break
				elif (l=='.') and (decimal==0):
					decimal=1
		if fail==0:
			unf=False
	return response
	
def get_poly(deg=-1,name='the polynomial'):
	if deg==-1:
		print 'what is the degree of ' + name + '?'
		n=int(get_int())
	else:
		n=deg
	print 'what is the coefficient of ' + name + ' for the...'
	coefs=[]
	for c in range(n+1):
		print 'x^' + str(c) + ' term?'
		coefs.append(float(get_num()))
	return coefs

def get_str(disallowed_chars=['\\'],quiet=False):
	unf=True
	while unf:
		if not quiet:
			print 'Please enter a string that doesn\'t contain any disallowed characters:'
		response=str(raw_input())
		char_lst=[l for l in response]
		fail=False
		for l in char_lst:
			if l in disallowed_chars:
				if not quiet:
					print 'I\'m sorry, but you are not allowed to use the char \'' + l + '\''
				fail=True
				break
		if not fail:
			unf=False
	return response
	
def get_allowed_str(allowed_chars,quiet=False):
	unf = True
	while unf:
		if not quiet:
			print "Please enter a string consisting only of allowed characters:"
		response=str(raw_input())
		char_lst=[l for l in response]
		fail=False
		for l in char_lst:
			if l not in allowed_chars:
				if not quiet:
					print "I\'m sorry, but you are not allowed to use the char \'" + l + "\'"
				fail=True
				break
		if not fail:
			unf=False
	return response

def get_t_f(quiet=False):
	unf=True
	while unf:
		if not quiet:
			print 'Please enter either \'True\' or \'False\':'
		response=str(raw_input())
#		char_lst=[l for l in response]
		if re.search('^[t](rue)?$|^[y](es)?$',response,re.I):
			return True
		elif re.search('^[f](alse)?$|^[n](o)?$',response,re.I):
			return False

def unzip(lst):
	string=unzip2(lst)
	new_lst=re.split('_SEP_',string)
	return new_lst[:-1]

def unzip2(lst):
	string=''
	for k in lst:
		if type(k) is list:
			string=string+unzip2(k)
		else:
			string=string+str(k)+'_SEP_'
	return string

def cls(size = 50):
	for x in range(size):
		print

#'^[-]{1,2}[b](oggle)?$'
#'^[-]{1,2}(boggle)$|^[-]{1,2}[q]$'

def flag_re_mk(word,dsf=False,dfl='q'):
	if dsf==False:
		fl=word[0]
		rw=word[1:]
		str1='^[-]{1,2}[' + str(fl) + '](' + str(rw)+')?$'
		return str1
	else:
		str1='^[-]{1,2}(' + str(word)+')?$|^[-]{1,2}[' + str(dfl) + ']$'
		return str1


### The flag_re's shouldn't care whether or not they are actually flags, so you should be able to just pass RE-distinct args by using 0-argc with the regexp for the arg... ###
def arg_flag_ordering(args,flag_argc,flag_re,overwrite=False,unziped_args=False,start_at_zero=False):
	nap=0
	used=[]
	new_args=[]
	unproc_ed=[]
	for x in flag_argc:
		used.append(0)
		new_args.append(None)
	if start_at_zero:
		k=0
	else:
		k=1
	max_k=len(args)
	while k < max_k:
		change=0
		temp_list=[]
		for x in range(len(flag_argc)):
			if change==0:
				flag_args=flag_argc[x]
				if used[x]==0 and re.search(flag_re[x], args[k], re.I):
					change=1
					nap=nap+1
					if overwrite==False:
						used[x]=nap
					if flag_args==0:
						new_args[x]=args[k]
						k=k+1
					elif flag_args==-1:
						searching=True
						k=k+1
						while searching:
							query=0
							for regexp in flag_re:
								if re.search(regexp,str(args[k]),re.I):
									query=1
							if query==0:
								temp_list.append(args[k])
								k=k+1
								if len(args)==k:
									searching=False
							else:
								searching=False
						new_args[x]=temp_list
					elif flag_args==1:
						k=k+2
						new_args[x]=args[k-1]						
					else:
						for j in range(flag_args):
							k=k+1
							temp_list.append(args[k])
						new_args[x]=temp_list
						k=k+1
		if change==0:
			unproc_ed.append(args[k])
			k=k+1
	if unziped_args:
		new_args=unzip(new_args)
	new_args.append(unproc_ed)
	return new_args

def arg_re_diff(args,re_list,overwrite=False):
	output=[]
	changed=[]
	un_proc_ed=[]
	for x in re_list:
		changed.append(0)
		output.append(None)
	for arg in args:
		change=0
		for x in range(len(re_list)):
			if change==0:
				this_re=re_list[x]
				if changed[x]==0 and re.search(this_re,arg,re.I):
					output[x]=arg
					change=1
					if overwrite==False:
						changed[x]=1
		if change==0:
			un_proc_ed.append(arg)
	output.append(un_proc_ed)
	return output

####- test run -####
#list1=['some_prgm','-d','apples','-a','chocolate','-b','bannana','-q','-f','1','2','2','3','4']
#list2=[1,1,1,0,-1]
#list3=['[-][a]','[-][b]','[-][c]','[-][q]','[-][f]']
#list4=arg_flag_ordering(list1,list2,list3)
#print list4
#list5=arg_re_diff(list4[-1],['^[a-z]+'])
#print list5
####-          -####
