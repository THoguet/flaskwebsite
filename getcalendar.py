import requests
from html.parser import unescape
from datetime import datetime
from time import localtime, mktime, strptime, tzset
from os import environ

environ["TZ"] = 'CET'
tzset()


def timeint(year: int, month: int, day: int, hour: int, minute: int) -> int:
	return ((((year * 100 + month) * 100 + day) * 100 + hour) * 100 + minute)


def sorted_schedule(s: list) -> list:
	return sorted(s, key=lambda x: x["timeint"])


def event_timeint(e: dict, interval_bound: str = 'start') -> int:
	date, time = e[interval_bound].split('T')
	year, month, day = map(int, date.split('-'))
	hour, minute, second = map(int, time.split(':'))
	return timeint(year, month, day, hour, minute)


def format_description(event: dict) -> filter:
	return filter(None, map(unescape, event['description'].replace('\r', '').replace('<br />', '').split('\n')))


def is_room(field: str) -> bool:
	return ('/' in field and not '//' in field) or 'CREMI -' in field


class WebApiURL:
	DOMAIN = 'https://celcat.u-bordeaux.fr/Calendar/Home/'
	GROUPS = 'ReadResourceListItems'
	CALENDARDATA = 'GetCalendarData'
	SIDEBAR = 'GetSideBarEvent'


def get_calendar(group: str) -> dict:
	data = {
	    'start': '2022-01-01',
	    'end': '2022-07-01',
	    'resType': '103',
	    'calView': 'agendaDay',
	    'federationIds[]': group,
	}
	url = WebApiURL.DOMAIN + WebApiURL.CALENDARDATA
	headers = {
	    'Connection': 'keep-alive',
	    'Pragma': 'no-cache',
	    'Cache-Control': 'no-cache',
	    'Accept': 'application/json',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	}
	r = requests.post(url, data=data, headers=headers)
	print(r)
	j = r.json()
	return {event['id']: event for event in j}


def parse_event(event: dict) -> dict:
	parsed_event = {
	    #'id':        event['id'],
	    #'day':       0,
	    'date': tuple(map(int, event['start'].split('T')[0].split('-'))),
	    'starttime': event['start'].split('T')[1],
	    'endtime': (event['end'].split('T')[1] if not event['allDay'] else '20:30:00'),
	    'startint': event_timeint(event, 'start'),
	    'endint': (event_timeint(event, 'end') if not event['allDay'] else event_timeint(event, 'start') // 10000 * 10000 + 2030),
	    'timeint': event_timeint(event),
	    'module': event['modules'] and event['modules'][0],
	    'category': event['eventCategory'],
	    #'groups':    [],
	    'room': None,
	    #'staff':     None,
	    'notes': None,
	}
	#parsed_event['day'] = datetime(*parsed_event['date']).weekday()
	for field in format_description(event):
		if field in (parsed_event['module'], parsed_event['category']):
			continue
		elif is_room(field):
			parsed_event['room'] = field
		# elif is_staff(field):
		# 	parsed_event['staff'] = [field]
		else:
			if parsed_event['notes']:
				parsed_event['notes'] += ' ' + field
			else:
				parsed_event['notes'] = field
	return parsed_event


def getcalendar(group):
	id_cal = get_calendar(group)
	sche_id_dict = {}
	for id, event in id_cal.items():
		if event['eventCategory'] != 'Vacances':
			if id not in sche_id_dict:
				sche_id_dict[id] = parse_event(event)
	t = sorted_schedule(sche_id_dict.values())
	res = []
	for i in t:
		if i["room"] == None:
			i["room"] = ""
		res.append(i)
	return res


#print(calendarinfo[43])
# for i in range(len(calendarinfo)):
# 	loc = ''
# 	if calendarinfo[i]["room"] != None:
# 		if calendarinfo[i]['room'][3] != '/':
# 			loc = 'A28, talence'
# 		else:
# 			loc = calendarinfo[i]['room'][:3]+', talence'
