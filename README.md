Documentation:
Utilizing Flask-Swagger and Flask-Swagger-UI Document Each Route of your API. Each Route Requires:

Path:
Endpoint
Type of request (post, get, put, delete)
tag (category for the route)
summary
description
security: Points to the security definition (Only need this for token authenticated routes)
parameters: Information about what the data the route requires(Only required for POST and PUT request)
responses: Information about what the data  route returns (Should include examples)
Definition(s):
PayloadDefinition: Defines the "Shape" of the incoming data (Only required for POST and PUT requests)
ResponseDefinitions: Defines the "Shape" of the outgoing data 
Testing:

Utilizing the built-in unittest library:
Create a tests folder inside you project folder
Create a test file for each of your blueprints (test_mechanics.py, test_customers.py, etc.) inside the tests folder
Create one test for every route in your API.
incorporate negative tests in your testing.
