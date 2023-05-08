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



def calculate_traveling_time_between_two_places(place1, place2, mode):
    """
    :param place1: (latitude, longitude). E.g.: (40.714, -73.998)
    :param place2: (latitude, longitude). E.g.: (42.3601, -71.0589)
    :param mode: traveling mode that the user prefers
    :return: traveling time between the origin and destination in second unit.
    """
    try:
        base_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={place1[0]},{place1[1]}&destinations={place2[0]},{place2[1]}"
        api_key = f"&key={API_KEY}"
        mode = f"&mode={mode}"
        request_url = base_url+mode+api_key
        print(request_url)
        response = requests.get(request_url)
        data = json.loads(response.text)
        #distance = data['rows'][0]['elements'][0]['distance']['text']
        traveling_time = data['rows'][0]['elements'][0]['duration']['value']
        # print("time in second: "+ str(traveling_time))
        return traveling_time
    except Exception as err:
        raise err


# def calculate_optimized_path(starting_point_info, destination_info, places_info_list):
#     pass


#
# if __name__ == "__main__":
#     origin = (42.3453547, -71.1068336)
#     destination = (42.339381, -71.094048)
#     duration = calculate_traveling_time_between_two_places(origin, destination, "driving")
#     converted_duration = convert_seconds(duration)
#     print("taken time: "+converted_duration)
