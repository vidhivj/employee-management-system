import getpass
import mysql.connector
from datetime import datetime


def get_number(message):
    while True:
        try:
            number = int(input(message))
            return number
        except ValueError:
            print("Invalid input! Please enter a number.")

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass.getpass("Enter MySQL password: "),
    database="company",
    use_pure=True
)

cur = con.cursor(buffered=True)


def salary_distribution():
    print("\n" + "=" * 75)
    print("                       SALARY DISTRIBUTION ANALYSIS")
    print("=" * 75)

    cur.execute("SELECT CASE WHEN Basic_Salary <= 20000 THEN '0 - 20000' WHEN Basic_Salary <= 40000 THEN '20001 - 40000' WHEN Basic_Salary <= 60000 THEN '40001 - 60000' WHEN Basic_Salary <= 80000 THEN '60001 - 80000' ELSE 'Above 80000' END AS Salary_Range, COUNT(*) AS Total_Employees FROM employee GROUP BY Salary_Range ORDER BY MIN(Basic_Salary)")

    data = cur.fetchall()

    if not data:
        print("\nNo employee records found!")
        return
  
    print()
    print("-" * 75)
    
    total_employees = 0

    for row in data:
        total_employees = total_employees + row[1]

    print("{:<20} {:>12} {:>15}".format("SALARY RANGE", "EMPLOYEES", "PERCENTAGE"))
    print("-" * 75)

    for row in data:
        percentage = (row[1] / total_employees) * 100
        print("{:<20} {:>12} {:>14.2f}%".format(row[0], row[1], percentage))

    print("-" * 75)
    print("{:<25} {:>25}".format("TOTAL EMPLOYEES", total_employees))
    print("-" * 75)

def attendance_summary():

    while True:

        print("\n" + "=" * 75)
        print("                             ATTENDANCE SUMMARY")
        print("=" * 75)

        print("\n1. Employee Attendance Summary")
        print("2. Overall Attendance Summary")
        print("3. Attendance Percentage")
        print("4. Back")

        choice = get_number("\nEnter your choice: ")

        if choice == 1:

            print("\n" + "=" * 75)
            print("                         EMPLOYEE ATTENDANCE SUMMARY")
            print("=" * 75)

            emp_id = get_number("Enter Employee ID: ")
            if emp_id <= 0:
                print("Employee ID must be greater than zero!")
                return

            cur.execute("SELECT Emp_Name FROM employee WHERE Emp_ID=%s",(emp_id,))

            employee = cur.fetchone()

            if employee:

                cur.execute("SELECT Status, COUNT(*) FROM attendence WHERE Emp_ID=%s GROUP BY Status",(emp_id,))

                data = cur.fetchall()

                total_days = 0
                present = 0
                absent = 0
                leave = 0

                for d in data:

                    if d[0] == "Present":
                        present = d[1]

                    elif d[0] == "Absent":
                        absent = d[1]

                    elif d[0] == "Leave":
                        leave = d[1]

                total_days = present + absent + leave

                print("\nEmployee ID:", emp_id)
                print("Employee Name:", employee[0])

                print("\nPresent:", present)
                print("Absent:", absent)
                print("Leave:", leave)
                print("Total Days:", total_days)

            else:
                print("\nEmployee ID not found!")

        elif choice == 2:

            print("\n" + "=" * 75)
            print("                         OVERALL ATTENDANCE SUMMARY")
            print("=" * 75)

            cur.execute("SELECT Status, COUNT(*) FROM attendence GROUP BY Status")

            data = cur.fetchall()

            present = 0
            absent = 0
            leave = 0

            for d in data:

                if d[0] == "Present":
                    present = d[1]

                elif d[0] == "Absent":
                    absent = d[1]

                elif d[0] == "Leave":
                    leave = d[1]

            total_records = present + absent + leave

            print("\nPresent:", present)
            print("Absent:", absent)
            print("Leave:", leave)
            print("Total Attendance Records:", total_records)
            
        elif choice == 3:

            print("\n" + "=" * 75)
            print("                           ATTENDANCE PERCENTAGE")
            print("=" * 75)

            emp_id = get_number("Enter Employee ID: ")
            if emp_id <= 0:
                print("Employee ID must be greater than zero!")
                return

            cur.execute("SELECT Emp_Name FROM employee WHERE Emp_ID=%s",(emp_id,))

            employee = cur.fetchone()

            if employee:

                cur.execute("SELECT COUNT(*) FROM attendence WHERE Emp_ID=%s",(emp_id,))

                total_days = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM attendence WHERE Emp_ID=%s AND Status='Present'",(emp_id,))

                present = cur.fetchone()[0]

                if total_days > 0:
                    percentage = (present / total_days) * 100
                else:
                    percentage = 0

                print("\nEmployee ID:", emp_id)
                print("Employee Name:", employee[0])
                print("Total Days:", total_days)
                print("Present Days:", present)
                print("Attendance Percentage:", round(percentage, 2), "%")

                if percentage >= 75:
                    print("Attendance Status: Good")

                else:
                    print("Attendance Status: Low")

            else:
                print("\nEmployee ID not found!")

        elif choice == 4:
            break

        else:
            print("\nInvalid choice!")
            
def mark_attendance():
    print("\n" + "=" *75)
    print("                             MARK ATTENDANCE")
    print("=" *75)

    
    emp_id = get_number("Enter Employee ID: ")
    if emp_id <= 0:
        print("Employee ID must be greater than zero!")
        return

    cur.execute("SELECT Emp_Name FROM employee WHERE Emp_ID = %s",(emp_id,))
    data = cur.fetchone()
    if data is None:
        print("\nEmployee not found!")
        return

    if data:
        print("Employee Name: ",data[0])
        date = input("Enter Date(YYYY-MM-DD): ")

        try:
            datetime.strptime(date,"%Y-%m-%d")

        except ValueError:
            print("\nInvalid date!")
            print("Please enter a valid date like: 2026-10-11")
            return
        
        cur.execute("SELECT *FROM attendence WHERE Emp_ID=%s AND Attendance_Date=%s",(emp_id,date))
        existing = cur.fetchone()
        
        if existing:
            print("\nAttendance already marked for this employee on this date!")
            return
        
        print("\n1. Present")
        print("2. Absent")
        print("3. Leave")

        choice = get_number("\nEnter Status: ")

        if choice==1:
            status = "Present"
        elif choice==2:
            status = "Absent"
        elif choice==3:
            status = "Leave"
        else:
            print("\nInvalid choice!")
            return
        
        cur.execute("INSERT INTO attendence (Emp_ID,Attendance_Date,Status) values (%s,%s,%s)",(emp_id,date,status))
        con.commit()
        print("\nAttendance Mark Sucessfully!")

    else:
        print("\nEmployee ID not found!")

def view_attendance():
    
    while True:

        print("\n" + "=" *75)
        print("                             VIEW ATTENDANCE")
        print("=" *75)

        print("\n1. View Full Attendance")
        print("2. View Attendance by Date")
        print("3. Back")

        choice = get_number("Enter your choice ")

        if choice == 1:

           print("\n" + "=" *75)
           print("                          VIEW FULL ATTENDANCE")
           print("=" *75)

           cur.execute("SELECT *FROM attendence")
           data = cur.fetchall()
         
           if data:
               print("-" * 75)
               print("{:<15} {:<12} {:<15} {:<15}".format("Attendance ID", "Emp ID", "Status", "Date"))
               print("-" * 75)

               for d in data:
                   print("{:<15} {:<12} {:<15} {:<15}".format(d[0], d[1], d[2], str(d[3])))
    
               print("-" * 75)

           else:
               print("\nNo attendance records found!")

        elif choice == 2:

           print("\n" + "=" *75)
           print("                           VIEW ATTENDANCE BY DATE")
           print("=" *75)

           ate = input("Enter Date(YYYY-MM-DD): ")

           try:
               datetime.strptime(ate,"%Y-%m-%d")

           except ValueError:
               print("\nInvalid date!")
               print("Please enter a valid date like: 2026-10-11")
               return

           cur.execute("SELECT *FROM attendence WHERE Attendance_Date=%s",(ate,))
           data = cur.fetchall()

           if data:
               print("-" * 75)
               print("{:<15} {:<12} {:<15} {:<15}".format("Attendance ID", "Emp ID", "Status", "Date"))
               print("-" * 75)

               for d in data:
                   print("{:<15} {:<12} {:<15} {:<15}".format(d[0], d[1], d[2], str(d[3])))
               print("-" * 75)

           else:
               print("\nNo attendance found on this date!")

        elif choice == 3:
           break

        else:
           print("\nInvalid Choice")
                   
def attendance_management():

    while True:

        print("\n" + "=" *75)
        print("                          ATTENDANCE MANAGEMENT")
        print("=" *75)

        print("\n1. Mark Attendance")
        print("2. View Attendance")
        print("3. Attendance Summary")
        print("4. Back")

        choice = get_number("Enter your choice: ")

        if choice == 1:
            mark_attendance()

        elif choice == 2:
            view_attendance()

        elif choice == 3:
            attendance_summary()

        elif choice == 4:
            break

        else:
            print("Invalid choice!")
            

def department_anlaysis():

    while True:

        print("\n" + "=" * 75)
        print("                           DEPARTMENT ANALYSIS")
        print("=" * 75)

        print("\n1. View Complete Department Report")
        print("2. Department with Highest Average Salary")
        print("3. Department with Lowest Average Salary")
        print("4. Department with Highest Salary Expense")
        print("5. Back")

        print("-" * 75)

        choice = get_number("Enter your choice: ")

        if choice == 1:

            cur.execute("SELECT Department, COUNT(*), AVG(Basic_Salary), SUM(Basic_Salary) FROM employee GROUP BY Department")

            data = cur.fetchall()

            if data:
                print("\n" + "-" * 75)
                print(" " * 25 + "DEPARTMENT ANALYSIS REPORT")
                print("-" * 75)

                print("{:<20} {:>12} {:>18} {:>18}".format("Department", "Employees", "Average Salary", "Total Salary"))
                print("-" * 75)

                for row in data:
                    print("{:<20} {:>12} {:>18,.2f} {:>18,.2f}".format(row[0], row[1], row[2], row[3]))

                print("-" * 75)

            else:
                print("\nNo employee records found!")

        elif choice == 2:

            cur.execute("SELECT Department, AVG(Basic_Salary) FROM employee GROUP BY Department ORDER BY AVG(Basic_Salary) DESC LIMIT 1")

            result = cur.fetchone()

            if result:
                print("\n" + "-" * 75)
                print("                   DEPARTMENT WITH HIGHEST AVERAGE SALARY")
                print("-" * 75)
                print("Department       :", result[0])
                print("Average Salary   : ₹{:,.2f}".format(result[1]))
                print("-" * 75)

            else:
                print("\nNo department data found!")

        elif choice == 3:

            cur.execute("SELECT Department, AVG(Basic_Salary) FROM employee GROUP BY Department ORDER BY AVG(Basic_Salary) ASC LIMIT 1")

            result = cur.fetchone()

            if result:
                print("\n" + "-" * 75)
                print("                   DEPARTMENT WITH LOWEST AVERAGE SALARY")
                print("-" * 75)
                print("Department       :", result[0])
                print("Average Salary   : ₹{:,.2f}".format(result[1]))
                print("-" * 75)

            else:
                print("\nNo department data found!")

        elif choice == 4:

            cur.execute("SELECT Department, SUM(Basic_Salary) FROM employee GROUP BY Department ORDER BY SUM(Basic_Salary) DESC LIMIT 1")

            result = cur.fetchone()

            if result:
                print("\n" + "-" * 75)
                print("                   DEPARTMENT WITH HIGHEST SALARY EXPENSE")
                print("-" * 75)
                print("Department       :", result[0])
                print("Total Salary     : ₹{:,.2f}".format(result[1]))
                print("-" * 75)

            else:
                print("\nNo department data found!")

        elif choice == 5:
            break

        else:
            print("\nInvalid choice! Please enter a number from 1 to 5.")

def employee_statistics():

    while True:

        print("\n" + "=" * 75)
        print("                            EMPLOYEE STATISTICS")
        print("=" * 75)

        print("\n1. View Overall Employee Statistics")
        print("2. View Employees Earning Above Average Salary")
        print("3. View Highest Paid Employee")
        print("4. View Lowest Paid Employee")
        print("5. Back")

        print("-" * 75)

        choice = get_number("Enter your choice: ")

        cur.execute("SELECT COUNT(*) FROM employee")
        total_employees = cur.fetchone()[0]

        if total_employees == 0:
            print("\nNo employee records found!")
            break

        if choice == 1:

            cur.execute("SELECT COUNT(DISTINCT Department), AVG(Basic_Salary), MAX(Basic_Salary), MIN(Basic_Salary), SUM(Basic_Salary) FROM employee")

            data = cur.fetchone()

            print("\n" + "-" * 75)
            print("                         OVERALL EMPLOYEE STATISTICS")
            print("-" * 75)

            print("Total Employees       :", total_employees)
            print("Total Departments     :", data[0])
            print("Average Salary        : ₹{:,.2f}".format(data[1]))
            print("Highest Salary        : ₹{:,.2f}".format(data[2]))
            print("Lowest Salary         : ₹{:,.2f}".format(data[3]))
            print("Total Salary Expense  : ₹{:,.2f}".format(data[4]))

            print("-" * 75)

        elif choice == 2:

            cur.execute("SELECT Emp_ID, Emp_Name, Department, Basic_Salary FROM employee WHERE Basic_Salary > (SELECT AVG(Basic_Salary) FROM employee) ORDER BY Basic_Salary DESC")

            data = cur.fetchall()

            print("\n" + "-" * 75)
            print("                     ABOVE AVERAGE SALARY ANALYSIS")
            print("-" * 75)

            if data:
                print("{:<10} {:<22} {:<18} {:>15}".format(
                    "Emp ID", "Employee Name", "Department", "Basic Salary"))
                print("-" * 75)

                for row in data:
                    print("{:<10} {:<22} {:<18} {:>15,.2f}".format(
                        row[0], row[1], row[2], row[3]))

            else:
                print("No employees earn above the average salary.")

            print("-" * 75)

        elif choice == 3:

            cur.execute("SELECT Emp_ID, Emp_Name, Department, Basic_Salary FROM employee ORDER BY Basic_Salary DESC LIMIT 1")

            result = cur.fetchone()

            print("\n" + "-" * 75)
            print("                           HIGHEST PAID EMPLOYEE")
            print("-" * 75)

            if result:
                print("Employee ID    :", result[0])
                print("Employee Name  :", result[1])
                print("Department     :", result[2])
                print("Basic Salary   : ₹{:,.2f}".format(result[3]))

            print("-" * 75)

        elif choice == 4:

            cur.execute("SELECT Emp_ID, Emp_Name, Department, Basic_Salary FROM employee ORDER BY Basic_Salary ASC LIMIT 1")

            result = cur.fetchone()

            print("\n" + "-" * 75)
            print("                           LOWEST PAID EMPLOYEE")
            print("-" * 75)

            if result:
                print("Employee ID    :", result[0])
                print("Employee Name  :", result[1])
                print("Department     :", result[2])
                print("Basic Salary   : ₹{:,.2f}".format(result[3]))

            print("-" * 75)

        elif choice == 5:
            break

        else:
            print("\nInvalid choice! Please enter a number from 1 to 5.")

def calculate_salary(salary):

    if salary <= 20000:
        hra = 20
        da = 5
        pf = 12
        medical = 3
        ta = 5

    elif salary <= 40000:
        hra = 25
        da = 7
        pf = 12
        medical = 3
        ta = 6

    elif salary <= 60000:
        hra = 30
        da = 10
        pf = 12
        medical = 3
        ta = 7

    elif salary <= 80000:
        hra = 35
        da = 12
        pf = 12
        medical = 3
        ta = 8

    else:
        hra = 40
        da = 15
        pf = 12
        medical = 3
        ta = 10

    hra_amount = (salary * hra) / 100
    da_amount = (salary * da) / 100
    medical_amount = (salary * medical) / 100
    ta_amount = (salary * ta) / 100
    pf_amount = (salary * pf) / 100

    gross_salary = salary + hra_amount + da_amount + medical_amount + ta_amount - pf_amount

    return hra, da, medical, ta, pf, gross_salary

def update_employee():
    print("\n" + "=" * 75)
    print("                             UPDATE EMPLOYEE")
    print("=" * 75)

    emp_id = get_number("Enter Employee ID: ")

    if emp_id <= 0:
        print("Employee ID must be greater than zero!")
        return
    
    cur.execute("SELECT * FROM employee WHERE Emp_ID=%s", (emp_id,))
    data = cur.fetchone()

    if data:
        print("\nEmployee found!")
        print("\nPrevious Record:")
        print("\n" + "-" * 75)
        print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
        print("-" * 75)
        print(str(data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
        print("-" * 75)


        print("\n1. Update Name")
        print("2. Update Department")
        print("3. Update Basic Salary")
        print("4. Increment in Basic Salary")
        print("5. Decrement in Basic Salary")

        choice = get_number("Enter your choice: ")

        if choice == 1:
            new_name = input("Enter New Name: ")

            while new_name.strip() == "":
                print("Employee name cannot be empty!")
                new_name = input("Enter New Name: ")

            cur.execute("UPDATE employee SET Emp_Name=%s WHERE Emp_ID=%s",(new_name, emp_id))
            con.commit()

        elif choice == 2:
            new_department = input("Enter New Department: ")

            while new_department.strip() == "":
                print("Department name cannot be empty!")
                new_department = input("Enter New Department: ")

            cur.execute("UPDATE employee SET Department=%s WHERE Emp_ID=%s",(new_department, emp_id))
            con.commit()

        elif choice == 3:
            new_salary = get_number("Enter Updated Salary: ")
            
            while new_salary <= 0:
                print("Salary must be greater than zero!")
                new_salary = get_number("Enter Updated Salary: ")

            hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)
            
            cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
            con.commit()
            cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
            new_data = cur.fetchone()

            print("\nEmployee Updated Successfully")
            print("\nNew Record:\n")
            print("-" * 75)
            print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
            print("-" * 75)
            print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
            print("-" * 75)

        elif choice == 4:
            cur.execute("SELECT * FROM employee WHERE Emp_ID=%s", (emp_id,))
            data = cur.fetchone()

            if data:
                current_salary = data[3]
                print("\nCurrent Basic Salary:", current_salary)

                amount = get_number("Enter Increment Amount: ")
                if amount <= 0:
                    print("Amount must be greater than zero!")
                    return
            
                new_salary = current_salary + amount

                print("New Basic Salary:", new_salary)

                hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)
                
                cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
                con.commit()
                cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
                new_data = cur.fetchone()

                print("\nSalary Incremented Successfully")
                print("Increment Amount:", amount)
                print("\nNew Record:")
                print("\n" + "-" * 75)
                print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                print("-" * 75)
                print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                print("-" * 75)

            else:
                print("\nEmployee ID is not Found!")

        elif choice == 5:
             cur.execute("SELECT * FROM employee WHERE Emp_ID=%s", (emp_id,))
             data = cur.fetchone()

             if data:
                 current_salary = data[3]
                 print("\nCurrent Basic Salary:", current_salary)

                 amount = get_number("Enter Decrement Amount: ")
                 
                 if amount <= 0:
                    print("Amount must be greater than zero!")
                    return
                
                 new_salary = current_salary - amount
                 
                 if new_salary <= 0:
                     print("Salary cannot become zero or negative!")
                     return

                 print("New Basic Salary:", new_salary)

                 hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)

                 cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
                 con.commit()
                 cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
                 new_data = cur.fetchone()

                 print("\nSalary Decremented Successfully")
                 print("Decrement Amount:", amount)
                 print("\nNew Record:")
                 print("\n" + "-" * 75)
                 print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                 print("-" * 75)
                 print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                 print("-" * 75)

             else:
                 print("\nEmployee ID is not Found!")

  

        else:
            print("\nYour choice is invalid!")
            return     

    else:
        print("\nEmployee ID not found!")

        forgot = input("Did you forget your Employee ID? (yes/no): ")

        if forgot.lower() == "yes":

            name = input("Enter Employee Name: ")

            cur.execute("SELECT Emp_ID FROM employee WHERE Emp_Name=%s",(name,))

            result = cur.fetchone()

            if result:
                print("\nYour Employee ID is:", result[0])

                emp_id = get_number("\nEnter Employee ID again: ")

                if emp_id <= 0:
                    print("Employee ID must be greater than zero!")
                    return

                cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))

                data = cur.fetchone()

                if data:
                    print("\nEmployee found!")
                    print("-" * 75)
                    print("\nPrevious Record:")
                    print("\nE_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                    print("-" * 75)
                    print(data)
                    print("-" * 75)

                    print("\n1. Update Name")
                    print("2. Update Department")
                    print("3. Update Basic Salary")
                    print("4. Increament in Basic Salary")
                    print("5. Decreament in Basic Salary")
                    
                    choice = get_number("Enter your choice: ")

                    if choice == 1:
                        new_name = input("Enter New Name: ")

                        while new_name.strip() == "":
                            print("Employee name cannot be empty!")
                            new_name = input("Enter New Name: ")

                        cur.execute("UPDATE employee SET Emp_Name=%s WHERE Emp_ID=%s",(new_name, emp_id))
                        con.commit()

                    elif choice == 2:
                        new_department = input("Enter New Department: ")

                        while new_department.strip() == "":
                            print("Department name cannot be empty!")
                            new_department = input("Enter New Department: ")

                        cur.execute("UPDATE employee SET Department=%s WHERE Emp_ID=%s",(new_department, emp_id))
                        con.commit()

                    elif choice == 3:
                        new_salary = get_number("Enter Updated Salary: ")

                        if new_salary <= 0:
                            print("Amount must be greater than zero!")
                            return
                        
                        hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)

                        cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
                        con.commit()
                        cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
                        new_data = cur.fetchone()


                        print("\nEmployee Updated Successfully")
                        print("\nNew Record:")
                        print("\n" + "-" * 75)
                        print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                        print("-" * 75)
                        print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                        print("-" * 75)

                    elif choice == 4:
                        cur.execute("SELECT * FROM employee WHERE Emp_ID=%s", (emp_id,))
                        data = cur.fetchone()

                        if data:
                            current_salary = data[3]
                            print("\nCurrent Basic Salary:", current_salary)

                            amount = get_number("Enter Increment Amount: ")
                            
                            if amount <= 0:
                                print("Amount must be greater than zero!")
                                return
                            
                            new_salary = current_salary + amount

                            print("New Basic Salary:", new_salary)

                            hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)

                            cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
                            con.commit()
                            cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
                            new_data = cur.fetchone()

                            print("\nSalary Incremented Successfully")
                            print("Increment Amount:", amount)
                            print("\nNew Record:")
                            print("\n" + "-" * 75)
                            print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                            print("-" * 75)
                            print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                            print("-" * 75)

                    elif choice == 5:
                        cur.execute("SELECT * FROM employee WHERE Emp_ID=%s", (emp_id,))
                        data = cur.fetchone()

                        if data:
                            current_salary = data[3]
                            print("\nCurrent Basic Salary:", current_salary)

                            amount = get_number("Enter Decrement Amount: ")

                            if amount <= 0:
                                print("Amount must be greater than zero!")
                                return
                            
                            new_salary = current_salary - amount

                            if new_salary <= 0:
                                print("Salary cannot become zero or negative!")
                                return

                            hra, da, medical, ta, pf, gross_salary = calculate_salary(new_salary)

                            cur.execute("UPDATE employee SET Basic_Salary=%s, HRA=%s, DA=%s, Medical=%s, TA=%s, PF=%s, Gross_Salary=%s WHERE Emp_ID=%s",(new_salary, hra, da, medical, ta, pf, gross_salary, emp_id))
                            con.commit()
                            cur.execute("SELECT * FROM employee WHERE Emp_ID=%s",(emp_id,))
                            new_data = cur.fetchone()

                            print("\nSalary Decremented Successfully")
                            print("Decrement Amount:", amount)
                            print("\nNew Record:")
                            print("\n" + "-" * 75)
                            print("E_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
                            print("-" * 75)
                            print(str(new_data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                            print("-" * 75)

                    else:
                        print("\nYour choice is invalid!")
                        return
                    
                else:
                    print("\nEmployee ID is still not found!")

            else:
                print("\nEmployee Name not found!")

        else:
            print("\nUpdate cancelled!")

def add_employee():
    print("\n" + "=" * 75)
    print("                              ADD EMPLOYEE")
    print("=" * 75)

    cur.execute("SELECT MAX(Emp_ID) FROM employee")
    last_id = cur.fetchone()[0]
    
    if last_id is None:
        emp_id = 101
    else:
        emp_id = last_id + 1
        
    print("Employee ID: ",emp_id)
    
    ename = input("Enter Employee Name: ")

    while ename.strip() == "":
        print("\nEmployee name cannot be empty!")
        ename = input("Enter Employee Name: ")
        
    print("\nSelect Department:")
    print("1. HR")
    print("2. IT")
    print("3. Finance")
    print("4. Marketing")
    print("5. Sales")

    choice = get_number("Enter your choice: ")

    if choice == 1:
        department = "HR"
    elif choice == 2:
        department = "IT"
    elif choice == 3:
        department = "Finance"
    elif choice == 4:
        department = "Marketing"
    elif choice == 5:
        department = "Sales"
    else:
        print("Invalid department choice!")
        return
    
    basic_salary = get_number("Enter Basic Salary: ")
    
    while basic_salary <= 0:
        print("Basic Salary must be greater than zero!")
        basic_salary = get_number("Enter Basic Salary: ")
        
    hra, da, medical, ta, pf, gross_salary = calculate_salary(basic_salary)

    print("HRA:", hra, "%")
    print("DA:", da, "%")
    print("Medical:", medical, "%")
    print("TA:", ta, "%")
    print("PF:", pf, "%")
    print("Gross Salary:", gross_salary)

    hra_amount = (basic_salary * hra) / 100
    da_amount = (basic_salary * da) / 100
    medical_amount = (basic_salary * medical) / 100
    ta_amount = (basic_salary * ta) / 100
    pf_amount = (basic_salary * pf)/ 100

    gross_salary = basic_salary + hra_amount + da_amount + medical_amount + ta_amount - pf_amount

    cur.execute("INSERT INTO employee(Emp_ID, Emp_Name, Department, Basic_Salary, HRA, DA, Medical, TA, PF, Gross_Salary)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(emp_id,ename,department,basic_salary,hra,da,medical,ta,pf,gross_salary))
    
    con.commit()

    print("\nEmployee added successfully!")
    print("Employee ID: ",emp_id)
    print("Gross Salary:", gross_salary)
    print("\n" + "=" *75)
    
def search_employee():
    print("\n" + "=" * 75)
    print("                             SEARCH EMPLOYEE")
    print("=" * 75)

    print("\n1. Search by Employee ID")
    print("2. Search by Employee Name")
    print("3. Search by Department")
    print("4. Search by Basic Salary")
    print("5. Search by Salary Range")

    choice = get_number("\nEnter your choice: ")

    if choice == 1:
        emp_id = get_number("Enter Employee ID: ")

        if emp_id <= 0:
            print("\nEmployee ID must be greater than zero!")
            return
        
        cur.execute("SELECT * FROM employee WHERE Emp_ID = %s", (emp_id,))
        data = cur.fetchall()           

    elif choice == 2:
        name = input("Enter Employee Name: ")

        while name.strip() == "":
            print("Employee name cannot be empty!")
            name = input("Enter Employee Name: ")

        cur.execute("SELECT * FROM employee WHERE Emp_Name = %s", (name,))
        data = cur.fetchall()

    elif choice == 3:
        department = input("Enter Department: ")

        while department.strip() == "":
            print("Department name cannot be empty!")
            department = input("Enter Department: ")

        cur.execute("SELECT * FROM employee WHERE Department = %s", (department,))
        data = cur.fetchall()

    elif choice == 4:
        salary = get_number("Enter Basic Salary: ")

        if salary < 0:
            print("\nSalary cannot be negative!")
            return
        cur.execute("SELECT * FROM employee WHERE Basic_Salary = %s", (salary,))
        data = cur.fetchall()

    elif choice == 5:
        min_salary = get_number("Enter Minimum Salary: ")
        max_salary = get_number("Enter Maximum Salary: ")

        if min_salary < 0 or max_salary < 0:
            print("\nSalary cannot be negative!")
            return

        if min_salary > max_salary:
            print("\nMinimum salary cannot be greater than maximum salary!")
            return
        
        cur.execute("SELECT *FROM employee WHERE Basic_Salary BETWEEN %s and %s",(min_salary,max_salary))
        data = cur.fetchall()
    else:
        print("\nInvalid choice!")
        return

    if data:
        print("\nE_ID | E_Name | Depart. | B.Salary | HRA | DA | Medi. | TA | PF | G.Salary")
        print("\n" + "-" * 75)

        for d in data:
            print(str(d).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
            print("-" * 75)

    else:
        print("\nNo employee records found!")
            
def display_employees():

    while True:
        
        print("\n" + "=" *75)
        print("                             DISPLAY EMPLOYEES")     
        print("=" * 75)

        print("\n1. Display All Employees")
        print("2. Display in Ascending Order")
        print("3. Display in Descending Order")
        print("4. Display by Department")
        print("5. Back to Main Menu")

        choice = int(input("\n Enter your choice: "))

        if choice == 1:
          cur.execute("SELECT * FROM employee")  
          data = cur.fetchall()
          print("E_ID | E_Name | Department | B Salary | HRA | DA | Medical | TA | PF | G Salary")
          print("-" * 75)
          for d in data:
              print(str(d).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
              print("-" * 75)

        elif choice == 2:
            cur.execute("SELECT *FROM employee ORDER BY Basic_Salary ASC")
            data = cur.fetchall()
            print("E_ID | E_Name | Department | B Salary | HRA | DA | Medical | TA | PF | G Salary")
            print("-" * 75)
            for d in data:
                print(str(d).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                print("-" * 75)

        elif choice == 3:
            cur.execute("SELECT *FROM employee ORDER BY Basic_Salary DESC")
            data = cur.fetchall()
            print("E_ID | E_Name | Department | B Salary | HRA | DA | Medical | TA | PF | G Salary")
            print("-" * 75)
            for d in data:
                print(str(d).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                print("-" * 75)

        elif choice == 4:
            department = input("Enter Department: ")
            
            while department.strip() == "":
                print("Department name cannot be empty!")
                department = input("Enter Department: ")
                
            cur.execute("SELECT *FROM employee WHERE department = %s",(department,))
            data = cur.fetchall()
            
            if data:
                print("\nEmployees in",department)
                print("-" * 75)
                print("E_ID | E_Name | Department | B Salary | HRA | DA | Medical | TA | PF | G Salary")
                print("-" * 75)
                for d in data:
                    print(str(d).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))
                    print("-" * 75)
            else:
                print("\nNo employee found in this department!")

        elif choice == 5:
            break

        else:
            print("Invalid Choice!")
              
def delete_employee():
    print("\n" + "=" * 75)
    print("                             DELETE EMPLOYEE")
    print("=" * 75)

    emp_id = int(input("Enter Employee ID to delete: "))

    cur.execute("SELECT * FROM employee WHERE Emp_ID = %s", (emp_id,))
    data = cur.fetchone()

    if data:
        print("\nEmployee found:")
        print("\nE_ID | E_Name | Department | B Salary | HRA | DA | Medical | TA | PF | G Salary")
        print(str(data).replace(",", "|").replace("(", "").replace(")", "").replace("'", ""))

        confirm = input("\nDo you want to delete this employee? (yes/no): ")

        if confirm.lower() == "yes":
            cur.execute("DELETE FROM employee WHERE Emp_ID = %s", (emp_id,))
            con.commit()

            print("\nEmployee deleted successfully!")

        else:
            print("\nDeletion cancelled!")

    else:
        print("\nEmployee ID not found!")
        
print("\n" + "=" * 75)
print("                        EMPLOYEE MANAGEMENT SYSTEM")
print("=" * 75)

while True:

    print("\n1. Add Employee")
    print("2. Search Employee")
    print("3. Display Employees")
    print("4. Delete Employee")
    print("5. Update Employee")
    print("6. Employee Statistics")
    print("7. Department Analysis")
    print("8. Attendance Management")
    print("9. Salary Distribution Analysis")
    print("10. Exit")

    choice = get_number("\nEnter your choice: ")


    if choice == 1:
        add_employee()

    elif choice == 2:
        search_employee()

    elif choice == 3:
        display_employees()

    elif choice == 4:
        delete_employee()

    elif choice == 5:
        update_employee()

    elif choice == 6:
        employee_statistics()

    elif choice == 7:
        department_anlaysis()

    elif choice == 8:
        attendance_management()

    elif choice == 9:
        salary_distribution()
        
    elif choice == 10:
        print("\nThank you for using Employee Management System!")
        break
    
    else:
        print("Invalid choice! Please select a valid option from the menu.")
