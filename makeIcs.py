from icalendar import Calendar, Event, vDatetime, vText, vCalAddress
import datetime
from backports.zoneinfo import ZoneInfo
from getcalendar import getcalendar


def exist(tab, test):
	if test in tab:
		return 1
	return 0


def cal(group, args):
	cal = Calendar()
	cal.add('prodid', 'EDT Université 2021-2022 ' + group)
	cal.add('version', '2.0')
	calendarinfo = getcalendar(group)
	for i in range(len(calendarinfo)):
		ignore = False
		if calendarinfo[i]["module"] != None:
			if calendarinfo[i]["module"][:8] in args and args[calendarinfo[i]["module"][:8]] != 0:
				if args[calendarinfo[i]["module"][:8]] != '1':
					if calendarinfo[i]["room"][-3:] != args[calendarinfo[i]["module"][:8]]:
						ignore = True
			else:
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
				if calendarinfo[i]['room'][3] != '/':
					loc = 'A28, 33400 Talence, France'
					desc = calendarinfo[i]['room'][17:] + '\n' + calendarinfo[i]['notes']
				else:
					loc = calendarinfo[i]['room'][:3] + ', 33400 Talence, France'
					desc = calendarinfo[i]['room'][4:] + '\n' + calendarinfo[i]['notes']
			else:
				desc = calendarinfo[i]['notes']
			addevent("[" + calendarinfo[i]["category"] + "] " + calendarinfo[i]["module"], calendarinfo[i]["startint"] - 200, calendarinfo[i]["endint"] - 200,
			         loc, desc, cal)
			f = open('/var/www/html/static/ics/calUni ' + group + ' ' + str(args)[20:-2].replace("(", "").replace(" ","_").replace("',", ":").replace("'", "").replace(")", "") + '.ics',
			         'wb')
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
	                      tzinfo=ZoneInfo("Europe/Paris")))
	event.add(
	    'dtend',
	    datetime.datetime(int(str(endint)[:4]),
	                      int(str(endint)[4:6]),
	                      int(str(endint)[6:8]),
	                      int(str(endint)[8:10]),
	                      int(str(endint)[10:12]),
	                      tzinfo=ZoneInfo("Europe/Paris")))
	event['location'] = vText(location)
	event['description'] = vText(description)
	cal.add_component(event)