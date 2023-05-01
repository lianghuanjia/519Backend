import requests
import json
API_KEY = 'AIzaSyAcxsLiKPBz71iLy8Tx_QV9tAnyZkcxYD8'

def convert_seconds(seconds):
    # Calculate the number of days, hours, minutes, and seconds
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Format the result as a string
    result = ""
    if days > 0:
        result += f"{days} day{'s' if days > 1 else ''}, "
    if hours > 0:
        result += f"{hours} hour{'s' if hours > 1 else ''}, "
    if minutes > 0:
        result += f"{minutes} minute{'s' if minutes > 1 else ''}, "
    if seconds > 0 or not result:
        result += f"{seconds} second{'s' if seconds > 1 else ''}"

    return result



def get_distance_and_duration_between_two_places(origin, destination):
    modes = ["driving", "walking", "bicycling", "transit"]
    base_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin[0]},{origin[1]}&destinations={destination[0]},{destination[1]}"
    api_key = f"&key={API_KEY}"
    durations = {}
    for mode in modes:
        mode = f"&mode={mode}"
        request_url = base_url+mode+api_key
        print(request_url)
        response = requests.get(request_url)
        data = json.loads(response.text)
        #distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['value']
        durations[mode] = duration
    fastest_mode = min(durations, key=durations.get)
    for i in durations:
        print("mode: "+i)
        print("time: "+ convert_seconds(durations[i]))
    return fastest_mode, durations[fastest_mode]




if __name__ == "__main__":
    origin = (40.714, -73.998)
    destination = (42.3601, -71.0589)
    fastest_mode, duration = get_distance_and_duration_between_two_places(origin, destination)
    print("fastest mode: "+fastest_mode)
    converted_duration = convert_seconds(duration)
    print("taken time: "+converted_duration)

