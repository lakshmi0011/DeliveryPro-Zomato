import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

st.set_page_config(page_title="DeliveryPro - Zomato Rider", page_icon="🍔", layout="wide")

# Session init
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
if "last_gen" not in st.session_state:
    st.session_state.last_gen = time.time()

areas = ["HSR", "Koramangala", "Indiranagar", "BTM", "Marathahalli", "Whitefield", "Jayanagar"]
customers = ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Kiran"]

PER_KM = 10

# LOGIN PAGE
if st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 🍔 DeliveryPro - Zomato Rider Partner")
        st.markdown("### Welcome! Please Register")
        st.markdown("---")
        name = st.text_input("👤 Your Name", placeholder="ex: lakshmi")
        phone = st.text_input("📱 Mobile Number", placeholder="ex: 8747941418")
        if st.button("✅ Register & Start Delivery", use_container_width=True, type="primary"):
            if name and phone and len(phone) >= 10:
                st.session_state.rider_name = name
                st.session_state.phone = phone
                st.session_state.page = "dashboard"
                st.session_state.logged_in = True
                st.session_state.rider_id = f"ZOMATO-{random.randint(10000, 99999)}"
                st.success(f"Welcome {name}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please enter valid Name and 10 digit Mobile Number!")
        st.info("Simulation app - No OTP needed!")

# DASHBOARD
else:
    # Placeholders - ALL defined together
    top_ph = st.empty()
    sidebar_total_ph = st.empty()
    sidebar_revenue_ph = st.empty()
    sidebar_peak_ph = st.empty()
    sidebar_last_ph = st.empty()
    sidebar_rider_ph = st.empty()
    map_ph = st.empty()
    mid_ph = st.empty()
    chart_ph = st.empty()

    with st.sidebar:
        with sidebar_total_ph.container():
            st.metric("Total Orders", st.session_state.total_orders)
        st.markdown("---")
        with sidebar_revenue_ph.container():
            st.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}")
        st.markdown("---")
        order_speed = st.slider("Order Speed (sec)", 1, 10, 2)
        st.markdown("---")
        if st.button("🔄 Reset Orders", use_container_width=True):
            st.session_state.total_orders = 0
            st.session_state.total_revenue = 0
            st.session_state.orders = []
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
        st.markdown("---")
        with sidebar_peak_ph.container():
            st.write("")
        with sidebar_last_ph.container():
            st.write("")
        with sidebar_rider_ph.container():
            st.write("")

    # Header
    with top_ph.container():
        st.markdown(f"## 🍔 Welcome, {st.session_state.rider_name}! 👋")
        st.markdown(f"""
        <div style="background-color:#DC2626; padding:18px; border-radius:12px; color:white;">
            <h3 style="margin:0; color:white;">🪪 Zomato Rider ID: {st.session_state.rider_id}</h3>
            <p style="margin:6px 0 0 0;">👤 {st.session_state.rider_name} | 📱 +91 {st.session_state.phone} | ⭐ 4.8 | 🕒 Online</p>
        </div>
        """, unsafe_allow_html=True)

    # Generate order logic
    def gen_order():
        area_from = random.choice(areas)
        area_to = random.choice([a for a in areas if a != area_from])
        dist = round(random.uniform(1.5, 12.5), 1)
        earn = round(dist * PER_KM + random.randint(20, 50), 0)
        return {
            "ID": random.randint(1000, 9999),
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Customer": random.choice(customers),
            "From": area_from,
            "To": area_to,
            "Distance": dist,
            "Rider_Rs": earn,
            "Status": random.choice(["Delivered", "On the way", "Picked"])
        }

    if time.time() - st.session_state.last_gen > order_speed:
        o = gen_order()
        st.session_state.orders.insert(0, o)
        st.session_state.total_orders += 1
        st.session_state.total_revenue += o["Rider_Rs"]
        st.session_state.last_gen = time.time()
        if len(st.session_state.orders) > 100:
            st.session_state.orders = st.session_state.orders[:100]

    # Update sidebar
    with sidebar_total_ph.container():
        st.metric("Total Orders", st.session_state.total_orders)
    with sidebar_revenue_ph.container():
        st.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}")
    
    if st.session_state.orders:
        recent = st.session_state.orders
        peak_area = max(set([x["To"] for x in recent]), key=[x["To"] for x in recent].count) if recent else "HSR"
        last = recent[0]
        dist = last["Distance"]
        with sidebar_peak_ph.container():
            st.metric("Peak Area", peak_area, f"{len(recent)} orders")
        with sidebar_last_ph.container():
            st.metric("Last Order", last["Time"], f"{last['From']} → {last['To']}")
        with sidebar_rider_ph.container():
            st.metric("Rider Earn", f"Rs.{last['Rider_Rs']:.0f}", f"{dist}km × Rs.{PER_KM}")
    else:
        peak_area = "HSR"
        last = {"Distance": 0, "Rider_Rs": 0, "From": "-", "To": "-", "Time": "-"}
        dist = 0

    # LIVE HIGH DEMAND MAP - Live color changing by location
    with map_ph.container():
        st.markdown("### 🗺️ Live High Demand Map - Real Time")
        live_demand = pd.DataFrame({
            'Area': ['Indiranagar', 'HSR', 'Koramangala', 'BTM', 'Marathahalli'],
            'lat': [12.9784, 12.9116, 12.9279, 12.9166, 12.9591],
            'lon': [77.6408, 77.6377, 77.6271, 77.6101, 77.6974],
            'orders': [random.randint(1, 10) for _ in range(5)]
        })
        st.map(live_demand, latitude='lat', longitude='lon', size='orders')
        for idx, row in live_demand.iterrows():
            if row['orders'] >= 7:
                st.markdown(f"🔴 **{row['Area']} - HIGH DEMAND - {row['orders']} orders - Go now!**")
            elif row['orders'] >= 4:
                st.markdown(f"🟠 {row['Area']} - {row['orders']} orders - Medium")
            else:
                st.markdown(f"🟢 {row['Area']} - {row['orders']} orders - Low")
        st.caption(f"⏰ Live: {datetime.now().strftime('%H:%M:%S')} - Color changes every {order_speed} sec by location!")

    # LIVE Orders & Demand Area
    with mid_ph.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"🍔 LIVE Orders - Every {order_speed} sec (Total {st.session_state.total_orders})")
            if st.session_state.orders:
                df_recent = pd.DataFrame(st.session_state.orders[:20])
                st.dataframe(df_recent[["Time", "Customer", "From", "To", "Distance", "Rider_Rs", "Status"]], use_container_width=True, height=350)
            else:
                st.info("Generating first order...")
        with col2:
            st.subheader("📍 Distance & Earnings")
            if st.session_state.orders:
                df_e = pd.DataFrame(st.session_state.orders[:10])
                st.bar_chart(df_e.set_index("From")["Rider_Rs"])
            st.markdown("---")
            st.subheader("🔥 Area Demand")
            if st.session_state.orders:
                ddf = pd.DataFrame(st.session_state.orders)
                area_counts = ddf["To"].value_counts()
                st.bar_chart(area_counts)

    with chart_ph.container():
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🔥 Area Demand")
            if st.session_state.orders:
                demand_df = pd.DataFrame(st.session_state.orders)
                sorted_demand = demand_df["To"].value_counts().reset_index()
                sorted_demand.columns = ['Area', 'Orders']
                demand_plot = sorted_demand.set_index('Area')
                st.bar_chart(demand_plot)
        with c2:
            st.subheader("💹 Avg Earning by Area")
            area_earn = {}
            for o in st.session_state.orders[-100:]:
                area_earn.setdefault(o['From'], []).append(o['Rider_Rs'])
            if area_earn:
                avg_earn = {k: sum(v)/len(v) for k, v in area_earn.items()}
                earn_df = pd.DataFrame(list(avg_earn.items()), columns=['Area', 'AvgEarn']).set_index('Area').sort_values('AvgEarn', ascending=False)
                st.bar_chart(earn_df)

    time.sleep(order_speed)
    st.rerun()
