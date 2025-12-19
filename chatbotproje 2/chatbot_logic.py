from database import get_student, get_student_details_full

def get_student_agno(student_id):
    """Calculates AGNO based on course final/midterm grades and credits."""
    _, courses_full = get_student_details_full(student_id)
    
    total_points = 0.0
    total_credits = 0
    
    formatted_details = ""
    
    for row in courses_full:
        c = dict(row)
        credit = c.get('credit', 0)
        
        # Determine Grade
        score = None
        if c['final'] is not None:
            score = c['final']
        elif c['midterm'] is not None:
            score = c['midterm']
        
        if score is None: continue 
        
        # Convert to 4.0 Scale
        points = 0.0
        letter = "FF"
        
        if score >= 90: points = 4.0; letter = "AA"
        elif score >= 85: points = 3.5; letter = "BA"
        elif score >= 80: points = 3.0; letter = "BB"
        elif score >= 75: points = 2.5; letter = "CB"
        elif score >= 70: points = 2.0; letter = "CC"
        elif score >= 65: points = 1.5; letter = "DC"
        elif score >= 60: points = 1.0; letter = "DD"
        elif score >= 50: points = 0.5; letter = "FD"
        else: points = 0.0; letter = "FF"
        
        weighted = points * credit
        total_points += weighted
        total_credits += credit
        
        formatted_details += f"<li>{c['code']}: {score} ({letter}) x {credit} Kredi = {weighted:.1f} Puan</li>"

    gpa = 0.00
    if total_credits > 0:
        gpa = total_points / total_credits
        
    return gpa, total_credits, total_points, formatted_details

def process_message(student_id, message):
    message = message.lower()
    
    # Fetch Student Info directly for Dept
    # Fetch Student Info
    student_basic_row = get_student(student_id)
    student_basic = dict(student_basic_row) if student_basic_row else {}
    
    advisor_row, courses_rows = get_student_details_full(student_id)
    advisor = dict(advisor_row) if advisor_row else None
    courses = [dict(row) for row in courses_rows] if courses_rows else []
    
    # Intent: Greeting & Small Talk (Genişletildi)
    if any(x in message for x in ["merhaba", "selam", "günaydın", "iyi günler", "hey", "tünaydın", "iyi akşamlar", "naber", "nasılsın"]):
        if "nasılsın" in message or "naber" in message:
             return f"Teşekkür ederim, sanal bir asistan olarak her zaman harikayım! 🤖 {student_basic.get('name', 'Öğrenci')} için ne yapabilirim?"
        return f"Merhaba {student_basic.get('name', '')}! Sana derslerin, sınavların, projelerin veya hocaların hakkında yardımcı olabilirim."

    # Intent: Capabilities / Help (Yetenekler - YENİ)
    if any(x in message for x in ["ne yapabilirsin", "yardım", "komutlar", "özellikler", "neler var", "kullanım"]):
        return """
        <strong>Yapabildiklerim:</strong><br>
        <ul>
            <li><b>Notlar:</b> "Matematik notum kaç?", "Transkriptimi göster"</li>
            <li><b>Ortalama:</b> "AGNO hesapla", "Ortalamam kaç?"</li>
            <li><b>Program:</b> "Ders programı", "Pazartesi dersim var mı?"</li>
            <li><b>Sınavlar:</b> "Vize tarihleri", "Yapay zeka sınavı ne zaman?"</li>
            <li><b>Devamsızlık:</b> "Devamsızlığım kaç gün?", "Kaldığım ders var mı?"</li>
            <li><b>Hocalar:</b> "Danışmanım kim?", "Fizik hocası nerede?"</li>
            <li><b>Projeler:</b> "Teslim tarihi ne zaman?", "Ödevim var mı?"</li>
        </ul>
        """

    # Intent: Department & Grade (Bölüm/Sınıf)
    if any(x in message for x in ["bölüm", "fakülte", "sınıf", "kaçıncı", "okuyorum", "statü"]):
        grade = student_basic.get('grade_level', '?')
        dept = student_basic.get('department', 'Bilinmiyor')
        return f"Şu anda <strong>{dept}</strong> bölümü <strong>{grade}. Sınıf</strong> öğrencisisiniz."

    # Intent: Instructors (Hocalar)
    if any(x in message for x in ["hocalar", "öğretmenler", "profesör", "kim veriyor", "dersin hocası"]):
        response = "<strong>Dersleriniz ve Öğretim Üyeleri:</strong><br><ul>"
        
        # Add Advisor first
        if advisor:
             response += f"<li><b>Danışman:</b> {advisor['name']} (Ofis: {advisor['office']})</li><br>"
        
        # Add Course Instructors
        for c in courses:
            if c['instructor_name']:
                response += f"<li><b>{c['name']} ({c['code']}):</b><br>{c['instructor_name']}<br>Ofis: {c['instructor_office']}<br>Email: {c['instructor_email']}</li>"
        
        response += "</ul>"
        return response

    # Intent: Advisor Info
    if any(x in message for x in ["danışman", "hoca", "kim", "akademik"]):
        if advisor:
            return f"Danışman Hocanız: {advisor['name']}<br>Email: {advisor['email']}<br>Ofis: {advisor['office']}"
        return "Danışman bilgisi bulunamadı."

    # Intent: Exam Dates (Sınavlar)
    if any(x in message for x in ["sınav", "tarih", "vize", "final", "büt", "ne zaman", "takvim"]):
        # Mock Date Logic for 'Yarın' (Assumption: Today is 2025-01-01 for demo purposes)
        # In a real app we would use datetime.now()
        demo_today_str = "2025-01-01"
        demo_tomorrow_str = "2025-01-02"

        filter_course = None
        filter_date = None
        
        # Check for 'yarın'
        if "yarın" in message or "yarin" in message:
            filter_date = demo_tomorrow_str

        # Check for specific course codes or names
        for c in courses:
             # Check exact code match first
             if c['code'].lower() in message:
                 filter_course = c
                 break
             # Check name parts
             name_parts = [part for part in c['name'].lower().split() if len(part) > 3]
             if any(part in message for part in name_parts):
                 filter_course = c
                 break
        
        response = ""
        if filter_date:
             response = f"<strong>Yarınki ({filter_date}) Sınavlarınız:</strong><br><ul>"
        else:
             response = "<strong>Sınav Tarihleri:</strong><br><ul>"

        found = False
        for c in courses:
            if not c.get('exam_date'): continue
            
            # Filter by Course if requested
            if filter_course and c['code'] != filter_course['code']: continue
            
            # Filter by Date if requested
            if filter_date and filter_date not in c['exam_date']: continue

            response += f"<li>{c['name']} ({c['code']}): {c['exam_date']}</li>"
            found = True
            
        response += "</ul>"
        
        if not found:
             if filter_date: return "Yarın herhangi bir sınavınız görünmüyor."
             if filter_course: return f"{filter_course['name']} dersi için planlanmış bir sınav tarihi bulunamadı."
             return "Sınav tarihi bilgisi bulunamadı."
             
        return response

    # Intent: Schedule / Program (Ders Programı)
    schedule_keywords = [
        "ders programı", "saat", "program", "hangi gün", "zaman", "günler", 
        "dersim var mı", "ne dersim var", "bugün ne var", "yarın ders var mı",
        "hangi derslere gireceğim", "ders çizelgesi", "haftalık program", "ders saatleri",
        "bugünkü dersler", "yarınki dersler", "dersim ne", "dersim", "hangi ders", "ne var", "ders var"
    ]
    if any(x in message for x in schedule_keywords):
        # Define day order for sorting
        days_order = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar", "Online"]
        
        # Group by day
        schedule_map = {day: [] for day in days_order}
        
        for c in courses:
            sched = c.get('schedule', '')
            if not sched: continue
            
            # Simple day extraction
            found_day = "Diğer"
            for day in days_order:
                if day in sched:
                    found_day = day
                    break
            
            if found_day in schedule_map:
                schedule_map[found_day].append(f"{c['name']} ({c['code']}): {sched}")
            else:
                 # Fallback if "Diğer" or unexpected
                 if "Diğer" not in schedule_map: schedule_map["Diğer"] = []
                 schedule_map["Diğer"].append(f"{c['name']}: {sched}")

        # Detect specific day request (Enhanced)
        tr_days = {"pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar", "bugün", "yarın"}
        found_day_in_msg = next((d for d in tr_days if d in message), None)
        
        requested_days = []
        if found_day_in_msg:
             # Handle today/tomorrow roughly (assuming fixed mock date or simple logic, here we map strictly to names)
             # For simplicity in mock, we map 'bugün' to 'Pazartesi' as default demo day or just ignore dynamic date
             if found_day_in_msg == "bugün": requested_days = ["Pazartesi"] # Demo assumption
             elif found_day_in_msg == "yarın": requested_days = ["Salı"]    # Demo assumption
             else: requested_days = [d for d in days_order if d.lower() == found_day_in_msg]

        response = ""
        if requested_days:
             response = f"<strong>{', '.join(requested_days)} Günü Ders Programınız:</strong><br>"
        else:
             response = "<strong>Haftalık Ders Programınız:</strong><br>"
             requested_days = days_order # Show all

        has_schedule = False
        
        for day in days_order:
            if day in requested_days:
                if schedule_map[day]:
                    has_schedule = True
                    response += f"<br><b>{day}:</b><ul>"
                    for item in schedule_map[day]:
                        response += f"<li>{item}</li>"
                    response += "</ul>"
                elif len(requested_days) == 1:
                    response += f"<br><b>{day}:</b> Ders programınızda bu gün için ders bulunmamaktadır."
                
        return response if has_schedule or len(requested_days) == 1 else "Ders programı bilgisi bulunamadı."

    # Intent: Project Info (Proje/Ödev)
    if any(x in message for x in ["proje", "ödev", "teslim", "konu", "yapılacak", "laboratuvar", "rapor"]):
        response = "<strong>Proje Bilgileri:</strong><br><ul>"
        found = False
        for c in courses:
            if c.get('project_topic'):
                found = True
                score = c.get('project_score')
                status = "<span style='color:green'>Tamamlandı</span>" if score is not None else "<span style='color:orange'>Devam Ediyor</span>"
                response += f"<li><b>{c['name']}</b> ({status})<br>Konu: {c['project_topic']}<br>Teslim T.: {c['project_deadline']}<br>"
                if score is not None: response += f"<b>Proje Notu: {score}/100</b><br>"
                response += f"Açıklama: {c['project_note']}</li>"
        response += "</ul>"
        return response if found else "Aktif proje ödeviniz görünmüyor."

    # Intent: Attendance (Devamsızlık)
    if any(x in message for x in ["devamsızlık", "yoklama", "gitmedim", "kaç gün", "kaldım", "devam durumu"]):
        # Check for specific course
        specific_course = None
        for c in courses:
             if c['code'].lower() in message:
                 specific_course = c
                 break
             name_parts = [part for part in c['name'].lower().split() if len(part) > 2]
             if any(part in message for part in name_parts):
                 specific_course = c
                 break
        
        if specific_course:
            val = specific_course.get('attendance_absent', 0)
            status = str(val) + " gün"
            if val > 4: status += " <span style='color:red'>(Dikkat!)</span>"
            return f"<strong>{specific_course['name']} Devamsızlık Durumu:</strong><br>{status}"

        response = "<strong>Devamsızlık Durumu:</strong><br><ul>"
        for c in courses:
            if c.get('attendance_absent') is not None:
                status = str(c['attendance_absent']) + " gün"
                if c['attendance_absent'] > 4: status += " <span style='color:red'>(Dikkat!)</span>"
                response += f"<li>{c['name']}: {status}</li>"
        response += "</ul>"
        return response

    # Intent: Failed Courses (Alttan)
    failed_keywords = [
        "alttan", "kaldı", "tekrar", "başarısız", "geçemedim", "büte", 
        "kaldığım", "ff", "geçemediğim", "kaldım fizik", "kaldım matematik"
    ]
    if any(x in message for x in failed_keywords):
        if student_basic.get('grade_level') == 1:
            return "1. Sınıf öğrencisi olduğunuz için henüz alttan dersiniz bulunmamaktadır."

        response = "<strong>Alttan Aldığınız Dersler:</strong><br><ul>"
        found = False
        for c in courses:
            if c.get('is_retake'):
                response += f"<li>{c['name']} ({c['code']})</li>"
                found = True
        response += "</ul>"
        return response if found else "Alttan aldığınız ders bulunmamaktadır."

    # Intent: Exemptions (Muafiyet)
    if any(x in message for x in ["muaf", "saydırma", "intibak", "onay"]):
        response = "<strong>Muafiyet Bilgileri:</strong><br>"
        exempted_courses = [c for c in courses if c.get('is_exempt')]
        if exempted_courses:
            response += "<ul>" + "".join([f"<li>{c['name']} ({c['code']}): <b>Muaf</b></li>" for c in exempted_courses]) + "</ul><br>"
        else:
            response += "Sistemde muaf olduğunuz ders kaydı bulunmamaktadır.<br><br>"
        response += "<i>Genel Bilgi: Muafiyet başvuruları her dönem başında fakülte öğrenci işlerine yapılmaktadır.</i>"
        return response

    # Intent: Filter by Letter Grade (Harf Notu Sorgulama)
    letter_grades = ["aa", "ba", "bb", "cb", "cc", "dc", "dd", "fd", "ff"]
    requested_grade = next((grade.upper() for grade in letter_grades if grade in message.split()), None)
    
    # Check for phrases like "aa aldığım" or just "aa var mı"
    if requested_grade:
        response = f"<strong>{requested_grade} Harf Notu Aldığınız Dersler:</strong><br>"
        found_courses = []
        
        for c in courses:
            # Skip if Exempt (Muaf) or incomplete
            if c.get('is_exempt') or c['midterm'] is None or c['final'] is None:
                continue
                
            # Calculate Grade
            avg = (c['midterm'] * 0.4) + (c['final'] * 0.6)
            
            letter = "FF"
            if avg >= 90: letter = "AA"
            elif avg >= 85: letter = "BA"
            elif avg >= 80: letter = "BB"
            elif avg >= 75: letter = "CB"
            elif avg >= 70: letter = "CC"
            elif avg >= 65: letter = "DC"
            elif avg >= 60: letter = "DD"
            elif avg >= 50: letter = "FD"
            
            if letter == requested_grade:
                found_courses.append(f"<li>{c['name']} ({c['code']}): {avg:.1f}</li>")
        
        if found_courses:
            response += "<ul>" + "".join(found_courses) + "</ul>"
            return response
        else:
            return f"{requested_grade} harf notu aldığınız herhangi bir ders bulunmamaktadır."

    # Intent: Transcript / All Grades (Tüm dersler, notlar)
    if any(x in message for x in ["not", "puan", "dersler", "transkript", "karne", "sonuçlar", "açıklandı mı"]):
        specific_courses = []
        for c in courses:
            if c['code'].lower() in message:
                specific_courses.append(c)
                continue
            name_parts = [part for part in c['name'].lower().split() if len(part) > 2]
            if any(part in message for part in name_parts):
                specific_courses.append(c)
        
        display_courses = specific_courses if specific_courses else courses
        title = "İstenen Dersin Notu:" if specific_courses else "Tüm Dersler ve Not Durumu:"
        
        response = f"<strong>{title}</strong><br><table border='1' style='width:100%; border-collapse: collapse; font-size: 0.9rem;'><tr><th>Ders</th><th>Vize</th><th>Final</th><th>Ortalama</th></tr>"
        for c in display_courses:
            mid = c['midterm'] if c['midterm'] is not None else "-"
            fin = c['final'] if c['final'] is not None else "-"
            avg_display = "-"
            
            if c.get('is_exempt'):
                mid = "MUAF"
                fin = "MUAF"
                avg_display = "MUAF"
            elif c['midterm'] is not None and c['final'] is not None:
                # Calculate Weighted Average
                avg = (c['midterm'] * 0.4) + (c['final'] * 0.6)
                
                # Determine Letter Grade
                letter = "FF"
                if avg >= 90: letter = "AA"
                elif avg >= 85: letter = "BA"
                elif avg >= 80: letter = "BB"
                elif avg >= 75: letter = "CB"
                elif avg >= 70: letter = "CC"
                elif avg >= 65: letter = "DC"
                elif avg >= 60: letter = "DD"
                elif avg >= 50: letter = "FD"
                
                avg_display = f"{avg:.1f} ({letter})"
            
            response += f"<tr><td>{c['code']} - {c['name']}</td><td>{mid}</td><td>{fin}</td><td>{avg_display}</td></tr>"
        response += "</table>"
        return response

    # Intent: AGNO / GPA Calculation (NEW)
    if any(x in message for x in ["agno", "gano", "genel ortalama", "gpa", "transkript puanı", "ortalamam kaç", "puanım ne"]):
        gpa, total_credits, total_points, details = get_student_agno(student_id)
        
        response = "<strong>AGNO Hesaplaması (Tahmini):</strong><br>"
        response += "<i>(Final notlarına göre 4.0'lık sistem)</i><br><ul>"
        response += details
        response += "</ul>"
        
        if total_credits > 0:
            response += f"<br>Toplam Kredi: {total_credits}<br>"
            response += f"Toplam Ağırlıklı Puan: {total_points}<br>"
            response += f"<strong style='font-size:1.2rem; color:#2d3748'>AGNO: {gpa:.2f}</strong>"
        else:
            response += "<br>Hesaplanabilir kredili ders notu bulunamadı."
            
        return response

    # Intent: Average (Ortalama - Legacy Term Average)
    if "ortalama" in message or "dönem notu" in message:
        total_score = 0
        count = 0
        response = "<strong>Dönem Ortalaması (100'lük Sistem):</strong><br><ul>"
        
        for c in courses:
            if c.get('is_exempt'): continue
                
            mid = c['midterm']
            fin = c['final']
            
            if mid is not None and fin is not None:
                # 40% Midterm, 60% Final
                avg = (mid * 0.4) + (fin * 0.6)
                total_score += avg
                count += 1
                response += f"<li>{c['code']}: {avg:.1f}</li>"
            elif mid is not None:
                 response += f"<li>{c['code']}: {mid} (Sadece Vize)</li>"
        
        response += "</ul>"
        
        if count > 0:
            gpa = total_score / count
            response += f"<br><strong>Dönem Ortalaması: {gpa:.2f}</strong>"
        else:
            response += "<br>Hesaplanabilir not bulunamadı."
            
        return response

    # Intent: Instructors (Hocalar/Ofisler) - KEEP AS IS
    instructor_keywords = ["hoca", "öğretmen", "prof", "doktor", "akademisyen", "ofis", "oda", "nerede"]
    if any(x in message for x in instructor_keywords) and not "ortala" in message and not "ders seç" in message:
        response = "<strong>Dersleriniz ve Öğretim Üyeleri:</strong><br><ul>"
        
        # Add Advisor first
        if advisor:
             response += f"<li><b>Danışman:</b> {advisor['name']} (Ofis: {advisor['office']})</li><br>"
        
        for c in courses:
            if c['instructor_name']:
                response += f"<li><b>{c['name']} ({c['code']}):</b><br>{c['instructor_name']}<br>Ofis: {c['instructor_office']}<br>Email: {c['instructor_email']}</li>"
        
        response += "</ul>"
        return response
    
    # Intent: Course Selection (Ders Seçimi) - KEEP AS IS
    if any(x in message for x in ["ders seç", "ders sec", "kayıt", "seçim", "secim"]):
        student_data = dict(student_basic)
        grade = student_data.get('grade_level', 0)
        dept = student_data.get('department', 'Bölüm Bilinmiyor')
        
        response = f"<strong>Ders Seçimi ve Kayıt Yenileme Bilgileri:</strong><br>"
        response += f"Sayın {student_basic['name']}, {grade}. Sınıf {dept} öğrencisisiniz.<br><br>"
        
        response += "<ul>"
        response += "<li><b>Tarihler:</b> 2024-2025 Bahar Yarıyılı ders kayıtları <b>10-14 Şubat 2025</b> tarihleri arasındadır.</li>"
        
        if grade == 1:
             response += "<li><b>Kural:</b> 1. sınıf olduğunuz için dersleriniz sistem tarafından otomatik atanacaktır. Onaylamanız yeterlidir.</li>"
        elif grade == 4:
             response += "<li><b>Kural:</b> 4. sınıf (Son Sınıf) olduğunuz için bitirme projesi ve eksik kalan AKTS kredilerinizi kontrol ediniz.</li>"
        else:
             response += "<li><b>Kural:</b> Seçmeli derslerinizi (en az 2 adet) kontenjan dolmadan seçmeniz önerilir. Alttan dersiniz varsa öncelikle onları seçmelisiniz.</li>"
             
        response += "<li><b>Danışman Onayı:</b> Ders seçimi yaptıktan sonra Danışmanınız <b>Dr. Ahmet Yılmaz</b>'ın onayı gerekmektedir.</li>"
        response += "</ul>"
        
        return response

    # Default Fallback
    topics = [
        "AGNO ve Ortalamalar",
        "Sınavlar ve Notlar",
        "Ders Programı",
        "Projeler ve Ödevler",
        "Devamsızlık Durumu",
        "Hocalar ve Ofisler",
        "Ders Seçimi ve Kayıt",
        "Alttan Dersler"
    ]
    return f"Üzgünüm, '{message}' ile ilgili net bir cevap bulamadım.<br>Şu konularda yardımcı olabilirim:<br><ul>" + "".join([f"<li>{t}</li>" for t in topics]) + "</ul>"
