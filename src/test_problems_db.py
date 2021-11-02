import os
import problems_db
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    test = problems_db.problemsDB(
        "localhost", "root", os.environ['MYSQL_PASSWORD'])

    test.reset_tables()
    # eventually we'll validate urls, but for now its an ok test
    test.insert_problem("two sum", "www.s3.com/twosum")
    test.insert_problem("three sum", "www.s3.com/threesum")
    test.insert_testcase(1, "www.s3.com/1", "www.s3.com/2")
    test.dump_all()
    test.cursor.close()
    test.db.close()
