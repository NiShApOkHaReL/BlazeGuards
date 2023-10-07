import streamlit as st
import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host = "localhost",
        database = "blazeguards",
        id = "root",
        password = ""
    )
    cursor = conn.cursor()
    return conn, cursor