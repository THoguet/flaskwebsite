from icalendar import Calendar, Event, vDatetime, vText, vCalAddress
import datetime
import time
from getcalendar import getcalendar

cal = Calendar()
cal.add('prodid', 'EDT Université 2021-2022 IN301A42')
cal.add('version', '2.0')

def main():
	calendarinfo = getcalendar()

	for i in range(len(calendarinfo)):
		col = "1"
		cbn = 1
		if calendarinfo[i]["module"] == '4TTV315U Anglais':
			calendarinfo[i]["module"] = 'Anglais'
			if calendarinfo[i]["room"] != 'A21/ Salle 162':
				cbn = 0
			if ((datetime.date(int(calendarinfo[i]["date"][0]) ,int(calendarinfo[i]["date"][1]), int(calendarinfo[i]["date"][2])).isocalendar()[1]) % 2) == 0:
				cbn = 0
		elif calendarinfo[i]["module"] == '4TINA01U Programmation Fonctionnelle':
			col = '4'
			calendarinfo[i]["module"] = 'Programmation Fonctionnelle'
		elif calendarinfo[i]["module"] == '4TIN303U Programmation C':
			col = '11'
			calendarinfo[i]["module"] = 'Programmation C'
		elif calendarinfo[i]["module"] == '4TIN403U Projets technologiques':
			col = '3'
			calendarinfo[i]["module"] = 'Projets technologiques'
		elif calendarinfo[i]["module"] == '4TIN310U Réseau':
			col = '7'
			calendarinfo[i]["module"] = 'Réseau'
		elif calendarinfo[i]["module"] == '4TIN302U Algo des structures données élémen':
			col = '8'
			calendarinfo[i]["module"] = 'Algo des structures données élémentaire'
		elif calendarinfo[i]["module"] == "4TPMA01U Connaissance de l\'entreprise":
			col = '5'
			calendarinfo[i]["module"] = 'Connaissance de l\'entreprise'
			if calendarinfo[i]["category"] != "Cours":
				if calendarinfo[i]["room"] != 'A29/ Salle 101':
					cbn = 0
		if calendarinfo[i]["module"] == "4TTVA35U Méthodes et outils pour l’utilisation des systèmes info":
			cbn = 0
		if cbn:
			loc = ''
			if calendarinfo[i]["room"] != None:
				if calendarinfo[i]['room'][3] != '/':
					loc = 'A28, 33400 Talence, France'
					desc = calendarinfo[i]['room'][17:]
				else:
					loc = calendarinfo[i]['room'][:3]+', 33400 Talence, France'
					desc = calendarinfo[i]['room'][4:]
			addevent(calendarinfo[i]["module"],calendarinfo[i]["startint"],calendarinfo[i]["endint"],loc,col,desc)
			f = open('./static/calUni.ics', 'wb')
			f.write(cal.to_ical())
			f.close()

def addevent(summary,startint,endint,location,color,description):
	event = Event()
	event.add('summary', summary)
	event.add('dtstart', datetime.datetime.strptime(str(startint),'%Y%m%d%H%M'))
	event.add('dtend', datetime.datetime.strptime(str(endint),'%Y%m%d%H%M'))
	event['location'] = vText(location)
	event['color'] = vText(color)
	event['description'] = vText(description)
	cal.add_component(event)

if __name__ == '__main__':
	while True:
		try:
			main()
			time.sleep(21600)
		except:
			time.sleep(30)