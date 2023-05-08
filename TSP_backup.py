# import googlemaps
# import numpy as np
# from python_tsp import
#
# # Set up the Google Maps API client
# gmaps = googlemaps.Client(api_key='YOUR_API_KEY')
#
# # Define the starting point and destination
# origin = 'New York, NY'
# destination = 'Los Angeles, CA'
#
# # Get directions from the Google Maps Directions API
# route = gmaps.directions(origin, destination, mode='driving', waypoints=['Chicago, IL', 'Denver, CO', 'Las Vegas, NV'])
#
# # Extract the latitude and longitude of the waypoints from the directions response
# waypoints = [(step['start_location']['lat'], step['start_location']['lng']) for leg in route for step in leg['steps']]
#
# # Compute the distance matrix between the waypoints
# dist_matrix = np.zeros((len(waypoints), len(waypoints)))
# for i in range(len(waypoints)):
#     for j in range(len(waypoints)):
#         if i != j:
#             dist_matrix[i][j] = gmaps.distance_matrix(waypoints[i], waypoints[j], mode='driving')['rows'][0]['elements'][0]['distance']['value']
#
# # Use the branch-and-bound algorithm to solve the TSP instance
# tsp_path = tsp.tsp(dist_matrix, branch_and_bound=True)
#
# # Insert the starting point and destination into the TSP path
# tsp_path.insert(0, 0)
# tsp_path.append(len(waypoints))
#
# # Print the optimal TSP path and its total length
# print("Optimal TSP path:", [waypoints[i] for i in tsp_path])
# print("Total length:", tsp.path_cost(tsp_path, dist_matrix))
