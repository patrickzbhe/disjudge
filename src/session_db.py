import mysql.connector

# We don't actually need this yet, I'll just put this here for now as a todo


class SessionDB:
    def __init__(self, host, user, password):
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        c = db.cursor()

        if "session_state" not in c.execute("SHOW DATABASES"):
            c.execute("CREATE DATABASE session_state")

        c.close()

        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="session_state"
        )

        self.c = self.db.cursor()
