
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import time
import math

st.set_page_config(page_title="DeliveryPro - Zomato", layout="wide", page_icon="🍔")

AREAS_COORDS = {
    "BTM": (12.9166, 77.6101),
    "Koramangala": (12.9279, 77.6271),
    "Indiranagar": (12.9784, 77.6408),
    "HSR": (12.9116, 77.6387),
    "Whitefield": (12.9698, 77.7500),
    "Jayanagar": (12.9279, 77.5937),
    "Marathahalli": (12.9591, 77.6974),
    "Bellandur": (12.9352, 77.6245),
    "Electronic City": (12.8456, 77.6603),
    "MG Road": (12.9759, 77.6063)
}

BASE_PAY = 35
PER_KM = 10

def calc_dist(a1, a2):
    if a1 == a2:
        return round(random.uniform(1.0, 3.0), 1)
    lat1, lon1 = AREAS_COORDS[a1]
    lat2, lon2 = AREAS_COORDS[a2]
    dlat = (lat2 - lat1) * 111
    dlon = (lon2 - lon1) * 111 * 0.8
    dist = math.sqrt(dlat**2 + dlon**2)
    return round(max(1.5, dist + random.uniform(-0.5, 0.5)), 1)

if 'page' not in st.session_state:
    st.session_state.page = "splash"
if 'orders' not in st.session_state:
    st.session_state.orders = []
    st.session_state.order_id = 1
    st.session_state.total_revenue = 0
    st.session_state.area_demand = {area: 0 for area in AREAS_COORDS.keys()}
if 'rider_id' not in st.session_state:
    st.session_state.rider_id = ""
if 'rider_phone' not in st.session_state:
    st.session_state.rider_phone = ""
if 'rider_name' not in st.session_state:
    st.session_state.rider_name = ""

st.markdown("""
<style>
.splash { text-align:center; padding:50px; }
.login-box { max-width:400px; margin:auto; padding:30px; border:1px solid #eee; border-radius:20px; box-shadow:0 4px 20px rgba(0,0,0,0.1); }
.id-card { background: linear-gradient(135deg, #CB202D, #E23744); color:white; padding:20px; border-radius:15px; }
</style>
""", unsafe_allow_html=True)

if st.session_state.page == "splash":
    st.markdown('<div class="splash">', unsafe_allow_html=True)
    st.markdown("# 🍔")
    st.markdown("# DeliveryPro")
    st.markdown("### Rider Partner App")
    st.markdown("#### Zomato Style")
    st.markdown("---")
    st.markdown("##### 🚀 Real-time Orders | 💰 Live Earnings | 📍 Demand Areas")
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True, type="primary"):
            st.session_state.page = "login"
            st.rerun()
        st.caption("✅ Real Customer Orders | No Fixed Logic | Unlimited Live")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### 🔐 Rider Login")
    st.markdown("Enter your mobile number")
    phone = st.text_input("📱 Mobile Number", placeholder="Ex: 9876543210", max_chars=10)
    name = st.text_input("👤 Your Name", placeholder="Ex: Lakshmi")
    if st.button("📩 Send OTP", use_container_width=True, type="primary"):
        if len(phone) == 10 and phone.isdigit() and name.strip() != "":
            otp = random.randint(1000, 9999)
            st.session_state.generated_otp = otp
            st.session_state.rider_phone = phone
            st.session_state.rider_name = name
            st.session_state.page = "otp"
            st.rerun()
        else:
            st.error("10 digit number and name beku!")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.page = "splash"
        st.rerun()

elif st.session_state.page == "otp":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("### 🔑 OTP Verification")
    st.info(f"OTP sent to +91 {st.session_state.rider_phone} (Demo OTP: {st.session_state.generated_otp})")
    otp_input = st.text_input("Enter 4-digit OTP", placeholder="Ex: 1234", max_chars=4)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Verify & Register", use_container_width=True, type="primary"):
            if otp_input.isdigit() and int(otp_input) == st.session_state.generated_otp:
                rider_id = f"ZOMATO-{random.randint(10000, 99999)}"
                st.session_state.rider_id = rider_id
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error(f"Wrong OTP! Correct is {st.session_state.generated_otp}")
    with col2:
        if st.button("🔄 Resend OTP", use_container_width=True):
            st.session_state.generated_otp = random.randint(1000, 9999)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    col1, col2 = st.columns([3,1])
    with col1:
        st.markdown(f"### 🍔 Welcome, {st.session_state.rider_name}! 👋")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.page = "splash"
            st.session_state.orders = []
            st.session_state.rider_id = ""
            st.rerun()
    
    st.markdown(f"""
    <div class="id-card">
        <h3>🪪 Zomato Rider ID: {st.session_state.rider_id}</h3>
        <p>👤 {st.session_state.rider_name} | 📱 +91 {st.session_state.rider_phone}</p>
        <p>⭐ Rating: {random.uniform(4.5,5.0):.1f} | 🕐 Online | 🏍️ Bike</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    sidebar_total_ph = st.sidebar.empty()
    sidebar_revenue_ph = st.sidebar.empty()
    speed = st.sidebar.slider("Order Speed (sec)", 1, 5, 2, key="dash_speed")
    st.sidebar.markdown(f"**Rider:** {st.session_state.rider_name}")
    st.sidebar.markdown(f"**ID:** {st.session_state.rider_id}")
    if st.sidebar.button("🔄 Reset Orders"):
        st.session_state.orders = []
        st.session_state.order_id = 1
        st.session_state.total_revenue = 0
        st.session_state.area_demand = {area: 0 for area in AREAS_COORDS.keys()}
    
    st.title("📦 Live Orders & Demand Area")
    top_ph = st.empty()
    mid_ph = st.empty()
    chart_ph = st.empty()
    
    restaurants = ["Truffles", "Toit", "Meghana Foods", "Corner House", "Empire", "A2B", "MCD", "KFC", "Dominos", "Beijing Bites"]
    
    for _ in range(10000):
        now = datetime.now()
        cust_area = random.choice(list(AREAS_COORDS.keys()))
        rest_area = random.choice(list(AREAS_COORDS.keys()))
        if random.random() < 0.7:
            rest_area = random.choice([cust_area] + list(AREAS_COORDS.keys())[:4])
        dist = calc_dist(rest_area, cust_area)
        rest = random.choice(restaurants)
        food = random.randint(150, 600)
        surge = random.uniform(1.2, 1.8) if 18 <= now.hour <= 22 else random.uniform(1.0, 1.2)
        delivery_fee = (BASE_PAY + dist * PER_KM) * surge
        total = food + delivery_fee
        rider_earn = delivery_fee * 0.8
        order = {
            "ID": st.session_state.order_id,
            "Time": now.strftime("%H:%M:%S"),
            "Restaurant": rest,
            "From": rest_area,
            "To": cust_area,
            "Dist_km": dist,
            "Total_Rs": int(total),
            "Rider_Rs": round(rider_earn, 1),
        }
        st.session_state.orders.append(order)
        st.session_state.order_id += 1
        st.session_state.total_revenue += total
        st.session_state.area_demand[rest_area] += 1
        total_count = len(st.session_state.orders)
        recent = st.session_state.orders[-15:][::-1]
        sorted_demand = sorted(st.session_state.area_demand.items(), key=lambda x: x[1], reverse=True)
        peak_area, peak_count = sorted_demand[0] if sorted_demand else ("BTM", 0)
        with sidebar_total_ph.container():
            st.metric("Total Orders", total_count)
        with sidebar_revenue_ph.container():
            st.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}")
        
    
    # --- PREDICTIVE EARNINGS FEATURE ---
    with sidebar_revenue_ph.container():
        if total_count > 0:
            avg_per_order = st.session_state.total_revenue / total_count
            next_10 = avg_per_order * 10
            next_hour = (3600 / 5) * avg_per_order  # if speed 5 sec
            
            st.markdown("---")
            st.metric("🔮 Next 10 Orders", f"Rs.{int(next_10)}")
            st.metric("🔮 Next 1 Hour", f"Rs.{int(next_hour)}")
            st.caption(f"Avg Rs.{int(avg_per_order)}/order")
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.markdown("**🔥 Peak Area**")
                st.markdown(f"### {peak_area}")
                st.caption(f"{int(peak_count)} orders")
            with c2:
                st.markdown("**📦 Total Orders**")
                st.markdown(f"### {total_count}")
                st.caption("Unlimited live")
            with c3:
                st.markdown("**🕐 Last Order**")
                st.markdown(f"### {order['Time']}")
                st.caption(f"{rest_area} → {cust_area}")
            with c4:
                st.markdown("**💰 Rider Earn**")
                st.markdown(f"### Rs.{order['Rider_Rs']}")
                st.caption(f"{dist}km × Rs.{PER_KM}")
        with mid_ph.container():
            col1, col2 = st.columns([2,1])
            with col1:
                st.subheader(f"🍔 LIVE Orders - Every {speed} sec (Total {total_count})")
                df_recent = pd.DataFrame(recent)
                st.dataframe(df_recent, use_container_width=True, height=350)
            with col2:
                st.subheader("📍 Distance & Earnings")
                st.success(f"Order #{order['ID']}\n{rest} ({rest_area}) → {cust_area}\nDistance: {dist}km\nRider: Rs.{rider_earn:.0f}\nID: {st.session_state.rider_id}")
        with chart_ph.container():
            c1,c2 = st.columns(2)
            with c1:
                st.subheader("🔥 Area Demand")
                demand_df = pd.DataFrame(sorted_demand, columns=['Area','Orders']).set_index('Area')
                st.bar_chart(demand_df)
            with c2:
                st.subheader("💵 Avg Earning by Area")
                area_earn = {}
                for o in st.session_state.orders[-100:]:
                    area_earn.setdefault(o['From'], []).append(o['Rider_Rs'])
                if area_earn:
                    avg_earn = {k: sum(v)/len(v) for k,v in area_earn.items()}
                    earn_df = pd.DataFrame(list(avg_earn.items()), columns=['Area','AvgEarn']).set_index('Area').sort_values('AvgEarn', ascending=False)
                    st.bar_chart(earn_df)
        time.sleep(speed)
