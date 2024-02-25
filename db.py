import sqlite3

class Database:
    def __init__(self,db):
        self.con=sqlite3.connect(db)
        self.cur=self.con.cursor()
        sql="""
        CREATE TABLE IF NOT EXISTS Pathology(
        id Integer Primary Key,
        name text,
        age text,
        doj text,
        gender text,
        blood text,
        testtype text,
        address text
         )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self,name,age,doj,gender,blood,testtype,address):
        self.cur.execute("insert into pathology values(NULL,?,?,?,?,?,?,?)",
                         (name,age,doj,gender,blood,testtype,address))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * from pathology")
        rows=self.cur.fetchall()
        return rows


    def remove(self,id):
        self.cur.execute("delete from pathology where id=?",(id,))
        self.con.commit()



    def update(self,id,name,age,dob,gender,blood,testtype,address):
        self.cur.execute("update pathology set name=?, age=?, dob=?, email =?, gender=?, contact=?, address=? where id=? ",
                         (name,age,dob,gender,blood,testtype,address,id))
        self.con.commit()

