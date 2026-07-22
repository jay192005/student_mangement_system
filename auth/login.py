import mysql.connector
import getpass  # This built-in module hides the password while typing

def login(username, password):
    """
    Authenticates a user by checking the MySQL database.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",                     # Update with your MySQL user
            password="Jay@2005",  # Update with your MySQL password
            database="new_aims"               # Update with your database name
        )
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return True, f"\nLogin successful! Welcome {user['username']} (Role: {user['role']})."
        else:
            return False, "\nInvalid username or password."

    except mysql.connector.Error as err:
        return False, f"\nDatabase error: {err}"
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def start_system():
    """
    This function runs the interactive login screen.
    """
    print("================================")
    print("    Welcome to new-AIMS         ")
    print("================================")
    
    # 1. Ask the user to enter data
    entered_username = input("Enter your username: ")
    
    # 2. Ask for password (getpass hides what they type)
    entered_password = getpass.getpass("Enter your password: ")
    
    # 3. Pass the entered data to the login function
    is_success, result_message = login(entered_username, entered_password)
    
    print(result_message)
    
    if is_success:
        print("\n--> Loading the main dashboard...")
        # Here is where you would call your next function, like showing the menu
    else:
        print("\n--> Access Denied. Please try again.")

# When you run this file, it will now ask for input
if __name__ == "__main__":
    start_system()