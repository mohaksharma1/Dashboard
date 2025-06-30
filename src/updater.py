import requests

def check_update():
    version=""
    with open('src\\version', 'r') as file:
        data = file.read()
        version=data
    url = "https://raw.githubusercontent.com/mohaksharma1/Dashboard/refs/heads/main/src/version"
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.json()
        if int(file_content) > int(version):
            print("Update available")
            return 1
        elif int(file_content) == int(version):
            print("Version Up to Date")
            return 0
        else:
            print("Update error contact Dev team")
            return 2
    else:
        return 2
