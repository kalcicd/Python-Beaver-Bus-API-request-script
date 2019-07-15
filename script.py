import requests
import pprint
import config

def main():
    token = generateToken(config.client_id, config.client_secret)
    if token:
        response = requestVehicles(token)
        printInfo(response)
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
        "Authorization": f"Bearer {token}"
    }
    return requests.get("https://api.oregonstate.edu/v1/beaverbus/vehicles", headers=parameters)
    
def printInfo(response):
    pp = pprint.PrettyPrinter()
    
    print(response.json()["data"][0]["attributes"]["name"], "Stats:")
    print("Latitude:", response.json()["data"][0]["attributes"]["latitude"])
    print("Longitude:", response.json()["data"][0]["attributes"]["longitude"])
    print("Current Speed:", response.json()["data"][0]["attributes"]["speed"])

    print("\nHere is the raw request data:")
    pp.pprint(response.json())

main()