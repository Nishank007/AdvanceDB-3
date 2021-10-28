import pyodbc

server = 'tcp:nishankgujar.database.windows.net,1433'
database = 'earthquake'
username = 'nishankgujar'
password = 'nishank@123'
driver = '{ODBC Driver 17 for SQL Server}'
try:
    connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
except Exception as e:
	print(e)
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
