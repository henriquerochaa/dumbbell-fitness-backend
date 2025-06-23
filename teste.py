import requests

url = "http://localhost:8000/api-token-auth/"
headers = {"Content-Type": "application/json"}

# Corpo da requisição com as credenciais
data = {
    "username": "lucas.silva@exemplo.com",
    "password": "lucasilva"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    token = response.json().get("token")
    print(f"Token recebido: {token}")
else:
    print(f"Falhou! Status: {response.status_code} - {response.text}")
