import psycopg2

def connect():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="Mergeed_DB",
        user="myuser",
        password="mypassword"
    )
