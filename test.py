from getcalendar import getcalendar
import datetime

argschiant = [('hidecode', '1'), ('anglais', '162'), ('theatre', '0'), ('lco', '0'), ('coentre', '1')]
args = [[],[]]

calendarinfo = getcalendar('IN301A42')

def exist(tab,test):
	for i in range(len(tab)):
		if test in tab[i]:
			return i
	return -1

def initargs(tab,value,newtab):
	i = exist(tab,value)
	if i != -1:
		newtab[0].append(tab[i][0])
		newtab[1].append(int(tab[i][1]))
	else:
		newtab[0].append(value)
		newtab[1].append(1)
args = [[],[]]
for i in ["sport","theatre","lco","entrep","coentre","anglais","anglais_sem","MOUSI","showcode"]:
	initargs(argschiant,i,args)
for i in range(len(calendarinfo)):
	ignore = False
	if calendarinfo[i]["module"] != None:
		if not(args[1][0]):
			if calendarinfo[i]["module"][:8] == '4TTV402U':
				ignore = True
		if args[1][1]:
			if calendarinfo[i]["module"][:8] == '4TTV403U':
				ignore = True
		if not(args[1][2]):
			if calendarinfo[i]["module"][:8] == '4TTV303U':
				ignore = True
		elif args[1][2] != 1:
			if calendarinfo[i]["module"][:8] == '4TTV303U':
				if calendarinfo[i]["room"][-3:] != str(args[1][2])[-3:]:
					ignore = True
		if args[1][3]:
			if calendarinfo[i]["module"][:8] == '4TIN309U':
				ignore = True
		if not(args[1][4]):
			if calendarinfo[i]["module"][:8] == '4TPMA01U':
				ignore = True
		elif args[1][4] != 1:
			if calendarinfo[i]["module"][:8] == '4TPMA01U':
				if calendarinfo[i]["category"] != "Cours":
					if calendarinfo[i]["room"][-3:] != str(args[1][4])[-3:]:
						ignore = True
		if args[1][5] != 1:
			if calendarinfo[i]["module"][:8] == '4TTV315U':
				if ((datetime.date(int(calendarinfo[i]["date"][0]) ,int(calendarinfo[i]["date"][1]), int(calendarinfo[i]["date"][2])).isocalendar()[1]) % 2) != int(args[1][6])%2:
					ignore = True
				elif calendarinfo[i]["room"][-3:] != str(args[1][5])[-3:]:
					ignore = True
		if args[1][7]:
			if calendarinfo[i]["module"][:8] == '4TTVA35U':
				ignore = True
		if not(args[1][8]):
			calendarinfo[i]["module"] = calendarinfo[i]["module"][9:]
	else:
		calendarinfo[i]["module"] = ""
	if not(ignore):
		loc = ''
		desc = ''
		if calendarinfo[i]['notes'] == None:
			calendarinfo[i]['notes'] = ""
		if calendarinfo[i]["room"] != "":
			if calendarinfo[i]['room'][3] != '/':
				loc = 'A28, 33400 Talence, France'
				desc = calendarinfo[i]['room'][17:]+'\n'+calendarinfo[i]['notes']
			else:
				loc = calendarinfo[i]['room'][:3]+', 33400 Talence, France'
				desc = calendarinfo[i]['room'][4:]+'\n'+calendarinfo[i]['notes']
		else:
			desc = calendarinfo[i]['notes']
		print("["+calendarinfo[i]["category"]+"] "+calendarinfo[i]["module"],calendarinfo[i]["startint"]-200,calendarinfo[i]["endint"]-200,loc,desc)