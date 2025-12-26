import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meril Clinical Trial Summary", layout="wide")

# --- Custom Header matching the original PDF ---
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("<h1 style='color: #0066CC; font-size: 60px;'>Meril</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<h2 style='text-align: center; margin-top: 20px;'>Clinical Trial Summary</h2>", unsafe_allow_html=True)



# --- Procedure & Date ---
st.header("Procedure & Date")

procedure_manual = st.text_area(
    "Procedure",
    height=1,
    key="procedure_manual",
    
)

date = st.text_input("Date (dd-mm-yyyy)", key="date")
surgeon_name = st.text_input("Surgeon Name", key="surgeon")
place = st.text_input("Place", key="place")

# --- Patient Profile ---
st.header("Patient Profile")
age = st.text_input("Age", key="age")
sex = st.radio("Sex", ["Female", "Male"], horizontal=True, key="sex")
bmi = st.text_input("BMI", key="bmi")
anatomical_challenges = st.text_area("Anatomical Challenges", height=100, key="anatom_chall")
previous_surgeries = st.text_area("Previous Surgeries", height=100, key="prev_surg")

# --- Pre-Operative Time ---
st.header("Pre-Operative Time")
pre_op_rows = ["System Setup", "Draping Time", "Anesthesia Time", "Port Placement", "Docking Time"]
pre_op_df = pd.DataFrame({
    "Start Time": [""] * 5,
    "End Time": [""] * 5,
    "Total Time": [""] * 5
}, index=pre_op_rows)
edited_pre_op = st.data_editor(pre_op_df, num_rows="fixed", key="preop_editor")

# --- Pre-Operative Steps ---
st.header("Pre-Operative Steps")
st.subheader("1. Port Placement")
port_location = st.text_input("Location", key="port_loc")
distance_from_target = st.text_input("Distance From Target", key="dist_target")
distance_bw_ports = st.text_input("Distance b/w Ports", key="dist_ports")

st.subheader("2. Patient Position")
patient_position = st.text_area("Patient Position (hidden)", height=120, key="patient_pos", label_visibility="collapsed")

st.subheader("3. Cart Position")
cart_height = st.text_input("Height (Vertical Column)", key="cart_height")
cart_position_wrt_port = st.text_area("Position w.r.t Port (describe or sketch)", height=300, key="cart_sketch")

st.subheader("4. Arm Position")
arm_camera = st.text_input("Camera", key="arm_cam")
arm_r1 = st.text_input("R1", key="arm_r1")
arm_r2 = st.text_input("R2", key="arm_r2")

# --- Intra-Operative Time ---
st.header("Intra-Operative Time")
intra_starting = st.text_input("Starting", key="intra_start")
intra_suturing = st.text_input("Suturing", key="intra_sut")
intra_ending = st.text_input("Ending", key="intra_end")
intra_total_duration = st.text_input("Total Duration", key="intra_total")
non_robotic_step = st.text_area("Non-robotic Step", height=100, key="non_robotic")
additional_instruments = st.text_area("Additional advanced (non-robotic) Instruments",height=100,key="add_instru")

# --- System Settings (No Serial No.) ---
st.header("System Settings")
st.subheader("Right Arm Instrument")
right_arm_df = pd.DataFrame({"Type": ["", "", ""], "Uses": ["", "", ""]})
edited_right_arm = st.data_editor(right_arm_df, num_rows="fixed", key="right_instr")

st.subheader("Left Arm Instrument")
left_arm_df = pd.DataFrame({"Type": ["", "", ""], "Uses": ["", "", ""]})
edited_left_arm = st.data_editor(left_arm_df, num_rows="fixed", key="left_instr")

# --- Visualization & Energy ---
st.header("Visualization & Energy")
camera_name = st.text_input("Camera Name", key="cam_name")

col1, col2, col3 = st.columns(3)
telescope_0 = col1.checkbox("0°", key="tel_0")
telescope_30 = col2.checkbox("30°", key="tel_30")
telescope_custom = col3.text_input("_____ mm", placeholder="e.g. 10", key="tel_custom")

esu_monopolar_cut = st.text_input("Monopolar Cut _____ W", key="esu_cut")
esu_monopolar_coag = st.text_input("Monopolar Coag _____ W", key="esu_coag")
esu_bipolar = st.text_input("Bipolar _____ W", key="esu_bip")
ligasure_lvl = st.text_input("Ligasure _____ lvl", key="ligasure")

# --- Observations ---
st.header("Observations")
obs_port_placement = st.text_area("Port Placement", height=100, key="obs_port")
obs_cart_placement = st.text_area("Cart Placement", height=100, key="obs_cart")
obs_arm_collisions = st.text_area("Arm Collisions", height=100, key="obs_collisions")
obs_camera = st.text_area("Camera Observation", height=100, key="obs_cam")
insufflator = st.text_input("Insufflator", key="insuff")
smoke_evacuator = st.text_input("Smoke evacuator", key="smoke")
system_observations = st.text_area("System Observations", height=100, key="sys_obs")
total_blood_loss = st.text_input("Total Blood Loss", key="blood_loss")

# --- Feedback ---
st.header("Surgeon Feedback")
surgeon_feedback = st.text_area("Surgeon Feedback (hidden)", height=100, key="surgeon_fb", label_visibility="collapsed")

st.header("Recommended Actions")
recommended_actions = st.text_area("Recommended Actions (hidden)", height=100, key="recomm_actions", label_visibility="collapsed")

# --- Generate Printable Text Summary ---
def generate_summary():
    # Telescope
    tel_parts = []
    if telescope_0: tel_parts.append("0°")
    if telescope_30: tel_parts.append("30°")
    if telescope_custom.strip(): tel_parts.append(telescope_custom + "mm")
    tel_line = "[x] " + "  [x] ".join(tel_parts) if tel_parts else "[ ] 0°  [ ] 30°  _____ mm"

    # Instrument tables
    right_lines = ""
    for _, row in edited_right_arm.iterrows():
        right_lines += "   " + (row["Type"] or "__________") + "     " + (row["Uses"] or "__________") + "\n"

    left_lines = ""
    for _, row in edited_left_arm.iterrows():
        left_lines += "   " + (row["Type"] or "__________") + "     " + (row["Uses"] or "__________") + "\n"

    blank = "____________________________"
    long_blank = "____________________________________________________________"
    newline = "\n"

    text = (
        "Clinical Trial Summary" + newline + newline +
        "Procedure & Date" + newline +
        "Procedure:" + newline +
        (procedure_manual or long_blank + newline + long_blank + newline + long_blank) + newline + newline +
        "Date (dd-mm-yyyy): " + (date or blank) + newline +
        "Surgeon Name: " + (surgeon_name or blank) + newline +
        "Place: " + (place or blank) + newline + newline +

        "Patient Profile" + newline +
        "Age: " + (age or blank) + newline +
        "Sex: " + ("[x] Female  [ ] Male" if sex == "Female" else "[ ] Female  [x] Male") + newline +
        "BMI: " + (bmi or blank) + newline +
        "Anatomical Challenges:" + newline +
        (anatomical_challenges or long_blank + newline + long_blank) + newline + newline +
        "Previous Surgeries:" + newline +
        (previous_surgeries or long_blank + newline + long_blank) + newline + newline +

        "Pre-Operative Time" + newline +
        edited_pre_op.to_string() + newline + newline +

        "Pre-Operative Steps:" + newline +
        "1. Port Placement" + newline +
        "   Location: " + (port_location or blank) + newline +
        "   Distance From Target: " + (distance_from_target or blank) + newline +
        "   Distance b/w Ports: " + (distance_bw_ports or blank) + newline + newline +
        "2. Patient Position" + newline +
        (patient_position or long_blank + newline + long_blank + newline + long_blank) + newline + newline +
        "3. Cart Position" + newline +
        "   Height (Vertical Column): " + (cart_height or blank) + newline +
        "   Position w.r.t Port" + newline +
        (cart_position_wrt_port or (long_blank + newline) * 25) + newline +
        "4. Arm Position:" + newline +
        "   Camera: " + (arm_camera or blank) + newline +
        "   R1: " + (arm_r1 or blank) + newline +
        "   R2: " + (arm_r2 or blank) + newline + newline +

        "Intra-Operative Time" + newline +
        "Starting: " + (intra_starting or blank) + newline +
        "Suturing: " + (intra_suturing or blank) + newline +
        "Ending: " + (intra_ending or blank) + newline +
        "Total Duration: " + (intra_total_duration or blank) + newline +
        "Non-robotic Step:" + newline +
        (non_robotic_step or long_blank + newline + long_blank) + newline +
        "Additional advanced (non-robotic) Instruments" + newline +
        (additional_instruments or long_blank + newline + long_blank) + newline + newline +

        "System Settings" + newline +
        "Right Arm Instrument" + newline +
        "   Type                           Uses" + newline +
        right_lines +
        "Left Arm Instrument" + newline +
        "   Type                           Uses" + newline +
        left_lines +

        "Visualization & Energy" + newline +
        "Camera Name: " + (camera_name or blank) + newline +
        "Telescope: " + tel_line + newline +
        "ESU: Monopolar Cut     " + (esu_monopolar_cut or "_____") + " W" + newline +
        "     Monopolar Coag    " + (esu_monopolar_coag or "_____") + " W" + newline +
        "     Bipolar           " + (esu_bipolar or "_____") + " W" + newline +
        "     Ligasure          " + (ligasure_lvl or "_____") + " lvl" + newline + newline +

        "Observations" + newline +
        "Port Placement" + newline +
        (obs_port_placement or (long_blank + newline) * 6) +
        "Cart Placement" + newline +
        (obs_cart_placement or (long_blank + newline) * 6) +
        "Arm Collisions:" + newline +
        (obs_arm_collisions or (long_blank + newline) * 6) +
        "Camera Observation:" + newline +
        (obs_camera or (long_blank + newline) * 6) +
        "Insufflator: " + (insufflator or blank) + newline +
        "Smoke evacuator: " + (smoke_evacuator or blank) + newline +
        "System Observations:" + newline +
        (system_observations or (long_blank + newline) * 10) +
        "Total Blood Loss: " + (total_blood_loss or blank) + newline + newline +

        "Surgeon Feedback" + newline +
        (surgeon_feedback or (long_blank + newline) * 12) + newline + newline +

        "Recommended Actions:" + newline +
        (recommended_actions or (long_blank + newline) * 15)
    )
    return text

# --- Export ---
st.markdown("---")
st.header("Export Summary")

if st.checkbox("Preview the printable summary"):
    st.text_area("Preview", generate_summary(), height=700, key="preview_area")

st.download_button(
    label="Download as Text File (Ready to Print)",
    data=generate_summary(),
    file_name="Meril_Clinical_Trial_Summary.txt",
    mime="text/plain"
)

