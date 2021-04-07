from django.shortcuts import render
import requests
from . import forms 
import pandas as pd
from datetime import datetime, date 
import math
# Create your views here.

weekdays = {
			0: 'Lunes, ',
			1: 'Martes, ', 
			2: 'Miércoles, ',
			3: 'Jueves, ',
			4: 'Viernes, ',
			5: 'Sábado, ',
			6: 'Domingo, ' 
		} 
		
def date_parser(date = None): 
	str_date = ""
	if date: 
		ddate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
		wkd = ddate.weekday() 
		str_date = weekdays.get(wkd)
		str_date = str_date + ddate.strftime("%d-%m-%Y")
	return str_date 

def generate_request(url): 
	response = requests.get(url)

	if response.status_code == 200: 
		return response.json() 
	else: 
		return None 


#print(generate_request("http://localhost:8000/api/pg_quants/206/2020-12-05/?format=json"))


def pq_quants(request):

	form = forms.POSForm() 

	if request.method == 'POST': 
		form = forms.POSForm(request.POST)
		if form.is_valid(): 
			pos_cod = form.cleaned_data['pos_cod']
			#fct_dt = form.cleaned_data['fct_date']
			
			today = date.today() 
			fct_dt = today.strftime("%Y-%m-%d")
			
			data = generate_request("http://localhost:8000/api/pg_quants/"+pos_cod+"/"+fct_dt+"/?format=json")

			hst_data = data['hst_data']
			hst_data_mat = []
			for k in hst_data['FCT_DT'].keys():
			    row = []
			    for field in hst_data.keys():
			        t = hst_data.get(field).get(k)
			        row.append(t) 
			    hst_data_mat.append(row)

			hst_dataframe = pd.DataFrame(hst_data_mat, columns = ["FCT_DT","POS_CD","PRDCT_NM", "SLS_QTY", "FRCST_QTY", "DIFF", "ERROR"])

			prdct_list = ["CHKN_QTY", "FRS_QTY", "SLD_QTY", "PIE_QTY"]

			hst_table_header = sorted(hst_dataframe.PRDCT_NM.unique())
			hst_table_body = []
			for d in sorted(hst_dataframe.FCT_DT.unique(), reverse = True): 
			    temp = hst_dataframe[(hst_dataframe.FCT_DT == d)] 
			    row = [date_parser(d)]
			    for p in prdct_list:
			        temp2 = temp[(temp.PRDCT_NM == p)] 
			        frcst_val = round(temp2.iloc[0]['FRCST_QTY']) 
			        real_val =  round(temp2.iloc[0]['SLS_QTY'])
			        
			        if (p == "CHKN_QTY"):
			        	frcst_val = str(frcst_val) + "(" + str(math.ceil(frcst_val / 21.0)) + ")"
			        	real_val = str(real_val) + "(" + str(math.ceil(real_val / 21.0)) + ")"
			        	
			        row.append(frcst_val)
			        row.append(real_val)
			        
			        row.append(str(round(temp2.iloc[0]['DIFF']))+" | "+str(round(temp2.iloc[0]['ERROR']))+"%")

			    hst_table_body.append(row)

			frcst_data = data['frcst_data']
			data_mat = []
			for k in frcst_data['FCT_DT'].keys():
			    row = []
			    for field in frcst_data.keys(): 
			        row.append(frcst_data.get(field).get(k)) 
			    data_mat.append(row)


			dataframe = pd.DataFrame(data_mat, columns = ["FCT_DT","POS_CD","PRDCT_NM", "FRCST_QTY"])
			
			frcst_table_header = sorted(dataframe.PRDCT_NM.unique())
			frcst_table_header = ["Pollo", "Papas", "Ensalada", "Pastelitos"]
			frcst_table_body = []
			
			for d in sorted(dataframe.FCT_DT.unique()): 
			    temp = dataframe[(dataframe.FCT_DT == d)] 
			    row = [date_parser(d)]
			    for p in prdct_list:
			        temp2 = temp[(temp.PRDCT_NM == p)]
			        val = round(temp2.iloc[0]['FRCST_QTY'])
			        unit = val 
			        if p == 'CHKN_QTY':
			        	band = math.ceil(unit / 21.0)
			        	unit = round(unit / 140.0, 1)  
			        	row.append(val)
			        	row.append(band)
			        	row.append(unit)
			        if p == 'FRS_QTY': 
			        	band = math.ceil(unit / (4.66 * 36))
			        	unit = math.ceil(unit / 4.66)
			        	row.append(val)
			        	row.append(unit)
			        	row.append(band)
			        if p == 'SLD_QTY':
			        	unit = math.ceil(unit / 60.0)
			        	row.append(val)
			        	row.append(unit)
			        if p == 'PIE_QTY':
			        	unit = math.ceil(unit / 60.0)
			        	row.append(val)
			        	row.append(unit)
			        
			    frcst_table_body.append(row)
			
			total = dataframe.groupby(['PRDCT_NM']).sum()

			total = total.add_suffix('_SUM').reset_index() 
			total_row = ['Total']

			for p in prdct_list: 
				temp = total[(total.PRDCT_NM == p)]
				val = math.ceil(temp.iloc[0]['FRCST_QTY_SUM'])
				if p == 'CHKN_QTY':
					band = math.ceil(val / 21.0)
					unit = math.ceil(val / 140.0)
					total_row.append(val)
					total_row.append(band)
					total_row.append(unit)
				if p == 'FRS_QTY': 
					band = math.ceil(val / (4.66 * 36))
					unit = math.ceil(val / 4.66)
					total_row.append(val)
					total_row.append(unit)
					total_row.append(band)
				if p == 'SLD_QTY':
					unit = math.ceil(val / 60.0)
					total_row.append(val)
					total_row.append(unit)
				if p == 'PIE_QTY':
					unit = math.ceil(val / 60.0)
					total_row.append(val)
					total_row.append(unit)
			frcst_table_body.append(total_row)
 


			return render(request , 'pg_quants_temp.html', {
		    	'form': form 
		    	,'POST_REQ': 1
		    	, 'fct_dt': date_parser(fct_dt+"T00:00:00")
		    	, 'pos_cd': pos_cod
		    	,'hst_table_header': hst_table_header
		    	,'frcst_table_header': frcst_table_header
		    	,'frcst_table_body': frcst_table_body
		    	,'hst_table_body': hst_table_body
		    	}
			)

	else:	    
		return render(request, 'pg_quants_temp.html', {'form': form })

