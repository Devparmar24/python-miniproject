def send_report_card(student_data):
    try:
        print("\n" + "="*50)
        print(f"📧 SIMULATED EMAIL SENT TO: {student_data['email']}")
        print("="*50)
        
        body = f"""
        Subject: Your Semester Report Card
        
        Hello {student_data['first_name']} {student_data['last_name']},
        
        Here is your performance report:
        SAP ID: {student_data['sapid']}
        
        Subjects (3 Credits Each):
        - Python: {student_data['python']}
        - EDC: {student_data['edc']}
        - DSD: {student_data['dsd']}
        - Maths 3: {student_data['maths_3']}
        
        Regards,
        Renia Dias
        """
        print(body)
        print("="*50 + "\n")
        
        # We return True so the UI updates the status to "Completed"
        return True, "Email successfully simulated in terminal!"
        
    except Exception as e:
        return False, f"Failed to simulate email: {str(e)}"