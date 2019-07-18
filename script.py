import json
import sys

import requests

import config


def main():
    if token:
        response = request_vehicles(token)
        print_info(response)
        return 0

    else:
        sys.exit()


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


def request_vehicles(*arg):
    if len(arg) == 1:
        return requests.get(f'{osu_API}v1/beaverbus/vehicles', headers={
            'Authorization': f'Bearer {arg[0]}'
        })
    if len(arg) == 2:
        return requests.get(f'{osu_API}v1/beaverbus/vehicles/{arg[1]}',
                            headers={'Authorization': f'Bearer {arg[0]}'}
                            )


def print_info(response):
    response_data_JSON = response.json()['data']
    s1 = (
            'Enter a vehicle ID number to look at, '
            '"all" to view info of all active buses, '
            '"raw" to view raw JSON, or "exit" to quit: '
        )
    s2 = (
            'You have entered an invalid command,'
            'or the bus ID you entered does not exist'
        )

    while True:
        available_buses()
        user_input = input(s1)

        if is_valid_bus(user_input, response_data_JSON):
            if user_input == 'exit':
                print('exiting...')
                sys.exit()

            elif user_input == 'all':
                response_data_JSON = request_vehicles(token).json()['data']
                for bus in response_data_JSON:
                    bus = bus['attributes']
                    print(f"Name: {bus['name']}",
                          f"Latitude: {bus['latitude']}",
                          f"Longitude: {bus['longitude']}",
                          f"Current Speed: {bus['speed']}\n",
                          sep="\n"
                          )

            elif user_input == 'raw':
                print(json.dumps(request_vehicles(token).json(),
                                 indent=4, sort_keys=True))

            else:
                vehicle_by_ID = request_vehicles(token, user_input)
                response_data_JSON = vehicle_by_ID.json()['data']['attributes']
                print(f"Name: {response_data_JSON['name']}",
                      f"Latitude: {response_data_JSON['latitude']}",
                      f"Longitude: {response_data_JSON['longitude']}",
                      f"Current Speed: {response_data_JSON['speed']}\n",
                      sep='\n'
                      )
        else:
            print(s2)


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


def available_buses():
    request = request_vehicles(token)

    if len(request.json()['data']) == 0:
        print("There are no currently active buses")
    else:
        print('Here are the IDs of buses currently in use:')
        for bus in request.json()['data']:
            print(f'{bus["id"]} ')


osu_API = 'https://api.oregonstate.edu/'
token = generate_token(config.client_id, config.client_secret)

main()
