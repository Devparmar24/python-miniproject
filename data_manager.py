import pandas as pd

FILE_NAME = "students_data.csv"

def load_data():
    return pd.read_csv(FILE_NAME)

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

def authenticate_student(sapid, first_name, last_name):
    df = load_data()
    for _, row in df.iterrows():
        # Case insensitive checks
        if (str(row['sapid']).strip() == str(sapid).strip() and
            row['first_name'].strip().lower() == first_name.strip().lower() and
            row['last_name'].strip().lower() == last_name.strip().lower()):
            return row.to_dict()
    return None

def get_all_students():
    return load_data().to_dict('records')

def get_class_stats():
    df = load_data()
    subjects = ['python', 'edc', 'dsd', 'maths_3']
    avg_scores = df[subjects].mean().to_dict()
    max_scores = df[subjects].max().to_dict()
    
    # Calculate totals and GPA (Assuming simple GPA = Average Marks / 10 for demonstration)
    df['avg_marks'] = df[subjects].mean(axis=1)
    df['gpa'] = df['avg_marks'] / 10
    
    avg_total_marks = df['avg_marks'].mean()
    max_total_marks = df['avg_marks'].max()
    
    avg_gpa = df['gpa'].mean()
    max_gpa = df['gpa'].max()
    
    return avg_scores, max_scores, avg_total_marks, max_total_marks, avg_gpa, max_gpa

def update_email_status(sapid):
    df = load_data()
    df.loc[df['sapid'] == int(sapid), 'email_status'] = 'completed'
    save_data(df)