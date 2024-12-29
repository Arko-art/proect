import mysql.connector
import time
from getpass import getpass

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="DAVBank"
)
cursor = conn.cursor()

# Welcome Screen
print("=== Welcome to DAV Bank ===")
time.sleep(1)

while True:
    print("=== Main Menu ===")
    print("1. Create Account")
    print("2. Login to Your Account")
    print("3. Exit")
    
    choice = int(input("Enter your choice: "))
    
    if choice == 1:
        print("=== Account Creation ===")
        username = input("Enter a username: ")
        password = getpass("Enter a password: ")
        account_type = input("Enter account type (Savings/Current): ")
        initial_deposit = float(input("Enter initial deposit (min 5000): "))
        
        if initial_deposit >= 5000:
            cursor.execute("""
                INSERT INTO accounts (username, password, account_type, balance) 
                VALUES (%s, %s, %s, %s)
            """, (username, password, account_type, initial_deposit))
            conn.commit()
            print("Account created successfully!")
        else:
            print("Minimum initial deposit is 5000. Try again.")
    
    elif choice == 2:
        print("=== Account Login ===")
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        
        cursor.execute("""
            SELECT * FROM accounts WHERE username = %s AND password = %s
        """, (username, password))
        account = cursor.fetchone()
        
        if account:
            print("\033[1;32mLogin successful!\033[0m")
            while True:
                print("=== Account Dashboard ===")
                print("1. View Account Details")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Issue Credit Card")
                print("5. Issue Debit Card")
                print("6. Logout")
                
                sub_choice = int(input("Enter your choice: "))
                
                if sub_choice == 1:
                    print("=== Account Details ===")
                    print(f"Account ID: {account[0]}")
                    print(f"Username: {account[1]}")
                    print(f"Account Type: {account[3]}")
                    print(f"Balance: ₹{account[4]}")
                    print(f"Credit Card Issued: {bool(account[5])}")
                    print(f"Debit Card Issued: {bool(account[6])}")
                
                elif sub_choice == 2:
                    amount = float(input("Enter amount to deposit: "))
                    cursor.execute("""
                        UPDATE accounts SET balance = balance + %s WHERE account_id = %s
                    """, (amount, account[0]))
                    conn.commit()
                    print("Deposit successful!")
                
                elif sub_choice == 3:
                    amount = float(input("Enter amount to withdraw: "))
                    if amount <= account[4]:
                        cursor.execute("""
                            UPDATE accounts SET balance = balance - %s WHERE account_id = %s
                        """, (amount, account[0]))
                        conn.commit()
                        print("Withdrawal successful!")
                    else:
                        print("Insufficient balance.")
                
                elif sub_choice == 4:
                    if not account[5]:
                        cursor.execute("""
                            UPDATE accounts SET credit_card_issued = TRUE WHERE account_id = %s
                        """, (account[0],))
                        conn.commit()
                        print("Credit Card issued successfully!")
                    else:
                        print("Credit Card already issued.")
                
                elif sub_choice == 5:
                    if not account[6]:
                        cursor.execute("""
                            UPDATE accounts SET debit_card_issued = TRUE WHERE account_id = %s
                        """, (account[0],))
                        conn.commit()
                        print("Debit Card issued successfully!")
                    else:
                        print("Debit Card already issued.")
                
                elif sub_choice == 6:
                    print("Logging out...")
                    break
                
                else:
                    print("Invalid choice. Try again.")
                
                # Refresh account data
                cursor.execute("""
                    SELECT * FROM accounts WHERE account_id = %s
                """, (account[0],))
                account = cursor.fetchone()
        
        else:
            print("Invalid username or password. Try again.")
    
    elif choice == 3:
        print("Thank you for using DAV Bank. Goodbye!")
        break
    
    else:
        print("Invalid choice. Try again.")

# Close connection
cursor.close()
conn.close()
