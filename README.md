# ILP API
Server Side ILP API

This is writen in Python Flask and integrates with MongoDB

This was writen for a school project and is the back end of our project display website.

# Install
To install this and run it yourself you must first:

- Install Python3

  - Install `flask` and `pymongo`

- Install MongoDB

  - Create an ilp database

  - Create a user who has permissions for the database

  - Write this information into config.json e.g. `{
    "mongodb": {
        "host": "localhost",
        "username": "ilpUser",
        "password": "5ECUR3P@55W0RD"
    }
}`
