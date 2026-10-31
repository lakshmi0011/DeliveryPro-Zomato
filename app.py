import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

st.set_page_config(page_title="DeliveryPro", page_icon="🍔", layout="wide")

if "page" not in st.session_state:
    st.session_state.page="login"
    st.session_state.rider_name=""
    st.session_state.phone=""
    st.session_state.total_orders=0
    st.session_state.total_revenue=0
    st.session_state.orders=[]
    st.session_state.rider_id=f"ZOMATO-{random.randint(10000,99999)}"
    st.session_state.last_gen=time.time()
    st.session_state.login_time=None

areas=["HSR","Koramangala","Indiranagar","BTM","Marathahalli","Whitefield","Jayanagar"]
customers=["Rahul","Priya","Amit","Sneha","Vikram"]
PER_KM=10

def gen_order():
    a_from=random.choice(areas)
    a_to=random.choice([a for a in areas if a!=a_from])
    d=round(random.uniform(1.5,12.5),1)
    e=round(d*PER_KM+random.randint(20,50),0)
    return {"Time":datetime.now().strftime("%H:%M:%S"),"Date":datetime.now().strftime("%d-%m-%Y"),"Customer":random.choice(customers),"From":a_from,"To":a_to,"Distance":d,"Rider_Rs":e,"Status":random.choice(["Delivered","On the way"])}

if st.session_state.page=="login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        st.markdown("## DeliveryPro - Zomato Rider Partner")
        st.divider()
        name=st.text_input("Your Name", placeholder="Mahalakshmi S")
        phone=st.text_input("Mobile Number", placeholder="8747941418")
        if st.button("Send OTP", use_container_width=True, type="primary"):
            if name and phone and len(phone)>=10:
                st.session_state.rider_name=name
                st.session_state.phone=phone
                st.session_state.page="otp"
                st.rerun()
            else:
                st.error("Enter valid details")

elif st.session_state.page=="otp":
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        st.markdown("## OTP Verification")
        st.divider()
        st.info(f"OTP sent to {st.session_state.phone} | Demo: 1234")
        otp=st.text_input("Enter OTP", placeholder="1234", max_chars=4)
        ca,cb=st.columns(2)
        with ca:
            if st.button("Verify OTP", use_container_width=True, type="primary"):
                if otp=="1234":
                    # RESET ON LOGIN - Yav time login adru, aa time inda start
                    st.session_state.total_orders=0
                    st.session_state.total_revenue=0
                    st.session_state.orders=[]
                    st.session_state.login_time=datetime.now()
                    st.session_state.rider_id=f"ZOMATO-{random.randint(10000,99999)}"
                    st.session_state.page="dashboard"
                    st.rerun()
                else:
                    st.error("Use 1234")
        with cb:
            if st.button("Back", use_container_width=True):
                st.session_state.page="login"
                st.rerun()

else:
    if time.time()-st.session_state.last_gen>2:
        o=gen_order()
        st.session_state.orders.insert(0,o)
        st.session_state.total_orders+=1
        st.session_state.total_revenue+=o["Rider_Rs"]
        st.session_state.last_gen=time.time()
        if len(st.session_state.orders)>100:
            st.session_state.orders=st.session_state.orders[:100]

    with st.sidebar:
        st.markdown(f"**{st.session_state.rider_name}**")
        st.caption(st.session_state.rider_id)
        if st.session_state.login_time:
            st.caption(f"Login: {st.session_state.login_time.strftime('%I:%M %p')}")
        st.divider()
        c1,c2=st.columns(2)
        c1.metric("Orders", st.session_state.total_orders)
        c2.metric("Revenue", f"Rs.{int(st.session_state.total_revenue)}")
        st.divider()
        speed=st.slider("Order Speed",1,5,2)
        st.divider()
        if st.button("Reset", use_container_width=True):
            st.session_state.total_orders=0
            st.session_state.total_revenue=0
            st.session_state.orders=[]
            st.session_state.login_time=datetime.now()
            st.rerun()
        if st.button("Logout", use_container_width=True):
            st.session_state.page="login"
            st.rerun()

    # LIVE TIMINGS ALREADY IDE - HAGEE IRLI
    st.markdown(f"### Welcome, {st.session_state.rider_name}")
    login_time_str = st.session_state.login_time.strftime('%I:%M %p on %d-%m-%Y') if st.session_state.login_time else datetime.now().strftime('%I:%M %p')
    st.markdown(f"""<div style="background:#16a34a; padding:10px; border-radius:8px; color:white;"><b>{st.session_state.rider_id} | Online | Live: {datetime.now().strftime('%I:%M:%S %p')} | Login: {login_time_str}</b></div>""", unsafe_allow_html=True)
    st.markdown("")

    if st.session_state.orders:
        recent=st.session_state.orders
        to_counts={}
        for x in recent[:50]:
            to_counts[x["To"]]=to_counts.get(x["To"],0)+1
        peak=max(to_counts, key=to_counts.get) if to_counts else "HSR"
        last=recent[0]
        # TOTAL ORDERS SHOW - AH TIME PRAKARA + DEMAND AREA + EACH ORDER AMT + PEAK + LIVE TIMINGS
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Total Orders", st.session_state.total_orders, f"Since {st.session_state.login_time.strftime('%I:%M %p')}" if st.session_state.login_time else "")
        m2.metric("Total Revenue", f"Rs.{int(st.session_state.total_revenue)}", f"Rs.{last['Rider_Rs']} last")
        m3.markdown(f"""<div style="background:#dcfce7; padding:8px; border-radius:8px; border-left:4px solid #16a34a;"><div style="font-size:11px; color:#15803d;">Peak Demand - {datetime.now().strftime('%I:%M %p')}</div><div style="font-size:16px; font-weight:bold; color:#166534;">{peak}</div><div style="font-size:10px; color:#15803d;">{to_counts.get(peak,0)} orders live</div></div>""", unsafe_allow_html=True)
        m4.metric("Last Order Amt", f"Rs.{last['Rider_Rs']}", f"{last['From']} → {last['To']} | {last['Time']}")

    st.divider()
    st.markdown("### High Demand Areas")
    st.caption(f"Live: {datetime.now().strftime('%I:%M:%S %p')} | Login: {login_time_str} | Total {st.session_state.total_orders} orders since login")

    if st.session_state.orders:
        live_counts={}
        for o in st.session_state.orders[:50]:
            live_counts[o["To"]]=live_counts.get(o["To"],0)+1
        cols=st.columns(3)
        sorted_areas=sorted(live_counts.items(), key=lambda x:x[1], reverse=True)
        for idx,(area,cnt) in enumerate(sorted_areas):
            col=cols[idx%3]
            amt_list=[o["Rider_Rs"] for o in st.session_state.orders[:50] if o["To"]==area]
            avg_amt=sum(amt_list)/len(amt_list) if amt_list else 0
            if idx==0:
                col.success(f"{area} - {cnt} orders - Rs.{avg_amt:.0f} avg - HIGH")
            elif cnt>=sorted_areas[0][1]*0.6:
                col.warning(f"{area} - {cnt} orders - Rs.{avg_amt:.0f} avg")
            else:
                col.info(f"{area} - {cnt} orders - Rs.{avg_amt:.0f} avg")

    st.divider()
    c1,c2=st.columns([2,1])
    with c1:
        st.subheader(f"Live Orders - Each Order Amount Changes")
        st.caption(f"Total {st.session_state.total_orders} orders since {login_time_str} | Each order amount Rs.50-180 based on distance")
        if st.session_state.orders:
            df=pd.DataFrame(st.session_state.orders[:20])
            st.dataframe(df[["Time","Customer","From","To","Distance","Rider_Rs","Status"]], use_container_width=True, height=400)
    with c2:
        st.subheader("Area Demand - Orders Count")
        if st.session_state.orders:
            ddf=pd.DataFrame(st.session_state.orders[:50])
            st.bar_chart(ddf["To"].value_counts())
        st.subheader("Amount per Order")
        if st.session_state.orders:
            ddf2=pd.DataFrame(st.session_state.orders[:20])
            st.bar_chart(ddf2.set_index("To")["Rider_Rs"])

    time.sleep(speed)
    st.rerun()
