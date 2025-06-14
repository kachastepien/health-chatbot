
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def get_user_by_email(email):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, first_name, last_name FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_patient_context(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT age, gender, weight, height FROM user WHERE id = %s", (user_id,))
    user_row = cursor.fetchone()
    cursor.execute("SELECT hearing, seeing, addictions, extra_diseases, medicine FROM patient_card WHERE user_id = %s", (user_id,))
    patient_row = cursor.fetchone()
    conn.close()

    if not user_row or not patient_row:
        return "Brak danych medycznych."

    context = f"""Pacjent ma {user_row[0]} lat, płeć: {user_row[1]}, waga {user_row[2]} kg, wzrost {user_row[3]} cm. 
Ma problemy ze słuchem: {patient_row[0]}, ze wzrokiem: {patient_row[1]}, uzależnienia: {patient_row[2]}. 
Choroby przewlekłe: {patient_row[3]}. Obecnie bierze leki: {patient_row[4]}."""
    return context
