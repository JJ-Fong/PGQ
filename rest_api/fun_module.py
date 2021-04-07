import pyodbc
import pandas as pd
import datetime 

def fetch_query(query): 
	server = 'cmiazsrvml03.database.windows.net'
	database = 'IDN_DB'
	username = 'cmia_etl'
	password = '(Mi@.3Tl'   

	#driver= '{SQL Server Native Client 11.0}'
	driver= '{SQL Server}'

	conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
	dataset = pd.read_sql(query, conn)
	return(dataset)

def pg_pos_list():
	dataset = fetch_query("""
		SELECT DISTINCT POS_CD INT_POS_CD, CONCAT('PG - ', POS_CD) STR_POS_CD 
		FROM ST.RCA_PG_QNTS_FRCST_SLS_D_3
		ORDER BY POS_CD
	""")

	element_list = []
	for ind, row in dataset.iterrows(): 
	    element = {}
	    element[row['INT_POS_CD']] = row['STR_POS_CD']
	    element_list.append(element)
	   
	result = {}
	result['POS_LIST'] = element_list 
	return(result)

def pg_date_list():
	dataset = fetch_query("""
		SELECT DISTINCT FRCST_DT DT_CD, FRCST_DT STR_DT_CD 
		FROM ST.RCA_PG_QNTS_FRCST_SLS_D_3
		ORDER BY FRCST_DT 
	""")

	element_list = []
	for ind, row in dataset.iterrows(): 
	    element = {}
	    element[row['DT_CD']] = row['STR_DT_CD']
	    element_list.append(element)
	   
	result = {}
	result['DT_LIST'] = element_list 
	return(result)

def pg_quants_data(pos = "206", date = "2020-12-05"): 

	
	today = datetime.datetime.strptime(date, "%Y-%m-%d")
	tomorrow = today + datetime.timedelta(days=1)
	yesterday =  today + datetime.timedelta(days=-1)
	lower_date = today + datetime.timedelta(days=-45)
	upper_date = today + datetime.timedelta(days=4)

	today = datetime.datetime.strftime(today, "%Y-%m-%d")
	yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
	tomorrow = datetime.datetime.strftime(tomorrow, "%Y-%m-%d")
	lower_date = datetime.datetime.strftime(lower_date, "%Y-%m-%d")
	upper_date = datetime.datetime.strftime(upper_date, "%Y-%m-%d")
	
	hst_query = """ 
		SELECT 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
			, SUM(SLS_UNIT_QTY) SLS_UNIT_QTY
		FROM ST.RCA_PG_QNTS_FCT_SLS 
		WHERE POS_CD = """+pos+""" AND FCT_DT BETWEEN '"""+lower_date+"""' AND '"""+yesterday+"""'
		GROUP BY 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
	"""

	hst_query = """ 
	SELECT 
		REALV.* 
		, coalesce(FRCST.FRSCT_UNIT_QTY, 0) FRSCT_UNIT_QTY
		, coalesce(FRCST.FRSCT_UNIT_QTY - REALV.SLS_UNIT_QTY, 0) DIFF 
		, coalesce( 
		ROUND(
			100 * (FRCST.FRSCT_UNIT_QTY - REALV.SLS_UNIT_QTY ) / REALV.SLS_UNIT_QTY
			, 0 
		),0) PERROR 
	FROM (
		SELECT 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
			, SUM(SLS_UNIT_QTY) SLS_UNIT_QTY
		FROM ST.RCA_PG_QNTS_FCT_SLS REALV
		WHERE POS_CD = """+pos+""" AND FCT_DT BETWEEN '"""+lower_date+"""' AND '"""+yesterday+"""'
		GROUP BY 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
	) REALV 
	LEFT JOIN (
		SELECT 
			FCT_DT
			, POS_CD
			, PRDCT_NM 
			, SUM(FRCST_SLS_QTY) FRSCT_UNIT_QTY
		FROM ST.RCA_PG_QNTS_FRCST_SLS_D_3 
		WHERE POS_CD = """+pos+""" AND FCT_DT BETWEEN '"""+lower_date+"""' AND '"""+yesterday+"""'
		GROUP BY 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
	) FRCST ON REALV.FCT_DT = FRCST.FCT_DT AND REALV.PRDCT_NM = FRCST.PRDCT_NM
	"""

	frcst_query = """ 
		SELECT 
			FCT_DT 
			, POS_CD 
			, PRDCT_NM 
			, FRCST_SLS_QTY SLS_UNIT_QTY
		FROM ST.RCA_PG_QNTS_FRCST_SLS_D_3
		WHERE POS_CD = """+pos+""" AND FCT_DT BETWEEN '"""+tomorrow+"""' AND '"""+upper_date+"""'
	"""

	

	hst_data = fetch_query(hst_query)
	frcst_data = fetch_query(frcst_query)

	rst = {} 
	rst['hst_data'] = hst_data.to_dict()	
	rst['frcst_data'] = frcst_data.to_dict()  
	return(rst)
