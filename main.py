import sqlite3
import bcrypt # type: ignore
from datetime import datetime
import csv

time_now = datetime.now()

(time_now.strftime("%x"), time_now.strftime("%X"))


connection = sqlite3.connect('capstone-database.db')

cursor = connection.cursor()


# with open("create_queries.txt", "r") as readfile:
#     create_queries = readfile.read()
    
#     cursor.executescript(create_queries)
    
    # if not user_check:
    
    
def login():
    while True: 
        print("--- Welcome to the Capstone! You must log in. ---\n")
        email = input("Please enter your email address: ")
        

        email_check = cursor.execute("SELECT email FROM Users WHERE email = ? AND active = 1",(email,)).fetchone()
        
        
        inactive_user = cursor.execute("SELECT email FROM Users WHERE email = ? AND active = 0",(email,)).fetchone()
        
        
        if not email_check and not inactive_user:
            email_input = input("No email found. Please press enter to try again or 'E' to exit: ")
            if email_input == "E" or email_input == "e":
                    print("You have selected exit. Goodbye!")
                    exit()
            else: 
                continue
            
        if email_check:
            print("Email confirmed!")
            
        
        if inactive_user:
            print("Your user is currently inactive. Goodbye!")
            exit()
            
                    
        original_password = cursor.execute("SELECT password FROM Users WHERE email = ? AND active = 1", (email,)).fetchone()

        user_input_password = input("Please enter your password here: ")
        
    
       
        if bcrypt.checkpw(user_input_password.encode('utf-8'), original_password[0]):
            print("Access Granted!")
       
        else:
            denied_input = input("Access Denied. Please press enter to try again or 'E' to exit: ")
            if denied_input == "E" or denied_input == "e":
                exit()
            else:
                return
            
        user_type = cursor.execute("SELECT user_id, user_type FROM Users WHERE email = ?", (email,)).fetchone()

        if user_type[1] == "user":
                print("You are currently a user.")
                user_menu(user_type[0])
        elif user_type[1] == "manager":
                input("Welcome Manager.")
                manager_menu(user_type[0])

        # user_type = cursor.execute("SELECT user_type FROM Users")
        
     
            
        # elif user_type == "manager":
        
# def user_menu():
    
    
    
    
# def manager_menu():

    
def add_user():
    
    time_now = datetime.now().strftime("%x")
    
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    phone = input("Please enter your phone number: ")
    email = input("Please enter your email address: ")
    existing_user = cursor.execute("SELECT email FROM Users WHERE email = ?", (email,)).fetchone()
    if existing_user:
        print("That email address is already in use. Please try again with a different email.")
        return
    password = input("Please enter your password: ") 
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    date_created = time_now
    hire_date = time_now
    user_type = input("Please enter [1] for Manager and [2] for User: ")
    if user_type == "1":
        user_type = 'manager'
    elif user_type == "2":
        user_type = 'user'
    else:
        print("Incorrect Input. Try again.")
        return
    
    query = "INSERT INTO Users (first_name, last_name, phone, email, password, date_created, hire_date, user_type) values(?,?,?,?,?,?,?,?)"
    values = (first_name, last_name, phone, email, password, date_created, hire_date, user_type)
    
    cursor.execute(query, values)
    
    connection.commit()
  
    
    input("Successfully added new user!")
    

def add_competency():
    
    time_now = datetime.now().strftime("%x")
    
    name = input("Please enter the name of your competency subject: ")
    date_created = time_now
    
    query = "INSERT INTO Competencies (name, date_created) values(?,?)"
    
    values = (name, date_created)
    
    cursor.execute(query, values)
    
    connection.commit()
    
    input("Your competency subject has successfully been added!")    
   
 
def add_assessment():
     
    time_now = datetime.now().strftime("%x")
    

    
    competency_id = input("Please enter the competency id:  ")
    
    
    if not cursor.execute("SELECT * FROM Competencies WHERE competency_id = ?",(competency_id,)).fetchone():
        input("Invalid Competency ID.")
        return
    
    name = input("Please enter the name of the assessment: ")
    date_created = time_now
    
    
    query = "INSERT INTO Assessments (competency_id, name, date_created) values(?,?,?)"
    values = (competency_id, name, date_created)
    
    cursor.execute(query, values)
    
    connection.commit()
    
    print("Success! Your assessment has been added to your competency.")
   
   
   
def assessment_result():
    
    user_id = input("Please enter your user id: ")
    assessment_id = input("Please enter the assessment id: ")
    score = input("Please enter your score: ")
    date_taken = input("Please enter the date taken MM/DD/YY: ")
    manager_id = input("Please enter the manager id that administered the test: ")
    
    if not cursor.execute("SELECT * FROM Users WHERE user_id = ?",(user_id,)).fetchone():
        input("Invalid User ID.")
        return
    
    if not cursor.execute("SELECT * FROM Assessments WHERE assessment_id = ?",(assessment_id,)).fetchone():
        input("Invalid Assessment ID.")
        return
    
    if not cursor.execute("SELECT * FROM Users WHERE user_id = ? AND user_type = 'manager'",(manager_id,)).fetchone():
        input("Invalid Manager ID.")
        return
    
    query = "INSERT INTO AssessmentResults (user_id, assessment_id, score, date_taken, manager_id) values(?,?,?,?,?)"
    
    values = (user_id, assessment_id, score, date_taken, manager_id)

    cursor.execute(query, values)
    
    connection.commit()
    
    input("You have successfully added assessment results.")    
    
    
def edit_user_manager():
    
    user_id = input("Please enter the user id you would like to edit: ")
    
    if not cursor.execute("SELECT * FROM Users WHERE user_id = ?",(user_id,)).fetchone():
        input("Invalid User ID.")
        return
    
    user_input = input("What would you like to edit? Please enter one of the following: First Name, Last Name, Phone, Email, Password, Deactivate, Reactivate: \n").lower()
    
    if user_input not in ['first name', 'last name', 'phone', 'email', 'password', 'deactivate', 'reactivate']:
            input("Incorrect input. Please try again.")
            return
        
    if user_input == 'first name':
        first_name = input("Please enter your new first name: ")
        cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (first_name, user_id))
        connection.commit()
        input("Your first name has been updated.")
        
    elif user_input == 'last name':
        last_name = input("Please enter your new last name: ")
        cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (last_name, user_id))
        connection.commit()
        input("Your last name has been updated.")
        
    elif user_input == 'phone':
        phone = input("Please enter your new phone number: ")
        cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?", (phone, user_id))
        connection.commit()
        input("Your phone number has been updated.")
        
    elif user_input == 'email':
        email = input("Please enter your new email address: ")
        existing_user = cursor.execute("SELECT email FROM Users WHERE email = ?", (email,)).fetchone()
        if existing_user:
            print("That email address is already in use. Please try again with a different email.")
            return
        cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?", (email, user_id))
        connection.commit()
        input("Your email address has been updated.")
        
           
    elif user_input == 'password':
        password = input("Please enter your new password: ")
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (password, user_id))
        connection.commit()
        input("Your password has been successfully updated.")
    
    elif user_input == 'deactivate':
        while True:  
            confirmation = input("Are you sure you would like to deactivate your user? Y/N: ").lower()
                
            if confirmation == "y":
                    cursor.execute("UPDATE Users SET active = 0 WHERE user_id = ?", (user_id,))
                    connection.commit()
                    input("You have successfully deactivated your user.")
                    break
            if confirmation == "n":
                    print("You have selected no to deactivation. Now exiting.")
                    break
            else:
                print("You must enter in Y or N. Please try again.")
                
    elif user_input == 'reactivate':
           while True:  
            confirmation = input("Are you sure you would like to reactivate your user? Y/N: ").lower()
                
            if confirmation == "y":
                    cursor.execute("UPDATE Users SET active = 1 WHERE user_id = ?", (user_id,))
                    connection.commit()
                    input("You have successfully reactivated your user.")
                    break
            if confirmation == "n":
                    print("You have selected no to reactivation. Now exiting.")
                    break
            else:
                print("You must enter in Y or N. Please try again.")
              
    
    
def edit_competency():
    
    competency_id = input("Please enter the competency id you would like to edit: ")
    
    user_input = input("What would you like to edit? Enter one of the following: 'Name' or 'Date Created': ").lower()
    
    
    if user_input not in ['name', 'date created']:
        input("Incorrect input. Please try again.")
        return
    
    if user_input == "name":
        name = input("Please enter the new name for your competency: ")
        cursor.execute("UPDATE Competencies SET name = ? WHERE competency_id = ?", (name, competency_id))
        connection.commit()
        input("You have successfully updated your competency name.")
        
        
    elif user_input == "date created":
        date_created = input("Please enter in the updated date created you would like: ")
        cursor.execute("UPDATE Competencies SET date_created = ? WHERE competency_id = ?", (date_created, competency_id))
        connection.commit()
        input("You have succesfully updated your competency date.")
        
        
        
def edit_assessment():
    assessment_id = input("Please enter the assessment id you would like to edit: ")
    
    user_input = input("What would you like to edit: Please enter one of the following: 'Name' or 'Date Created': ").lower()
    
    if user_input not in ['name', 'date created']:
        input("Incorrect input. Please enter one of the following: 'Name' or 'Date Created'")
        return
    
    if user_input == "name":
        name = input("Please enter in the new name for your assessment: ")
        cursor.execute("UPDATE Assessments SET name = ? WHERE assessment_id = ?", (name, assessment_id))    
        connection.commit()
        input("You have successfully renamed your assessment.")
        
    elif user_input == "date created":
        date_created = input("Please enter in the new date created for your assessment: ")
        cursor.execute("UPDATE Assessments SET date_created = ? WHERE assessment_id = ?", (date_created, assessment_id))
        connection.commit()
        input("You have successfully updated the date for your assessment.")
    
    

def edit_results():
    result_id = input("Please enter your result id: ")
    user_id = input("Please enter your user id: ")
    assessment_id = input("Please enter in the assessment id: ")
    
    user_input = input("What would you like to edit? 'Score', 'Date Taken', 'Manager': ").lower()
    
    if user_input not in ['score', 'date taken', 'manager']:
        input("Invalid input. Please enter one of the given choices.")
        return
    
    
    if user_input == "score":
        score = input("Please enter in your new score: ")
        cursor.execute("UPDATE AssessmentResults SET score = ? WHERE result_id = ? AND user_id = ? AND assessment_id = ?", (score, result_id, user_id, assessment_id))
        connection.commit()
        input("You have succesfully updated your assessment score.")
        
    elif user_input == "date taken":
        date_taken = input("Please enter in the updated date taken in this format MM/DD/YY: ")
        cursor.execute("UPDATE AssessmentResults SET date_taken = ? WHERE result_id = ? AND user_id = ? AND assessment_id = ?", (date_taken, result_id, user_id, assessment_id))
        connection.commit()
        input("You have succesfully updated the date taken for your assessment.")
        
    elif user_input == "manager":
        manager_id = input("Please enter in the updated manager id: ")
        cursor.execute("UPDATE AssessmentResults SET manager_id = ? WHERE result_id = ? AND user_id = ? AND assessment_id = ?", (manager_id, result_id, user_id, assessment_id))
        connection.commit()
        input("You have successfully updated the manager for your assessment.")
        

def delete_assessment_result():
   while True:  
            confirmation = input("Are you sure you would like to delete an assessment result? (Y)es or (N)o: ").lower()
                
            if confirmation == "y":
                    result_id = input("Please enter in the result id of the assessment result or (N) to exit: ").lower()
                    if result_id == "n":
                        print("You have chosen to exit.")
                        break
                    cursor.execute("DELETE FROM AssessmentResults WHERE result_id = ?", (result_id,))
                    connection.commit()
                    input("You have successfully deleted your Assessment Results.")
                    break
            if confirmation == "n":
                    print("You have selected no to deletion. Now exiting.")
                    break
            else:
                print("You must enter in (Y)es or (N)o. Please try again.")
          
def view_users():
    users = cursor.execute("SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users").fetchall()
    print("~~~ All Users ~~~")
    print(f'{"user_id":<9} {"first_name":<12} {"last_name":<12} {"phone":<15} {"email":<20} {"active":<12} {"date_created":<15} {"hire_date":<10} {"user_type":<10}')
    for user in users:
        print(f"{user[0]:<9} {user[1]:<12} {user[2]:<12} {user[3]:<15} {user[4]:<20} {user[5]:<12} {user[6]:<15} {user[7]:<10} {user[8]:<10}")
    
   
    while True:
        user_input = input("Press Enter to Return or (E) To Exit: ")
        if user_input == "":
            return
        elif user_input == "E" or user_input == "e":
                print("Exiting. Goodbye!")
                exit()
        else:
            print("Command not recognized. Please press enter to return or (E) to exit.")
            if user_input == "E" or user_input == "e":
                print("Exiting. Goodbye!")
                exit()


def user_search():
    while True:
        user_input = input("Welcome to User Search! Please enter the first or last name of the user you would like to search: \n")
        
        users = cursor.execute("SELECT user_id, first_name, last_name, phone, email, active, date_created, hire_date, user_type FROM Users WHERE first_name LIKE ? OR last_name LIKE ?",(f"%{user_input}%", f"%{user_input}%")).fetchall()

        if users == []:
            result_input = input("No results found. Press Enter To Search Again or (E) for Exit.\n")
            if result_input == "E" or result_input == 'e':
                print("Exiting! Goodbye.")
                exit()
            elif result_input == "":
                user_search()
        else:
            print("~~~ Search Results ~~~\n")
            print(f'{"user_id":<9} {"first_name":<12} {"last_name":<12} {"phone":<15} {"email":<20} {"active":<12} {"date_created":<15} {"hire_date":<10} {"user_type":<10}')
            for user in users:
                print(f"{user[0]:<9} {user[1]:<12} {user[2]:<12} {user[3]:<15} {user[4]:<20} {user[5]:<12} {user[6]:<15} {user[7]:<10} {user[8]:<10}")
    
   
       
        
        while True:
            user_input = input("Press Enter to Search Again or (E) to exit. ")
            if user_input == "":
               user_search()
            elif user_input == "E" or user_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
            else:
                print("Command not recognized. Please press enter to search or (E) to exit.")
                if user_input == "E" or user_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
  
def user_reports():
    competency_id = input("Enter the competency id you would like to view: ")
      
      
    users = cursor.execute("SELECT u.user_id, u.first_name, c.name, ar.score, MAX(ar.date_taken) FROM Users u LEFT OUTER JOIN AssessmentResults ar ON ar.user_id = u.user_id LEFT OUTER JOIN Assessments a ON ar.assessment_id = a.assessment_id LEFT OUTER JOIN Competencies c ON a.competency_id = c.competency_id WHERE c.competency_id = ? GROUP BY u.user_id", (competency_id,)).fetchall()

    if users == []:
            result_input = input("No results found. Press Enter To Search Again or (E) to exit.\n")
            if result_input == "E" or result_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
            elif result_input == "":
                user_reports()
                return
        
    else: 
        print("~~~ Competency Results ~~~\n")
        print(f'{"user_id":<9} {"first_name":<12} {"competency_name":<20} {"score":<9} {"date_taken":<20}')
        for user in users:
            print(f"{user[0]:<9} {user[1]:<12} {user[2]:<20} {user[3]:<9} {user[4]:<20}")
    
def assessment_list():
        
    user_id = input("Please enter the User ID you would like to view assessments for: ")   
    
    users = cursor.execute("SELECT u.first_name, u.last_name, a.name, ar.score, ar.date_taken FROM Users u JOIN AssessmentResults ar ON ar.user_id = u.user_id JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE u.user_id = ? ORDER BY a.competency_id;", (user_id,)).fetchall() 

    if users == []:
            result_input = input("No results found. Press Enter To Search Again or (E) to exit\n")
            if result_input == "E" or result_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
            elif result_input == "":
                assessment_list()
                return
                
    else:           
        print("~~~ Assessment Results ~~~\n")
        print(f'{"first_name":<12} {"last_name":<12} {"assessment_name":<45} {"score":<12} {"date_taken":<9}')

        for user in users:
                print(f"{user[0]:<12} {user[1]:<12} {user[2]:<45} {user[3]:<12} {user[4]:<9}")
            
        
    
def user_competency():
    
    user_id = input("Please enter the User ID you would like a competency report for: ")
    
    users = cursor.execute("SELECT c.competency_id, c.name AS competency_name, ar.score AS latest_score, MAX(ar.date_taken) AS last_taken FROM Competencies c LEFT JOIN Assessments a ON a.competency_id = c.competency_id LEFT JOIN AssessmentResults ar ON a.assessment_id = ar.assessment_id AND ar.user_id = ? GROUP BY c.competency_id", (user_id,)).fetchall()
   
    total = 0
    
    for user in users:
        total += user[2] or 0
        
    
    if users == []:
            result_input = input("No results found. Press Enter To Search Again or (E) To Exit\n")
            if result_input == "E" or result_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
            elif result_input == "":
                user_competency()
                return
    
    else:            
        print("~~~ Competency Results ~~~\n")
        print(f'Average Competency Score is: {total / len(users):.2f}')
        print(f'{"competency_name":<20} {"competency_name":<30} {"score":<12}  {"date_taken":<9}')
        for user in users:
            print(f"{user[0]:<20} {user[1]:<30} {user[2] or '':<12} {user[3] or '':<20} ")
        
    # if users == []:
    #     print("No results found.")
    #     return
    
    
    
def edit_user_user(user_id):
    
    user_input = input("What would you like to edit? Please enter one of the following: First Name, Last Name, Password\n").lower()
    
    if user_input not in ['first name', 'last name', 'password',]:
            input("Incorrect input. Please try again.")
            return
        
    
    if user_input == 'first name':
        first_name = input("Please enter your new first name: ")
        cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?", (first_name, user_id))
        connection.commit()
        input("Your first name has been updated.")
     
        
    elif user_input == 'last name':
        last_name = input("Please enter your new last name: ")
        cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?", (last_name, user_id))
        connection.commit()
        input("Your last name has been updated.")
        
    elif user_input == 'password':
        password = input("Please enter your new password: ")
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (password, user_id))
        connection.commit()
        input("Your password has been successfully updated.")

def user_assessment_data(user_id):
    
    users = cursor.execute("SELECT u.first_name, u.last_name, a.name, ar.score, ar.date_taken FROM Users u JOIN AssessmentResults ar ON ar.user_id = u.user_id JOIN Assessments a ON ar.assessment_id = a.assessment_id WHERE u.user_id = ? ORDER BY a.competency_id;", (user_id,)).fetchall() 

    if users == []:
            input("No results found. Returning to menu.\n")
            return
            # if result_input == "E" or result_input == "e":
            #         print("Exiting. Goodbye!")
            #         exit()
            # elif result_input == "":
            #     user_assessment_data(user_id)
            #     return
    else:          
        print("~~~ Assessment Results ~~~\n")
        print(f'{"first_name":<12} {"last_name":<12} {"assessment_name":<45} {"score":<12} {"date_taken":<9}')
        for user in users:
            if None in user:
                print("No results found. Returning to Menu.")
                continue 
            print(f"{user[0]:<12} {user[1]:<12} {user[2]:<45} {user[3]:<12} {user[4]:<9}")
            

def user_competency_data(user_id):
    
    
    users = cursor.execute("SELECT u.user_id, u.first_name, u.last_name, c.name, ar.score, MAX(ar.date_taken) FROM Users u LEFT OUTER JOIN AssessmentResults ar ON ar.user_id = u.user_id LEFT OUTER JOIN Assessments a ON ar.assessment_id = a.assessment_id LEFT OUTER JOIN Competencies c ON a.competency_id = c.competency_id WHERE u.user_id = ? GROUP BY c.competency_id", (user_id,)).fetchall()
    
    if users == []:
            result_input = input("No results found. Press Enter To Search Again or (E) To Exit\n")
            if result_input == "E" or result_input == "e":
                    print("Exiting. Goodbye!")
                    exit()
            elif result_input == "":
                user_competency_data(user_id)
                return
    else:        
        print("~~~ Competency Results ~~~\n")
        print(f'{"user_id":<9} {"first_name":<12} {"last_name":<12} {"competency_name":<20} {"score":<9} {"date_taken":<9}')
        for user in users:
            if None in user:
                print("No results found. Returning to Menu.")
                continue 
            print(f"{user[0]:<9} {user[1]:<12} {user[2]:<12} {user[3]:<20} {user[4]:<9} {user[5]:<9} ")
            
    
    
    
def user_menu(user_id):
    while True:
        input(f"~~~ Welcome to the User Menu! User ID: {user_id}~~~")  
        menu_input = input("[1] View My Assessment Data\n[2] View My Competency Data\n[3] Change My Password or Edit My First or Last Name\n[Q]uit\n")
        
        if menu_input == "1":
            user_assessment_data(user_id)
            
        elif menu_input == "2":
            user_competency_data(user_id)
        
        elif menu_input == "3":
            edit_user_user(user_id)
            
        elif menu_input.lower() == "q":
            print("Cya later!")
            exit()
            
        else:
            print("Invalid Input. Try again")
    
    
    
def manager_menu(user_id):
    while True:
        input(f"~~ Welcome to the Manager Menu! User ID: {user_id} ~~")
        user_input = input("[V]iew all users in a list, View Report For All Users and Competency Levels, Search For Users,\n View a Report of All Users and Their Cometency Levels For a Competency, View a List of Assessments For a Given User\n[A]dd a User, Competency, New Assessment To a Competency, or an Assessment Result for a User\n[E]dit or Deactivate User, Edit a Competency, Edit an Assessment, Edit An Assessment Result\n[D]elete An Assessment Result\n[C]SV Actions\n[Q]uit\n")

        if user_input == "A":
            print("What would you like to do?\n")
            add_input = input("[1] Add A User\n[2] Add a Competency\n[3] Add a New Assessment To a Competency\n[4] Add an Assessment Result for a User\n")  
            if add_input == "1":
                add_user()
            elif add_input == "2":
                add_competency()
            elif add_input == "3":
                add_assessment()
            elif add_input == "4":
                assessment_result()
            else:
                print("Invalid Input. Try again")

        elif user_input == "V":
            print("What would you like to do?")
            new_input = input("[1] View All Users In A list\n[2] Search For Users\n[3] View a Report of All Users and Their Cometency Levels For a Competency\n[4] View a Competency Level Report For an Individual User\n[5] View a List of Assessments For a Given User\n")
            if new_input == "1":
                view_users()
            elif new_input == "2":
                user_search()
            elif new_input == "3":
                user_reports()
            elif new_input == "4":
                user_competency() 
            elif new_input == "5":
                assessment_list()
            else:
                print("Invalid Input. Try again")

        elif user_input == "E":
            print("What would you like to do?\n")
            edit_input = input("[1] Edit or Reactivate/Deactivate User, [2] Edit a Competency, [3] Edit an Assessment, [4] Edit An Assessment Result\n")
            if edit_input == "1":
                edit_user_manager()
            elif edit_input == "2":
                edit_competency()
            elif edit_input == "3":
                edit_assessment()
            elif edit_input == "4":
                edit_results()
            else:
                print("Invalid Input. Please Try Again.")

        elif user_input == "D":
            delete_assessment_result()

        elif user_input == "C":
            print("What would you like to do? CSV Actions\n")
            csv_input = input("[1] Competency Report by Competency and Users [2] Competency Report For a Single User [3] Import Assessment Results From CSV\n")
            if csv_input == "1":
                competency_report_competency()
            elif csv_input == "2":
                competency_report_user()
            elif csv_input == "3":
                import_csv_data()
            else:
                print("Invalid Input. Try again")

        elif user_input.lower() == "q":
            print("Cya later!")
            exit()

        else:
            print("Invalid Input. Please Try Again.")





def competency_report_user():
    user_id = input("Please enter in the User ID you would like to see a competency report for: ")
    users = cursor.execute("SELECT u.user_id, u.first_name, u.last_name, c.name, ar.score, MAX(ar.date_taken) FROM Users u LEFT OUTER JOIN AssessmentResults ar ON ar.user_id = u.user_id LEFT OUTER JOIN Assessments a ON ar.assessment_id = a.assessment_id LEFT OUTER JOIN Competencies c ON a.competency_id = c.competency_id WHERE u.user_id = ? GROUP BY c.competency_id", (user_id,)).fetchall()
    # print(users)
    header = ['user_id', 'first_name', 'last_name', 'competency name', 'score', 'date_taken']
    if users:
        with open('users.csv', 'w') as outfile:
            wrt = csv.writer(outfile)
            wrt.writerow(header)
            wrt.writerows(users)
        print("Competency Report saved as 'users.csv'.")
    else:
        print("No data found for that competency.")





def competency_report_competency():
    competency_id = input("Please enter in the competency ID you would like to see a report for: ")

    results = cursor.execute("SELECT u.user_id, u.first_name, u.last_name, c.name, ar.score, ar.date_taken FROM Users u JOIN AssessmentResults ar ON u.user_id = ar.user_id JOIN Assessments a ON ar.assessment_id = a.assessment_id JOIN Competencies c ON a.competency_id = c.competency_id WHERE c.competency_id = ? ORDER BY u.user_id", (competency_id,)).fetchall()
    header = ['user_id', 'first_name', 'last_name', 'competency_name', 'score', 'date_taken']
    if results:
        with open('competency_report.csv', 'w') as outfile:
            wrt = csv.writer(outfile)
            wrt.writerow(header)
            wrt.writerows(results)
        print("Competency report saved as 'competency_report.csv'.")
    else:
        print("No data found for that competency.")



def import_csv_data():
    data_list = []
    
    with open('ar-data.csv', 'r') as outfile:
        csvreader = csv.reader(outfile)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)
            
        
    query = ("INSERT INTO AssessmentResults (user_id, assessment_id, score, date_taken, manager_id) values(?,?,?,?,?)")
    for row in data_list:
        cursor.execute(query,row)
    
    connection.commit()
    print("You have successfully imported results!")
    
    

while True:
    login()
    
    
    

# competency_report_user()

# competency_report_competency()
