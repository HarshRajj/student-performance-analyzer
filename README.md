# Serverless Student Performance Analyzer 🚀

A full-stack, serverless web application that provides instant, detailed analysis and visualization of student performance data from a CSV file. Built entirely on AWS.

---

## 🌐 Live Demo

You can try the application live here:

[http://harsh-marks-analyzer.s3-website.eu-north-1.amazonaws.com/](#)


## ✨ Key Features

- **Interactive UI:** A premium, modern frontend with a "glassmorphism" dark theme for a seamless user experience.
- **Instant Analysis:** Upload a CSV and get immediate results, including top performers, pass/fail statistics, and subject-level breakdowns.
- **Dynamic Charting:** Automatically generates a bar chart of top performers using Chart.js for clear data visualization.
- **Serverless Backend:** Powered by AWS Lambda and API Gateway for infinite scalability and cost-efficiency, requiring zero server management.

---

## 🛠️ Tech Stack

| Category   | Technology                                 |
|------------|--------------------------------------------|
| Cloud      | AWS (S3, Lambda, API Gateway, IAM)         |
| Backend    | Python, Pandas                             |
| Frontend   | HTML5, CSS3, JavaScript, Chart.js          |

---

## 🏗️ Architecture Overview

This project follows a modern, event-driven serverless pattern:

- **Frontend Hosting:** The static website (`index.html`) is hosted on Amazon S3.
- **API Layer:** Amazon API Gateway provides a public HTTP endpoint.
- **Compute Layer:** An AWS Lambda function contains the Python logic to process the data.
- **Workflow:** The user uploads a file on the S3 website, which calls the API Gateway endpoint. This triggers the Lambda function, which performs the analysis and returns the results directly to the user's browser.

---

## 🚀 Quick Start & Deployment Guide

To get this project running in your own AWS account, follow these steps:

### Backend Deployment
1. **Create Lambda Function:** In AWS Lambda, create a new function with a Python runtime.
2. **Add Layer:** Add the pre-built AWSDataWrangler Lambda Layer to include the Pandas library.
3. **Deploy Code:** Copy the Python code from the `backend/` directory into the Lambda function editor.
4. **Create API Trigger:** Add a new API Gateway trigger, ensuring you select "HTTP API" as the type.
5. **Configure CORS:** In the API Gateway console, configure CORS to allow requests from your frontend's domain.
6. **Note the URL:** Copy the generated API endpoint URL.

### Frontend Deployment
1. **Create S3 Bucket:** Create a new S3 bucket. In the properties, enable static website hosting.
2. **Allow Public Access:** In the bucket's permissions, disable "Block all public access".
3. **Set Bucket Policy:** Add the following bucket policy to allow public read access to your files:

   ```json
   {
	   "Version": "2012-10-17",
	   "Statement": [
		   {
			   "Sid": "PublicReadGetObject",
			   "Effect": "Allow",
			   "Principal": "*",
			   "Action": "s3:GetObject",
			   "Resource": "arn:aws:s3:::your-bucket-name/*"
		   }
	   ]
   }
   ```
   > Replace `your-bucket-name` with the actual name of your S3 bucket.

4. **Update Endpoint:** Paste your copied API endpoint URL into the `API_ENDPOINT` constant in the `frontend/index.html` file.
5. **Upload:** Upload the updated `index.html` file to your S3 bucket.
6. **Launch:** Access your application using the S3 bucket's static website hosting URL.

---

## 👨‍💻 About the Creator

This project was built by **Harsh**, a passionate AI developer focused on creating impactful and efficient solutions.