import requests
import json

base_url = "http://0.0.0.0:8000/api/login"
headers = {"Content-Type": "application/json"}

credentials = [
    {"student_id": "21010101", "password": "12345"}, # Valid
    {"student_id": "21010102", "password": "12345"}, # Valid
    {"student_id": "21010101", "password": "WRONG"}, # Invalid
    {"student_id": "99999999", "password": "12345"}  # Non-existent
]

print("Testing Login Endpoint...")

for cred in credentials:
    try:
        r = requests.post(base_url, json=cred, headers=headers)
        print(f"ID: {cred['student_id']} | Pass: {cred['password']} -> Status: {r.status_code} | Response: {r.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")
