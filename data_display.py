# from generate_data import *
import mysql.connector

database = mysql.connector.connect(
    user='pythonAccess',
    password='password',
    host='localhost',
    database='CSE4701_COMPANY_P2')

cursor = database.cursor()

def add_employee():
    fname = input("Enter first name: ")
    minit = input("Enter middle initial: ")
    lname = input("Enter last name: ")
    ssn = input("Enter employee SSN: ")
    bdate = input("Enter birth date: ")
    address = input("Enter address: ")
    sex = input("Enter sex: ")
    salary = input("Enter salary: ")
    super_ssn = input("Enter Supervisor's SSN: ")
    dno = input("Enter department number: ")

    try:
        query = "INSERT INTO EMPLOYEE VALUES ('" + str(fname) + "', '" + str(minit) + "', '" + str(lname) + "', '" + str(ssn) + "', '" + str(bdate) + "', '" + str(address) + "', '" + str(sex) + "', " + str(salary) + ", '" + str(super_ssn) + "', " + str(dno) + ")"
        cursor.execute(query)
        database.commit()
    except mysql.connector.Error as e:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    print("Employee added.")
    return

# add_employee("Chris", "A", "Pokotylo", "333333333", "2001-01-12", "71 K Rd, Farmington, CT", "M", 10000, "123456789", 5)

def view_employee():
    ssn = input("Enter Employee SSN: ")
    # [Fname, Minit, Lname, SSN, Bdate, Address, Sex, Salary, Mgr_ssn, Dno]
    employee_data = []
    super_data = []
    dept_data = []
    dependent_data = []
    try:
        # Get all attributes from EMPLOYEE table
        query = "SELECT * FROM EMPLOYEE WHERE Ssn = " + str(ssn)
        cursor.execute(query)
        employee_data = cursor.fetchall()

        # Get supervisor name (Fname, Minit, Lname)
        query = "SELECT Fname, Minit, Lname FROM EMPLOYEE WHERE Ssn = " + str(employee_data[0][8])
        cursor.execute(query)
        super_data = cursor.fetchall()

        # Get department name
        query = "SELECT Dname FROM DEPARTMENT WHERE Dnumber = " + str(employee_data[0][9])
        cursor.execute(query)
        dept_data = cursor.fetchall()

        # Get dependents
        query = "SELECT * FROM DEPENDENT WHERE Essn = " + str(employee_data[0][3])
        cursor.execute(query)
        dependent_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    # print(employee_data, super_data, dept_data, dependent_data)
    # print(employee_data[0])
    # return employee_data + super_data + dept_data + dependent_data

    print("---")
    if len(employee_data) == 0:
        print("Employee not found.")
        return
    else:
        employee_data = employee_data[0]
        print("Employee Name:", employee_data[0], employee_data[1], employee_data[2])
        print("Employee SSN:", employee_data[3])
        print("Birthday:", employee_data[4])
        print("Address:", employee_data[5])
        print("Sex:", employee_data[6])
        print("Salary:", employee_data[7])
        print("Supervisor's SSN:", employee_data[8])
        print("Department Number:", employee_data[9])

    print("---")

    if len(super_data) == 0:
        print("Supervisor not found.")
    else:
        super_data = super_data[0]
        print("Supervisor Name:", str(super_data[0]), str(super_data[1]), str(super_data[2]))
    print("---")

    print("Department Name:", dept_data[0][0])

    print("---")
    if len(dependent_data) == 0:
        print("Dependents not found.")
    else:
        for i in range(len(dependent_data)):
            print("Dependent", i)
            print("Dependent Name:", dependent_data[i][1])
            print("Dependent Sex:", dependent_data[i][2])
            print("Dependent Birthday:", dependent_data[i][3])
            print("Dependent Relation:", dependent_data[i][4])
            print("---")

def modify_employee():
    ssn = input("Enter Employee SSN: ")

    # Lock table for reading and writing.
    # Don't want to display information to other clients while employee data is being updated.
    # Unlock once all operations are completed.
    try:
        query = "LOCK TABLE EMPLOYEE WRITE, EMPLOYEE AS ER READ"
        cursor.execute(query)
        database.commit() # Is this needed?
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return

    employee_data = []
    try:
        query = "SELECT * FROM EMPLOYEE AS ER WHERE Ssn = " + str(ssn)
        cursor.execute(query)
        employee_data = cursor.fetchall()
    except mysql.connector.error as e:
        print("Produced an error in fetching data. Detailed information below.")
        print(str("Error:" + e.msg))
        return

    print("---")
    if len(employee_data) == 0:
        print("Employee not found. Exiting...")
        return
    else:
        employee_data = employee_data[0]
        print("Employee Name:", employee_data[0], employee_data[1], employee_data[2])
        print("Employee SSN:", employee_data[3])
        print("Birthday:", employee_data[4])
        print("Address:", employee_data[5])
        print("Sex:", employee_data[6])
        print("Salary:", employee_data[7])
        print("Supervisor's SSN:", employee_data[8])
        print("Department Number:", employee_data[9])

    while 1:
        print("---")
        print("1. Employee First Name")
        print("2. Employee Middle Initial")
        print("3. Employee Last Name")
        print("4. Employee Birthday")
        print("5. Employee Address")
        print("6. Employee Sex")
        print("7. Employee Salary")
        print("8. Employee Supervisor (SSN)")
        print("9. Employee Department (Number)")
        print("Other. Quit")

        selection = input("Which field would you like to modify? Enter a value: ")

        match selection:
            case '1':
                try:
                    new_fname = input("Enter the new first name: ")
                    query = "UPDATE EMPLOYEE SET Fname = '" + str(new_fname) + "' WHERE Ssn=" + str(ssn)
                    print(query)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee first name.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '2':
                try:
                    new_minit = input("Enter the new middle initial (one char, ex. 'A'): ")
                    query = "UPDATE EMPLOYEE SET Minit = '" + str(new_minit) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee middle initial.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '3':
                try:
                    new_lname = input("Enter the new last name: ")
                    query = "UPDATE EMPLOYEE SET Lname = '" + str(new_lname) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee last name.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '4':
                try:
                    new_bdate = input("Enter the new birthday (YYYY-MM-DD): ")
                    query = "UPDATE EMPLOYEE SET Bdate = '" + str(new_bdate) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee birthday.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '5':
                try:
                    new_addr = input("Enter the new address: ")
                    query = "UPDATE EMPLOYEE SET Address = '" + str(new_addr) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee address.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '6':
                try:
                    new_sex = input("Enter the new sex (one char, ex. 'M', 'F'): ")
                    query = "UPDATE EMPLOYEE SET Sex = '" + str(new_sex) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee sex.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '7':
                try:
                    new_salary = input("Enter the new salary: ")
                    query = "UPDATE EMPLOYEE SET Salary = '" + str(new_salary) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee salary.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '8':
                try:
                    new_ssn = input("Enter the new Supervisor's SSN (9 digits, ex. XXXXXXXXX): ")
                    query = "UPDATE EMPLOYEE SET Super_ssn = '" + str(new_ssn) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee supervisor's SSN.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    
            case '9':
                try:
                    new_dept_num = input("Enter the new department number (must already be established / exist): ")
                    query = "UPDATE EMPLOYEE SET Dno = '" + str(new_dept_num) + "' WHERE Ssn=" + str(ssn)
                    cursor.execute(query)
                    database.commit()
                    print("Successfully updated employee department number.")
                except mysql.connector.Error as e:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
            case _:
                # Unlock once done updating records
                try:
                    query = "UNLOCK TABLES"
                    cursor.execute(query)
                    database.commit()
                    print("Exiting...")
                except:
                    print("Produced an error. Check values and try again. Detailed information below.")
                    print(str("Error:" + e.msg))
                    return
                return

def remove_employee():
    ssn = input("Enter the Employee SSN: ")

    try:
        query = "LOCK TABLE EMPLOYEE WRITE, EMPLOYEE AS ER READ"
        cursor.execute(query)
        database.commit() # Is this needed?
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    employee_data = []
    try:
        query = "SELECT * FROM EMPLOYEE AS ER WHERE Ssn = '" + str(ssn) + "'"
        cursor.execute(query)
        employee_data = cursor.fetchall()
    except mysql.connector.error as e:
        print("Produced an error in fetching data. Detailed information below.")
        print(str("Error:" + e.msg))
        return

    print("---")
    if len(employee_data) == 0:
        print("Employee not found. Exiting...")
        return
    else:
        employee_data = employee_data[0]
        print("Employee Name:", employee_data[0], employee_data[1], employee_data[2])
        print("Employee SSN:", employee_data[3])
        print("Birthday:", employee_data[4])
        print("Address:", employee_data[5])
        print("Sex:", employee_data[6])
        print("Salary:", employee_data[7])
        print("Supervisor's SSN:", employee_data[8])
        print("Department Number:", employee_data[9])

    confirm = input("Are you sure you want to delete this employee? ('y' to confirm, any other value to decline): ")
    match confirm:
        case 'y':
            try:
                query = "DELETE FROM EMPLOYEE WHERE Ssn= '" + str(ssn) + "'"
                cursor.execute(query)
                database.commit()
            except mysql.connector.Error as e:
                print("Produced an error. Check values and try again. Detailed information below.")
                print("It could be that there is an existing dependency, resulting in this error.")
                print(str("Error:" + e.msg))
                return
        case _:
            return
        
    # Unlock once done updating records
    try:
        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully removed employee.")
    except:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return

# Ask for employee SSN. Lock employee record. Show all
# dependents. Ask for new dependent information and create a new dependent record.
def add_dependent():
    ssn = input("Enter employee SSN: ")
    dependent_data = []

    try:
        query = "LOCK TABLE DEPENDENT AS DR READ, DEPENDENT WRITE"
        cursor.execute(query)
        database.commit() # Is this needed?
        cursor.fetchall()

        query = "SELECT * FROM DEPENDENT AS DR WHERE Essn = '" + str(ssn) + "'"
        cursor.execute(query)
        dependent_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    print("---")
    if len(dependent_data) == 0:
        print("Dependents not found.")
    else:
        for i in range(len(dependent_data)):
            dependent_data = dependent_data[i]
            print("Dependent", i)
            print("Dependent Name:", dependent_data[1])
            print("Dependent Sex:", dependent_data[2])
            print("Dependent Birthday:", dependent_data[3])
            print("Dependent Relation:", dependent_data[4])
            print("---")
    
    dependent_name = input("Enter the new dependent's name: ")
    dependent_sex = input("Enter the new dependent's sex (ex. 'M', 'F'): ")
    dependent_bdate = input("Enter the dependent's birthday (YYYY-MM-DD format): ")
    dependent_relation = input("Enter the new dependent's relation to the employee (ex. 'Brother', 'Sister'): ")

    try:
        query = "INSERT INTO DEPENDENT VALUES ('" + str(ssn) + "', '" + str(dependent_name) + "', '" + str(dependent_sex) + "', '" + str(dependent_bdate) + "', '" + str(dependent_relation) + "')"
        cursor.execute(query)
        database.commit()

        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully added dependent record. Exiting...")
    except mysql.connector.Error as e:
        print("Produced an error. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return
    
def remove_dependent():
    ssn = input("Enter employee SSN: ")
    dependent_data = []

    try:
        query = "LOCK TABLE DEPENDENT AS DR READ, DEPENDENT WRITE"
        cursor.execute(query)
        cursor.fetchall()
        database.commit() # Is this needed?

        query = "SELECT * FROM DEPENDENT AS DR WHERE Essn = '" + str(ssn) + "'"
        cursor.execute(query)
        dependent_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    print("---")
    if len(dependent_data) == 0:
        print("Dependents not found.")
    else:
        for i in range(len(dependent_data)):
            print("Dependent", i)
            print("Dependent Name:", dependent_data[i][1])
            print("Dependent Sex:", dependent_data[i][2])
            print("Dependent Birthday:", dependent_data[i][3])
            print("Dependent Relation:", dependent_data[i][4])
            print("---")
    
    remove = int(input("Which dependent would you like to remove? Enter a valid number from the list above: "))

    try:
        query = "DELETE FROM DEPENDENT WHERE Essn= '" + str(ssn) + "'" + " AND DEPENDENT_NAME = '" + str(dependent_data[remove][1]) + "'"
        print(query)
        cursor.execute(query)
        database.commit()
    except IndexError or ValueError:
        print("Error: invalid index", str(remove), "entered. Exiting...")
        return
    
    try:
        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully removed dependent record. Exiting...")
    except mysql.connector.Error as e:
        print("Produced an error. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return

def add_department():
    new_dname = input("Enter new department name: ")
    new_dnumber = input("Enter new department number: ")
    new_mgr_ssn = input("Enter new manager SSN (be sure they are added to employee records): ")
    new_mgr_start_date = input("Enter new manager start date (YYYY-MM-DD format): ")
    try:
        query = "INSERT INTO DEPARTMENT VALUES ('" + str(new_dname) + "', '" + str(new_dnumber) + "', '" + str(new_mgr_ssn) + "', '" + str(new_mgr_start_date) + "')"
        cursor.execute(query)
        database.commit()
        print("Successfully added new department.")
    except mysql.connector.Error as e:
        print("Produced an error. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return

def view_department():
    dnumber = int(input("Enter valid department number: "))
    dept_data = []
    mgr_data = []
    dept_loc_data = []

    try:
        query = "SELECT * FROM DEPARTMENT WHERE Dnumber = '" + str(dnumber) + "'"
        cursor.execute(query)
        dept_data = cursor.fetchall()

        query = "SELECT Fname, Minit, Lname FROM EMPLOYEE WHERE Ssn = '" + str(dept_data[0][2]) + "'"
        cursor.execute(query)
        mgr_data = cursor.fetchall()

        query = "SELECT Dlocation FROM DEPT_LOCATIONS WHERE Dnumber = '" + str(dnumber) + "'"
        cursor.execute(query)
        dept_loc_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    print("---")
    print("Department Number:", dept_data[0][1])
    print("Department Name:", dept_data[0][0])
    print("Department Manager's SSN:", dept_data[0][2])
    print("Department Manager's Start Date:", dept_data[0][3])
    print("Department Manager's Name:", mgr_data[0][0], mgr_data[0][1], mgr_data[0][2])
    print("Department Locations:", end = " ")
    if len(dept_loc_data) >= 1:
        for i in range(len(dept_loc_data) - 1):
            print(dept_loc_data[i][0], end=", ")
        if(dept_loc_data[i+1]):
            print(dept_loc_data[i+1][0])
    else:
        print("No department locations found.")

    return

def remove_department():
    dnumber = int(input("Enter valid Department Number: "))
    dept_data = []

    try:
        query = "LOCK TABLE DEPARTMENT AS DR READ, DEPARTMENT WRITE"
        cursor.execute(query)
        cursor.fetchall()
        database.commit() # Is this needed?

        query = "SELECT * FROM DEPARTMENT AS DR WHERE Dnumber = '" + str(dnumber) + "'"
        cursor.execute(query)
        dept_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    print("---")
    print("Department Number:", dept_data[0][1])
    print("Department Name:", dept_data[0][0])
    print("Department Manager's SSN:", dept_data[0][2])
    print("Department Manager's Start Date:", dept_data[0][3])

    confirm = input("Are you sure you want to delete this department? ('y' to confirm, any other value to decline): ")
    match confirm:
        case 'y':
            try:
                query = "DELETE FROM DEPARTMENT WHERE Dnumber= '" + str(dnumber) + "'"
                cursor.execute(query)
                database.commit()
            except mysql.connector.Error as e:
                print("Produced an error. Check values and try again. Detailed information below.")
                print("It could be that there is an existing dependency, resulting in this error.")
                print(str("Error:" + e.msg))
        case _:
            return
        
    # Unlock once done updating records
    try:
        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully deleted department record. Exiting...")
    except:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return

def add_department_location():
    dnumber = int(input("Enter existing department number: "))

    dloc_data = []

    try:
        query = "LOCK TABLE DEPT_LOCATIONS AS DR READ, DEPT_LOCATIONS WRITE"
        cursor.execute(query)
        cursor.fetchall()
        database.commit() # Is this needed?

        query = "SELECT * FROM DEPT_LOCATIONS AS DR WHERE Dnumber = '" + str(dnumber) + "'"
        cursor.execute(query)
        dloc_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return

    print("---")
    if len(dloc_data) >= 1:
        for i in range(len(dloc_data) - 1):
            print(dloc_data[i][1], end=", ")
        if(dloc_data[i+1]):
            print(dloc_data[i+1][1])
    else:
        print("No department locations found.")

    new_dloc = input("Enter new department location: ")

    try:
        query = "INSERT INTO DEPT_LOCATIONS VALUES ('" + str(dnumber) + "', '" + str(new_dloc) + "')"
        cursor.execute(query)
        database.commit()
    except mysql.connector.Error as e:
        print("Produced an error. Detailed information below.")
        print(str("Error:" + e.msg))
        return

    # Unlock once done updating records
    try:
        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully added new department location. Exiting...")
    except:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return

def remove_department_location():
    dnumber = int(input("Enter valid Department Number: "))
    dloc_data = []

    try:
        query = "LOCK TABLE DEPT_LOCATIONS AS DR READ, DEPT_LOCATIONS WRITE"
        cursor.execute(query)
        cursor.fetchall()
        database.commit() # Is this needed?

        query = "SELECT * FROM DEPT_LOCATIONS AS DR WHERE Dnumber = '" + str(dnumber) + "'"
        cursor.execute(query)
        dloc_data = cursor.fetchall()
    except mysql.connector.Error as e:
        print("Produced an error in locking data. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    
    print("---")
    if len(dloc_data) >= 1:
        for i in range(len(dloc_data) - 1):
            print(dloc_data[i][1], end=", ")
        if(dloc_data[i+1]):
            print(dloc_data[i+1][1])
    else:
        print("No department locations found. Exiting...")
        return

    del_dloc = input("Which department location would you like to delete?: ")

    confirm = input("Are you sure you want to delete this department location? ('y' to confirm, any other value to decline): ")
    match confirm:
        case 'y':
            try:
                query = "DELETE FROM DEPT_LOCATIONS WHERE Dnumber= '" + str(dnumber) + "' AND Dlocation = '" + str(del_dloc) + "' "
                cursor.execute(query)
                database.commit()
            except mysql.connector.Error as e:
                print("Produced an error. Check values and try again. Detailed information below.")
                print("It could be that there is an existing dependency, resulting in this error.")
                print(str("Error:" + e.msg))
        case _:
            return
        
    # Unlock once done updating records
    try:
        query = "UNLOCK TABLES"
        cursor.execute(query)
        database.commit()
        print("Successfully deleted department location record. Exiting...")
    except:
        print("Produced an error. Check values and try again. Detailed information below.")
        print(str("Error:" + e.msg))
        return
    return