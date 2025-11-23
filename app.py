import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import os  # 파일 저장을 위해 필요한 도구

# 1. Page Configuration
st.set_page_config(page_title="PETRONAS FLNG Manager", layout="wide")

# --- Data Persistence Logic (데이터 영구 저장) ---
EQUIPMENT_FILE = 'equipment_data.csv'
TASK_FILE = 'task_data.csv'

def load_data():
    """앱 시작 시 파일에서 데이터를 불러옵니다."""
    # 1. Equipment DB Load
    if 'equipment_db' not in st.session_state:
        if os.path.exists(EQUIPMENT_FILE):
            st.session_state.equipment_db = pd.read_csv(EQUIPMENT_FILE)
            # 날짜 컬럼 형변환 (String -> String 유지하거나 필요시 변경)
            st.session_state.equipment_db['DAC'] = st.session_state.equipment_db['DAC'].astype(str)
            st.session_state.equipment_db['SMCC'] = st.session_state.equipment_db['SMCC'].astype(str)
        else:
            # 파일이 없으면 초기 샘플 데이터 생성
            data = {
                'Tag No': ['P-101A', 'P-101B', 'K-201', 'V-305'],
                'Equipment Name': ['Feed Water Pump A', 'Feed Water Pump B', 'Gas Compressor', 'Separator Vessel'],
                'Sub-System': ['SS-01', 'SS-01', 'SS-05', 'SS-09'],
                'PO No': ['PO-9981', 'PO-9981', 'PO-5521', 'PO-1102'],
                'Module': ['M10', 'M10', 'M12', 'M15'],
                'Deck': ['Main Deck', 'Main Deck', 'Upper Deck', 'Cellar Deck'],
                'DAC': ['2023-11-30', '2023-12-05', '2023-12-10', '2024-01-15'],
                'SMCC': ['2024-02-01', '2024-02-01', '2024-03-15', '2024-04-20']
            }
            st.session_state.equipment_db = pd.DataFrame(data)
            # 초기 데이터 파일로 저장
            st.session_state.equipment_db.to_csv(EQUIPMENT_FILE, index=False)

    # 2. Task DB Load
    if 'task_db' not in st.session_state:
        if os.path.exists(TASK_FILE):
            st.session_state.task_db = pd.read_csv(TASK_FILE)
        else:
            # 파일이 없으면 초기 샘플 데이터 생성
            task_data = {
                'ID': [1, 2, 3],
                'Tag No': ['P-101A', 'K-201', 'V-305'],
                'Title': ['Vibration Issue', 'Alignment Check', 'Painting Defect'],
                'Work Type': ['Test Run / Commissioning', 'Installation Check', 'Punch List (Defect)'],
                'MER No': ['MER-001', 'MER-002', 'MER-005'],
                'Description': ['High vibration observed at DE.', 'Coupling alignment required.', 'Touch-up required on shell.'],
                'Status': ['Ongoing', 'Completed', 'Before Start'],
                'Created Date': ['2023-11-20', '2023-11-21', '2023-11-23'],
                'Due Date': ['2023-11-25', '2023-11-22', '2023-11-30']
            }
            st.session_state.task_db = pd.DataFrame(task_data)
            # 초기 데이터 파일로 저장
            st.session_state.task_db.to_csv(TASK_FILE, index=False)

def save_data():
    """데이터가 변경될 때마다 파일에 저장합니다."""
    if 'equipment_db' in st.session_state:
        st.session_state.equipment_db.to_csv(EQUIPMENT_FILE, index=False)
    if 'task_db' in st.session_state:
        st.session_state.task_db.to_csv(TASK_FILE, index=False)

# 앱 실행 시 데이터 불러오기
load_data()

# --- Custom CSS (Login & Layout) ---
def local_css():
    st.markdown("""
    <style>
    /* Login Buttons (Admin/Shared) */
    div.stHorizontalBlock div.stButton > button {
        width: 300px !important;  
        height: 200px !important; 
        border: none;
        border-radius: 20px;
        color: black !important; 
        font-size: 32px !important; 
        font-weight: 900 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0 auto; 
    }
    div.stHorizontalBlock div.stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"]:nth-of-type(1) div.stButton > button {
        background: linear-gradient(135deg, #007bff 0%, #80bdff 100%);
    }
    div[data-testid="column"]:nth-of-type(2) div[data-testid="stHorizontalBlock"]:nth-of-type(2) div.stButton > button {
        background: linear-gradient(135deg, #28a745 0%, #85e0a3 100%);
    }
    /* Reset Form Button */
    div[data-testid="stForm"] div.stButton > button {
        width: auto !important; height: auto !important; font-size: 16px !important;
        background: #f0f2f6 !important; color: black !important; box-shadow: none !important;
        margin: 0 !important; transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Authentication ---
if 'role' not in st.session_state: st.session_state.role = None
if 'admin_login_step' not in st.session_state: st.session_state.admin_login_step = False

def login():
    local_css()
    st.markdown("<br><br><h1 style='text-align: center; font-size: 50px;'>PETRONAS FLNG</h1><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.session_state.admin_login_step:
            c_a, c_b = st.columns([1, 1])
            with c_a: st.button("Admin Only")
            with c_b:
                st.write("<br><br><br>", unsafe_allow_html=True)
                with st.form("admin_form"):
                    st.write("**Enter Password:**")
                    pwd = st.text_input("Password", type="password", label_visibility="collapsed")
                    if st.form_submit_button("Login"):
                        if pwd == "5241":
                            st.session_state.role = "Admin"
                            st.success("Success!"); time.sleep(0.5); st.rerun()
                        else: st.error("Incorrect Password!")
        else:
            c_x = st.columns([1])
            if c_x[0].button("Admin Only"):
                st.session_state.admin_login_step = True; st.rerun()
        
        st.write("")
        c_y = st.columns([1])
        if c_y[0].button("Shared User"):
            st.session_state.role = "Guest"; st.session_state.admin_login_step = False; st.rerun()

def logout():
    st.session_state.role = None; st.session_state.admin_login_step = False; st.rerun()

if st.session_state.role is None:
    login(); st.stop()

# --- Main App Logic ---

# Sidebar
st.sidebar.title(f"🔧 Menu ({st.session_state.role})")
menu_options = ["Dashboard", "Equipment Log", "Register Data", "Task Management", "Search"]
if st.session_state.role == "Guest":
    pass 

choice = st.sidebar.radio("Navigation", menu_options)
st.sidebar.markdown("---"); 
if st.sidebar.button("Log out"): logout()

# --- 1. Dashboard ---
if choice == "Dashboard":
    st.title("📊 Project Dashboard")
    st.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Prepare Data
    eq_df = st.session_state.equipment_db
    task_df = st.session_state.task_db
    
    # 1. Sub System Status (Sorted by DAC)
    st.subheader("1. Sub System Status (Imminent DAC)")
    if not eq_df.empty:
        eq_df['DAC_Date'] = pd.to_datetime(eq_df['DAC'], errors='coerce')
        sorted_eq = eq_df.sort_values(by='DAC_Date').head(5)
        for i, row in sorted_eq.iterrows():
            st.info(f"📅 **{row['DAC']}** | Sub-System: **{row['Sub-System']}** (Tag: {row['Tag No']})")
    
    # Task Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Ongoing Tasks")
        ongoing = task_df[task_df['Status'] == 'Ongoing']
        if not ongoing.empty:
            for i, row in ongoing.iterrows():
                st.write(f"▶️ {row['Title']} ({row['Tag No']})")
        else:
            st.write("No ongoing tasks.")
            
        st.subheader("4. This Week Tasks")
        today = datetime.now()
        next_week = today + timedelta(days=7)
        task_df['Due_Date_Dt'] = pd.to_datetime(task_df['Due Date'], errors='coerce')
        
        this_week = task_df[(task_df['Due_Date_Dt'] >= today) & (task_df['Due_Date_Dt'] <= next_week)]
        if not this_week.empty:
            for i, row in this_week.iterrows():
                st.warning(f"⏳ **{row['Due Date']}** | {row['Title']} ({row['Tag No']})")
        else:
            st.write("No tasks due this week.")
            
        st.subheader("6. Open Issues (New)")
        task_df['Created_Date_Dt'] = pd.to_datetime(task_df['Created Date'], errors='coerce')
        recent = task_df[task_df['Created_Date_Dt'] >= (today - timedelta(days=7))]
        if not recent.empty:
            for i, row in recent.iterrows():
                st.write(f"🆕 {row['Title']} ({row['Tag No']})")
    
    with col2:
        st.subheader("3. Urgent Work")
        urgent = task_df[task_df['Work Type'].str.contains("Punch List", na=False)]
        if not urgent.empty:
            for i, row in urgent.iterrows():
                st.error(f"🚨 {row['Title']} ({row['Tag No']})")
        
        st.subheader("5. Backlog Issues")
        backlog = task_df[(task_df['Status'] != 'Completed') & (task_df['Due_Date_Dt'] < today)]
        if not backlog.empty:
            for i, row in backlog.iterrows():
                st.error(f"⚠️ Overdue: {row['Title']} ({row['Tag No']})")
        else:
            st.success("No backlog items!")

# --- 2. Equipment Log ---
elif choice == "Equipment Log":
    st.title("🗂️ Equipment Log")
    
    tab1, tab2, tab3 = st.tabs(["View Log", "Add Manual Entry", "Upload Excel"])
    
    with tab1:
        st.dataframe(st.session_state.equipment_db, use_container_width=True)
    
    with tab2:
        if st.session_state.role == "Admin":
            with st.form("add_eq_manual"):
                c1, c2 = st.columns(2)
                tag = c1.text_input("Tag No")
                name = c2.text_input("Equipment Name")
                ss = c1.text_input("Sub-System")
                po = c2.text_input("PO No")
                mod = c1.text_input("Module")
                deck = c2.text_input("Deck")
                dac = c1.date_input("DAC Date")
                smcc = c2.date_input("SMCC Date")
                
                if st.form_submit_button("Add Equipment"):
                    new_row = pd.DataFrame([{
                        'Tag No': tag, 'Equipment Name': name, 'Sub-System': ss,
                        'PO No': po, 'Module': mod, 'Deck': deck, 
                        'DAC': str(dac), 'SMCC': str(smcc)
                    }])
                    st.session_state.equipment_db = pd.concat([st.session_state.equipment_db, new_row], ignore_index=True)
                    # SAVE DATA
                    save_data()
                    st.success("Added Successfully!")
                    st.rerun()
        else:
            st.warning("Admin access required to add data.")
            
    with tab3:
        if st.session_state.role == "Admin":
            uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'])
            st.info("Required Columns: Tag No, Equipment Name, Sub-System, PO No, Module, Deck, DAC, SMCC")
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.write("Preview:", df.head())
                    if st.button("Merge to Database"):
                        # Ensure columns match to prevent errors
                        st.session_state.equipment_db = pd.concat([st.session_state.equipment_db, df], ignore_index=True)
                        # SAVE DATA
                        save_data()
                        st.success("Data Merged!")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        else:
            st.warning("Admin access required to upload data.")

# --- 3. Register Data ---
elif choice == "Register Data":
    st.title("📝 Register New Task / Issue")
    
    if st.session_state.role != "Admin":
        st.error("Access Denied. Admin only.")
    else:
        # Select Tag
        eq_list = st.session_state.equipment_db['Tag No'].unique().tolist()
        if not eq_list:
            st.warning("No Equipment Found. Please add equipment in 'Equipment Log' first.")
        else:
            selected_tag = st.selectbox("Select Tag No", eq_list)
            related_rows = st.session_state.equipment_db[st.session_state.equipment_db['Tag No'] == selected_tag]
            related_names = related_rows['Equipment Name'].unique().tolist()
            selected_name = st.selectbox("Equipment Name", related_names)
            
            # Show Info
            if not related_rows.empty:
                info_row = related_rows[related_rows['Equipment Name'] == selected_name].iloc[0]
                st.caption(f"ℹ️ Info: {info_row['Sub-System']} | {info_row['Module']} | {info_row['Deck']}")

            with st.form("register_task_form"):
                c1, c2 = st.columns(2)
                work_type = c1.selectbox("Work Type", ["Installation Check", "Punch List (Defect)", "Test Run / Commissioning", "Routine Inspection"])
                mer_no = c2.text_input("MER No.")
                desc = st.text_area("Description / Issues Found")
                
                st.write("---")
                st.write("**📷 Evidence Upload**")
                cam_pic = st.camera_input("Take a Photo")
                file_pic = st.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
                draw_file = st.file_uploader("Upload Drawing", type=['pdf'])
                
                if st.form_submit_button("Register Task"):
                    new_id = len(st.session_state.task_db) + 1
                    today_str = datetime.now().strftime('%Y-%m-%d')
                    due_str = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d') 
                    
                    new_task = pd.DataFrame([{
                        'ID': new_id,
                        'Tag No': selected_tag,
                        'Title': f"{work_type} - {mer_no}",
                        'Work Type': work_type,
                        'MER No': mer_no,
                        'Description': desc,
                        'Status': 'Before Start',
                        'Created Date': today_str,
                        'Due Date': due_str
                    }])
                    
                    st.session_state.task_db = pd.concat([st.session_state.task_db, new_task], ignore_index=True)
                    # SAVE DATA
                    save_data()
                    st.success(f"Task #{new_id} Registered Successfully!")

# --- 4. Task Management ---
elif choice == "Task Management":
    st.title("✅ Task Management")
    
    st.subheader("All Registered Tasks")
    st.dataframe(st.session_state.task_db, use_container_width=True)
    st.write("---")
    
    st.subheader("Update Task Status")
    task_ids = st.session_state.task_db['ID'].tolist()
    
    if not task_ids:
        st.info("No tasks to manage.")
    else:
        selected_id = st.selectbox("Select Task ID to Manage", task_ids)
        if selected_id:
            current_task = st.session_state.task_db[st.session_state.task_db['ID'] == selected_id].iloc[0]
            st.write(f"**Target:** {current_task['Tag No']} - {current_task['Title']}")
            st.write(f"**Current Status:** {current_task['Status']}")
            
            with st.form("update_task"):
                c1, c2 = st.columns(2)
                new_status = c1.selectbox("Update Status", ["Before Start", "Ongoing", "Completed"])
                completion_report = c2.file_uploader("Upload Completion Report", type=['pdf', 'docx', 'xlsx'])
                update_desc = st.text_area("Add Update Notes / Remarks")
                
                if st.form_submit_button("Update Task"):
                    idx = st.session_state.task_db[st.session_state.task_db['ID'] == selected_id].index[0]
                    st.session_state.task_db.at[idx, 'Status'] = new_status
                    # SAVE DATA
                    save_data()
                    st.success(f"Task #{selected_id} updated to '{new_status}'!")
                    st.rerun()

# --- 5. Search ---
elif choice == "Search":
    st.title("🔍 Advanced Search")
    
    col1, col2 = st.columns(2)
    search_txt = col1.text_input("Global Search (Tag, Name, PO, MER)")
    filter_type = col2.selectbox("Filter by Work Type", ["All"] + st.session_state.task_db['Work Type'].unique().tolist() if not st.session_state.task_db.empty else ["All"])
    
    st.write("---")
    
    results = st.session_state.task_db.copy()
    if not results.empty:
        if search_txt:
            mask = results.astype(str).apply(lambda x: x.str.contains(search_txt, case=False, na=False)).any(axis=1)
            results = results[mask]
        if filter_type != "All":
            results = results[results['Work Type'] == filter_type]
            
        st.subheader(f"Search Results ({len(results)})")
        if not results.empty:
            st.dataframe(results, use_container_width=True)
            for i, row in results.iterrows():
                with st.expander(f"📄 Detail: {row['Tag No']} - {row['Title']}"):
                    st.write(f"**Status:** {row['Status']}")
                    st.write(f"**MER No:** {row['MER No']}")
                    st.write(f"**Description:** {row['Description']}")
                    st.write(f"**Dates:** Created {row['Created Date']} | Due {row['Due Date']}")
        else:
            st.info("No matching records found.")
    else:
        st.info("No tasks data available.")