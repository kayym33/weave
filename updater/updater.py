import requests
from constants.constants import VERSION

def get_latest_release():
	LATEST_RELEASE_URL = "https://api.github.com/repos/kayym33/weave/releases/latest"
	response = requests.get(LATEST_RELEASE_URL, timeout=10)
	data = response.json()
	return data["tag_name"], data["assets"][0]["browser_download_url"]


def download_url_file(url, path):
	response = requests.get(url, timeout=10)
	with open(path, "wb") as file_writer:
		file_writer.write(response.content)
  
  
def update_program():
	latest_version, download_url = get_latest_release()
	latest_version = latest_version.lstrip("v")

	if latest_version == VERSION:
		print("[WEAVE]: Already up to date.")
		return

	print(f"[WEAVE]: Updating to {latest_version}...")

	download_url_file(download_url, "weave_new")

	import os, sys
	os.replace("weave_new", sys.argv[0])

	print("[WEAVE]: Update complete.")