from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

async def post(request):
	"""
	{
		"url": string,
		"error_code": int,
		"redirect": string
	}
	"""
	try:
		request = await request.json()
		url = request["url"]
		doc_id = hashlib.md5(url.encode('utf-8')).hexdigest()
		error_code = request["error_code"]
		redirect = request["redirect"]

		#feel free to add or change html error codes
		if (int(error_code) == 301):
			sql_statement = "UPDATE doc_store SET url = '%s' WHERE url = '%s';" %(redirect,url)
			settings.cur.execute(sql_statement)

		#feel free to add or change html error codes
		elif (int(error_code) == 404):
			sql_statement = "DELETE FROM doc_store WHERE url = '%s';" %(url)
			settings.cur.execute(sql_statement)

		#For debugging purposes, I like to see what the DB looks like after the request
		settings.cur.execute("SELECT * FROM doc_store LIMIT 15")
		db_result = settings.cur.fetchall()
		print(db_result)

		response_obj = {"status": "Successfully modified data"}

		#settings.cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)