# -Movie-Recommender-and-Cinema-Booking-System-with-email-conformation-message
It is a web based app  all tools and skills ate mentioned ::: • Programming Languages: Python, C# • Frameworks &amp; Tools: Streamlit,, PyCharm • Data Science Tools: Pandas, NumPy, Pickle • Other Skills: API integration, email automation (SMTP), UI/UX with Streamlit

Step 1 open PyCharm.

Step 2: Create a New Project

Click “New Project”.
Select a location for your project.
Python interpreter: Make sure you select a valid Python 3.x interpreter (preferably Python 3.10+).
Click Create.

Step 3: Add Your Code
In your PyCharm project, right-click the project folder → New → Python File.

Name it , app.py.
Copy your entire Streamlit code from main.py into app.py.

Step 4: Add Required Files
You are using pickle files and APIs:
Add movie_dict.pkl and similarity.pkl to the same folder as app.py.
Make sure your TMDB API key is valid (currently d8333ad6badf22a6c737c8b52079bfca).

Step 5: Install Required Python Packages
You need to install packages used in your code.
Open Terminal in PyCharm (bottom panel).
Run:
    pip install streamlit pandas requests
Optional: If you want email sending to work, smtplib and email are standard libraries in Python, so no need to install.

Step 6: Run Streamlit App
Open Terminal in PyCharm.
Navigate to your project folder (if not already there).
Run the Streamlit command:
      streamlit run app.py
This will open a browser window with your Streamlit app.
If not, check the terminal for a URL like: http://localhost:8501 and open it manually.

