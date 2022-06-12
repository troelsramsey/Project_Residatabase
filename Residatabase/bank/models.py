# write all your SQL queries in this file.
from datetime import datetime
from bank import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql
import math

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    schema = 'customers'
    id = 'cpr_number'
    if str(user_id).startswith('60'):
        schema = 'employees'
        id = 'id'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        return Employees(cur.fetchone()) if schema == 'employees' else Customers(cur.fetchone())
    else:
        return None


class Customers(tuple, UserMixin):
    def __init__(self, user_data):
        self.CPR_number = user_data[0]
        self.risktype = False
        self.password = user_data[2]
        self.name = user_data[3]
        self.address = user_data[4]

    def get_id(self):
       return (self.CPR_number)

class Employees(tuple, UserMixin):
    def __init__(self, employee_data):
        self.id = employee_data[0]
        self.name = employee_data[1]
        self.password = employee_data[2]

    def get_id(self):
       return (self.id)

class CheckingAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.create_date = user_data[1]
        self.CPR_number = user_data[2]
        self.amount = 0

class InvestmentAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.start_date = user_data[1]
        self.maturity_date = user_data[2]
        self.amount = 0

class Transfers(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.amount = user_data[1]
        self.transfer_date = user_data[2]

def insert_Customers(name, CPR_number, password):
    cur = conn.cursor()
    sql = """
    INSERT INTO Customers(name, CPR_number, password)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (name, CPR_number, password))
    conn.commit()
    cur.close()

def select_Customers(CPR_number):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Customers
    WHERE CPR_number = %s
    """
    cur.execute(sql, (CPR_number,))
    user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Employees(id):
    cur = conn.cursor()
    sql = """
    SELECT * FROM Employees
    WHERE id = %s
    """
    cur.execute(sql, (id,))
    user = Employees(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user



def search_apt(depo, rent, dist, size, sort):
    cur = conn.cursor()
    # sql = """SELECT * MAX(rent) FROM ap
    # WHERE Rent <= %s AND Rent <= %s AND Size >= %s)
    # groupby Municipality
    # """
    sql = """
    SELECT * FROM ap
    WHERE ap.rent <= %s AND ap.rent <= %s + ap.distance * 10 AND ap.size >= %s AND ap.distance < %s
    """
    #ORDER BY ap.%s
    x1 = str(math.ceil(float(depo)/4))
    x2 = str(math.ceil(float(rent)))
    x3 = str(math.ceil((float(size) - 45) / 10))
    x4 = str(dist)
    x5 = ('"'+sort+'"').strip('"\'')
    print(x5)
    cur.execute(sql, (x1, x2, x3, x4))
    apt = cur.fetchall() if cur.rowcount > 0 else None;
    cur.close()
    return apt



def update_CheckingAccount(amount, CPR_number):
    cur = conn.cursor()
    sql = """
    UPDATE CheckingAccount
    SET amount = %s
    WHERE CPR_number = %s
    """ 
    cur.execute(sql, (amount, CPR_number))
    conn.commit()
    cur.close()
    
def transfer_account(date, amount, from_account, to_account):
    cur = conn.cursor()
    sql = """
    INSERT INTO Transfers(transfer_date, amount, from_account, to_account)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (date, amount, from_account, to_account))
    conn.commit()
    cur.close()

def select_emp_cus_accounts(emp_cpr_number):
    cur = conn.cursor()
    sql = """
    SELECT
      e.name employee
    , c.name customer 
    , cpr_number
    , account_number 
    FROM manages m
      NATURAL JOIN accounts  
      NATURAL JOIN customers c
      JOIN employees e ON m.emp_cpr_number = e.id
	WHERE emp_cpr_number = %s 
    ;
    """
    cur.execute(sql, (emp_cpr_number,))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_investments(CPR_number):
    cur = conn.cursor()
    sql = """
    SELECT i.account_number, a.cpr_number, a.created_date 
    FROM investmentaccounts i
    JOIN accounts a ON i.account_number = a.account_number    
    WHERE a.cpr_number = %s
    """
    cur.execute(sql, (CPR_number,))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_investments_with_certificates(CPR_number):
    cur = conn.cursor()
    sql = """
    SELECT i.account_number, a.cpr_number, a.created_date
    , cd.cd_number, start_date, maturity_date, rate, amount 
    FROM investmentaccounts i
    JOIN accounts a ON i.account_number = a.account_number
    JOIN certificates_of_deposit cd ON i.account_number = cd.account_number    
    WHERE a.cpr_number = %s
    """
    cur.execute(sql, (CPR_number,))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def select_investments_certificates_sum(CPR_number):
    print(CPR_number)
    cur = conn.cursor()
    sql = """
    SELECT account_number, cpr_number, created_date, sum
    FROM vw_cd_sum
    WHERE cpr_number = %s
    """
    cur.execute(sql, (CPR_number,))
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset
