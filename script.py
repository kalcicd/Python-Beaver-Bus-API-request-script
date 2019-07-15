import requests
import pprint
import login

def main():
    token = generateToken(login.client_id, login.client_secret)
    if(token):
        requestVehicles(token)
    return 0

def generateToken(client_id, client_secret):
    tokenResponse = requests.post("https://api.oregonstate.edu/oauth2/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    })
    if(tokenResponse.status_code == 200):
        return tokenResponse.json()['access_token']
    else:
        print("Invalid credentials")
        return None

def requestVehicles(token):
    parameters = {
        "Authorization": "Bearer " + token
    }
    response = requests.get("https://api.oregonstate.edu/v1/beaverbus/vehicles", headers=parameters)
    pp = pprint.PrettyPrinter()
    pp.pprint(response.json())

main()