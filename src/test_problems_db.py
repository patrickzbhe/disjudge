import os
import problems_db
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    test = problems_db.problemsDB(
        "localhost", "root", os.environ['MYSQL_PASSWORD'])

    test.reset_tables()
    test.insert_problem("two sum", "Find the smallest array that can contain your mother mod 10**9 + 7")
    test.insert_problem("three sum", "asdfasdfasdfasdfasdfasdfasdfasdf")
    test.insert_testcase(1, "AMITTTTAMI APTEL", "ssssssssssssssssssssssssssssss")
    test.dump_all()
    test.cursor.close()
    test.db.close()
