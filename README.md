## 501Backend

### Introduction
 This is the backend development for 501 Team Not Yet's final project. It is a FastAPI application that have HTTP
 requests for adding itineraries, getting a user's all itineraries, and calculating the optimized route for one 
 itinerary and getting its direction steps
 

### Architecture

<img width="567" alt="Screenshot 2023-05-09 at 2 46 26 PM" src="https://github.com/lianghuanjia/501Backend/assets/36748450/97c139ba-59b2-430b-bdb5-095cd5b5d519">

Brief introduction:
The application uses FastAPI framework, built APIs using Python, and do CRUD operations to AWS RDS MySQL database 
using SQLAlchemy ORM to make SQL operations easier and prevent database injection. The application itself is deployed
in an AWS EC2 Instance.


### API Usage:
1. Google Map Distance Matrix API
2. Google Map Direction API

### ChatGPT Usage:
1. Asked it questions about some SQLAlchemy operations
2. Asked it questions about how to use the Google Map Distance Matrix API with mode
3. Asked it how to use the Google Direction APIs to get direction steps from one place to another with specific travel 
mode
4. Asked it some Python terminal commands, such as how to load the installed requirements in the app to the 
requirements.txt
