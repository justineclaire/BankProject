# Bank Management System by Justine Langridge and Artyom McNiff!
# Program to provide a number of banking services to any particular customer who requires them
# The program stores the customer and account details into external files which are written into and read out of when
# required.
# importing datetime to be able to calculate from dates
import datetime
from datetime import date
from random import randint


class Account(object):
    def __init__(self, acc_id, iban, funds, cid, transactions):
        """Defines the parameters for Account"""
        self.acc_id = acc_id
        self.iban = iban
        self.funds = funds
        self.cid = cid
        self.transactions = self.recent_transactions()

    def recent_transactions(self):
        """Method to store the 5 most recent account transactions"""
        # making a list to store all transactions
        transac_list = []
        # reading the file and appending transactions to the list
        transac_file = ""
        try:
            transac_file = open("accountsTransactions.txt", "r")
        except IOError:
            print("Error: File could not be opened")

        for line in transac_file:
            if str(self.acc_id) in line:
                transac_list.append(line.rstrip("\n"))
        transac_file.close()
        # create a string of the 5 or less most recent transactions
        transac_str = ""
        counter = 0
        for i in reversed(transac_list):
            if counter < 5:
                counter += 1
                transac_str += "\n{}. {}".format(str(counter), i)
        # return the string to be a parameter
        return transac_str

    def checkbalance(self):
        """Method which prints the current cash balance of an Account instance"""
        print("Balance: €{:.2f}".format(float(self.funds)))

    def interestcalc(self):
        """Method which allows a user to calculate a mortgage repayment"""
        # initialising interest rate at 3%
        annual_interest = 0.03
        monthly_interest = annual_interest/12
        # display menu to user
        print("Would you like to: 1. Use our mortgage repayment calculator\n2. Calculate projected profit on savings"
              " at current interest rates")
        # while loop to ensure user only chooses out of 2 options
        while True:
            choice = input("choice: ")
            # if the user chooses to calculate mortgage repayments
            if choice == '1':
                # if the user chooses to calculate profit from their savings using current interest rates
                # ensuring property value is greater than 0
                while True:
                    # ensuring property value is a number
                    while True:
                        try:
                            # getting the user to input property value
                            print("How much did your property cost?")
                            property_val = float(input("amount: "))
                            break
                        except ValueError:
                            print("Invalid input: Please only enter numbers (don't include any commas)\n")

                    if property_val > 0:
                        break
                    else:
                        print("Invalid input: Please only enter a number greater than 0\n")

                # getting the user to input the deposit they paid
                while True:
                    # ensuring deposit paid is greater than 0 using a while loop
                    while True:
                        try:
                            # getting the user to input deposit paid
                            print("How much was the deposit that you paid?")
                            deposit_paid = float(input("amount: "))
                            break
                        except ValueError:
                            print("Invalid input: Please only enter numbers (don't include any commas)\n")

                    if deposit_paid > 0:
                        break
                    else:
                        print("Invalid input: Please only enter a number greater than 0\n")

                # getting the user to input the length of their mortgage
                while True:
                    print("What type of mortgage did you get?\n1. 30 year fixed-term")
                    print("2. 15 year fixed-term")
                    option = int(input("Please choose 1 or 2: "))
                    if option == 1:
                        months_term = 360
                        break
                    elif option == 2:
                        months_term = 180
                        break
                    else:
                        print("Invalid input: Please only enter 1 or 2\n")

                # calculate monthly payments using inputted information
                mortgage_principle = property_val - deposit_paid
                monthly_payment = mortgage_principle / months_term
                mortgage_interest = monthly_payment * monthly_interest
                monthly_payment += mortgage_interest

                # display monthly payments for mortgage to user
                print("\nYour monthly payments for this mortgage at an annual interest rate of {}% would be €{}". \
                      format(annual_interest * 100, str("{:.2f}".format(monthly_payment))))

                # break out of the while true loop
                break
            # if the user wants to calculate interest accumulated from their savings if interest rates stay the same
            elif choice == '2':
                # getting the user to input how many years they would like to calculate the profit of
                while True:
                    # ensuring years entered is greater than 0
                    while True:
                        try:
                            # getting the user to input years
                            print("After how many years would you like to see the estimated profit from your savings?"
                                  " if your balance and current interest rates remain the same")
                            years = int(input("amount: "))
                            break
                        except ValueError:
                            print("Invalid input: Please only enter a number\n")

                    if years > 0:
                        break
                    else:
                        print("Invalid input: Please only enter a number greater than 0\n")

                # calculating profit from current interest rates
                added_interest = float(self.funds) * annual_interest
                profit = added_interest * years
                new_balance = float(self.funds) + profit

                print("Calculated profit after {} years with the interest rate at {}% : {}". \
                      format(str(years), str(annual_interest * 100), str("{:.2f}".format(profit))))
                print("Your total savings would be: €{}".format(str("{:.2f}".format(new_balance))))

                # break out of the while true loop
                break
            else:
                print("Option not available. Please only enter 1 or 2.")

    def deposit(self, amount):
        """Method for a customer to deposit money to their account
            Updates the account.txt file with the new balance and timeframe
            Updates the accountsTransactions.txt file also"""

        # calculating the new balance
        result = float(self.funds) + amount

        while True:
            # confirming the amount to deposit
            confirm = input("Please confirm you would like to deposit €{}\npress y/n: ".format(amount))

            # if the user confirms, update class objects and files
            if confirm == 'y':
                print("Thank you! Deposit complete")
                old_funds = self.funds
                self.funds = result
                print("New balance: €{:.2f}".format(result))

                # adding transaction to transaction file
                transac_list = ""
                transac = self.acc_id + " +" + str(amount) + " " + str(datetime.date.today()) + " " + str(result) + "\n"
                try:
                    transac_list = open("accountsTransactions.txt", "a")
                except IOError:
                    print("File could not be opened.")
                    exit()
                transac_list.write(transac)
                transac_list.close()

                # updating account file with new balance
                accounts_list = ""
                try:
                    accounts_list = open("accounts.txt", "r")
                except IOError:
                    print("File could not be opened.")
                    exit()
                replacement = ""
                for line in accounts_list:
                    if self.acc_id and self.iban not in line:
                        replacement += line
                    elif self.acc_id and self.iban in line:
                        new_line = line.replace(str(old_funds), str(self.funds))
                        replacement += new_line
                accounts_list.close()

                try:
                    accounts_list = open("accounts.txt", "w")
                except IOError:
                    print("File could not be opened.")
                    exit()
                accounts_list.write(replacement)
                accounts_list.close()
                break
            elif confirm == 'n':
                while True:
                    no_confirm = input("Would you like to deposit another amount?\npress y/n: ")
                    if no_confirm == 'y':
                        new_amount = input("How much would you like to deposit?\namount: ")
                        self.deposit(float(new_amount))
                        break
                    elif no_confirm == 'n':
                        break
                    else:
                        print("Invalid input: Please only enter y or n")
                break
            else:
                print("Invalid input: Please only enter y or n")

            # updating recent transactions to include the new one
            self.transactions = self.recent_transactions()
            return

    def __str__(self):
        """Prints the parameters for Account"""
        result = "account id:{}\niban:{}\nbalance:{}\n".format(self.acc_id, self.iban, self.funds)
        return result

class SavingsAccount(Account):
    def __init__(self, acc_id, iban, funds, cid, transactions, timeframe):
        """Defines the parameters for SavingsAccount"""
        Account.__init__(self, acc_id, iban, funds, cid, transactions)
        nums = []
        for num in timeframe.split("-"):
            nums.append(int(num))
        self.timeframe = date(nums[0], nums[1], nums[2])

    def add_acc(self, file="accounts.txt"):
        """Adds a new bank account to the txt file """
        f = open(file, "a")
        new_acc = f"\n{self.acc_id} {self.iban} {self.funds} {self.cid} {self.timeframe} savings"
        f.write(new_acc)
        f.close()

    def transfer(self, receiver):
        """Method to allow one user to transfer funds to another and check account they wish to transfer to exists
            and update each accounts balance in the accounts.txt file
            and update the accountsTransaction.txt file for both accounts"""
        # variable to check that account exists
        check = 0
        # open file to look for account to transfer to
        acc_file = open("accounts.txt", "r")
        for line in acc_file:
            if receiver in line:
                check = 1
        acc_file.close()
        # if account cannot be found
        if check == 0:
            print("Sorry we cannot find an account linked to that IBAN please try again.")
            return
        # transfer funds if account was found
        elif check == 1:
            # calculating the amount of days since the last withdrawal/transfer
            today = datetime.date.today()
            lasttransac = self.timeframe
            limit_check = today - lasttransac
            limit_check = limit_check.days

            # checking that it has been at least 30 days since the last withdrawal/transfer
            if limit_check <= 30:
                print("It has only been {} days since your last withdrawal/transfer.".format(limit_check))
                print("Please try again once it has been at least 30 days since your last withdrawal/transfer")
                return
            # if it has been at least 30 days
            else:
                # prompt user for amount to transfer
                amount = 0.0
                try:
                    amount = float(input("How much would you like to transfer: "))
                # if an invalid value is entered call the function again until a valid number is entered
                except ValueError:
                    print("Invalid input please only enter a number")
                    self.transfer(receiver)

                # checking the user can afford to make the transfer
                result = float(self.funds) - amount
                if result < 0:
                    print("Insufficient funds: your balance is {}.\nPlease try again".format(self.funds))

                    # prompt user for amount to transfer
                    try:
                        amount = float(input("How much would you like to transfer: "))
                    # if an invalid value is entered call the function again until a valid number is entered
                    except ValueError:
                        print("Invalid input please only enter a number")
                        self.transfer(receiver)
                # transfer funds if the user can afford it
                else:
                    # updating instance variables
                    self.funds = result
                    self.timeframe = datetime.date.today()

                    # create list variables of user information to update balance and timeframe
                    acc_file = open("accounts.txt", "r")
                    other_user = ""
                    self_user = ""
                    for line in acc_file:
                        if receiver in line:
                            other_user = line.split(" ")
                        elif self.iban in line:
                            self_user = line.split(" ")
                    acc_file.close()

                    # updating balance in other user variables
                    result2 = float(other_user[2]) + amount
                    other_user[2] = str("{:.2f}".format(result2))

                    # updating balance in self
                    self_user[2] = str("{:.2f}".format(result))
                    self_user[4] = str(datetime.date.today())

                    # creating new strings to go in the file
                    replacement = ""
                    self_user = " ".join(self_user)
                    other_user2 = " ".join(other_user)

                    acc_file = open("accounts.txt", "r")
                    for line in acc_file:
                        if receiver in line:
                            replacement += other_user2
                        elif self.iban in line:
                            replacement += self_user
                        else:
                            replacement += line
                    acc_file.close()

                    # writing the updated information to the accounts.txt file
                    acc_file = open("accounts.txt", "w+")
                    acc_file.write(replacement)
                    acc_file.close()

                    # making the strings to add to the accountsTransactions.txt file
                    self_transac = self.acc_id + " -" + str(amount) + " " + str(datetime.date.today()) \
                                   + " " + str("{:.2f}".format(result)) + "\n"
                    other_transac = other_user[0].strip() + " +" + str(amount) + " " + str(datetime.date.today()) + \
                                    " " + str("{:.2f}".format(result2)) + "\n"

                    try:
                        transac_list = open("accountsTransactions.txt", "a")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    # write the new strings to the file
                    transac_list.write(self_transac)
                    transac_list.write(other_transac)
                    transac_list.close()

                    print("Thank you transfer complete!\nYour balance is now €{:.2f}".format(result))

                    # updating recent transactions to include the new one
                    self.transactions = self.recent_transactions()
                    return

    def withdraw(self, amount):
        """Method for a customer to withdraw money from their account
        Updates the account.txt file with the new balance and timeframe
        Updates the accountsTransactions.txt file also"""

        # calculating the amount of days since the last withdrawal/transfer
        today = datetime.date.today()
        lasttransac = self.timeframe
        limit_check = today - lasttransac
        limit_check = limit_check.days

        # checking that it has been at least 30 days since the last withdrawal/transfer
        if limit_check <= 30:
            print("It has only been {} days since your last withdrawal/transfer.".format(limit_check))
            print("Please try again once it has been at least 30 days since your last withdrawal/transfer")
        else:
            result = float(self.funds) - amount
            old_funds = self.funds
            old_timeframe = self.timeframe
            # checking the user can afford to take that much money out
            if result < 0:
                print("Insufficient funds")
            else:
                confirm = input("Please confirm you would like to withdraw €{}\npress y/n: ".format(amount))
                if confirm == 'y':
                    print("Thank you! Withdraw complete")

                    # updating the instance information
                    self.funds = result
                    self.timeframe = datetime.date.today()

                    # adding transaction to transaction file
                    transac = self.acc_id + " -" + str(amount) + " " + str(datetime.date.today()) + " " + str(result) \
                              + "\n"
                    try:
                        transac_list = open("accountsTransactions.txt", "a")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    transac_list.write(transac)
                    transac_list.close()
                    print(transac)

                    # updating account file with new balance
                    try:
                        accounts_list = open("accounts.txt", "r")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    replacement = ""
                    for line in accounts_list:
                        if self.acc_id and self.iban not in line:
                            replacement += line
                        elif self.acc_id and self.iban in line:
                            new_line = line.replace(str(old_funds), str(self.funds))
                            new_line = new_line.replace(str(old_timeframe), str(datetime.date.today()))
                            replacement += new_line
                    accounts_list.close()

                    try:
                        accounts_list = open("accounts.txt", "w")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    accounts_list.write(replacement)
                    accounts_list.close()

                elif confirm == 'n':
                    while True:
                        no_confirm = input("Would you like to withdraw another amount?\npress y/n: ")
                        if no_confirm == 'y':
                            new_amount = input("How much would you like to withdraw?\namount: ")
                            self.withdraw(float(new_amount))
                            break
                        elif no_confirm == 'n':
                            break
                        else:
                            print("Invalid input: Please only enter y or n")

                else:
                    print("Invalid input: Please only enter y or n")

                # updating recent transactions to include the new one
                self.transactions = self.recent_transactions()
                return

    def __str__(self):
        """Prints the parameters for SavingsAccount"""
        result = Account.__str__(self)
        return result


class CheckingAccount(Account):
    def __init__(self, acc_id, iban, funds, cid, transactions, credit_limit):
        """Defines the parameters for CheckingAccount"""
        Account.__init__(self, acc_id, iban, funds, cid, transactions)
        self.credit_limit = credit_limit

    def add_acc(self, file="accounts.txt"):
        """Adds new customer to txt file"""
        f = open(file, "a")
        new_acc = f"\n{self.acc_id} {self.iban} {self.funds} {self.cid} {self.credit_limit} checking"
        f.write(new_acc)
        f.close()

    def withdraw(self, amount):
        """Method for a customer to withdraw money from their account
            Updates the account.txt file with the new balance and timeframe
            Updates the accountsTransactions.txt file also"""
        result = float(self.funds) - amount
        if result < -(float(self.credit_limit)):
            print("Insufficient funds: credit limit reached")
            return
        else:
            while True:
                confirm = input("Please confirm you would like to withdraw €{}\npress y/n: ".format(amount))
                if confirm == 'y':
                    old_funds = self.funds
                    print("Thank you! Withdraw complete")
                    self.funds = result

                    # adding transaction to transaction file
                    transac = self.acc_id + " -" + str(amount) + " " + str(datetime.date.today()) +  \
                              " " + str("{:.2f}".format(result)) + "\n"
                    try:
                        transac_list = open("accountsTransactions.txt", "a")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    transac_list.write(transac)
                    transac_list.close()
                    print(transac)

                    # updating account file with new balance
                    try:
                        accounts_list = open("accounts.txt", "r")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    replacement = ""
                    for line in accounts_list:
                        if self.acc_id and self.iban not in line:
                            replacement += line
                        elif self.acc_id and self.iban in line:
                            new_line = line.replace(str(old_funds), str("{:.2f}".format(self.funds)))
                            replacement += new_line
                    accounts_list.close()

                    try:
                        accounts_list = open("accounts.txt", "w")
                    except IOError:
                        print("File could not be opened.")
                        exit()
                    accounts_list.write(replacement)
                    accounts_list.close()
                    break
                elif confirm == 'n':
                    while True:
                        no_confirm = input("Would you like to withdraw another amount?\npress y/n: ")
                        if no_confirm == 'y':
                            new_amount = input("How much would you like to withdraw?\namount: ")
                            self.withdraw(float(new_amount))
                            break
                        elif no_confirm == 'n':
                            break
                        else:
                            print("Invalid input: Please only enter y or n")
                    break
                else:
                    print("Invalid input: Please only enter y or n")

            # updating recengt transactions to include the new one
            self.transactions = self.recent_transactions()
            return

    def __str__(self):
        """Prints the parameters for CheckingAccount"""
        result = Account.__str__(self)
        result += "\ncredit limit{}".format(self.credit_limit)
        return result

    def transfer(self, receiver):
        """Method to allow one user to transfer funds to another, Check account they wish to transfer to exists
            Update each accounts balance in the accounts.txt file
            Update the accountsTransaction.txt file for both accounts"""

        # variable to check that account exists
        check = 0

        # open file to look for account to transfer to
        acc_file = open("accounts.txt", "r")
        for line in acc_file:
            if receiver in line:
                check = 1
        acc_file.close()
        # if account cannot be found
        if check == 0:
            print("Sorry we cannot find an account linked to that IBAN please try again.")
            return
        # transfer funds if account was found
        elif check == 1:
            # prompt user for amount to transfer
            try:
                amount = float(input("How much would you like to transfer: "))
            # if an invalid value is entered call the function again until a valid number is entered
            except ValueError:
                print("Invalid input please only enter a number")
                self.transfer(receiver)

            # checking the user can afford to make the transfer
            result = float(self.funds) - amount
            if result < 0:
                print("Insufficient funds: your balance is {}.\nPlease try again".format(self.funds))
                # prompt user for amount to transfer
                try:
                    amount = float(input("How much would you like to transfer: "))
                # if an invalid value is entered call the function again until a valid number is entered
                except ValueError:
                    print("Invalid input please only enter a number")
                    self.transfer(receiver)
            # transfer funds if the user can afford it
            else:
                # create list variables of user information to update balance and timeframe
                acc_file = open("accounts.txt", "r")
                for line in acc_file:
                    if receiver in line:
                        other_user = line.split(" ")
                    elif self.iban in line:
                        self_user = line.split(" ")
                acc_file.close()

                # update instance information
                self.funds = result

                # updating balance in other user variables
                result2 = float(other_user[2]) + amount
                other_user[2] = str("{:.2f}".format(result2))

                # updating balance in self
                self_user[2] = str("{:.2f}".format(result))

                # creating new strings to go in the file
                replacement = ""
                self_user = " ".join(self_user)
                other_user2 = " ".join(other_user)

                acc_file = open("accounts.txt", "r")
                for line in acc_file:
                    if receiver in line:
                        replacement += other_user2
                    elif self.iban in line:
                        replacement += self_user
                    else:
                        replacement += line
                acc_file.close()

                # writing the updated information to the accounts.txt file
                acc_file = open("accounts.txt", "w+")
                acc_file.write(replacement)
                acc_file.close()

                # making the strings to add to the accountsTransactions.txt file
                self_transac = self.acc_id + " -" + str(amount) + " " + str(datetime.date.today()) \
                               + " " + str("{:.2f}".format(result)) + "\n"
                other_transac = other_user[0].strip() + " +" + str(amount) + " " + str(datetime.date.today()) \
                                + " " + str("{:.2f}".format(result2)) + "\n"

                try:
                    transac_list = open("accountsTransactions.txt", "a")
                except IOError:
                    print("File could not be opened.")
                    exit()
                # write the new strings to the file
                transac_list.write(self_transac)
                transac_list.write(other_transac)
                transac_list.close()
                print("Thank you transfer complete!\nYour balance is now €{:.2f}".format(result))
                # updating recent transactions to include the new onw
                self.transactions = self.recent_transactions()


class Customer(object):
    def __init__(self, cust_id, fname, surname, age, no_of_accounts,
                 password):
        """Defines the parameters for Customer"""
        self.cust_id = cust_id
        self.fname = fname
        self.surname = surname
        self.age = age
        self.no_of_accounts = no_of_accounts
        self.password = password

    def __str__(self):
        """Prints the parameters of Customer"""
        result = "name:{} {}\nage:{}\naccounts:{}\npassword:{}\n" . \
            format(self.fname, self.surname, self.age, self.no_of_accounts,
                   self.password)
        return result

    def add_cust(self, file="customers.txt"):
        """Adds a customer to the txt files"""
        # Opens the file in append mode
        f = open(file, "a")
        new_cust = f"\n{self.cust_id} {self.fname} {self.surname} {self.age} {self.no_of_accounts} {self.password}"
        f.write(new_cust)
        f.close()

    def update_cust(self, file, flag):
        """Updates the number of accounts the customer has after
        creating or deleting an account"""
        f1 = open(file, "r")

        # if account is created
        if flag == 0:
            # reverting number to previous state
            old_num = int(self.no_of_accounts) - 1
        # if account is deleted
        elif flag == 1:
            # reverting number to previous state
            old_num = int(self.no_of_accounts) + 1

        # converting back to string for replace call
        self.no_of_accounts = str(self.no_of_accounts)
        update = ""
        for line in f1:
            if self.cust_id in line:
                # replaces old number of accounts with new number of accounts
                col = line.strip().split(" ")
                edit = col[0] + " " + col[1] + " " + col[2] + " " + col[3] + \
                       " " + col[4].replace(str(old_num), self.no_of_accounts) \
                       + " " + col[5] + "\n"
                update += edit
            else:
                update += line
        f1.close()

        # reopening file in order to write to it
        f2 = open(file, "w")
        f2.write(update)
        f2.close()


class Card(object):
    def __init__(self, card_num, expr_date, cvv, pin, a_id):
        self.card_num = card_num
        self.expr_date = expr_date
        self.cvv = cvv
        self.pin = pin
        self.a_id = a_id

    def __str__(self):
        result = "Card number {}\nExpiration date {}\nCVV {}\nPIN {}\n". \
            format(self.card_num, self.expr_date, self.cvv, self.pin)
        return result


class CreditCard(Card):
    def __init__(self, card_num, expr_date, cvv, pin, a_id, card_type="credit"):
        Card.__init__(self, card_num, expr_date, cvv, pin, a_id)
        self.card_type = card_type

    def add_card(self, file="cards.txt"):
        """Adds a new card to the txt file"""
        f = open(file, "a")
        new_card = f"\n{self.card_num} {self.expr_date} {self.cvv} {self.pin} {self.a_id} {self.card_type}"
        f.write(new_card)
        f.close()

    def __str__(self):
        result = Card.__str__(self)
        result += "Card type {}\n".format(self.card_type)
        return result


class DebitCard(Card):
    def __init__(self, card_num, expr_date, cvv, pin, a_id, card_type="debit"):
        Card.__init__(self, card_num, expr_date, cvv, pin, a_id)
        self.card_type = card_type

    def add_card(self, file="cards.txt"):
        """Adds a new card to the txt file"""
        f = open(file, "a")
        new_card = f"\n{self.card_num} {self.expr_date} {self.cvv} {self.pin} {self.a_id} {self.card_type}"
        f.write(new_card)
        f.close()

    def __str__(self):
        result = Card.__str__(self)
        result += "Card type{}\n".format(self.card_type)
        return result


def returningcust():
    """function to create objects for returning customers by
    finding their information by opening the text files customers.txt,
    accounts.txt, accountsTransactions.txt"""
    flag = 0
    # asking the user to input their customer id
    while True:
        cust_id = input("Please enter your User id: ")
        if cust_id == "":
            print("\nError: Cannot enter a blank value\n")
        if len(cust_id) != 3:
            print("\nError: Customer id must be 3 digits long\n")
        else:
            # break out of loop if correct format of id entered
            break

    try:
        customers_list = open("customers.txt", "r")
    except IOError:
        print("File could not be opened.")
        exit()

    for line in customers_list:
        if cust_id in line:
            # creating the account object
            print("User found successfully")
            cust_params = line.strip().split(" ")
            cust = Customer(cust_params[0],  cust_params[1],
                            cust_params[2], cust_params[3],
                            cust_params[4], cust_params[5])
            # variable to indicate account exists
            flag = 1
    # if account exists ask for user password
    if flag == 1:
        pass_check = ""
        pass_limit = 4
        # while the passwords don't match up and the user still has attempts left
        while pass_check != cust.password and pass_limit != 0:
            pass_check = input("please enter your password: ")
            if pass_check != cust.password:
                pass_limit -= 1
                print("Incorrect password entered")
                print("You have", pass_limit, "attempts left")

        if pass_limit == 0:
            print("You have run out of attempts.")
            main()
        else:
            customers_list.close()
            acc_list(cust)
    else:
        print("We could not find your account")
        customers_list.close()
        main()


def acc_list(cust):
    """Provides the user with options relating to bank accounts
    Option 1: 'View existing accounts', prints a list of the accounts
     the user owns
     Option 2: 'Create new account' calls the function newacc() which
     creates a new bank account for the user
     Option 3: 'Log out' brings the user back to the starting menu"""

    print("\n\nWelcome back {}, what would you like to do?".format(cust.fname))
    pick = 0
    # Read list of transactions from accountsTransactions.txt
    # value is placeholder
    transactions = '0'
    while pick != 3:
        accounts_list = ""
        flag = 0
        print("1. View existing accounts")
        print("2. Create new account")
        print("3. Log out")
        pick = input("Enter: ")

        try:
            accounts_list = open("accounts.txt", "r")
        except IOError:
            print("File could not be opened.")
            exit()

        # Prints list of accounts
        if pick == '1':
            # if check stays 0, the user has no account
            check = 0
            # Get account list from file via customer's details
            for acc_line in accounts_list:
                if cust.cust_id in acc_line:
                    # check user has an account
                    check = 1
                    # read parameters from the file
                    acc_params = acc_line.strip().split(" ")
                    # create and print the accounts
                    if 'savings' in acc_line:
                        acc1 = SavingsAccount(acc_params[0], acc_params[1],
                                              acc_params[2], acc_params[3],
                                              transactions, acc_params[4])
                        print(acc1)
                    elif 'checking' in acc_line:
                        acc2 = CheckingAccount(acc_params[0], acc_params[1],
                                               acc_params[2], acc_params[3],
                                               transactions, acc_params[4])

                        print(acc2)
            if check == 0:
                print("Sorry, it doesn't seem like you have an account with us")
                flag = 1

            if flag != 1:
                accounts_list = open("accounts.txt", "r")
                while True:
                    there = 0
                    choice = input("Enter the account id of the account you wish to use: ")
                    if len(choice) == 5:
                        for acc_line in accounts_list:
                            if choice and cust.cust_id in acc_line:
                                there = 1
                    else:
                        print("Error: Account id can only be 5 digits long")

                    if there == 1:
                        break

                # Read account chosen

                # Reset the file
                accounts_list.close()
                accounts_list = open("accounts.txt", "r")
                check = 0
                for acc_line in accounts_list:
                    if choice in acc_line:
                        print(acc_line)
                        check = 1
                        acc_params = acc_line.strip().split(" ")
                        if 'savings' in acc_line:
                            acc = SavingsAccount(acc_params[0], acc_params[1],
                                                 acc_params[2], acc_params[3],
                                                 transactions, acc_params[4])
                            print(acc)
                            interface(cust, acc)
                        elif 'checking' in acc_line:
                            acc = CheckingAccount(acc_params[0], acc_params[1],
                                                  acc_params[2], acc_params[3],
                                                  transactions,  acc_params[4])
                            print(acc)
                            interface(cust, acc)
                if check == 0:
                    print("Sorry, we could not find the account ID you have chosen")
            break
        # creates new account
        elif pick == '2':
            newacc(cust)
            break
        elif pick == '3':
            main()
            break
        else:
            print("\nInvalid option entered. Please only choose 1, 2 or 3")
            acc_list(cust)


def interface(cust1, acc1):
    """Function to display a list of banking functions to the user
    Option 1: 'Check Balance' prints the amount of cash in the customer's account
    Option 2: 'Deposit to own account' deposits an amount of money into the customer's account
    Option 3: 'Transfer funds' transfers funds from one account to another
    Option 4: 'Withdraw cash' withdraws an amount of cash from the user's account
    Option 5: 'View recent transactions' lists the five most recent transactions
    Option 6: 'Manage cards' calls the card menu
    Option 7: 'Use interest/Mortgage calculator' allows the user to make calculations based on current interest rates
    Option 8: 'Close Account' deletes the account the customer is currently using
    Option 9: 'Open a different existing account' re-displays the acc_list function
    Option 10: 'Log out' returns the user to the main menu"""

    option = '0'
    # list will repeat until program exits or user decides to open a different existing account
    while option != '9':
        print("\n\nWelcome back {}, what would you like to do?".format(cust1.fname))
        print("1. Check Balance")
        print("2. Deposit to own account")
        print("3. Transfer funds")
        print("4. Withdraw cash")
        print("5. View Recent Transactions")
        print("6. Use interest/Mortgage calculator")
        print("7. Manage cards")
        print("8. Close Account")
        print("9. Open a different existing account")
        print("10. Log out")
        option = input("please select an option: ")

        if option == '1':
            acc1.checkbalance()
        elif option == '2':
            try:
                amount = float(input("How much would you like to deposit: "))
                acc1.deposit(amount)
            except ValueError:
                print("\nError: Invalid input please only enter a number")
        elif option == '3':
            # repeat loop until correct iban format is inputted
            while True:
                # prompting the user for the iban they wish to transfer to
                trans_iban = input("Please enter the iban of the account you wish to transfer to: ")
                if len(trans_iban) == 9 and trans_iban[:4] == 'IEAJ':
                    #
                    if trans_iban != acc1.iban:
                        acc1.transfer(trans_iban)
                        break
                    elif trans_iban == acc1.iban:
                        print("You cannot transfer to your own account. Please try again.")
                else:
                    print("Sorry invalid iban format please try again.")
        elif option == '4':
            try:
                amount = float(input("How much would you like to withdraw: "))
                acc1.withdraw(amount)
            except ValueError:
                print("\nError: Invalid input please only enter a number")
        elif option == '5':
            transacs = acc1.recent_transactions()
            print(transacs)
        elif option == '6':
            acc1.interestcalc()
        elif option == '7':
            card_menu(cust1, acc1)
        elif option == '8':
            delete_acc(cust1, acc1)
        elif option == '9':
            acc_list(cust1)
        elif option == '10':
            print("Are you sure you wish to exit?")
            print("1. Yes")
            print("2. No")
            while True:
                choice = input("Choose: ")
                if choice == '1':
                    main()
                    break
                elif choice == '2':
                    break
                else:
                    print("Invalid input: Please only input 1 or 2")
        else:
            print("Invalid input entered: Please only enter a number from the list")


def card_menu(cust, acc):
    print("Welcome to the card menu")
    option = 0
    while option != 5:
        print("1. Create a new debit card")
        print("2. Create a new credit card")
        print("3. View card linked to this account")
        print("4. Delete card linked to this account")
        print("5. Back to previous menu")
        option = input("Enter ")
        # card_num, expr_date, cvv, pin, a_id, card_type
        if option == "1":
            # make sure there is no card linked to account
            check = 0
            cards_list = ""
            try:
                cards_list = open("cards.txt", "r")
            except IOError:
                print("File can't be opened")
                exit()
            for line in cards_list:
                if acc.acc_id in line:
                    check = 1

            if check == 0:
                newcard(acc, option)
            else:
                print("Sorry, could not find card")
            cards_list.close()
        elif option == "2":
            # make sure there is no card linked to account
            check = 0
            cards_list = ""
            try:
                cards_list = open("cards.txt", "r")
            except IOError:
                print("File can't be opened")
                exit()

            for cline in cards_list:
                if acc.acc_id in cline:
                    check = 1

            if check == 0:
                newcard(acc, option)
            elif check == 1:
                print("Sorry, you can only link one card per account")
            cards_list.close()
        elif option == "3":
            cards_list = ""
            check = 0
            try:
                cards_list = open("cards.txt", "r")
            except IOError:
                print("File can't be opened")
                exit()
            for line in cards_list:
                if acc.acc_id in line:
                    check = 1
                    card_params = line.strip().split(" ")
                    if "debit" in line:
                        card = DebitCard(card_params[0], card_params[1],
                                         card_params[2], card_params[3],
                                         card_params[4], card_params[5])
                        print(card)
                    elif "credit" in line:
                        card = CreditCard(card_params[0], card_params[1],
                                          card_params[2], card_params[3],
                                          card_params[4], card_params[5])
                        print(card)
            if check == 0:
                print("You have no card linked to your account")
            cards_list.close()
        elif option == "4":
            # check to see if a card exists
            check = 1
            cards_list = ""
            try:
                cards_list = open("cards.txt", "r")
            except IOError:
                print("File can't be opened")
                exit()

            # first checks
            for line in cards_list:
                if acc.acc_id in line:
                    check = 0
                    break
            cards_list.close()

            if check == 0:

                choice = 0
                cards_list = open("cards.txt", "r")

                for cline in cards_list:
                    if acc.acc_id in cline:
                        card_params = cline.strip().split(" ")
                        if "credit" in cline:
                            card = CreditCard(card_params[0], card_params[1],
                                              card_params[2], card_params[3],
                                              card_params[4])

                        elif "debit" in cline:
                            card = DebitCard(card_params[0], card_params[1],
                                             card_params[2], card_params[3],
                                             card_params[4])

                while choice != "2":
                    print("Are you sure you wish to cancel your card?")
                    print("1. Yes\n2. No")
                    choice = input("Enter: ")
                    if choice == "1":
                        pin_check = ""
                        while pin_check != card.pin:
                            pin_check = input("Please enter your card pin to block"
                                              " your account")
                            if pin_check == card.pin:
                                card_file = open("cards.txt", "r")
                                lines = card_file.readlines()
                                card_file.close()

                                newcard_file = open("cards.txt", "w")
                                for line in lines:
                                    if card.card_num not in line.strip("\n"):
                                        newcard_file.write(line)

                                newcard_file.close()
                                print("Card successfully blocked")
                                card_menu(cust, acc)
                    elif choice == "2":
                        print("Action cancelled")
            elif check == 1:
                print("You do not have a card to delete")
            cards_list.close()
        elif option == "5":
            interface(cust, acc)
        else:
            print("Invalid input")


def newcard(acc, c_type):
    if c_type == "1":
        # card creation

        # Generates random 16 digit card number
        cardNo = randint(1000000000000000, 9999999999999999)

        # where 09 is the month and 23 is the year
        expires = "09/23"

        cvv = randint(100, 999)

        pin = randint(1000, 9999)

        a_id = acc.acc_id

        new_card = DebitCard(cardNo, expires, cvv, pin, a_id)

        # write card to card file
        new_card.add_card()
        print("Your new card is\n", new_card)

    elif c_type == "2":

        # card creation

        # Generates random 16 digit card number
        cardNo = randint(1000000000000000, 9999999999999999)

        # where 09 is the month and 23 is the year
        expires = "09/23"

        cvv = randint(100, 999)

        pin = randint(1000, 9999)

        a_id = acc.acc_id

        new_card = CreditCard(cardNo, expires, cvv, pin, a_id)

        # write card to card file
        new_card.add_card()
        print("Your new card is\n", new_card)


def newcust():
    """Function to create a new customer account"""
    print("\n\nPlease enter your details")
    fname = age = surname = password = ""

    # loops until fname contains letters only
    while not fname.strip().isalpha():
        fname = input("First name: ")
        if not fname.strip().isalpha():
            print("Wrong value entered: letters only")

    while not surname.strip().isalpha():
        surname = input("Surname: ")
        if not surname.strip().isalpha():
            print("Wrong value entered: letters only")

    # loops until age contains numbers only
    while not age.strip().isdigit():
        age = input("Age: ")
        if not age.strip().isdigit():
            print("Wrong value entered: numbers only")

    while password == "" or 15 < len(password) < 3:
        password = input("Password: ")
        if password == "":
            print("Cannot enter blank value")
        if 15 < len(password) < 3:
            print("Password must be between 3 and 15 characters in length")

    cust_file = open("customers.txt", "r")
    customer_list = []
    id_list = []
    for line in cust_file:
        customer_list.append(line.strip().split(" "))

    for ele in customer_list:
        id_list.append(ele[0])

    cid = int(max(id_list)) + 1
    num_acc = 0
    new_cust = Customer(cid, fname, surname, age, num_acc, password)
    print(new_cust)
    new_cust.add_cust()
    print("Account successfully created")
    print("Your customer id is: ", new_cust.cust_id)


def newacc(cust):
    """Function to create a new bank account or to view
    accounts you have created previously"""
    choice = 0
    while choice != 3:
        print("Press 1 to open a savings account", end="")
        print(" or 2 to open a checking account")
        print(" or 3 to go back to the previous menu")
        choice = int(input("\nEnter: "))

        if choice == 1:
            acc_file = open("accounts.txt", "r")
            account_list = []
            id_list = []
            for line in acc_file:
                account_list.append(line.strip().split(" "))

            for ele in account_list:
                id_list.append(ele[0])

            # instance creation
            accid = int(max(id_list)) + 1
            accid = str(accid)
            iban = "IEAJ" + accid
            funds = "0.00"
            transactions = 0
            tf = "2000-01-01"
            new_acc = SavingsAccount(accid, iban, funds, cust.cust_id,
                                     transactions, tf)
            # write account to account file
            new_acc.add_acc()
            # update the amount of accounts the customer has in the file
            cust.no_of_accounts = int(cust.no_of_accounts) + 1
            cust.no_of_accounts = str(cust.no_of_accounts)
            cust.update_cust("customers.txt", 0)
            print("New savings account successfully created")
        elif choice == 2:
            if int(cust.age) < 18:
                print("Sorry, you must be 18 to open a checking account")
            else:
                acc_file = open("accounts.txt", "r")
                account_list = []
                id_list = []
                for line in acc_file:
                    account_list.append(line.strip().split(" "))

                for ele in account_list:
                    id_list.append(ele[0])

                accid = int(max(id_list)) + 1
                iban = "IEAJ" + str(accid)
                funds = 0.0
                transactions = 0
                credit_limit = 0.00
                # 300 being the minimum and 9000 being the max euro credit limit
                while credit_limit < 300.00 or credit_limit > 9000.00:
                    credit_limit = float(input("Enter the amount of credit you wish"
                                               " to limit yourself to"
                                               " (between €300 and €9000)"))

                # write account to account file
                new_acc = CheckingAccount(accid, iban, funds, cust.cust_id,
                                          transactions, credit_limit)
                new_acc.add_acc()
                print("New checking account successfully created")
                cust.no_of_accounts = int(cust.no_of_accounts) + 1
                cust.no_of_accounts = str(cust.no_of_accounts)
                cust.update_cust("customers.txt", 0)

        elif choice == 3:
            acc_list(cust)
        else:
            print("Invalid option entered")


def delete_acc(cust, acc):
    """Deletes an account from the txt file"""
    #keep repeating the loop until the customer inputs the correct information
    while True:
        print("Are you sure you wish to close your account?")
        print("1. Yes\n2. No")
        choice = input("Enter: ")
        # If the user chooses to close their account
        if choice == '1':
            # while loop to ensure funds are 0 by repeating until the funds are 0
            while True:
                if float(acc.funds) > 0.0:
                    print("There are existing funds in your account which means your account cannot be deleted")
                    while True:
                        print("Do you wish to transfer your funds to another account?")
                        print("1. Now\n2. Later")
                        option = input("option: ")
                        if option == '1':
                            # prompting the user for the iban they wish to transfer to
                            while True:
                                trans_iban = input("Please enter the iban of the account you wish to transfer to: ")

                                # ensuring the iban entered is the correct format and isn't their own
                                if len(trans_iban) == 9 and trans_iban[:4] == 'IEAJ':
                                    if trans_iban != acc.iban:
                                        acc.transfer(trans_iban)
                                        break
                                elif trans_iban == acc.iban:
                                    print("You cannot transfer to your own account. Please try again.")
                                else:
                                    print("Sorry invalid iban format please try again.")
                        # display the list of
                        elif option == '2':
                            acc_list(cust)
                        else:
                            print("\nInvalid option. Please only press 1 or 2")
                        break
                elif float(acc.funds) == 0.0:
                    break

            pass_check = ""
            while pass_check != cust.password:
                pass_check = input("Please enter your password to delete your account")
                if pass_check == cust.password:
                    acc_file = open("accounts.txt", "r")
                    lines = acc_file.readlines()
                    acc_file.close()

                    newacc_file = open("accounts.txt", "w")
                    for line in lines:
                        if acc.acc_id not in line.strip("\n"):
                            newacc_file.write(line)

                    newacc_file.close()
                    print("Account successfully deleted")
                    cust.no_of_accounts = int(cust.no_of_accounts) - 1
                    cust.no_of_accounts = str(cust.no_of_accounts)
                    cust.update_cust("customers.txt", 1)
                    acc_list(cust)

        elif choice == '2':
            interface(cust, acc)
        else:
            print("Invalid option entered: Please only choose 1 or 2")


def main():
    """Landing menu for the program. Contains 3 choices
    Option 1: 'Login' if you have a customer account
    Option 2: 'Register' if you do not have a customer account
    Option 3: 'Exit' to stop the program from running"""
    print("Welcome to AJ International Bank.")
    choice = 0
    while choice != 3:
        print("\nPlease select the following options:\n")
        print("1. Login\n2. Register\n3. Exit")
        try:
            choice = int(input("option: "))
        except ValueError:
            print("Numbers only")
        if choice == 1:
            choice = 0
            returningcust()
        elif choice == 2:
            choice = 0
            newcust()
        elif choice == 3:
            print("Exiting program, see you soon!")
            exit()
        else:
            choice = 0
            print("Invalid input")


main()

