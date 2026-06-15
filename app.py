import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide"
)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Ensure the persistent CSV storage exists with proper headers
if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["Username", "Password"]).to_csv("users.csv", index=False)

# Seed default admin account into CSV if the file is completely empty
try:
    users_df = pd.read_csv("users.csv")
    if users_df.empty:
        pd.DataFrame({"Username": ["admin"], "Password": ["1234"]}).to_csv("users.csv", index=False)
except Exception:
    pd.DataFrame({"Username": ["admin"], "Password": ["1234"]}).to_csv("users.csv", index=False)

# Initialize trip history
if "trip_history" not in st.session_state:
    st.session_state.trip_history = []
    
ALL_DESTINATIONS = sorted([
    "Goa","Jaipur","Udaipur","Ujjain","Lonavala",
    "Manali","Shimla","Delhi","Mumbai","Pune",
    "Varanasi","Rishikesh","Amritsar","Agra","Munnar",
    "Ooty","Darjeeling","Mysore","Hyderabad","Bengaluru",
    "Srinagar","Leh","Andaman","Mahabaleshwar","Kodaikanal",
    "Dubai","Singapore","Bali","Paris","Maldives",
    "Bangkok","London","Tokyo","New York","Zurich"
])

# ==================== AUTHENTICATION ====================
if not st.session_state.logged_in:
    st.title("🔐 TravelMate AI")

    auth_option = st.radio(
        "Choose an option",
        ["Login", "Sign Up"]
    )

    # Read latest users database from the persistent CSV file
    users_df = pd.read_csv("users.csv")

    # LOGIN
    if auth_option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # Check credentials against matching rows in the CSV file
            matched_user = users_df[(users_df["Username"] == username) & (users_df["Password"] == str(password))]
            
            if not matched_user.empty:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    # SIGN UP
    else:
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")

        if st.button("Sign Up"):
            if new_username.strip() == "" or new_password.strip() == "":
                st.error("Username and Password fields cannot be empty.")
            elif new_username in users_df["Username"].astype(str).values:
                st.error("Username already exists.")
            else:
                # Append new user details structurally to the CSV file
                new_user_row = pd.DataFrame({"Username": [new_username], "Password": [str(new_password)]})
                updated_users_df = pd.concat([users_df, new_user_row], ignore_index=True)
                updated_users_df.to_csv("users.csv", index=False)
                
                st.success("Account created successfully!")
                st.info("Now login using your new account.")

    st.stop()

# ==================== MAIN APPLICATION ====================
st.title("✈️ TravelMate AI")
st.subheader("Smart Trip Planner with Local Experiences and Group Expense Management")

st.sidebar.success(f"👋 Welcome, {st.session_state.username}")

menu = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Trip Planner",
        "Local Experiences",
        "Budget Predictor",
        "Expense Manager",
        "Analytics",
        "Destination Insights",
        "Trip History",
        "Logout"
    ]
)

# ==================== HOME ====================
if menu == "Home":
    st.header(f"Welcome {st.session_state.username} 👋")
    st.write("""
TravelMate AI helps users:
- 🗺️ Plan trips
- 🍽️ Discover local experiences
- 💰 Predict travel budgets
- 🏨 Find hotel recommendations
- 👥 Manage group expenses
- 📊 Analyze travel spending
    """)

# ==================== TRIP PLANNER ====================
elif menu == "Trip Planner":
    st.header("🗺️ Smart Trip Planner")

    destination = st.selectbox(
        "Select Destination",
        ["Select Destination"] + ALL_DESTINATIONS,
        key="planner_dest"
    )

    if destination == "Select Destination":
        st.info("Please select a destination.")
        st.stop()

    days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=3,
        value=2
    )

    budget = st.number_input(
        "Budget (₹)",
        min_value=1000,
        step=1000,
        value=10000
    )

    if st.button("Generate Itinerary"):
        df = pd.read_csv("destinations.csv")
        trip = df[
            (df["Destination"] == destination) &
            (df["Days"] <= days)
        ]

        st.subheader("Your Itinerary")

        if not trip.empty:
            for _, row in trip.iterrows():
                st.write(f"📍 Day {row['Days']}: {row['Place']}")
            st.success(f"Estimated Budget: ₹{budget}")
        else:
            st.warning("No itinerary found.")

# ==================== LOCAL EXPERIENCES ====================
elif menu == "Local Experiences":
    st.header("🍴 Local Experience Recommender")

    destination = st.selectbox(
        "Choose Destination",
        ["Select Destination"] + ALL_DESTINATIONS,
        key="experience_dest"
    )

    if destination == "Select Destination":
        st.info("Please select a destination.")
        st.stop()

    budget_type = st.selectbox(
        "Food Budget",
        ["Low", "Medium", "Luxury"],
        key="food_budget"
    )

    # Existing experiences
    exp_df = pd.read_csv("experiences.csv")
    result = exp_df[exp_df["Destination"] == destination]

    st.subheader("🎭 Experiences")

    if not result.empty:
        for _, row in result.iterrows():
            st.write("🎭 Cultural Experience:", row["Cultural Experience"])
            st.write("🏕️ Activity:", row["Activity"])
            st.write("💎 Hidden Gem:", row["Hidden Gem"])
            st.markdown("---")

    # Food Recommendations
    st.subheader("🍽️ Recommended Food Spots")
    food_df = pd.read_csv("food.csv")
    food_result = food_df[
        (food_df["Destination"] == destination) &
        (food_df["Budget Type"] == budget_type)
    ]

    if not food_result.empty:
        for _, row in food_result.iterrows():
            st.markdown(f"### 🍽️ {row['Restaurant']}")
            st.write(f"🍲 Famous Dish: {row['Famous Dish']}")
            st.link_button("📍 Open in Google Maps", row["Google Maps"])
            st.markdown("---")
    else:
        st.warning("No food recommendations found.")

# ==================== BUDGET PREDICTOR ====================
elif menu == "Budget Predictor":
    st.header("💰 Trip Budget Predictor")

    destination = st.selectbox(
        "Select Destination",
        ["Select Destination"] + ALL_DESTINATIONS,
        key="budget_dest"
    )

    if destination == "Select Destination":
        st.info("Please select a destination.")
        st.stop()

    budget_type = st.selectbox(
        "Budget Preference",
        ["Low", "Medium", "Luxury"]
    )

    travelers = st.number_input(
        "Number of Travelers",
        min_value=1,
        value=2
    )

    days = st.number_input(
        "Trip Duration (Days)",
        min_value=1,
        value=2
    )

    user_budget = st.number_input(
        "Your Maximum Budget (₹)",
        min_value=1000,
        step=1000,
        value=10000
    )

    budget_df = pd.read_csv("budget.csv")
    selected_trip = budget_df[budget_df["Destination"] == destination]

    if not selected_trip.empty:
        trip_data = selected_trip.iloc[0]

        if budget_type == "Low":
            hotel_per_night = trip_data["Low Hotel"]
        elif budget_type == "Medium":
            hotel_per_night = trip_data["Medium Hotel"]
        else:
            hotel_per_night = trip_data["Luxury Hotel"]

        hotel_cost = hotel_per_night * days
        food_cost = trip_data["Food Per Person"] * travelers * days
        transport_cost = trip_data["Transport"]

        # Save for Expense Manager
        st.session_state["hotel_cost"] = int(hotel_cost)
        st.session_state["food_cost"] = int(food_cost)
        st.session_state["transport_cost"] = int(transport_cost)

        total = hotel_cost + food_cost + transport_cost

        st.subheader("💰 Estimated Expenses")
        st.write(f"🏨 Hotel Cost: ₹{hotel_cost}")
        st.write(f"🍽️ Food Cost: ₹{food_cost}")
        st.write(f"🚌 Transport Cost: ₹{transport_cost}")

        st.success(f"💵 Total Estimated Budget: ₹{total}")

        # Save Trip Option
        trip_record = {
            "Destination": destination,
            "Budget Type": budget_type,
            "Travelers": travelers,
            "Days": days,
            "Total Budget": total
        }

        if st.button("💾 Save This Trip"):
            st.session_state.trip_history.append(trip_record)
            st.success("Trip saved successfully!")

        # Budget Check Logic Block
        if total > user_budget:
            st.warning(f"Your trip exceeds the budget by ₹{total - user_budget}")
            st.info("""
Suggestions:
• Choose Low Budget stays
• Reduce trip duration
• Skip premium activities
            """)
        else:
            st.success(f"You are within budget! You can save ₹{user_budget - total}")

        # Hotel Recommendations Section
        st.subheader("🏨 Recommended Hotels")
        hotels = pd.read_csv("hotels.csv")
        recommended = hotels[
            (hotels["Destination"] == destination) &
            (hotels["Budget Type"] == budget_type)
        ]

        if not recommended.empty:
            for _, hotel in recommended.iterrows():
                st.write(f"**{hotel['Hotel Name']}**")
                st.link_button("🔗 View Hotel", hotel["Booking Link"])
                st.markdown("---")
        else:
            st.warning("No hotel recommendations found.")
    else:
        st.warning("Budget data not available for this destination.")
    
# ==================== EXPENSE MANAGER ====================
elif menu == "Expense Manager":
    st.header("👥 Group Expense Manager")
    st.write("Split trip expenses among your group members.")

    num_members = st.number_input(
        "Number of Group Members",
        min_value=2,
        value=2,
        step=1
    )

    members = []
    st.subheader("Enter Member Names")

    for i in range(num_members):
        member = st.text_input(
            f"Member {i+1} Name",
            key=f"member_{i}"
        )
        members.append(member)

    st.subheader("Add Expenses")

    hotel_expense = st.number_input(
        "🏨 Hotel Expense (₹)",
        min_value=0,
        value=st.session_state.get("hotel_cost", 0),
        step=100
    )

    food_expense = st.number_input(
        "🍽️ Food Expense (₹)",
        min_value=0,
        value=st.session_state.get("food_cost", 0),
        step=100
    )

    transport_expense = st.number_input(
        "🚌 Transport Expense (₹)",
        min_value=0,
        value=st.session_state.get("transport_cost", 0),
        step=100
    )

    activity_expense = st.number_input(
        "🎟️ Activity Expense (₹)",
        min_value=0,
        value=0,
        step=100
    )

    if st.button("Split Expenses"):
        valid_members = [member.strip() for member in members if member.strip() != ""]

        if len(valid_members) < 2:
            st.error("Please enter at least 2 member names.")
        else:
            total_expense = hotel_expense + food_expense + transport_expense + activity_expense
            split_amount = total_expense / len(valid_members)

            st.subheader("💰 Expense Summary")
            st.write(f"Total Expense: ₹{total_expense}")
            st.write(f"Each Person Pays: ₹{split_amount:.2f}")

            st.subheader("🧾 Settlement")
            for member in valid_members:
                st.success(f"{member} should pay ₹{split_amount:.2f}")

# ==================== ANALYTICS ====================
elif menu == "Analytics":
    st.header("📊 Travel Analytics Dashboard")

    hotel = st.session_state.get("hotel_cost", 0)
    food = st.session_state.get("food_cost", 0)
    transport = st.session_state.get("transport_cost", 0)

    activity = st.number_input(
        "🎟️ Activity Expense (₹)",
        min_value=0,
        value=0,
        step=100
    )

    members = st.number_input(
        "👥 Number of Travelers",
        min_value=1,
        value=2,
        step=1
    )

    total = hotel + food + transport + activity

    st.subheader("💰 Expense Summary")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏨 Hotel", f"₹{hotel}")
    col2.metric("🍽️ Food", f"₹{food}")
    col3.metric("🚌 Transport", f"₹{transport}")
    col4.metric("🎟️ Activity", f"₹{activity}")

    st.success(f"💵 Total Estimated Expense: ₹{total}")

    per_person = total / members
    st.info(f"👤 Cost Per Person: ₹{per_person:.2f}")

    expense_df = pd.DataFrame({
        "Category": ["Hotel", "Food", "Transport", "Activity"],
        "Expense": [hotel, food, transport, activity]
    })

    st.subheader("📋 Expense Breakdown")
    st.dataframe(expense_df, use_container_width=True)

    # Pie Chart
    st.subheader("🥧 Expense Distribution")
    if expense_df["Expense"].sum() > 0:
        fig, ax = plt.subplots()
        ax.pie(
            expense_df["Expense"],
            labels=expense_df["Category"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("No expense data available to display the pie chart.")

    # Bar Chart
    st.subheader("📈 Expense Comparison")
    st.bar_chart(expense_df.set_index("Category"))

    # Budget Health
    st.subheader("💡 Budget Health")
    if total <= 10000:
        st.success("✅ Budget Friendly Trip")
    elif total <= 30000:
        st.warning("⚠️ Moderate Spending")
    else:
        st.error("💸 High Expense Trip")

    csv = expense_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Expense Report",
        data=csv,
        file_name="travel_expense_report.csv",
        mime="text/csv"
    )

# ==================== DESTINATION INSIGHTS ====================
elif menu == "Destination Insights":
    st.header("ℹ️ Destination Insights")
    insights = pd.read_csv("insights.csv")

    destination = st.selectbox(
        "Choose Destination",
        ["Select Destination"] + ALL_DESTINATIONS,
        key="insights_dest"
    )

    if destination == "Select Destination":
        st.info("Please select a destination.")
        st.stop()

    data = insights[insights["Destination"] == destination]

    if not data.empty:
        data = data.iloc[0]
        st.subheader(f"🌍 {destination}")
        st.write("🌤️ Best Season:", data["Best Season"])
        st.write("⏳ Ideal Duration:", data["Ideal Duration"])
        st.write("💵 Average Budget: ₹", data["Average Budget"])
        st.write("⭐ Top Attraction:", data["Top Attraction"])
    else:
        st.warning("No insights available.")

# ==================== TRIP HISTORY ====================
elif menu == "Trip History":
    st.header("📝 Trip History")

    if st.session_state.trip_history:
        history_df = pd.DataFrame(st.session_state.trip_history)
        st.dataframe(history_df, use_container_width=True)

        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Trip History",
            data=csv,
            file_name="trip_history.csv",
            mime="text/csv"
        )
    else:
        st.info("No trips saved yet.")

# ==================== LOGOUT ====================
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.rerun()
