import json
import requests

import config


def main():
    if token:
        response = request_vehicles(token)
        print_info(response)
        return 0

    else:
        return 1


def generate_token(client_id, client_secret):
    token_response = requests.post(f'{osu_API}oauth2/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    })

    if(token_response.status_code == 200):
        return token_response.json()['access_token']
    else:
        print('Invalid credentials')


def request_vehicles(token):
    return requests.get(f'{osu_API}v1/beaverbus/vehicles', headers={
        'Authorization': f'Bearer {token}'
    })


def request_vehicle_by_ID(token, ID):
    return requests.get(f'{osu_API}v1/beaverbus/vehicles/{ID}', headers={
        'Authorization': f'Bearer {token}'
    })


def print_info(response):
    response_data_JSON = response.json()['data']
    s = (
            'Enter a vehicle ID number to look at, '
            '"all" to view info of all active buses, '
            '"raw" to view raw JSON, or "exit" to quit: '
        )
    while True:
        user_input = input(s)

        if is_valid_bus(user_input, response_data_JSON):
            break
        else:
            print('invalid input')

    if user_input == 'exit':
        print('exiting...')
        exit()

    elif(user_input == 'all'):
        for bus in response_data_JSON:
            print(f"{bus['attributes']['name']} Stats:")
            print(f"Latitude: {bus['attributes']['latitude']}")
            print(f"Longitude: {bus['attributes']['longitude']}")
            print(f"Current Speed: {bus['attributes']['speed']}\n")

    elif(user_input == 'raw'):
        print(json.dumps(response.json(), indent=4, sort_keys=True))

    else:
        vehicle_by_ID = request_vehicle_by_ID(token, user_input)
        response_data_JSON = vehicle_by_ID.json()['data']['attributes']
        print(f"{response_data_JSON['name']} Stats:")
        print(f"Latitude: {response_data_JSON['latitude']}")
        print(f"Longitude: {response_data_JSON['longitude']}")
        print(f"Current Speed: {response_data_JSON['speed']}\n")


def is_valid_bus(user_input, response_data_JSON):
    if(
        user_input.lower() == 'all'
        or user_input.lower() == 'exit'
        or user_input.lower() == 'raw'
    ):
        return True

    for bus in response_data_JSON:
        if(bus['id'] == user_input):
            return True

    return False


osu_API = 'https://api.oregonstate.edu/'
token = generate_token(config.client_id, config.client_secret)

main()
