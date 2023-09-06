## PopUpTrip-AWS-Backend

### Introduction
 This is the backend development for the Android app PopUpTrip. It is a FastAPI application that have HTTP
 requests for adding itineraries, getting a user's all itineraries, and calculating the optimized route for one 
 itinerary and getting its direction steps
 

### Architecture

<img width="882" alt="architecture" src="https://github.com/lianghuanjia/501Backend/assets/36748450/47e7845a-6c9c-4c68-98b4-af13a72280fa">

Image stored in Google drive if the image above is not working: https://drive.google.com/file/d/1g6IOZsVVVB0GN9iJT5mwWB3H5ahZq7nq/view?usp=share_link 

Brief introduction:
The application uses FastAPI framework, built APIs using Python, and do CRUD operations to AWS RDS MySQL database 
using SQLAlchemy ORM to make SQL operations easier and prevent database injection. The application itself is deployed
in an AWS EC2 Instance.


### API Usage:
1. Google Map Distance Matrix API
2. Google Map Direction API

### PopUpTrip Android frontend:
https://github.com/whisperzh/PopUpTrip
