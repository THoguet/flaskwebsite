from icalendar import Calendar, Event, vDatetime, vText, vCalAddress
import datetime
import time
from getcalendar import getcalendar

def calperso():
	cal = Calendar()
	cal.add('prodid', 'EDT Université 2021-2022 IN301A42')
	cal.add('version', '2.0')
	calendarinfo = getcalendar('IN301A42')

	for i in range(len(calendarinfo)):
		cbn = 1
		if calendarinfo[i]["module"][:8] == '4TTV315U':
			calendarinfo[i]["module"] = 'Anglais'
			if calendarinfo[i]["room"] != 'A21/ Salle 162':
				cbn = 0
			if ((datetime.date(int(calendarinfo[i]["date"][0]) ,int(calendarinfo[i]["date"][1]), int(calendarinfo[i]["date"][2])).isocalendar()[1]) % 2) == 0:
				cbn = 0
		elif calendarinfo[i]["module"][:8] == '4TINA01U':
			calendarinfo[i]["module"] = 'Programmation Fonctionnelle'
		elif calendarinfo[i]["module"][:8] == '4TIN303U':
			calendarinfo[i]["module"] = 'Programmation C'
		elif calendarinfo[i]["module"][:8] == '4TIN403U':
			calendarinfo[i]["module"] = 'Projets technologiques'
		elif calendarinfo[i]["module"][:8] == '4TIN310U':
			calendarinfo[i]["module"] = 'Réseau'
		elif calendarinfo[i]["module"][:8] == '4TIN302U':
			calendarinfo[i]["module"] = 'Algo des structures données élémentaire'
		elif calendarinfo[i]["module"][:8] == "4TPMA01U":
			calendarinfo[i]["module"] = 'Connaissance de l\'entreprise'
			if calendarinfo[i]["category"] != "Cours":
				if calendarinfo[i]["room"] != 'A29/ Salle 101':
					cbn = 0
		if calendarinfo[i]["module"][:8] == "4TTVA35U":
			cbn = 0
		if (calendarinfo[i]["module"][:8] != "4TTV303U" and calendarinfo[i]["module"][:8] != "4TTV402U" and calendarinfo[i]["module"][:8] != "4TTV403U" and calendarinfo[i]["module"][:8] != "4TIN309U"):
			cbn = 0
		if cbn:
			loc = ''
			if calendarinfo[i]["room"] != "":
				if calendarinfo[i]['room'][3] != '/':
					loc = 'A28, 33400 Talence, France'
					desc = calendarinfo[i]['room'][17:]
				else:
					loc = calendarinfo[i]['room'][:3]+', 33400 Talence, France'
					desc = calendarinfo[i]['room'][4:]
			addevent("["+calendarinfo[i]["category"]+"] "+calendarinfo[i]["module"],calendarinfo[i]["startint"]-200,calendarinfo[i]["endint"]-200,loc,desc,cal)
			f = open('./static/calUniperso.ics', 'wb')
			f.write(cal.to_ical())
			f.close()

def exist(tab,test):
	if test in tab:
		return 1
	return 0

def initargs(tab,value,newtab):
	if exist(tab,value):
		newtab[0].append(tab[value])
		newtab[1].append(int(tab[value]))
	else:
		newtab[0].append(value)
		newtab[1].append(1)

def cal(group, argschiant):
	cal = Calendar()
	cal.add('prodid', 'EDT Université 2021-2022 '+group)
	cal.add('version', '2.0')
	calendarinfo = getcalendar(group)
	args = [[],[]]
	for i in ["sport","theatre","lco","entrep","coentre","anglais","anglais_sem","MOUSI","showcode"]:
		initargs(argschiant,i,args)
	for i in range(len(calendarinfo)):
		ignore = False
		if calendarinfo[i]["module"] != None:
			if not(args[1][0]):
				if calendarinfo[i]["module"][:8] == '4TTV402U':
					ignore = True
			if not(args[1][1]):
				if calendarinfo[i]["module"][:8] == '4TTV403U':
					ignore = True
			if not(args[1][2]):
				if calendarinfo[i]["module"][:8] == '4TTV303U':
					ignore = True
			elif args[1][2] != 1:
				if calendarinfo[i]["module"][:8] == '4TTV303U':
					if calendarinfo[i]["room"][-3:] != str(args[1][2])[-3:]:
						ignore = True
			if not(args[1][3]):
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
			if not(args[1][7]):
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
			addevent("["+calendarinfo[i]["category"]+"] "+calendarinfo[i]["module"],calendarinfo[i]["startint"]-200,calendarinfo[i]["endint"]-200,loc,desc,cal)
			f = open('./static/calUni '+group+' '+str(argschiant)[20:-2].replace("(","").replace("',",":").replace("'","").replace(")","")+'.ics', 'wb')
			f.write(cal.to_ical())
			f.close()

def addevent(summary,startint,endint,location,description,cal):
	event = Event()
	event.add('summary', summary)
	event.add('dtstart', datetime.datetime.strptime(str(startint),'%Y%m%d%H%M'))
	event.add('dtend', datetime.datetime.strptime(str(endint),'%Y%m%d%H%M'))
	event['location'] = vText(location)
	event['description'] = vText(description)
	cal.add_component(event)