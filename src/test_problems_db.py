import os
import problems_db
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    test = problems_db.problemsDB(
        "localhost", "root", os.environ['MYSQL_PASSWORD'])

    test.reset_tables()
    test.insert_problem("two sum", "Find the smallest array that can contain your mother mod 10**9 + 7")
    test.insert_problem("find sum", "add two numbers\nINPUT:\nfirst line is n\nafter that n lines of two numbers to sum")
    test.insert_testcase(1, "2\n1 2\n2 3", "3\n5")
    test.insert_testcase(1, "2\n9 1\n2 5", "10\n7")
    test.insert_testcase(1, "1\n100 1", "101")
    test.insert_testcase(2, "2\n1 2\n2 3", "3\n5")
    test.dump_all()
    test.cursor.close()
    test.db.close()
