from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

async def post(request):
	"""
	{
		"url": string[],
		"pagerank": double[],
		"normalized_pagerank": double[]
	}
	"""
	try:
		request = await request.json()
		url = request["url"]
		pagerank = request["pagerank"]
		normalized_pagerank = request["normalized_pagerank"]

		"""
		So right now, every section has to do this individually, and it's not a great practice tbh.
		I'll likely subclass all these sections so that I only have to put imports once
		and only have to connect once, but there's not enough time right now to refactor all this.
		"""

		for i in range(0,len(url)):
			i_url = url[i]
			doc_id = hashlib.md5(url[i].encode('utf-8')).hexdigest()
			i_pagerank = pagerank[i]
			i_normalized_pagerank = normalized_pagerank[i]
			settings.cur.execute("SELECT 1 FROM doc_store WHERE doc_id='%s';" %(doc_id))
			if(len(settings.cur.fetchall())==0):
				sql_statement = "INSERT INTO doc_store (doc_id, url, pagerank, norm_pagerank) VALUES ('%s','%s', %.8f, %.8f);" %(doc_id, i_url, i_pagerank, i_normalized_pagerank)
			else:
				sql_statement = "UPDATE doc_store SET url='%s', pagerank=%.8f, norm_pagerank=%.8f WHERE doc_id='%s';" %(i_url, i_pagerank, i_normalized_pagerank, doc_id)
			settings.cur.execute(sql_statement)

		#For debugging purposes, I like to see what the DB looks like after the request
		settings.cur.execute("SELECT * FROM doc_store LIMIT 15")
		db_result = settings.cur.fetchall()
		print(db_result)

		response_obj = {"status": "Successfully added data"}

		#settings.cur.close()
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		print(e)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)