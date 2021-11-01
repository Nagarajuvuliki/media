import requests
url="http://127.0.0.1:8000/freshdesk/api/createticket/"
headers = {"Content-Type": "application/json"}
params =("vulikinagaraju@gmail.com","nagaswrn")
data={
        "subject": "sfds",
        "description": "sdfdf",
        "email": "arya1234@gmail.com",
        "priority":43,
        "status": 3234,
    }
r=requests.post(url, data=data)
print(r.text)