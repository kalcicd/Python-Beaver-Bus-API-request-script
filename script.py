import json
import sys

import requests

import config


def main():
    if token:
        response = request_vehicles(None)
        print_info(response)
        sys.exit(signal)

    else:
        sys.exit('Invalid credentials')


def generate_token(client_id, client_secret):
    token_response = requests.post(f'{osu_API}oauth2/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    })

    if(token_response.status_code == 200):
        return token_response.json()['access_token']


def request_vehicles(id):
    authorization_header = {'Authorization': f'Bearer {token}'}
    beaverbus_vehicles = 'v1/beaverbus/vehicles/'
    if id:
        return requests.get(f'{osu_API}{beaverbus_vehicles}{id}',
                            headers=authorization_header
                            )
    else:
        return requests.get(f'{osu_API}{beaverbus_vehicles}',
                            headers=authorization_header
                            )


def print_info(response):
    response_data_json = response.json()['data']
    instructions = (
            'Enter a vehicle ID number to look at, '
            '"all" to view info of all active buses, '
            '"raw" to view raw JSON, or "exit" to quit: '
        )
    error = (
            'You have entered an invalid command,'
            'or the bus ID you entered does not exist'
        )

    while True:
        available_buses()
        user_input = input(instructions)
        response_data_json = request_vehicles(None).json()['data']

        if is_valid_bus(user_input, response_data_json):
            if user_input == 'exit':
                print('Goodbye!')
                sys.exit(signal)

            elif user_input == 'all':
                for bus in response_data_json:
                    bus = bus['attributes']
                    print(f"Name: {bus['name']}",
                          f"Latitude: {bus['latitude']}",
                          f"Longitude: {bus['longitude']}",
                          f"Current Speed: {bus['speed']}\n",
                          sep="\n"
                          )

            elif user_input == 'raw':
                print(json.dumps(request_vehicles(None).json(),
                                 indent=4, sort_keys=True))

            else:
                vehicle_by_id = request_vehicles(user_input)
                response_data_json = vehicle_by_id.json()['data']['attributes']
                print(f"Name: {response_data_json['name']}",
                      f"Latitude: {response_data_json['latitude']}",
                      f"Longitude: {response_data_json['longitude']}",
                      f"Current Speed: {response_data_json['speed']}\n",
                      sep='\n'
                      )
        else:
            print(error)


def is_valid_bus(user_input, response_data_json):
    if(
        user_input.lower() == 'all'
        or user_input.lower() == 'exit'
        or user_input.lower() == 'raw'
    ):
        return True

    for bus in response_data_json:
        if bus['id'] == user_input:
            return True

    return False


def available_buses():
    response = request_vehicles(None)
    if len(response.json()['data']) == 0:
        print('There are no currently active buses')
    else:
        print('Here are the IDs of buses currently in use:')
        for bus in response.json()['data']:
            print(f'{bus["id"]} ')


signal = 0
osu_API = 'https://api.oregonstate.edu/'
token = generate_token(config.client_id, config.client_secret)

main()
