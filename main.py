from data_display import *

if __name__ == '__main__':
    # Options
    while 1:
        print("Select an option:\n")
        print("'ae': Add Employee")
        print("'ve': View Employee")
        print("'me': Modify Employee")
        print("'re': Remove Employee")
        print("'adep': Add dependent")
        print("'rdep': Remove dependent")
        print("'adept': Add department")
        print("'vdept': View department")
        print("'rdept': Remove department")
        print("'adloc': Add department location")
        print("'rdloc': Remove department location")
        print("Any other value: exit the program")
        selection = input("Hello, what would you like to do? ")
        print()

        match selection:
            case 'ae':
                add_employee()
            case 've':
                view_employee()
            case 'me':
                modify_employee()
            case 're':
                remove_employee()
            case 'adep':
                add_dependent()
            case 'rdep':
                remove_dependent()
            case 'adept':
                add_department()
            case 'vdept':
                view_department()
            case 'rdept':
                remove_department()
            case 'adloc':
                add_department_location()
            case 'rdloc':
                remove_department_location()
            case _:
                print("Exiting...")
                break