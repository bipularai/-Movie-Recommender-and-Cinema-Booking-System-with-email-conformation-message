import streamlit as st
import pickle
import pandas as pd
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return pd.DataFrame(movies_dict), similarity

movies, similarity = load_data()

# -----------------------------
# Gmail Sending Function
# -----------------------------
def send_confirmation_email(to_email, movie_title, seats):
    sender_email = "sanchitapoudel606@gmail.com"
    sender_password = "wbsztondyepyevpk"  # Gmail App Password

    subject = f"🎟️ Booking Confirmation for {movie_title}"
    body = f"""
    Hi there,

    Your booking for *{movie_title}* has been confirmed!

    🎬 Movie: {movie_title}
    🪑 Seats: {', '.join(seats)}

    Enjoy your movie! 🍿

    Regards,
    Movie Recommender Team
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False

# -----------------------------
# TMDB Poster Function
# -----------------------------
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d8333ad6badf22a6c737c8b52079bfca'
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    return "https://via.placeholder.com/500x750?text=No+Image"

# -----------------------------
# Recommend Function
# -----------------------------
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies, recommended_posters = [], []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_posters
    except IndexError:
        return [], []

# -----------------------------
# Latest Movies Function
# -----------------------------
def fetch_latest_movies():
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=d8333ad6badf22a6c737c8b52079bfca&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    latest_movies = data.get("results", [])[:8]
    return [
        {
            "title": m["title"],
            "poster": "https://image.tmdb.org/t/p/w500" + m["poster_path"] if m.get("poster_path") else None,
            "id": m["id"]
        }
        for m in latest_movies
    ]

# -----------------------------
# Cinema Booking
# -----------------------------
def cinema_booking(movie_title):
    st.header(f"🎟️ Book Tickets for {movie_title}")
    rows = ['A', 'B', 'C', 'D', 'E']
    cols = range(1, 9)

    if "booked_seats" not in st.session_state:
        st.session_state.booked_seats = []
    if "selected_seats" not in st.session_state:
        st.session_state.selected_seats = []

    st.write("🪑 Select your seats:")
    for row in rows:
        seat_cols = st.columns(len(cols))
        for i, c in enumerate(cols):
            seat_id = f"{row}{c}"
            disabled = seat_id in st.session_state.booked_seats

            if seat_cols[i].button(seat_id, key=f"{seat_id}_btn", disabled=disabled, use_container_width=True):
                if seat_id in st.session_state.selected_seats:
                    st.session_state.selected_seats.remove(seat_id)
                else:
                    st.session_state.selected_seats.append(seat_id)
                st.rerun()

    if st.session_state.selected_seats:
        st.success(f"Selected seats: {', '.join(st.session_state.selected_seats)}")
        if st.button("✅ Confirm Booking"):
            st.session_state.booked_seats.extend(st.session_state.selected_seats)
            success = send_confirmation_email(st.session_state["email"], movie_title, st.session_state.selected_seats)
            st.session_state.selected_seats = []
            if success:
                st.success("🎉 Booking Confirmed! A confirmation email has been sent.")
                st.balloons()
            else:
                st.error("❌ Booking confirmed, but email could not be sent. Check connection or credentials.")

    if st.button("⬅️ Back to Cinema List"):
        st.session_state.page = "cinema"
        st.rerun()

# -----------------------------
# 🆕 Netflix-style Subscription Page
# -----------------------------
def subscription_page():
    st.title("💳 Choose Your Streaming Plan")
    st.write("Enjoy unlimited movies and series anytime, anywhere — choose a plan that fits you best!")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📺 Basic Plan")
        st.markdown("**Rs. 499/month**")
        st.markdown("- 1 Screen at a time\n- 720p HD Streaming\n- Watch on Mobile & Tablet")
        if st.button("Subscribe Basic"):
            st.session_state.subscription = "Basic"
            st.success("✅ Subscribed to Basic Plan!")
            st.balloons()

    with col2:
        st.subheader("🎬 Standard Plan")
        st.markdown("**Rs. 799/month**")
        st.markdown("- 2 Screens at a time\n- 1080p Full HD\n- Watch on any device")
        if st.button("Subscribe Standard"):
            st.session_state.subscription = "Standard"
            st.success("✅ Subscribed to Standard Plan!")
            st.balloons()

    with col3:
        st.subheader("🌟 Premium Plan")
        st.markdown("**Rs. 1199/month**")
        st.markdown("- 4 Screens at a time\n- 4K + HDR Quality\n- Download & Watch Offline")
        if st.button("Subscribe Premium"):
            st.session_state.subscription = "Premium"
            st.success("✅ Subscribed to Premium Plan!")
            st.balloons()

    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# Cinema Page
# -----------------------------
def cinema_page():
    st.title("🎥 Now Showing in Cinemas")
    movies_now = fetch_latest_movies()
    cols = st.columns(4)
    for i, movie in enumerate(movies_now):
        with cols[i % 4]:
            st.image(movie["poster"], use_container_width=True)
            st.markdown(f"**{movie['title']}**")
            if st.button("🎟️ Book Now", key=f"book_{i}"):
                if "email" in st.session_state:
                    st.session_state.page = "booking"
                    st.session_state.booking_movie = movie["title"]
                    st.rerun()
                else:
                    st.warning("Please log in first to book tickets!")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# -----------------------------
# Login Page
# -----------------------------
def login_page():
    st.title("🔐 Login to Continue")

    email = st.text_input("Enter your Gmail")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email.endswith("@gmail.com") and password:
            st.session_state.email = email
            st.success("✅ Logged in successfully!")
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Please enter a valid Gmail and password!")

# -----------------------------
# 🏠 Home Page (with Subscription button)
# -----------------------------
def home_page():
    st.title("🎬 Movie Recommender")

    selected_movie = st.selectbox("Select a movie to get recommendations", movies['title'].values, key="movie_select")

    if st.button("Get Recommendations"):
        names, posters = recommend(selected_movie)
        if names:
            st.subheader("Recommended Movies:")
            cols = st.columns(5)
            for i in range(min(5, len(names))):
                with cols[i]:
                    st.image(posters[i], use_container_width=True)
                    st.markdown(f"**{names[i]}**")
        else:
            st.warning("No recommendations found.")

    st.markdown("---")

    # 🎥 Watch in Cinema + 💳 Get Subscription side by side
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎥 Watch in Cinema"):
            st.session_state.page = "cinema"
            st.rerun()
    with col2:
        if st.button("💳 Get Subscription"):
            st.session_state.page = "subscription"
            st.rerun()

# -----------------------------
# Main Controller
# -----------------------------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "cinema":
        cinema_page()
    elif st.session_state.page == "booking":
        cinema_booking(st.session_state.booking_movie)
    elif st.session_state.page == "subscription":
        subscription_page()

if __name__ == "__main__":
    main()
