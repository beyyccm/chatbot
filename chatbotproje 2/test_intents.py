import requests
import json

base_url = "http://0.0.0.0:8000/api/chat"
headers = {"Content-Type": "application/json"}

intents = [
    "Sınav tarihlerim ne zaman?",
    "Ders programım nasıl?",
    "Danışmanım kim?",
    "Alttan dersim var mı?",
    "Notlarımı göster",
    "Hocalarım kim?",
    "Proje bilgileri nedir?",
    "Ders seçimi hakkında bilgi ver",
    "Ahmet hocanın ofisi nerede?",
    "Hocaların odalarını göster",
    # New NLP Tests
    "merhaba",
    "selam",
    "hangi bölümdeyim?",
    "kaçıncı sınıfım?",
    "vize tarihleri",
    "final ne zaman?",
    "ödevim var mı?",
    "devamsızlıktan kaldım mı?",
    "okula gitmedim",
    "alttan dersim var mı?",
    "muafiyet durumu",
    # Course Selection Specifics
    "ders seçimim ne",
    "ders seçimi hakkında bilgi ver",
    "hangi dersleri seçmeliyim",
    "kayıt yenileme",
    # Specific Grade Tests
    "matematik notum kaç",
    "fizik notu",
    "ingilizce notum"
]

students = ["21010101", "21010102", "21010103", "21010104"]

for student_id in students:
    print(f"\n--- Testing Student {student_id} ---")

    for msg in intents:
        payload = {"student_id": student_id, "message": msg}
        try:
            r = requests.post(base_url, json=payload, headers=headers)
            if r.status_code != 200:
                print(f"[FAIL {r.status_code}] '{msg}'")
                print(f"Error: {r.text}")
            else:
                print(f"[OK] '{msg}'")
        except Exception as e:
            print(f"[ERR] '{msg}': {e}")
