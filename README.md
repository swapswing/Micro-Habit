🌱 Micro Habits - Python Version

A beginner-friendly Micro Habits Tracker built with Python and Streamlit.

The app helps users build small daily habits, track completion, maintain streaks, create custom habits, and save progress locally.

✨ Features

Preset micro-habits

Create custom habits

Simple micro-habit suggestions

Mark habits as completed

Daily progress tracking

Streak tracking

Edit and delete habits

Local data saving using habits_data.json

Automatic daily completion reset

Simple Streamlit interface

🛠 Technologies Used

Python

Streamlit

JSON

HTML/CSS inside Streamlit

datetime

pathlib

📁 Project Structure

Micro-Habit/
│
├── app.py
├── requirements.txt
├── README.md
└── habits_data.json   # created automatically after running the app

You may also see:

.venv/

The .venv folder is your local Python virtual environment and should not be uploaded to GitHub.

🚀 How to Run the Project From Scratch

1. Install Python

Download Python from:

https://www.python.org/downloads/

During installation, make sure you enable:

Add Python to PATH

Check the installation:

python --version

You should see a Python version number.

2. Install VS Code

Download Visual Studio Code from:

https://code.visualstudio.com/

It is recommended to install the Python extension by Microsoft from the VS Code Extensions panel.

3. Download or Clone This Repository

Option A: Download ZIP

On GitHub:

Code → Download ZIP

Extract the ZIP file and open the project folder in VS Code.

Option B: Clone With Git

git clone https://github.com/swapswing/Micro-Habit.git

Then enter the project folder:

cd Micro-Habit

Open it in VS Code:

code .

4. Create a Virtual Environment

Open a VS Code terminal:

Terminal → New Terminal

Then run:

python -m venv .venv

5. Activate the Virtual Environment

Windows Command Prompt

.venv\Scripts\activate

Windows PowerShell

.venv\Scripts\Activate.ps1

After activation, the terminal should look similar to:

(.venv) C:\Users\YourName\...\Micro-Habit>

6. Install Dependencies

Run:

pip install -r requirements.txt

If Streamlit is not installed for any reason, run:

pip install streamlit

7. Run the App

Run:

streamlit run app.py

Streamlit will start a local server.

You should see something similar to:

Local URL: http://localhost:8501

Open this address in your browser:

http://localhost:8501

🛑 How to Stop the App

Return to the terminal and press:

Ctrl + C

💾 How Data Is Stored

The app saves habit information locally in:

habits_data.json

This file can contain:

Habit name

Micro action

Completion status

Streak

Last completion date

The file is created automatically after the app saves data.

🔄 Reset the App

To reset the application:

Stop Streamlit with Ctrl + C

Delete habits_data.json

Start the app again:

streamlit run app.py

The default habits will be recreated.

❗ Common Errors

python is not recognized

Python is either not installed or not added to PATH.

Reinstall Python and enable:

Add Python to PATH

Then restart VS Code or Command Prompt.

pip is not recognized

Try:

python -m pip --version

Then install dependencies using:

python -m pip install -r requirements.txt

streamlit is not recognized

Make sure your virtual environment is activated, then run:

pip install streamlit

You can also run the app with:

python -m streamlit run app.py

PowerShell Blocks Virtual Environment Activation

Use a Command Prompt terminal in VS Code and run:

.venv\Scripts\activate

📦 requirements.txt

A basic requirements.txt file for this project can contain:

streamlit>=1.40,<2.0

Install it with:

pip install -r requirements.txt

🙈 Recommended .gitignore

Create a .gitignore file with:

.venv/
venv/
__pycache__/
*.pyc
habits_data.json
.vscode/
.DS_Store
Thumbs.db

This keeps local and unnecessary files out of GitHub.

📤 How to Upload Changes to GitHub

After editing the project:

git add .

Commit your changes:

git commit -m "Update Micro Habits project"

Push them:

git push

📌 Quick Start

For a beginner, the full setup is:

git clone https://github.com/swapswing/Micro-Habit.git
cd Micro-Habit
python -m venv .venv

Activate the environment on Windows CMD:

.venv\Scripts\activate

Then:

pip install -r requirements.txt
streamlit run app.py

Open:

http://localhost:8501

🔮 Future Improvements

Possible future upgrades include:

AI-generated micro-habit recommendations

User login and authentication

Firebase or Supabase database

Weekly and monthly analytics

Habit completion charts

Reminder notifications

Personalized recommendations

LLM integration

Cloud deployment

👨‍💻 Project

Micro Habits - Python Version

Built using Python and Streamlit for habit tracking and daily behavioral improvement.