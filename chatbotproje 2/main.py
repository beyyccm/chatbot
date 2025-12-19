from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
import chatbot_logic

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
@app.on_event("startup")
def startup():
    database.init_db()

# Models
class LoginRequest(BaseModel):
    student_id: str
    password: str

class ChatRequest(BaseModel):
    student_id: str
    message: str

# API Routes
@app.post("/api/login")
def login(data: LoginRequest):
    # Sanitize input
    s_id = data.student_id.strip()
    s_pass = data.password.strip()
    
    print(f"DEBUG: Received ID={repr(s_id)} PASS={repr(s_pass)}")
    
    student = database.get_student(s_id)
    if student:
        print(f"DEBUG: Stored ID={repr(student['id'])} PASS={repr(student['password'])}")
        
        if str(student['password']).strip() == str(s_pass).strip():
             # Calculate AGNO
             gpa, _, _, _ = chatbot_logic.get_student_agno(student['id'])
             
             return {
                "status": "success", 
                "name": student['name'], 
                "student_id": student['id'],
                "grade_level": student['grade_level'],
                "agno": f"{gpa:.2f}"
            }
        else:
            print("DEBUG: Password Mismatch!")
    else:
        print("DEBUG: User not found in DB")
    
    raise HTTPException(status_code=401, detail="Hatalı öğrenci numarası veya şifre")

@app.post("/api/chat")
def chat(data: ChatRequest):
    try:
        response_text = chatbot_logic.process_message(data.student_id, data.message)
        return {"response": response_text}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Mount Static Files (Frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
