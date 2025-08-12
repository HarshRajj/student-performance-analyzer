import pandas as pd

try:
    # --- 1. Read and Process Data ---
    df = pd.read_csv('marks.csv')
    print("--- Successfully read local marks.csv ---")

    non_subject_cols = ['StudentID', 'Name']
    subject_cols = [col for col in df.columns if col not in non_subject_cols]

    # Calculate the maximum possible marks (assuming each subject is out of 100)
    max_possible_marks = len(subject_cols) * 100

    # Calculate total marks and percentage for each student
    df['TotalMarks'] = df[subject_cols].sum(axis=1)
    df['Percentage'] = (df['TotalMarks'] / max_possible_marks) * 100

    # Get the top 3 students
    top_3_students = df.nlargest(3, 'TotalMarks')


    # --- 2. Generate and Print the Text Summary ---
    print("\n" + "="*50)
    print("        Student Performance Summary (Local Test)")
    print("="*50)
    print("\nTop 3 Students (Overall):")

    # Select and format the columns for a clean report
    # .round(2) will round the percentage to 2 decimal places
    report_df = top_3_students[['Name', 'TotalMarks', 'Percentage']].round(2)

    print(report_df.to_string(index=False))
    print("\n" + "="*50)


except FileNotFoundError:
    print("ERROR: 'marks.csv' not found. Make sure it's in the same folder.")
except Exception as e:
    print(f"An error occurred: {e}")



import boto3
import pandas as pd
import io
import os

# Initialize the S3 client to interact with AWS S3
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    This function is triggered by an S3 file upload. It reads a CSV of 
    student marks, calculates detailed statistics including subject-level
    analysis and pass/fail counts, and saves a summary report to another S3 bucket.
    """
    try:
        # --- 1. Get the uploaded file's info from the S3 event ---
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']

        # --- 2. Read the CSV file from the source S3 bucket ---
        response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        csv_content = response['Body'].read()
        df = pd.read_csv(io.BytesIO(csv_content))

        # --- 3. Process the data using pandas ---
        non_subject_cols = ['StudentID', 'Name']
        subject_cols = [col for col in df.columns if col not in non_subject_cols]

        # Calculate max marks and totals
        max_possible_marks = len(subject_cols) * 100
        df['TotalMarks'] = df[subject_cols].sum(axis=1)
        df['Percentage'] = (df['TotalMarks'] / max_possible_marks) * 100
        
        # Get the top 3 students overall
        top_3_students = df.nlargest(3, 'TotalMarks')

        # NEW: Define the passing percentage
        passing_percentage = 40

        # NEW: Determine Pass/Fail status for each student
        df['Status'] = df['Percentage'].apply(lambda p: 'Pass' if p >= passing_percentage else 'Fail')
        
        # NEW: Count the number of students who passed and failed
        pass_fail_counts = df['Status'].value_counts()
        total_passed = pass_fail_counts.get('Pass', 0)
        total_failed = pass_fail_counts.get('Fail', 0)

        # --- 4. Generate the detailed summary report text ---
        report_lines = []
        report_lines.append("="*60)
        report_lines.append("        Enhanced Student Performance Summary Report")
        report_lines.append("="*60)
        report_lines.append(f"\nAnalysis of file: {file_key}\n")

        # Add Overall Top Performers
        report_lines.append("-" * 60)
        report_lines.append("Top 3 Students (Overall)")
        report_lines.append("-" * 60)
        report_df = top_3_students[['Name', 'TotalMarks', 'Percentage']].round(2)
        report_lines.append(report_df.to_string(index=False))
        report_lines.append("\n")

        # NEW: Add Class Pass/Fail Summary
        report_lines.append("-" * 60)
        report_lines.append("Class Pass/Fail Summary")
        report_lines.append("-" * 60)
        report_lines.append(f"Passing Percentage Threshold: {passing_percentage}%")
        report_lines.append(f"Total Students Passed: {total_passed}")
        report_lines.append(f"Total Students Failed: {total_failed}")
        report_lines.append("\n")

        # NEW: Add Subject-Level Analysis
        report_lines.append("-" * 60)
        report_lines.append("Subject-Level Analysis")
        report_lines.append("-" * 60)
        for subject in subject_cols:
            avg_score = df[subject].mean()
            top_student_in_subject = df.loc[df[subject].idxmax()]
            top_student_name = top_student_in_subject['Name']
            top_student_score = top_student_in_subject[subject]
            report_lines.append(f"-> {subject}:")
            report_lines.append(f"   - Average Score: {avg_score:.2f}")
            report_lines.append(f"   - Top Scorer: {top_student_name} ({top_student_score} marks)")
        report_lines.append("\n")

        final_report = "\n".join(report_lines)

        # --- 5. Save the report to the destination S3 bucket ---
        dest_bucket = os.environ.get('DESTINATION_BUCKET')
        if not dest_bucket:
            raise ValueError("DESTINATION_BUCKET environment variable not set.")
            
        report_key = f"summary-{os.path.basename(file_key).replace('.csv', '.txt')}"

        s3_client.put_object(
            Bucket=dest_bucket,
            Key=report_key,
            Body=final_report
        )

        return {'statusCode': 200, 'body': 'Enhanced report generated successfully!'}

    except Exception as e:
        print(f"Error processing file: {e}")
        raise e
