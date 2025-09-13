import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional
import uuid

# Configure Streamlit page
st.set_page_config(
    page_title="WorkFlow Hub - Universal Team Management",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'dashboard'

if 'departments' not in st.session_state:
    st.session_state.departments = [
        {"id": "1", "name": "Operations", "description": "Day-to-day operations and management", "color": "blue"},
        {"id": "2", "name": "Production", "description": "Manufacturing and production activities", "color": "green"},
        {"id": "3", "name": "Quality Control", "description": "Quality assurance and testing", "color": "purple"},
        {"id": "4", "name": "Safety", "description": "Workplace safety and compliance", "color": "red"},
        {"id": "5", "name": "Logistics", "description": "Supply chain and warehouse", "color": "orange"},
    ]

if 'team_members' not in st.session_state:
    st.session_state.team_members = [
        {
            "id": "1", "name": "Sarah Johnson", "role": "Operations Manager", "department": "Operations",
            "email": "sarah.johnson@company.com", "level": 5, "status": "active",
            "skills": ["Leadership", "Process Management", "Quality Control"], "completion_rate": 95
        },
        {
            "id": "2", "name": "Mike Davis", "role": "Senior Technician", "department": "Production",
            "email": "mike.davis@company.com", "level": 3, "status": "active",
            "skills": ["Machine Operation", "Troubleshooting", "Training"], "completion_rate": 72
        },
        {
            "id": "3", "name": "Lisa Chen", "role": "Quality Inspector", "department": "Quality Control",
            "email": "lisa.chen@company.com", "level": 3, "status": "active",
            "skills": ["Quality Testing", "Documentation", "Analysis"], "completion_rate": 98
        },
        {
            "id": "4", "name": "John Smith", "role": "Team Lead", "department": "Production",
            "email": "john.smith@company.com", "level": 4, "status": "busy",
            "skills": ["Team Management", "Production Planning", "Safety"], "completion_rate": 85
        },
        {
            "id": "5", "name": "Emma Brown", "role": "Safety Coordinator", "department": "Safety",
            "email": "emma.brown@company.com", "level": 4, "status": "active",
            "skills": ["Safety Protocols", "Training", "Compliance"], "completion_rate": 91
        },
        {
            "id": "6", "name": "Tom Wilson", "role": "Technician", "department": "Production",
            "email": "tom.wilson@company.com", "level": 2, "status": "offline",
            "skills": ["Equipment Maintenance", "Basic Repairs"], "completion_rate": 78
        }
    ]

if 'reminders' not in st.session_state:
    st.session_state.reminders = [
        {
            "id": "1", "title": "Weekly Team Meeting", "description": "Mandatory team meeting to discuss project updates",
            "assigned_to": ["Sarah Johnson", "Mike Davis", "Lisa Chen"], "due_date": "2024-12-13",
            "due_time": "14:00", "priority": "high", "status": "active", "type": "meeting",
            "created_date": "2024-12-10", "responses": 2
        },
        {
            "id": "2", "title": "Equipment Maintenance Check", "description": "Monthly maintenance check for production equipment",
            "assigned_to": ["Mike Davis", "Tom Wilson"], "due_date": "2024-12-14",
            "due_time": "09:00", "priority": "medium", "status": "active", "type": "maintenance",
            "created_date": "2024-12-09", "responses": 0
        },
        {
            "id": "3", "title": "Safety Training Completion", "description": "Complete mandatory safety training module",
            "assigned_to": ["All Workers"], "due_date": "2024-12-20",
            "due_time": "17:00", "priority": "high", "status": "active", "type": "training",
            "created_date": "2024-12-08", "responses": 15
        }
    ]

if 'workflows' not in st.session_state:
    st.session_state.workflows = [
        {
            "id": "1", "name": "New Employee Onboarding", "description": "Complete onboarding process for new team members",
            "category": "HR", "is_active": True, "trigger": "manual", "steps": 3,
            "created_at": "2024-12-01", "last_used": "2024-12-10"
        },
        {
            "id": "2", "name": "Quality Control Process", "description": "Standard quality control workflow for production items",
            "category": "Quality", "is_active": True, "trigger": "event", "steps": 2,
            "created_at": "2024-11-15", "last_used": "2024-12-12"
        },
        {
            "id": "3", "name": "Equipment Maintenance", "description": "Scheduled maintenance workflow for critical equipment",
            "category": "Maintenance", "is_active": True, "trigger": "scheduled", "steps": 3,
            "created_at": "2024-11-20", "last_used": "2024-12-11"
        }
    ]

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your AI management assistant. I can help you with worker management, scheduling reminders, analyzing team performance, and providing insights. How can I assist you today?"
        }
    ]

def main():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #030213 0%, #1a1a2e 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.625rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.625rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .status-active { color: #10b981; }
    .status-offline { color: #6b7280; }
    .status-busy { color: #f59e0b; }
    .priority-high { color: #ef4444; }
    .priority-medium { color: #f59e0b; }
    .priority-low { color: #6b7280; }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🏢 WorkFlow Hub")
        st.markdown("*Universal Team Management*")
        st.markdown("---")
        
        # Main navigation
        st.markdown("**Main**")
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.active_tab = 'dashboard'
        if st.button("👥 Team Members", use_container_width=True):
            st.session_state.active_tab = 'workers'
        if st.button("🔔 Reminders", use_container_width=True):
            st.session_state.active_tab = 'reminders'
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.session_state.active_tab = 'chat'
        
        st.markdown("---")
        st.markdown("**Organization**")
        if st.button("🏢 Organization Setup", use_container_width=True):
            st.session_state.active_tab = 'organization-setup'
        if st.button("🌐 Team Connections", use_container_width=True):
            st.session_state.active_tab = 'team-connections'
        if st.button("⚙️ Workflow Builder", use_container_width=True):
            st.session_state.active_tab = 'workflow-builder'
        
        st.markdown("---")
        if st.button("🛠️ Settings", use_container_width=True):
            st.session_state.active_tab = 'settings'
        
        st.markdown("---")
        if st.button("➕ New Reminder", use_container_width=True, type="primary"):
            st.session_state.active_tab = 'create-reminder'

    # Main content area
    if st.session_state.active_tab == 'dashboard':
        show_dashboard()
    elif st.session_state.active_tab == 'workers':
        show_workers()
    elif st.session_state.active_tab == 'reminders':
        show_reminders()
    elif st.session_state.active_tab == 'chat':
        show_ai_chat()
    elif st.session_state.active_tab == 'create-reminder':
        show_create_reminder()
    elif st.session_state.active_tab == 'organization-setup':
        show_organization_setup()
    elif st.session_state.active_tab == 'team-connections':
        show_team_connections()
    elif st.session_state.active_tab == 'workflow-builder':
        show_workflow_builder()
    elif st.session_state.active_tab == 'settings':
        show_settings()

def show_dashboard():
    st.markdown('<div class="main-header"><h1>📊 Dashboard</h1><p>Overview of your team and reminders</p></div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Workers",
            value=len(st.session_state.team_members),
            delta="2 new this month"
        )
    
    with col2:
        active_reminders = len([r for r in st.session_state.reminders if r['status'] == 'active'])
        st.metric(
            label="🔔 Active Reminders",
            value=active_reminders,
            delta="3 due today"
        )
    
    with col3:
        completed_today = 8
        st.metric(
            label="✅ Completed Today",
            value=completed_today,
            delta="↗️ +2 from yesterday"
        )
    
    with col4:
        pending_tasks = 4
        st.metric(
            label="⏳ Pending",
            value=pending_tasks,
            delta="↘️ -1 from yesterday"
        )
    
    st.markdown("---")
    
    # Charts and analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Team Performance")
        
        # Create performance chart
        members_df = pd.DataFrame(st.session_state.team_members)
        fig = px.bar(
            members_df, 
            x='name', 
            y='completion_rate',
            title='Completion Rates by Team Member',
            color='completion_rate',
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Department Distribution")
        
        # Department pie chart
        dept_counts = members_df['department'].value_counts()
        fig = px.pie(
            values=dept_counts.values,
            names=dept_counts.index,
            title='Team Members by Department'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    
    activities = [
        {"worker": "John Smith", "action": "Completed safety training reminder", "time": "2 hours ago", "status": "completed"},
        {"worker": "Sarah Johnson", "action": "Acknowledged equipment check", "time": "4 hours ago", "status": "completed"},
        {"worker": "Mike Davis", "action": "Missed meeting reminder", "time": "6 hours ago", "status": "missed"},
        {"worker": "Lisa Chen", "action": "Submitted timesheet", "time": "8 hours ago", "status": "completed"},
    ]
    
    for activity in activities:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                st.write(f"**{activity['worker']}**")
            with col2:
                st.write(activity['action'])
            with col3:
                status_color = "🟢" if activity['status'] == 'completed' else "🔴"
                st.write(f"{status_color} {activity['time']}")

def show_workers():
    st.markdown('<div class="main-header"><h1>👥 Team Members</h1><p>Manage your team members and track their progress</p></div>', unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search workers...", placeholder="Enter name or role")
    with col2:
        department_filter = st.selectbox("Department", ["All"] + list(set([m['department'] for m in st.session_state.team_members])))
    with col3:
        if st.button("➕ Add Worker", type="primary"):
            st.session_state.show_add_worker = True
    
    # Filter workers
    filtered_members = st.session_state.team_members
    if search_term:
        filtered_members = [m for m in filtered_members if search_term.lower() in m['name'].lower() or search_term.lower() in m['role'].lower()]
    if department_filter != "All":
        filtered_members = [m for m in filtered_members if m['department'] == department_filter]
    
    # Display workers in a grid
    cols = st.columns(3)
    for i, member in enumerate(filtered_members):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"### {member['name']}")
                st.markdown(f"**{member['role']}**")
                st.markdown(f"📧 {member['email']}")
                st.markdown(f"🏢 {member['department']}")
                
                # Status indicator
                status_colors = {"active": "🟢", "offline": "⚪", "busy": "🟡"}
                st.markdown(f"Status: {status_colors.get(member['status'], '🟢')} {member['status'].title()}")
                
                # Completion rate
                st.progress(member['completion_rate'] / 100)
                st.markdown(f"Completion Rate: {member['completion_rate']}%")
                
                # Skills
                st.markdown("**Skills:**")
                for skill in member['skills']:
                    st.markdown(f"• {skill}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"✉️ Email", key=f"email_{member['id']}")
                with col2:
                    st.button(f"📞 Call", key=f"call_{member['id']}")
                
                st.markdown("---")

def show_reminders():
    st.markdown('<div class="main-header"><h1>🔔 Reminders</h1><p>Manage and track all worker reminders</p></div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search reminders...", placeholder="Enter title or description")
    with col2:
        status_filter = st.selectbox("Status", ["All", "active", "completed", "overdue"])
    with col3:
        if st.button("➕ Create Reminder", type="primary"):
            st.session_state.active_tab = 'create-reminder'
    
    # Filter reminders
    filtered_reminders = st.session_state.reminders
    if search_term:
        filtered_reminders = [r for r in filtered_reminders if search_term.lower() in r['title'].lower()]
    if status_filter != "All":
        filtered_reminders = [r for r in filtered_reminders if r['status'] == status_filter]
    
    # Display reminders
    for reminder in filtered_reminders:
        with st.expander(f"{reminder['title']} - {reminder['priority'].title()} Priority"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {reminder['description']}")
                st.markdown(f"**Type:** {reminder['type'].title()}")
                st.markdown(f"**Due:** {reminder['due_date']} at {reminder['due_time']}")
                st.markdown(f"**Assigned to:** {', '.join(reminder['assigned_to'])}")
                
            with col2:
                priority_colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                st.markdown(f"**Priority:** {priority_colors.get(reminder['priority'], '🟢')} {reminder['priority'].title()}")
                st.markdown(f"**Status:** {reminder['status'].title()}")
                st.markdown(f"**Responses:** {reminder['responses']}")
                
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    st.button("✏️ Edit", key=f"edit_{reminder['id']}")
                with col2_btn:
                    st.button("🗑️ Delete", key=f"delete_{reminder['id']}")

def show_ai_chat():
    st.markdown('<div class="main-header"><h1>🤖 AI Assistant</h1><p>Get intelligent insights and assistance for team management</p></div>', unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_actions = [
        ("📊 Performance Review", "Show me team performance analytics"),
        ("👥 Team Insights", "Analyze team collaboration patterns"),
        ("📅 Schedule Helper", "Help me find optimal meeting times"),
        ("⚙️ Workflow Optimizer", "Help me optimize our organizational workflows")
    ]
    
    for i, (label, action) in enumerate(quick_actions):
        with [col1, col2, col3, col4][i]:
            if st.button(label, use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": action})
                # Generate AI response
                response = generate_ai_response(action)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("💬 Chat")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI Assistant:** {message['content']}")
        st.markdown("---")
    
    # Chat input
    with st.form("chat_form"):
        user_input = st.text_area("Ask me anything about team management...", height=100)
        submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            response = generate_ai_response(user_input)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()

def generate_ai_response(user_input: str) -> str:
    """Generate AI response based on user input"""
    input_lower = user_input.lower()
    
    if "performance" in input_lower or "analytics" in input_lower:
        return """📊 **Performance Summary:**
• Overall completion rate: 85%
• Most active worker: Lisa Chen (98% completion)
• Needs attention: Mike Davis (72% completion)
• Average response time: 2.3 hours

🎯 **Recommendations:**
• Schedule a check-in with Mike Davis
• Consider recognizing Lisa Chen's excellent performance
• Team meeting efficiency could be improved by 15%"""
    
    elif "workflow" in input_lower or "optimize" in input_lower:
        return """🔄 **Workflow Analysis:**
• Your organization has 3 active workflows
• Average completion time: 2.5 days
• Most efficient: Quality Control Process (95% completion rate)
• Needs improvement: Equipment Maintenance (delays in step 2)

💡 **Recommendations:**
• Consider adding automated notifications
• Set up parallel approval processes
• Create role-specific templates
• Add escalation rules for overdue items"""
    
    elif "schedule" in input_lower or "meeting" in input_lower:
        return """📅 **Optimal Times Based on Team Availability:**
• Tuesday 2-3 PM (100% availability)
• Wednesday 10-11 AM (95% availability)
• Thursday 3-4 PM (90% availability)

⏰ **Tips:**
• Avoid Monday mornings and Friday afternoons
• 30-45 minutes is ideal for team meetings
• Send agenda 24 hours in advance
• Include dial-in options for remote workers"""
    
    else:
        return """🎯 **What I can do:**
• Analyze team performance and productivity
• Suggest optimal reminder timing and content
• Help with scheduling and resource allocation
• Provide insights on worker engagement
• Draft professional communications
• Optimize organizational workflows
• Design team connection strategies
• Create custom role hierarchies

What specific area would you like to focus on?"""

def show_create_reminder():
    st.markdown('<div class="main-header"><h1>➕ Create New Reminder</h1><p>Send reminders and tasks to your team members</p></div>', unsafe_allow_html=True)
    
    with st.form("create_reminder_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Reminder Details")
            title = st.text_input("Title *", placeholder="e.g., Weekly Team Meeting")
            description = st.text_area("Description", placeholder="Provide additional details...")
            
            col1_inner, col2_inner = st.columns(2)
            with col1_inner:
                priority = st.selectbox("Priority *", ["low", "medium", "high"])
            with col2_inner:
                reminder_type = st.selectbox("Type *", ["meeting", "task", "training", "maintenance", "safety", "administrative", "review"])
        
        with col2:
            st.subheader("Scheduling")
            col1_inner, col2_inner = st.columns(2)
            with col1_inner:
                due_date = st.date_input("Due Date *")
            with col2_inner:
                due_time = st.time_input("Due Time *")
            
            is_recurring = st.checkbox("Make this a recurring reminder")
            if is_recurring:
                recurring_type = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
        
        st.subheader("Assign Workers")
        
        # Multi-select for workers
        worker_names = [member['name'] for member in st.session_state.team_members]
        selected_workers = st.multiselect("Select Team Members", worker_names)
        
        if st.checkbox("Select All"):
            selected_workers = worker_names
        
        submitted = st.form_submit_button("Send Reminder", type="primary")
        
        if submitted and title and priority and reminder_type and due_date and due_time and selected_workers:
            new_reminder = {
                "id": str(uuid.uuid4()),
                "title": title,
                "description": description,
                "assigned_to": selected_workers,
                "due_date": due_date.strftime("%Y-%m-%d"),
                "due_time": due_time.strftime("%H:%M"),
                "priority": priority,
                "status": "active",
                "type": reminder_type,
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "responses": 0
            }
            
            st.session_state.reminders.append(new_reminder)
            st.success("Reminder created successfully!")
            st.session_state.active_tab = 'reminders'
            st.rerun()

def show_organization_setup():
    st.markdown('<div class="main-header"><h1>🏢 Organization Setup</h1><p>Configure your organizational structure, roles, and relationships</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Departments", "Roles", "Templates"])
    
    with tab1:
        st.subheader("Departments")
        
        # Add new department
        with st.expander("➕ Add New Department"):
            with st.form("add_department"):
                col1, col2 = st.columns(2)
                with col1:
                    dept_name = st.text_input("Department Name")
                    dept_desc = st.text_area("Description")
                with col2:
                    dept_color = st.selectbox("Color", ["blue", "green", "purple", "red", "orange"])
                
                if st.form_submit_button("Add Department"):
                    if dept_name:
                        new_dept = {
                            "id": str(uuid.uuid4()),
                            "name": dept_name,
                            "description": dept_desc,
                            "color": dept_color
                        }
                        st.session_state.departments.append(new_dept)
                        st.success(f"Department '{dept_name}' added successfully!")
                        st.rerun()
        
        # Display departments
        for dept in st.session_state.departments:
            with st.container():
                col1, col2, col3 = st.columns([2, 3, 1])
                with col1:
                    st.markdown(f"### {dept['name']}")
                    st.markdown(f"Color: {dept['color']}")
                with col2:
                    st.markdown(f"**Description:** {dept['description']}")
                    member_count = len([m for m in st.session_state.team_members if m['department'] == dept['name']])
                    st.markdown(f"**Members:** {member_count}")
                with col3:
                    st.button("✏️ Edit", key=f"edit_dept_{dept['id']}")
                    st.button("🗑️ Delete", key=f"delete_dept_{dept['id']}")
                st.markdown("---")
    
    with tab2:
        st.subheader("Roles & Permissions")
        st.info("Role management functionality - define custom roles, authority levels, and permissions for your organization.")
        
        # Display current roles from team members
        roles = list(set([member['role'] for member in st.session_state.team_members]))
        for role in roles:
            with st.expander(f"Role: {role}"):
                members_with_role = [m for m in st.session_state.team_members if m['role'] == role]
                st.write(f"**Members with this role:** {len(members_with_role)}")
                for member in members_with_role:
                    st.write(f"• {member['name']} ({member['department']})")
    
    with tab3:
        st.subheader("Industry Templates")
        st.write("Quick start with pre-configured organizational structures for common industries.")
        
        templates = [
            {"name": "Healthcare", "departments": ["Emergency", "Surgery", "Nursing", "Administration", "Laboratory"]},
            {"name": "Construction", "departments": ["Project Management", "Site Operations", "Safety", "Quality", "Equipment"]},
            {"name": "Retail", "departments": ["Sales", "Customer Service", "Inventory", "Management", "Marketing"]},
            {"name": "Education", "departments": ["Academic", "Administration", "Student Services", "Facilities", "Technology"]},
            {"name": "Software Development", "departments": ["Engineering", "Product", "Design", "QA", "DevOps"]}
        ]
        
        for template in templates:
            with st.expander(f"{template['name']} Template"):
                st.write(f"**Departments:** {', '.join(template['departments'])}")
                if st.button(f"Apply {template['name']} Template", key=f"template_{template['name']}"):
                    # Apply template logic here
                    st.success(f"{template['name']} template applied!")

def show_team_connections():
    st.markdown('<div class="main-header"><h1>🌐 Team Connections</h1><p>Visualize and manage relationships within your organization</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Network View", "Team Members", "Connections"])
    
    with tab1:
        st.subheader("Organization Network")
        
        # Create a simple network visualization using plotly
        members_df = pd.DataFrame(st.session_state.team_members)
        
        # Department-based network
        fig = px.scatter(
            members_df, 
            x='level', 
            y='completion_rate',
            color='department',
            size='level',
            hover_data=['name', 'role'],
            title='Team Network by Department and Performance'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Connection legend
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🔵 **Reports To**")
        with col2:
            st.markdown("🟢 **Collaborates With**")
        with col3:
            st.markdown("🟠 **Mentors**")
    
    with tab2:
        st.subheader("Team Member Details")
        
        for member in st.session_state.team_members:
            with st.expander(f"{member['name']} - {member['role']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Department:** {member['department']}")
                    st.write(f"**Level:** {member['level']}")
                    st.write(f"**Status:** {member['status']}")
                    st.write(f"**Email:** {member['email']}")
                
                with col2:
                    st.write(f"**Completion Rate:** {member['completion_rate']}%")
                    st.write(f"**Skills:** {', '.join(member['skills'])}")
                
                # Show connections (simplified)
                st.markdown("**Team Connections:**")
                same_dept_members = [m['name'] for m in st.session_state.team_members if m['department'] == member['department'] and m['name'] != member['name']]
                if same_dept_members:
                    st.write(f"Works with: {', '.join(same_dept_members)}")
    
    with tab3:
        st.subheader("Manage Connections")
        
        with st.form("add_connection"):
            col1, col2, col3 = st.columns(3)
            
            worker_names = [m['name'] for m in st.session_state.team_members]
            
            with col1:
                from_worker = st.selectbox("From Worker", worker_names)
            with col2:
                connection_type = st.selectbox("Connection Type", ["reports_to", "collaborates_with", "manages", "mentors"])
            with col3:
                to_worker = st.selectbox("To Worker", worker_names)
            
            if st.form_submit_button("Add Connection"):
                if from_worker != to_worker:
                    st.success(f"Connection added: {from_worker} {connection_type.replace('_', ' ')} {to_worker}")

def show_workflow_builder():
    st.markdown('<div class="main-header"><h1>⚙️ Workflow Builder</h1><p>Create and manage automated workflows for your team processes</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Workflows", "Builder", "Templates"])
    
    with tab1:
        st.subheader("Active Workflows")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Create Workflow", type="primary"):
                st.session_state.show_workflow_form = True
        
        # Display workflows
        for workflow in st.session_state.workflows:
            with st.expander(f"{workflow['name']} - {workflow['category']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Description:** {workflow['description']}")
                    st.write(f"**Trigger:** {workflow['trigger']}")
                    st.write(f"**Steps:** {workflow['steps']}")
                
                with col2:
                    status = "🟢 Active" if workflow['is_active'] else "⚪ Inactive"
                    st.write(f"**Status:** {status}")
                    st.write(f"**Created:** {workflow['created_at']}")
                    st.write(f"**Last Used:** {workflow.get('last_used', 'Never')}")
                
                col1_btn, col2_btn, col3_btn = st.columns(3)
                with col1_btn:
                    st.button("▶️ Run", key=f"run_{workflow['id']}")
                with col2_btn:
                    st.button("✏️ Edit", key=f"edit_wf_{workflow['id']}")
                with col3_btn:
                    toggle_text = "⏸️ Disable" if workflow['is_active'] else "▶️ Enable"
                    st.button(toggle_text, key=f"toggle_{workflow['id']}")
        
        # Add new workflow form
        if st.session_state.get('show_workflow_form', False):
            with st.form("create_workflow"):
                st.subheader("Create New Workflow")
                
                col1, col2 = st.columns(2)
                with col1:
                    wf_name = st.text_input("Workflow Name")
                    wf_description = st.text_area("Description")
                with col2:
                    wf_category = st.selectbox("Category", ["HR", "Quality", "Maintenance", "Safety", "Production", "Training", "Administrative", "Custom"])
                    wf_trigger = st.selectbox("Trigger", ["manual", "scheduled", "event"])
                
                if st.form_submit_button("Create Workflow"):
                    if wf_name:
                        new_workflow = {
                            "id": str(uuid.uuid4()),
                            "name": wf_name,
                            "description": wf_description,
                            "category": wf_category,
                            "is_active": True,
                            "trigger": wf_trigger,
                            "steps": 0,
                            "created_at": datetime.now().strftime("%Y-%m-%d"),
                            "last_used": None
                        }
                        st.session_state.workflows.append(new_workflow)
                        st.session_state.show_workflow_form = False
                        st.success("Workflow created successfully!")
                        st.rerun()
    
    with tab2:
        st.subheader("Workflow Builder")
        st.info("Advanced workflow step builder - drag and drop interface for creating complex automated processes.")
        
        # Simplified workflow builder
        selected_workflow = st.selectbox("Select Workflow to Edit", [w['name'] for w in st.session_state.workflows])
        
        if selected_workflow:
            st.write(f"Editing: **{selected_workflow}**")
            
            # Step types
            step_types = ["Task", "Approval", "Notification", "Review", "Reminder"]
            
            with st.form("add_step"):
                col1, col2 = st.columns(2)
                with col1:
                    step_name = st.text_input("Step Name")
                    step_type = st.selectbox("Step Type", step_types)
                with col2:
                    step_description = st.text_area("Step Description")
                    assigned_roles = st.multiselect("Assigned Roles", [m['role'] for m in st.session_state.team_members])
                
                if st.form_submit_button("Add Step"):
                    st.success(f"Step '{step_name}' added to workflow '{selected_workflow}'")
    
    with tab3:
        st.subheader("Workflow Templates")
        
        workflow_templates = [
            {"name": "Employee Onboarding", "description": "Complete new hire process with training and setup", "category": "HR", "steps": 5, "duration": "3-5 days"},
            {"name": "Equipment Maintenance", "description": "Scheduled maintenance workflow for machinery", "category": "Maintenance", "steps": 4, "duration": "4-8 hours"},
            {"name": "Quality Control", "description": "Standard QC process for production items", "category": "Quality", "steps": 3, "duration": "1-2 hours"},
            {"name": "Safety Incident Report", "description": "Process for handling safety incidents", "category": "Safety", "steps": 6, "duration": "1-3 days"},
        ]
        
        for template in workflow_templates:
            with st.expander(f"{template['name']} Template"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {template['description']}")
                    st.write(f"**Category:** {template['category']}")
                with col2:
                    st.write(f"**Steps:** {template['steps']}")
                    st.write(f"**Duration:** {template['duration']}")
                
                if st.button(f"Use {template['name']} Template", key=f"wf_template_{template['name']}"):
                    st.success(f"{template['name']} template applied!")

def show_settings():
    st.markdown('<div class="main-header"><h1>🛠️ Settings</h1><p>Manage your account and application preferences</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Notifications", "System"])
    
    with tab1:
        st.subheader("👤 Profile Information")
        
        with st.form("profile_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", value="Alex Manager")
                email = st.text_input("Email Address", value="alex.manager@company.com")
            
            with col2:
                role = st.text_input("Role", value="Operations Manager")
                department = st.text_input("Department", value="Operations")
            
            if st.form_submit_button("Save Profile"):
                st.success("Profile updated successfully!")
    
    with tab2:
        st.subheader("🔔 Notification Settings")
        
        st.checkbox("Email Reminders", value=True, help="Receive email notifications for new reminders")
        st.checkbox("Push Notifications", value=True, help="Browser notifications for urgent updates")
        st.checkbox("Weekly Reports", value=True, help="Summary of team performance and activity")
        st.checkbox("Overdue Alerts", value=True, help="Notifications when reminders become overdue")
        st.checkbox("Worker Updates", value=False, help="Notifications when workers complete tasks")
        
        if st.button("Save Notification Settings"):
            st.success("Notification settings saved!")
    
    with tab3:
        st.subheader("⚙️ System Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox("Theme", ["Light", "Dark", "System"])
            timezone = st.selectbox("Timezone", ["America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles", "UTC"])
        
        with col2:
            date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
            default_priority = st.selectbox("Default Priority", ["low", "medium", "high"])
        
        if st.button("Save System Settings"):
            st.success("System settings saved!")

if __name__ == "__main__":
    main()