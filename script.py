import json
import requests

import config

def main():
    if token:
        response = requestVehicles(token)
        printInfo(response)
    return 0


def generateToken(client_id, client_secret):
    tokenResponse = requests.post(f'{osuAPI}oauth2/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    })

    if(tokenResponse.status_code == 200):
        return tokenResponse.json()['access_token']
    else:
        print('Invalid credentials')


def requestVehicles(token):
    return requests.get(f'{osuAPI}v1/beaverbus/vehicles', headers={
        'Authorization': f'Bearer {token}'
    })


def requestVehicleByID(token, ID):
    return requests.get(f'{osuAPI}v1/beaverbus/vehicles/{ID}', headers={
        'Authorization': f'Bearer {token}'
    })


def printInfo(response):
    responseDataJSON = response.json()['data']
    while True:
        userInput = input('Enter a vehicle ID to look at, "all" to view info of all active buses, "raw" to view raw JSON, or "exit" to quit: ')
        if isValidBus(userInput, responseDataJSON):
            break
        else:
            print('invalid input')

    if(userInput == 'exit'):
        print('exiting...')
        exit()

    elif(userInput == 'all'):
        for bus in responseDataJSON:
            print(f"{bus['attributes']['name']} Stats:")
            print(f"Latitude: {bus['attributes']['latitude']}")
            print(f"Longitude: {bus['attributes']['longitude']}")
            print(f"Current Speed: {bus['attributes']['speed']}\n")

    elif(userInput == 'raw'):
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    else:
        responseDataJSON = requestVehicleByID(token, userInput).json()['data']['attributes']
        print(f"{responseDataJSON['name']} Stats:")
        print(f"Latitude: {responseDataJSON['latitude']}")
        print(f"Longitude: {responseDataJSON['longitude']}")
        print(f"Current Speed: {responseDataJSON['speed']}\n")


def isValidBus(userInput, responseDataJSON):
    if(userInput.lower() == 'all' or userInput.lower() == 'exit' or userInput.lower() == 'raw'):
        return True

    for bus in responseDataJSON:
        if(bus['id'] == userInput):
            return True
    
    return False


osuAPI = 'https://api.oregonstate.edu/'
token = generateToken(config.client_id, config.client_secret)

main()
