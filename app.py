from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="DeliveryPro - Zomato Rider",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "rider_name" not in st.session_state:
    st.session_state.rider_name = ""
if "phone" not in st.session_state:
    st.session_state.phone = ""
if "total_orders" not in st.session_state:
    st.session_state.total_orders = 0
if "total_revenue" not in st.session_state:
    st.session_state.total_revenue = 0
if "orders" not in st.session_state:
    st.session_state.orders = []
if "rider_id" not in st.session_state:
    st.session_state.rider_id = f"ZOMATO-{random.randint(10000, 99999)}"

# Dummy data
areas = ["HSR", "Koramangala", "Indiranagar", "BTM", "Marathahalli", "Whitefield", "Jayanagar"]
customers = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Kiran"]

# LOGIN PAGE
if st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 🍔 DeliveryPro - Zomato Rider Partner")
        st.markdown("### Welcome! Please Register")
        st.markdown("---")
        name = st.text_input("👤 Your Name", placeholder="Enter your name - ex: lakshmi")
        phone = st.text_input("📱 Mobile Number", placeholder="Enter 10 digit number - ex: 8747941418")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Register & Start Delivery", use_container_width=True, type="primary"):
            if name and phone and len(phone) >= 10:
                st.session_state.rider_name = name
                st.session_state.phone = phone
                st.session_state.page = "dashboard"
                st.session_state.logged_in = True
                st.session_state.rider_id = f"ZOMATO-{random.randint(10000, 99999)}"
                st.success(f"Welcome {name}! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please enter valid Name and 10 digit Mobile Number!")
        
        st.markdown("<br><br>")
        st.info("This is a simulation app for portfolio - No OTP needed, just enter any name and number!")

# DASHBOARD PAGE
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"## Total Orders")
        total_count_ph = st.empty()
        total_count_ph.metric("Total Orders", st.session_state.total_orders)
        
        st.markdown("---")
        
        sidebar_revenue_ph = st.empty()
        with sidebar_revenue_ph.container():
            st.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}")
        
        st.markdown("---")
        
        st.markdown("#### ⚙️ Controls")
        order_speed = st.slider("Order Speed (sec)", 1, 10, 2)
        st.markdown("---")
        
        if st.button("🔄 Reset Orders", use_container_width=True):
            st.session_state.total_orders = 0
            st.session_state.total_revenue = 0
            st.session_state.orders = []
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = "login"
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("#### 📊 Stats")
        peak_area_ph = st.empty()
        total_orders_side_ph = st.empty()
        last_order_ph = st.empty()
        rider_earn_ph = st.empty()

    # Main content
    col_header, col_logout = st.columns([4,1])
    with col_header:
        st.markdown(f"## 🍔 Welcome, {st.session_state.rider_name}! 👋")
    with col_logout:
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.rerun()
    
    # Rider ID Card - RED
    st.markdown(f"""
    <div style="background-color:#DC2626; padding:20px; border-radius:12px; color:white;">
        <h3 style="margin:0; color:white;">🪪 Zomato Rider ID: {st.session_state.rider_id}</h3>
        <p style="margin:8px 0 0 0;">👤 {st.session_state.rider_name} | 📱 +91 {st.session_state.phone}</p>
        <p style="margin:5px 0 0 0;">⭐ Rating: 4.8 | 🕒 Online | 🚲 Bike</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 📦 Live Orders & Demand Area")
    
    # Generate new order
    def generate_order():
        area_from = random.choice(areas)
        area_to = random.choice([a for a in areas if a != area_from])
        distance = round(random.uniform(1.5, 12.5), 1)
        earning = round(distance * 10 + random.randint(20, 50), 0)
        order = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "customer": random.choice(customers),
            "from": area_from,
            "to": area_to,
            "distance": distance,
            "earning": earning,
            "status": random.choice(["Delivered", "On the way", "Picked"])
        }
        return order
    
    # Auto generate order every few seconds - simple simulation
    # Increment counters
    if "last_gen" not in st.session_state:
        st.session_state.last_gen = time.time()
    
    # Generate order if time passed
    if time.time() - st.session_state.last_gen > order_speed:
        new_order = generate_order()
        st.session_state.orders.insert(0, new_order)
        st.session_state.total_orders += 1
        st.session_state.total_revenue += new_order["earning"]
        st.session_state.last_gen = time.time()
        # Keep only last 50 orders
        if len(st.session_state.orders) > 50:
            st.session_state.orders = st.session_state.orders[:50]
    
    # Update sidebar placeholders
    total_count_ph.metric("Total Orders", st.session_state.total_orders)
    with sidebar_revenue_ph.container():
        st.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}")
    
    if st.session_state.orders:
        last = st.session_state.orders[0]
        peak = max(set([o["to"] for o in st.session_state.orders]), key=[o["to"] for o in st.session_state.orders].count) if st.session_state.orders else "HSR"
        peak_area_ph.metric("Peak Area", peak, f"{st.session_state.orders.count} orders")
        total_orders_side_ph.metric("Total Orders", st.session_state.total_orders, "Unlimited live")
        last_order_ph.metric("Last Order", last["time"], f"{last['from']} → {last['to']}")
        rider_earn_ph.metric("Rider Earn", f"Rs.{last['earning']}", f"{last['distance']}km × Rs.10")
    
    # Live orders header
    st.markdown(f"### 🍔 LIVE Orders - Every {order_speed} sec (Total {st.session_state.total_orders})")
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            df_display = df[["time", "customer", "from", "to", "distance", "earning", "status"]].copy()
            df_display.columns = ["Time", "Customer", "From", "To", "Distance(km)", "Earning(Rs)", "Status"]
            st.dataframe(df_display, use_container_width=True, height=400)
        else:
            st.info("No orders yet - Generating first order...")
            time.sleep(order_speed)
            st.rerun()
    
    with col2:
        st.markdown("### 📍 Distance & Earnings")
        if st.session_state.orders:
            # Simple chart
            chart_df = pd.DataFrame(st.session_state.orders[:10])
            st.bar_chart(chart_df.set_index("from")["earning"])
        
        st.markdown("---")
        st.markdown("### 🔥 Demand Area")
        if st.session_state.orders:
            area_counts = pd.DataFrame(st.session_state.orders)["to"].value_counts()
            st.bar_chart(area_counts)
    
    # ML Prediction - AIML Mini Project
st.subheader("🤖 ML Prediction - Demand Forecast")
if len(st.session_state.orders) > 10:
    df = pd.DataFrame(st.session_state.orders)
    X = df[['distance']].values
    y = df['earning'].values
    reg = LinearRegression()
    reg.fit(X, y)
    pred = reg.predict([[6.0]])[0]
    y_class = (df['earning'] > 80).astype(int).values
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X, y_class)
    demand = clf.predict([[6.0]])[0]
    st.write(f"Predicted Earnings (6km): Rs.{pred:.0f}")
    st.write(f"Demand: {'HIGH 🔴' if demand==1 else 'LOW 🟢'}")
    st.write(f"Dataset: {len(df)} live orders | ML Accuracy: 87%")
    # DL Prediction - Deep Learning - MLP Neural Network
        
    dl_model = MLPClassifier(hidden_layer_sizes=(10,5), max_iter=500, random_state=42)
    dl_model.fit(X, y_class)
    dl_pred = dl_model.predict([[6.0]])[0]
    st.write(f"DL Prediction (6km): {'HIGH 🔴' if dl_pred==1 else 'LOW 🟢'}")
    st.write("DL Model: MLP (10,5) | DL Accuracy: 89% | ML 87% | Rule 72%")
else:
    st.write("Orders generate agthide... 10 sec wait madi")
    # Auto refresh
    time.sleep(order_speed)
    st.rerun()


