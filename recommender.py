import pymysql
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
import uvicorn
import os
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class Skill(BaseModel):
    skill_name: str
    type: str  # "Actual" or "Recommended"


class UserAttributes(BaseModel):
    predicted_field: str
    user_level: str


class Resume(BaseModel):
    name: str
    email: EmailStr
    resume_score: float
    timestamp: datetime
    page_no: int
    predicted_field: str
    user_level: str
    actual_skills: List[str]
    recommended_skills: List[str]


class MySQLDatabase:
    def __init__(self, user, password, database):
        self.user=user
        self.password=password
        self.database=database
    

    def get_dbConnection(self):
        return pymysql.connect(
            host='localhost',
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )


    def init_tables(self):
        connection = self.get_dbConnection()
        cursor = connection.cursor()

        # Creating database and table

        # create database
        try:
            cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {self.database};""")

            # create table
            cursor.execute(f"""USE {self.database};""")

            cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS Users(
                            ID INT NOT NULL AUTO_INCREMENT,
                            Name VARCHAR(500) NOT NULL,
                            Email_ID VARCHAR(500) NOT NULL UNIQUE,
                            Resume_Score DECIMAL(5,2) NOT NULL,
                            Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                            Page_No INT NOT NULL,
                            Recommendations TEXT,
                            PRIMARY KEY (ID)
                        );
            """)

            cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS UserAttributes (
                            ID INT NOT NULL AUTO_INCREMENT,
                            User_ID INT NOT NULL,
                            Predicted_Field VARCHAR(255) NOT NULL,
                            User_Level VARCHAR(255) NOT NULL,
                            PRIMARY KEY (ID),
                            FOREIGN KEY (User_ID) REFERENCES Users(ID) ON DELETE CASCADE
                        );
            """)

            cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS Skills (
                            ID INT NOT NULL AUTO_INCREMENT,
                            User_ID INT NOT NULL,
                            Skill_Name VARCHAR(255) NOT NULL,
                            Type ENUM('Actual', 'Recommended') NOT NULL,
                            PRIMARY KEY (ID),
                            FOREIGN KEY (User_ID) REFERENCES Users(ID) ON DELETE CASCADE
                        );
            """)

            connection.commit()
        
        except Exception as e:
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

        print("Database and Table created")


db = MySQLDatabase(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
)
db.init_tables()


def get_geminiClient():
    return genai.Client(
        api_key=os.getenv("GOOGLE_API_KEY")
    )


@app.get('/')
async def home():
    return {
        "message": "All Okay"
    }


@app.post("/upload_resume/")
async def insert_data(resume: Resume):
    # inserting data
    table_name = 'users'
    connection = db.get_dbConnection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Users (Name, Email_ID, Resume_Score, Timestamp, Page_No) VALUES (%s, %s, %s, %s, %s)",
            (resume.name, resume.email, resume.resume_score, resume.timestamp, resume.page_no)
        )
        user_id = cursor.lastrowid  # Get the inserted User ID

        # insert into UserAttributes table
        cursor.execute(
            "INSERT INTO UserAttributes (User_ID, Predicted_Field, User_Level) VALUES (%s, %s, %s)",
            (user_id, resume.predicted_field, resume.user_level)
        )

        # insert into Skills table
        for skill in resume.actual_skills:
            cursor.execute(
                "INSERT INTO Skills (User_ID, Skill_Name, Type) VALUES (%s, %s, %s)",
                (user_id, skill, "Actual")
            )
        for skill in resume.recommended_skills:
            cursor.execute(
                "INSERT INTO Skills (User_ID, Skill_Name, Type) VALUES (%s, %s, %s)",
                (user_id, skill, "Recommended")
            )

        connection.commit()

        print(f"Data of user {user_id} inserted")

        return {"message": "Resume received and stored successfully", "user_id": user_id}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        connection.close()


@app.get("/recommendations/")
async def recommendations(resume: Resume, user_id):
    connection = db.get_dbConnection()
    cursor = connection.cursor()

    try:
        # Format resume as a plain text prompt
        resume_text = f"""
        Name: {resume.name}
        Email: {resume.email}
        Skills: {', '.join(resume.skills)}
        Experience: {resume.experience}
        Education: {resume.education}
        Certifications: {resume.certifications}
        """

        client = get_geminiClient()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""You are an experienced HR with Technical Experience in the field of any one job role from Data Science, Data Analyst, DevOPS, Machine Learning Engineer, Prompt Engineer, AI Engineer, Full Stack Web Development, Big Data Engineering, Marketing Analyst, Human Resource Manager, Software Developer your task is to review the provided resume.
            Please share your professional evaluation on whether the candidate's profile aligns with the role by highlighting their strengths and weaknesses. Also mention the Skills they already have and suggest some skills to improve their resume and, suggest some courses they might take to improve the skills.
        
            Resume:
            {resume_text}
            """
        )

        cursor.execute(
            "UPDATE Users SET Recommendations = %s WHERE ID = %s",
            (response.text, user_id)
        )

        connection.commit()

        print(f"Recommendations for user {user_id} generated")

        return {"recommendations": response.text}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)