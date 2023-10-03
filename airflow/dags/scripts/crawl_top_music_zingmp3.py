import json
from datetime import date
from playwright.sync_api import sync_playwright 

from common.work_file import save_json
		

def extract_zingchart(): 
	url = "https://zingmp3.vn/zing-chart" 
	with sync_playwright() as p: 
		def handle_response(response): 
			if ("zingmp3.vn/api/v2/page/get/chart-home" in response.url): 
				file_name = str(date.today())
				save_json(file_name, response.json()["data"])
				print("[EXTRACT] Get success data:", response.json()["data"].keys())
				
		browser = p.chromium.launch() 
		page = browser.new_page() 
	
		page.on("response", handle_response) 
		page.goto(url, wait_until="networkidle") 
		page.context.close() 
		browser.close()