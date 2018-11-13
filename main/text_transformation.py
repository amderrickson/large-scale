from aiohttp import web
import psycopg2
import json

async def post(request):
	"""
	{
		"metadata": {
			"url": string,
			"title": string,
			"description": string,
			"keywords": string[],
			"authors": string[]
		},
		"text": {
			"headings": string[],
			"body": []
		},
		"grams": [{
			"gram": string,
			"headingfreq": double,
			"bodyfreq": double
		}]
	}
	"""
	try:
		request = await request.json()
		url = request["metadata"]["url"] #Doc store
		title = request["metadata"]["title"] #Doc store
		description = request["metadata"]["description"] #Doc store
		headings = title = request["text"]["headings"] #Doc store
		body = title = request["text"]["body"] #Doc store

		
		keywords = request["metadata"]["keywords"]
		authors = request["metadata"]["authors"]

		gram = title = request["text"]["gram"]
		headingfreq = title = request["text"]["headingfreq"]
		bodyfreq = title = request["text"]["bodyfreq"]

		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)