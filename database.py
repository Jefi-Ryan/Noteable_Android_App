import sqlite3
from datetime import datetime

# Database of All In One app

class db_app:
    def __init__(self):
        self.name = 'app.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS APP (name text,theme_color text)""")
        cursor.execute("""SELECT * FROM APP""")
        data = cursor.fetchall()
        if len(data)==0:
            cursor.execute("""INSERT INTO APP VALUES (?,?)""",('theme','Light'))
        conn.commit()
        conn.close()

    def update(self,color):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE APP SET theme_color=? WHERE name=?""",(color,'theme'))
        conn.commit()
        conn.close()

    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM APP""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()

        return data

class db_notes:
    def __init__(self):
        self.name='notes.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS NOTES (title text,content text,color text)""")
        conn.commit()
        conn.close()

    def insert(self,title,content,color):
        if len(color)==3:
            color=list(color).append(0)
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM NOTES WHERE title=?""",(title,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(title,title,content,color)
        else:
            cursor.execute("""INSERT INTO NOTES VALUES (?,?,?)""",(title,content,str(color)))
            conn.commit()
            conn.close()



    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM NOTES""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            title, content, color = i
            if '(' in color:
                temp = color.strip("()")
            else:
                temp = color.strip("[]")
            temp = temp.split(",")
            if color=='None':
                color=[0,0,0,0]
            else:
                color = list(map(lambda x: float(x.strip()), temp))
            all_data.update({title: [content, color]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM NOTES""")
        conn.commit()
        conn.close()

    def update(self,old_title,title,content,color):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE NOTES SET title=?,content=?,color=? WHERE title=?""",(title,content,str(color),old_title))
        conn.commit()
        conn.close()

    def delete(self,title):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM NOTES WHERE title=?""",(title,))
        conn.commit()
        conn.close()

class db_todo:
    def __init__(self):
        self.name='todo.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS TODO (title text,date text,time text,status text)""")
        conn.commit()
        conn.close()

    def insert(self,title,date,time,status):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM TODO WHERE title=?""",(title,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(title,title,date,time)
        else:
            cursor.execute("""INSERT INTO TODO VALUES (?,?,?,?)""",(title,date,time,status))
            conn.commit()
            conn.close()



    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM TODO""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            title, date, time, status = i
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            all_data.update({title: [date, time, status]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM TODO""")
        conn.commit()
        conn.close()

    def update(self,old_title,title,date,time,status):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE TODO SET title=? , date=? , time=?, status=? WHERE title=?""",(title,date,time,status,old_title))
        conn.commit()
        conn.close()

    def delete(self,title):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM TODO WHERE title=?""",(title,))
        conn.commit()
        conn.close()


class db_reminder:
    def __init__(self):
        self.name='reminder.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS REMINDER (title text,date text,time text,cycle text)""")
        conn.commit()
        conn.close()

    def insert(self,title,date,time,cycle):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM REMINDER WHERE title=?""",(title,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(title,title,date,time,cycle)
        else:
            cursor.execute("""INSERT INTO REMINDER VALUES (?,?,?,?)""",(title,date,time,str(cycle)))
            conn.commit()
            conn.close()



    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM REMINDER""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            title, date, time, cycle = i
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            all_data.update({title: [date, time, cycle]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM REMINDER""")
        conn.commit()
        conn.close()

    def update(self,old_title,title,date,time,cycle):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE REMINDER SET title=? , date=? , time=?, cycle=? WHERE title=?""",(title,date,time,str(cycle),old_title))
        conn.commit()
        conn.close()

    def delete(self,title):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM REMINDER WHERE title=?""",(title,))
        conn.commit()
        conn.close()


class db_income:
    def __init__(self):
        self.name='income.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS INCOME (source text,amount text,cycle text,date text)""")
        conn.commit()
        conn.close()

    def insert(self,source,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM INCOME WHERE source=?""",(source,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(source,source,amount,cycle,date)
        else:
            cursor.execute("""INSERT INTO INCOME VALUES (?,?,?,?)""",(source,str(amount),str(cycle),date))
            conn.commit()
            conn.close()

    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM INCOME""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            source,amount,cycle,date = i
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            all_data.update({source: [amount, cycle, date]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM INCOME""")
        conn.commit()
        conn.close()

    def update(self,old_source,source,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE INCOME SET source=? , amount=? , cycle=?, date=? WHERE source=?""",(source,str(amount),str(cycle),date,old_source))
        conn.commit()
        conn.close()

    def delete(self,source):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM INCOME WHERE source=?""",(source,))
        conn.commit()
        conn.close()


class db_my_list:
    def __init__(self):
        self.name='my_list.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS LIST (title text,amount text,cycle text,date text)""")
        conn.commit()
        conn.close()

    def insert(self,title,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM LIST WHERE title=?""",(title,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(title,title,amount,cycle,date)
        else:
            cursor.execute("""INSERT INTO LIST VALUES (?,?,?,?)""",(title,str(amount),str(cycle),date))
            conn.commit()
            conn.close()

    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM LIST""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            title,amount, cycle,date = i
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            all_data.update({title: [amount, cycle,date]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM LIST""")
        conn.commit()
        conn.close()

    def update(self,old_title,title,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE LIST SET title=? , amount=? , cycle=?, date=? WHERE title=?""",(title,str(amount),str(cycle),date,old_title))
        conn.commit()
        conn.close()

    def delete(self,title):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM LIST WHERE title=?""",(title,))
        conn.commit()
        conn.close()

class db_loan:
    def __init__(self):
        self.name='loan.db'
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS LOAN (title text,amount text,cycle text,date text)""")
        conn.commit()
        conn.close()

    def insert(self,title,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM LOAN WHERE title=?""",(title,))
        test_data=cursor.fetchall()
        if len(test_data)>0:
            conn.close()
            self.update(title,title,amount,cycle,date)
        else:
            cursor.execute("""INSERT INTO LOAN VALUES (?,?,?,?)""",(title,str(amount),str(cycle),date))
            conn.commit()
            conn.close()

    def retrieve(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM LOAN""")
        data=cursor.fetchall()
        conn.commit()
        conn.close()
        all_data = dict()
        for i in data:
            title,amount, cycle,date = i
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            all_data.update({title: [amount, cycle,date]})
        return all_data

    def delete_all(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM LOAN""")
        conn.commit()
        conn.close()

    def update(self,old_title,title,amount,cycle,date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""UPDATE LOAN SET title=? , amount=? , cycle=?, date=? WHERE title=?""",(title,str(amount),str(cycle),date,old_title))
        conn.commit()
        conn.close()

    def delete(self,title):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM LOAN WHERE title=?""",(title,))
        conn.commit()
        conn.close()

