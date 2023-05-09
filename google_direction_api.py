import requests
from credential import GOOGLE_MAP_API_KEY
import re

# Replace YOUR_API_KEY with your actual API key
api_key = GOOGLE_MAP_API_KEY

# ['Soldiers Field Road', '42.3645558', '-71.1359136']
# ['655 Commonwealth Ave', '42.34993389999999', '-71.1027624']


# Make an HTTP request to the Directions API

'''
ChatGPT usage: Asked ChatGPT how to get the direction from one place to another given those places' latitudes and 
longitude. Also asked it how to use Python regular expression to trim the return answers
'''
def get_direction_from_one_place_to_another(origin, destination, mode):
    """
    Use it to get all the directions steps from one place to another
    :param one_place:
        A string that contains latitude and longitude, with "," in the middle:
        e.g.:'42.3645558,-71.1359136'
    :param another_place:
         A string that contains latitude and longitude, with "," in the middle:
         e.g.: '42.34993389999999, -71.1027624'
    :param traveling_mode: The traveling mode that the user prefers. E.g.: driving
    :return: A list of all steps, each step is a string.
    """
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&key={api_key}"
    response = requests.get(url)

    # Parse the JSON response
    result = response.json()
    if result['status'] == 'OK':
        # print("OK")
        # Extract the steps from the first route
        route = result["routes"][0]
        legs = route["legs"]
        steps = [step for leg in legs for step in leg["steps"]]

        directions = []
        for i, step in enumerate(steps):
            if step['html_instructions'] == "Head":
                step_str = f"Step {i + 1}: Stay at your location"
            else:
                step_str = f"Step {i + 1}: {step['html_instructions']}"
            # get rid of <div ...> and </div>
            deleted_div_step = re.sub(r'<div.*?>|</div>', '', step_str)
            # get rid of <b> </b>
            deleted_b_step = re.sub(r'<\/?b>', '', deleted_div_step)
            deleted_wbr_step = re.sub(r'<wbr\s?\/?>', ' ', deleted_b_step)
            directions.append(deleted_wbr_step)
        return directions
    else:
        return []

#
# if __name__ == "__main__":
#     # Define the starting and ending addresses
#     origin_m = '42.3645558,-71.1359136' #  Worked: 42.3645558,-71.1359136
#     destination_m = "42.34993389999999, -71.1027624"  # "42.34993389999999, -71.1027624"
#
#     #42.3465259, 42.3465259
#     #42.3493136, -71.0781875
#
#
#     # Define the mode of transportation
#     mode = "driving"
#     d = get_direction_from_one_place_to_another(origin_m, destination_m, mode)
#     print(d)
