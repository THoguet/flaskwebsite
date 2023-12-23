from icalendar import Calendar, Event, vDatetime, vText, vCalAddress
import datetime
from getcalendar import getcalendar
import pytz


def cal(group, args, dir, fileName):
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	day = datetime.datetime.now().day
	semester = False
	if month < 9 or (month == 12 and day >= 23):
		if month == 12:
			year += 1
		semester = True
	cal = Calendar()
	yearDisplay = str(year) + '-' + str(year + 1)
	if semester:
		yearDisplay = str(year - 1) + '-' + str(year)
	cal.add('prodid', 'EDT Université ' + yearDisplay + ' ' + group)
	cal.add('version', '2.0')
	calendarinfo = getcalendar(group, str(year), semester)
	for i in range(len(calendarinfo)):
		ignore = False
		if calendarinfo[i]["module"] != None:
			if calendarinfo[i]["module"][:8] in args:
				if args[calendarinfo[i]["module"][:8]] == 0:
					ignore = True
				if args[calendarinfo[i]["module"][:8]] != '1':
					if calendarinfo[i]["room"][-3:] != args[calendarinfo[i]["module"][:8]]:
						ignore = True
			if ("showcode" in args and args["showcode"] == '0'):
				calendarinfo[i]["module"] = calendarinfo[i]["module"][9:]
		else:
			calendarinfo[i]["module"] = ""
		if not (ignore):
			loc = ''
			desc = ''
			if calendarinfo[i]['notes'] == None:
				calendarinfo[i]['notes'] = ""
			if calendarinfo[i]["room"] != "":
				if "CREMI" in calendarinfo[i]['room']:
					loc = 'A28, 33400 Talence, France'
					desc = calendarinfo[i]['room'][17:] + '\n' + calendarinfo[i]['notes']
				elif '/' in calendarinfo[i]['room']:
					slashindex = calendarinfo[i]['room'].find('/')
					loc = calendarinfo[i]['room'][:slashindex] + ', 33400 Talence, France'
					desc = calendarinfo[i]['room'][slashindex + 1:] + '\n' + calendarinfo[i]['notes']
			else:
				desc = calendarinfo[i]['notes']
			for info in calendarinfo[i]:
				if calendarinfo[i][info] == None:
					calendarinfo[i][info] = "???"
			addevent("[" + calendarinfo[i]["category"] + "] " + calendarinfo[i]["module"], calendarinfo[i]["startint"], calendarinfo[i]["endint"], loc, desc,
			         cal)
	f = open(dir + fileName, 'wb')
	f.write(cal.to_ical())
	f.close()


def addevent(summary, startint, endint, location, description, cal):
	event = Event()
	event.add('summary', summary)
	event.add(
	    'dtstart',
	    datetime.datetime(int(str(startint)[:4]),
	                      int(str(startint)[4:6]),
	                      int(str(startint)[6:8]),
	                      int(str(startint)[8:10]),
	                      int(str(startint)[10:12]),
	                      tzinfo=pytz.timezone('Europe/Paris')))
	event.add(
	    'dtend',
	    datetime.datetime(int(str(endint)[:4]),
	                      int(str(endint)[4:6]),
	                      int(str(endint)[6:8]),
	                      int(str(endint)[8:10]),
	                      int(str(endint)[10:12]),
	                      tzinfo=pytz.timezone('Europe/Paris')))
	event['location'] = vText(location)
	event['description'] = vText(description)
	cal.add_component(event)
