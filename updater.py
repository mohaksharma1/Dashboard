import requests

url = "https://raw.githubusercontent.com/mohaksharma1/Dashboard/main/version"
response = requests.get(url)

if response.status_code == 200:
    file_content = response.json()
    print(file_content)
else:
    print("Failed to retrieve file content")
