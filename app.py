"""
CampusRide — Student Ride-Sharing Platform
ICT Group Project | Mobility as a Service (MaaS)
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusRide — Student Ride-Sharing",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E2761 0%, #028090 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 16px;
        padding: 6px 0;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #f0f8ff;
        border: 1px solid #d1faf0;
        border-radius: 12px;
        padding: 16px;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #1E2761, #028090);
        color: white;
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 20px;
        font-weight: 600;
    }

    /* Privacy card */
    .privacy-card {
        background: #f8fffe;
        border-left: 4px solid #028090;
        padding: 16px 20px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
    }

    /* Ride card */
    .ride-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───────────────────────────────────────────────────────
if "privacy_accepted" not in st.session_state:
    st.session_state.privacy_accepted = False
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "total_co2" not in st.session_state:
    st.session_state.total_co2 = round(random.uniform(320, 480), 1)
if "total_commuters" not in st.session_state:
    st.session_state.total_commuters = random.randint(1200, 1800)
if "total_rides" not in st.session_state:
    st.session_state.total_rides = random.randint(400, 700)

# ─── Mock Data ────────────────────────────────────────────────────────────────
# Karachi coordinates (near a university area)
BASE_LAT = 24.8607
BASE_LON = 67.0011

np.random.seed(42)

def generate_vehicles():
    """Generate mock available vehicles around campus."""
    vehicle_types = ["🚗 Carpool", "🛴 E-Scooter", "🚲 Bicycle", "🚗 Carpool", "🛴 E-Scooter"]
    drivers     = ["Ali R.", "Sara M.", "Usman K.", "Fatima A.", "Hassan B."]
    destinations = [
        "Main Gate → Gulshan",
        "Block-5 → DHA",
        "Campus Loop",
        "North Nazimabad → City",
        "Clifton → Defense",
    ]
    seats = [3, 1, 1, 2, 1]
    times = ["Leaves in 5 min", "Available now", "Available now", "Leaves in 12 min", "Available now"]

    records = []
    for i in range(5):
        records.append({
            "lat":         BASE_LAT + np.random.uniform(-0.012, 0.012),
            "lon":         BASE_LON + np.random.uniform(-0.012, 0.012),
            "type":        vehicle_types[i],
            "driver":      drivers[i],
            "route":       destinations[i],
            "seats":       seats[i],
            "time":        times[i],
            "rating":      round(random.uniform(4.2, 5.0), 1),
        })
    return pd.DataFrame(records)

vehicles_df = generate_vehicles()

LOCATIONS = [
    "Main Campus Gate",
    "Library Block",
    "Engineering Building",
    "Student Cafeteria",
    "Sports Complex",
    "Gulshan-e-Iqbal",
    "DHA Phase 2",
    "North Nazimabad",
    "Clifton",
    "PECHS",
]

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚗 CampusRide")
    st.markdown("*Student Ride-Sharing Platform*")
    st.markdown("---")

    page = st.radio(
        "Navigate to:",
        ["📍 Find a Ride", "🔒 Privacy & Data Ethics", "📈 Community Impact"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Live status panel
    st.markdown("### 🟢 Live Status")
    st.markdown(f"**{len(vehicles_df)} rides** available now")
    st.markdown(f"**{st.session_state.total_commuters:,}** students served")
    st.markdown(f"**{st.session_state.total_rides}** rides today")

    st.markdown("---")
    privacy_status = "✅ Accepted" if st.session_state.privacy_accepted else "⚠️ Not accepted"
    st.markdown(f"**Privacy Agreement:** {privacy_status}")

    if not st.session_state.privacy_accepted:
        st.warning("Accept the Privacy Agreement to book rides.")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:11px; opacity:0.7;'>ICT Group Project 2025<br>Data deleted after 30 days.</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — FIND A RIDE
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📍 Find a Ride":

    st.markdown('<div class="section-header">📍 Find a Ride Near You</div>', unsafe_allow_html=True)

    # Map + Available Rides side by side
    col_map, col_list = st.columns([3, 2])

    with col_map:
        st.markdown("#### 🗺️ Live Vehicle Map")
        st.caption("Real-time locations of available carpools, e-scooters & bicycles on campus")

        map_data = vehicles_df[["lat", "lon"]].copy()
        st.map(map_data, zoom=14, use_container_width=True)

        st.caption("📍 Each pin represents an available vehicle. Locations update every 30 seconds.")

    with col_list:
        st.markdown("#### 🚦 Available Rides")
        for _, row in vehicles_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="ride-card">
                    <strong>{row['type']}</strong> &nbsp; ⭐ {row['rating']}<br>
                    <span style='color:#028090'>👤 {row['driver']}</span><br>
                    🗺️ {row['route']}<br>
                    💺 {row['seats']} seat(s) left &nbsp;|&nbsp; 🕐 {row['time']}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Booking Form ──────────────────────────────────────────────────────────
    st.markdown("#### 🎫 Book a Ride")

    if not st.session_state.privacy_accepted:
        st.warning("⚠️ You must accept the **Privacy Agreement** (in the Privacy tab) before booking a ride.")
        st.info("👈 Go to **🔒 Privacy & Data Ethics** in the sidebar and accept the agreement.")
    else:
        with st.form("booking_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                pickup = st.selectbox("📍 Pickup Location", LOCATIONS, index=0)
            with col2:
                dropoff = st.selectbox("🏁 Drop-off Location", LOCATIONS, index=5)
            with col3:
                ride_type = st.selectbox("🚗 Ride Type", ["Carpool 🚗", "E-Scooter 🛴", "Bicycle 🚲"])

            col4, col5 = st.columns(2)
            with col4:
                ride_time = st.time_input("⏰ Departure Time", value=datetime.now().time())
            with col5:
                seats_needed = st.number_input("💺 Seats Needed", min_value=1, max_value=4, value=1)

            special_note = st.text_input("📝 Special Note (optional)", placeholder="e.g. I have a large bag")

            submitted = st.form_submit_button("🚀 Book Ride Now", use_container_width=True)

            if submitted:
                if pickup == dropoff:
                    st.error("❌ Pickup and drop-off locations cannot be the same!")
                else:
                    # Save booking
                    booking_id = f"CR-{random.randint(1000, 9999)}"
                    booking = {
                        "id": booking_id,
                        "pickup": pickup,
                        "dropoff": dropoff,
                        "type": ride_type,
                        "time": str(ride_time),
                        "seats": seats_needed,
                        "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    st.session_state.bookings.append(booking)

                    # Update impact stats
                    st.session_state.total_co2 += round(random.uniform(0.8, 2.1), 1)
                    st.session_state.total_commuters += 1
                    st.session_state.total_rides += 1

                    st.success(f"""
                    ✅ **Ride Booked Successfully!**

                    🎫 **Booking ID:** `{booking_id}`
                    📍 **From:** {pickup} → **To:** {dropoff}
                    🚗 **Type:** {ride_type} | 💺 **Seats:** {seats_needed}
                    ⏰ **Departure:** {ride_time.strftime('%I:%M %p')}

                    Your driver will be notified. Location shared only for this trip.
                    Your data will be **automatically deleted in 30 days**.
                    """)

    # ── Booking History ───────────────────────────────────────────────────────
    if st.session_state.bookings:
        st.markdown("---")
        st.markdown("#### 📋 Your Booking History")
        st.caption("🔒 This data is stored only on your device session and never shared.")

        history_df = pd.DataFrame(st.session_state.bookings)
        history_df.columns = ["Booking ID", "Pickup", "Drop-off", "Type", "Time", "Seats", "Booked At"]
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear My History (Right to Erasure)"):
            st.session_state.bookings = []
            st.success("✅ Your booking history has been permanently deleted.")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRIVACY & DATA ETHICS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔒 Privacy & Data Ethics":

    st.markdown('<div class="section-header">🔒 Privacy & Data Ethics Policy</div>', unsafe_allow_html=True)

    st.markdown("""
    > *CampusRide is built on the principle that your data belongs to you.
    Below is a full, transparent explanation of how we handle your information.*
    """)

    # ── Privacy Principles ────────────────────────────────────────────────────
    st.markdown("### 🛡️ Our 5 Privacy Principles")

    principles = [
        {
            "icon": "📍",
            "title": "Location Obfuscation",
            "desc": (
                "We never store your precise GPS coordinates. Instead, we apply **fuzzing** — "
                "rounding your location to the nearest 100 meters. Drivers only see your "
                "approximate pickup zone, not your exact position. Once your ride starts, "
                "location access is automatically revoked."
            ),
        },
        {
            "icon": "🗂️",
            "title": "Data Minimization",
            "desc": (
                "We collect only what is strictly necessary to match you with a ride: "
                "your pickup zone, destination, and ride time. We do **not** collect "
                "your name, student ID, phone number, or any identifying information "
                "unless you voluntarily provide it. No profiling. No targeted ads."
            ),
        },
        {
            "icon": "🗑️",
            "title": "Automatic Deletion After 30 Days",
            "desc": (
                "All trip records, location logs, and matching data are **automatically "
                "and permanently deleted** 30 days after your ride. You can also invoke "
                "your Right to Erasure at any time from the booking history panel "
                "and your data is deleted immediately."
            ),
        },
        {
            "icon": "🔐",
            "title": "Encrypted Data in Transit",
            "desc": (
                "All communication between your device and our servers uses "
                "**TLS 1.3 encryption** — the same standard used by banks. "
                "Your location and booking data are never transmitted in plain text. "
                "Data at rest is encrypted using AES-256."
            ),
        },
        {
            "icon": "🚫",
            "title": "No Third-Party Sharing",
            "desc": (
                "Your data is **never sold, rented, or shared** with advertisers, "
                "third-party analytics providers, or any external organization. "
                "The only parties who see trip data are the matched driver and "
                "our anonymized internal system logs (no names attached)."
            ),
        },
    ]

    for p in principles:
        st.markdown(f"""
        <div class="privacy-card">
            <strong style="font-size:16px;">{p['icon']} {p['title']}</strong><br><br>
            {p['desc']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")

    # ── Data Flow Diagram (text-based) ────────────────────────────────────────
    st.markdown("### 🔄 How Your Data Flows")

    col1, col2, col3, col4, col5 = st.columns(5)
    flow_steps = [
        ("📱", "You Request a Ride", "Pickup zone only (obfuscated)"),
        ("🔀", "Matching Algorithm", "Anonymous — no names used"),
        ("🚗", "Driver Notified", "Sees zone, not exact address"),
        ("✅", "Ride Completed", "Trip record created"),
        ("🗑️", "Auto-Delete", "All data erased after 30 days"),
    ]
    for col, (icon, title, sub) in zip([col1, col2, col3, col4, col5], flow_steps):
        with col:
            st.markdown(f"""
            <div style='text-align:center; background:#f0f8ff; border-radius:10px; padding:14px 8px; border:1px solid #d1faf0;'>
                <div style='font-size:28px'>{icon}</div>
                <div style='font-weight:600; font-size:13px; color:#1E2761; margin:6px 0 4px;'>{title}</div>
                <div style='font-size:11px; color:#64748b;'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Comparison Table ──────────────────────────────────────────────────────
    st.markdown("### 📊 CampusRide vs Commercial Apps")

    comparison = pd.DataFrame({
        "Feature":            ["Collects your name?", "Stores precise GPS?", "Sells data to advertisers?", "Auto-deletes data?", "Encrypts data?", "Student-only access?"],
        "CampusRide ✅":      ["No",                  "No (obfuscated)",     "Never",                     "Yes — 30 days",      "Yes (TLS 1.3)",  "Yes"],
        "Uber / Careem ❌":   ["Yes",                  "Yes (full history)",  "Yes (partners)",             "No clear policy",    "Yes",            "No"],
    })
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── Pakistan Data Law ─────────────────────────────────────────────────────
    st.markdown("### 🇵🇰 Legal Framework")
    st.info("""
    **Pakistan Personal Data Protection Act (PDPA) — Draft 2023**

    CampusRide is designed to comply with Pakistan's emerging data protection framework:

    - **Consent required** before collecting any personal data ✅ (this agreement)
    - **Purpose limitation** — data used only for ride matching ✅
    - **Right to erasure** — delete your data anytime ✅
    - **Data localization** — all data stored on local servers ✅
    - **Breach notification** — users notified within 72 hours of any breach ✅
    """)

    st.markdown("---")

    # ── Privacy Agreement Checkbox ────────────────────────────────────────────
    st.markdown("### ✍️ User Privacy Agreement")

    with st.expander("📄 Read Full Agreement Before Accepting", expanded=False):
        st.markdown("""
        **CampusRide Privacy Agreement — Version 1.0**

        By accepting this agreement, you acknowledge and consent to the following:

        1. CampusRide will collect your **approximate location** (obfuscated to 100m radius) solely for the purpose of ride matching.
        2. No personally identifiable information (name, student ID, phone) is required or stored without your explicit consent.
        3. All trip data will be **automatically and permanently deleted 30 days** after each trip.
        4. You may request **immediate deletion** of your data at any time using the "Clear My History" button.
        5. Your data will **never be sold, shared, or used for advertising** purposes.
        6. Data is encrypted in transit (TLS 1.3) and at rest (AES-256).
        7. CampusRide operates as a **student-only, non-commercial** platform.
        8. You are at least **18 years of age** or have guardian consent to use this platform.
        9. This agreement can be **withdrawn at any time** by deleting your session data.
        10. CampusRide complies with Pakistan's Personal Data Protection Act (Draft 2023).

        *Last updated: June 2025*
        """)

    accepted = st.checkbox(
        "✅ I have read and accept the CampusRide Privacy Agreement. I understand how my data is collected, used, and deleted.",
        value=st.session_state.privacy_accepted,
    )

    if accepted and not st.session_state.privacy_accepted:
        st.session_state.privacy_accepted = True
        st.success("🎉 Privacy agreement accepted! You can now book rides from the **Find a Ride** tab.")
        st.balloons()
    elif not accepted and st.session_state.privacy_accepted:
        st.session_state.privacy_accepted = False
        st.warning("⚠️ Privacy agreement withdrawn. You will not be able to book rides until you re-accept.")

    if st.session_state.privacy_accepted:
        st.success("✅ **Status: Privacy Agreement Accepted.** You are authorized to book rides.")
    else:
        st.error("❌ **Status: Not Accepted.** Accept the agreement above to unlock booking.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — COMMUNITY IMPACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Community Impact":

    st.markdown('<div class="section-header">📈 Community Impact Dashboard</div>', unsafe_allow_html=True)

    st.markdown("""
    > *Every ride shared is a step toward a greener, more connected campus.
    Here's the real-world impact CampusRide has made so far.*
    """)

    # ── Key Metrics ───────────────────────────────────────────────────────────
    st.markdown("### 🌍 Live Impact Metrics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="🌿 CO₂ Saved (kg)",
            value=f"{st.session_state.total_co2:,.1f}",
            delta=f"+{round(random.uniform(1.2, 3.5), 1)} today",
        )
    with col2:
        st.metric(
            label="👥 Commuters Assisted",
            value=f"{st.session_state.total_commuters:,}",
            delta=f"+{random.randint(8, 25)} this week",
        )
    with col3:
        st.metric(
            label="🚗 Rides Completed",
            value=f"{st.session_state.total_rides:,}",
            delta=f"+{random.randint(12, 30)} today",
        )
    with col4:
        st.metric(
            label="⏱️ Avg. Commute Reduced",
            value="18 min",
            delta="-3 min vs last month",
        )

    st.markdown("---")

    # ── Weekly Ride Trend Chart ────────────────────────────────────────────────
    st.markdown("### 📊 Weekly Ride Trend")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rides_per_day = [random.randint(60, 130) for _ in days]
    co2_per_day   = [round(r * random.uniform(0.9, 1.3), 1) for r in rides_per_day]

    trend_df = pd.DataFrame({
        "Day":         days,
        "Rides":       rides_per_day,
        "CO₂ Saved (kg)": co2_per_day,
    }).set_index("Day")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("**Rides per Day**")
        st.bar_chart(trend_df[["Rides"]], color="#028090")
    with col_chart2:
        st.markdown("**CO₂ Saved per Day (kg)**")
        st.bar_chart(trend_df[["CO₂ Saved (kg)"]], color="#02C39A")

    st.markdown("---")

    # ── Ride Type Breakdown ────────────────────────────────────────────────────
    st.markdown("### 🚗 Ride Type Breakdown")

    col_a, col_b = st.columns([2, 3])
    with col_a:
        breakdown = pd.DataFrame({
            "Type":       ["Carpool 🚗", "E-Scooter 🛴", "Bicycle 🚲"],
            "Rides":      [random.randint(200, 350), random.randint(100, 200), random.randint(80, 150)],
            "CO₂ Saved":  [random.randint(150, 250), random.randint(40, 90),  random.randint(30, 70)],
        })
        st.dataframe(breakdown, use_container_width=True, hide_index=True)

    with col_b:
        st.bar_chart(breakdown.set_index("Type")[["Rides", "CO₂ Saved"]])

    st.markdown("---")

    # ── Environmental Equivalence ─────────────────────────────────────────────
    st.markdown("### 🌱 What Our CO₂ Savings Equal")

    co2_total = st.session_state.total_co2
    col1, col2, col3 = st.columns(3)
    with col1:
        trees = round(co2_total / 21, 1)
        st.markdown(f"""
        <div style='text-align:center; background:#eaf3de; border-radius:12px; padding:20px;'>
            <div style='font-size:40px'>🌳</div>
            <div style='font-size:28px; font-weight:600; color:#3B6D11;'>{trees}</div>
            <div style='color:#3B6D11; font-size:14px;'>Trees worth of CO₂ absorbed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        km_driven = round(co2_total / 0.21, 0)
        st.markdown(f"""
        <div style='text-align:center; background:#faeeda; border-radius:12px; padding:20px;'>
            <div style='font-size:40px'>🚗</div>
            <div style='font-size:28px; font-weight:600; color:#633806;'>{km_driven:,.0f} km</div>
            <div style='color:#633806; font-size:14px;'>Equivalent car distance avoided</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        phones = round(co2_total * 121.6, 0)
        st.markdown(f"""
        <div style='text-align:center; background:#e6f1fb; border-radius:12px; padding:20px;'>
            <div style='font-size:40px'>📱</div>
            <div style='font-size:28px; font-weight:600; color:#0C447C;'>{phones:,.0f}</div>
            <div style='color:#0C447C; font-size:14px;'>Smartphone charges equivalent</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Student Testimonials ──────────────────────────────────────────────────
    st.markdown("### 💬 Student Testimonials")

    testimonials = [
        ("Sara M., CS Year 2",     "⭐⭐⭐⭐⭐", "CampusRide cut my commute from 50 mins to 25 mins. And I love that they don't track my location after the ride ends!"),
        ("Ali R., Engineering",    "⭐⭐⭐⭐⭐", "Finally a ride-sharing app built for students. No surge pricing, no data selling. Just honest carpooling."),
        ("Fatima K., Business",    "⭐⭐⭐⭐☆",  "The privacy policy is actually readable! I checked the 30-day deletion myself and it works. Great project."),
        ("Hassan B., Year 3",      "⭐⭐⭐⭐⭐", "Saved over Rs. 3,000 this month on commute costs. Plus I met some great people from other departments."),
    ]

    col1, col2 = st.columns(2)
    for i, (name, stars, quote) in enumerate(testimonials):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:12px; padding:16px; margin:8px 0;'>
                <div style='font-size:14px;'>{stars}</div>
                <div style='font-style:italic; color:#334155; margin:8px 0;'>"{quote}"</div>
                <div style='font-size:12px; font-weight:600; color:#028090;'>— {name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── SDG Alignment ─────────────────────────────────────────────────────────
    st.markdown("### 🌐 UN Sustainable Development Goals Alignment")

    sdgs = [
        ("🏙️ SDG 11", "Sustainable Cities", "Reducing urban congestion and promoting shared transport"),
        ("🌍 SDG 13", "Climate Action",      "Cutting CO₂ emissions through ride-sharing"),
        ("⚖️ SDG 10", "Reduced Inequality",  "Affordable transport access for all students"),
        ("🔋 SDG 7",  "Clean Energy",        "Promoting e-scooters and low-emission vehicles"),
    ]

    cols = st.columns(4)
    for col, (sdg, title, desc) in zip(cols, sdgs):
        with col:
            st.markdown(f"""
            <div style='background:#f0f8ff; border-radius:12px; padding:14px; text-align:center; border:1px solid #d1faf0; height:150px;'>
                <div style='font-size:24px'>{sdg.split()[0]}</div>
                <div style='font-weight:600; color:#1E2761; font-size:13px;'>{sdg.split()[1]} {title}</div>
                <div style='font-size:11px; color:#64748b; margin-top:6px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🚗 <strong>CampusRide</strong> — ICT Group Project 2025 &nbsp;|&nbsp;
    Built with Streamlit &nbsp;|&nbsp;
    🔒 Privacy-first &nbsp;|&nbsp;
    🌿 Carbon-conscious &nbsp;|&nbsp;
    📍 Karachi, Pakistan
</div>
""", unsafe_allow_html=True)
