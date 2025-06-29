import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",      # או השם של ה-container אם את עם Docker
        port="5432",
        database="Mergeed_DB",
        user="myuser",
        password="mypassword"
    )
