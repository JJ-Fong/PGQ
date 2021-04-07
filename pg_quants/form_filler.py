import requests

def pos_codes(flag = None): 

	pos_codes_choices = []
	if flag: 
		response = requests.get("http://localhost:8000/api/pos_codes/")
		if response.status_code == 200:
			codes = response.json()
			codes = codes['POS_LIST']
			for item in codes:
				pos_codes_choices.append((list(item.keys())[0], list(item.values())[0]))
	return pos_codes_choices
	
def available_date(flag = None): 
	date_choices = []
	if flag: 
		response = requests.get("http://localhost:8000/api/available_dates/")
		if response.status_code == 200:
			codes = response.json()
			codes = codes['DT_LIST']
			for item in codes:
				date_choices.append((list(item.keys())[0], list(item.values())[0]))
	return date_choices
