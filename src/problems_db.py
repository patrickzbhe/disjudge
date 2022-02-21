import mysql.connector
import random

class problemsDB:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connect()

    def connect(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        c = db.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS Problems")
        c.close()

        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database="Problems"
        )
        self.cursor = self.db.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Problems (problemID INT NOT NULL AUTO_INCREMENT, problem_name VARCHAR(255), description_url VARCHAR(1024), PRIMARY KEY (problemID))"
        )

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS TestCases 
                (testcaseID INT NOT NULL AUTO_INCREMENT,
                problemID INT, input_url VARCHAR(1024), output_url VARCHAR(1024),
                PRIMARY KEY (testcaseID), 
                FOREIGN KEY (problemID) REFERENCES Problems(problemID))"""
        )
        self.db.commit()

    def insert_problem(self, problem_name, description_url):
        self.cursor.execute(
            "INSERT INTO Problems (problem_name, description_url) VALUES ('{0}', '{1}')".format(
                problem_name, description_url)
        )
        self.db.commit()

    def delete_problem(self, problemID):
        self.cursor.execute(
            "DELETE FROM Problems WHERE problemID='{0}'".format(problemID)
        )
        self.db.commit()

    def insert_testcase(self, problemID, input_url, output_url):
        self.cursor.execute(
            "INSERT INTO TestCases (problemID, input_url, output_url) VALUES ({0}, '{1}', '{2}')".format(
                problemID, input_url, output_url)
        )
        self.db.commit()

    def delete_testcase(self, testcaseID):
        self.cursor.execute(
            "DELETE FROM TestCases WHERE testcaseID='{0}'".format(testcaseID)
        )
        self.db.commit()

    def reset_tables(self):
        self.cursor.execute("DROP TABLE TestCases")
        self.cursor.execute("DROP TABLE Problems;")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Problems (problemID INT NOT NULL AUTO_INCREMENT, problem_name VARCHAR(255), description_url VARCHAR(1024), PRIMARY KEY (problemID))")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS TestCases 
                (testcaseID INT NOT NULL AUTO_INCREMENT,
                problemID INT, input_url VARCHAR(1024), output_url VARCHAR(1024),
                PRIMARY KEY (testcaseID), 
                FOREIGN KEY (problemID) REFERENCES Problems(problemID))""")
        self.db.commit()

    def getProblems(self):
        self.cursor.execute("SELECT * FROM Problems")
        return self.cursor.fetchall()

    def getProblemsSize(self):
        self.cursor.execute("SELECT COUNT(*) FROM Problems")
        count = self.cursor.fetchall()
        return count[0][0]

    def getRandomProblem(self):
        randomRow = random.randint(0,self.getProblemsSize())
        self.cursor.execute(f"SELECT * FROM Problems LIMIT 1 OFFSET {randomRow}")
        return self.cursor.fetchall()


    def dump_problems(self):
        self.cursor.execute("SELECT * FROM Problems")
        for res in self.cursor.fetchall():
            print(res)

    def dump_testcases(self):
        self.cursor.execute("SELECT * FROM TestCases")
        for res in self.cursor.fetchall():
            print(res)

    def dump_all(self):
        self.dump_problems()
        self.dump_testcases()
