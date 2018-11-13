from aiohttp import web
import json
import os
from main import data,settings,index

def init_routes(app):
	app.router.add_get('/', index.index)
	app.router.add_post('/crawling', data.crawling.post)
	app.router.add_post('/tt', data.text_transformation.post)
	app.router.add_post('/la', data.link_analysis.post)

	#This is technically a GET i guess, but it's not good pratice to put json in a GET request
	#Option 1: Make this a post instead and just return a lot of data
	#Option 2: Make docId a parameter in the URL instead and not have it be an array
	app.router.add_post('/querying', data.querying.get)

#Load config.yaml settings. Can be accessed with app['config']. config.yaml is located in .\config\

if __name__ == "__main__":
	app = web.Application()
	settings.get_config(os.path.dirname(os.path.realpath(__file__))+"\\config\\config.yaml")
	init_routes(app)
	web.run_app(app, host=settings.config['host'], port=settings.config['port'])