# Welcome To My Capstone Project!

## How To Use My Project: 

## Ensure you are in a pipenv shell and you have the proper packages installed:
import sqlite3
import bcrypt
from datetime import datetime
import csv

## Login Credentials

Here are the log in credentials to test my app:

Manager:
- Email: lacy@test.com
- Password: lacy123

User:
- Email: lorelai@test.com
- Password: lorelai123

## You Must First Log In To Access The Features Of My App. Use Manager Log In Credentials to View the Manager Menu and Features,
## Or User Log In Credentials to View the User Menu and Features

## Once logged in, you can navigate through the different menus with your input. For users, there are 4 menu options:
- [1] View My Assessment Data
- [2] View My Competency Data
- [3] Change My Password or Edit My First or Last Name
- [Q]uit

## If logged in with the manager credentials you can view the manager menu which has these options. Each entry then goes to a submenu with the actions listed.
[V]iew all users in a list, View Report For All Users and Competency Levels, Search For Users, View a Report of All Users and Their Cometency Levels For a Competency, View a List of Assessments For a Given User
[A]dd a User, Competency, New Assessment To a Competency, or an Assessment Result for a User
[E]dit or Deactivate User, Edit a Competency, Edit an Assessment, Edit An Assessment Result
[D]elete An Assessment Result
[C]SV Actions
[Q]uit



## Features of My Project

### Login and Logout
- My program tracks user emails and passwords to allow for secure login.
- Passwords are hashed so they are not stored in the database.
- Allows you to try again if you enter in a wrong email or password.
- Does not allow inactive users to log in.
- User log in and manager log in have access to different menu interfaces.
- Takes in your User ID at log in for the user menu interface so users can't access other users information.
- Only allows managers to be able to add managers.

## User Types and Access

### User
A user is an individual that can:
- View their OWN and ONLY THEIR OWN competency and assessment data.
- Edit their OWN AND ONLY THEIR OWN user data such as changing their name and editing their password.

### Manager
A manager is an individual that can manage users. They can:

#### View
- All users in a list
- Search for users by first name or last name
- View a report of all users and their competency levels for a given competency
- View a competency level report for an individual user
- View a list of assessments for a given user

#### Add
- Add a user
- Add a new competency
- Add a new assessment to a competency
- Add an assessment result for a user for an assessment (record test results)
- When a new user is added with the same email, I added exception handling to print out an error as the email field is UNIQUE.

#### Edit
- Edit a user's information
- When a user's information is edited with the same email, I added exception handling to print out an error as the email field is UNIQUE.
- Edit a competency
- Edit an assessment
- Edit an assessment result

#### Delete
- Delete an assessment result
- Added in two steps of confirmation where if "N" entered, you can leave the deletion at anytime.

## Export Reports to CSV
- Competency report by competency and users
- Competency report for a single user

## Import Assessment Results from CSV
- Ability to import assessment results from a CSV file
- The CSV file should contain columns: user_id, assessment_id, score, date_taken
- I also added in manager_id to be consistent with the assessment results that are already in the AR table.

# Exception Handling
- Exception Handling is included in ALL of the functions and menu interfaces where if the user enters in something unknown,
- it will automatically print an error statement and ask you to try again/exit/return to the main menu.
- I also added in FOREIGN KEY checks where if the user tries to add an assessment id, or something else that doesn't exist, for example, it will error and let you know. 

