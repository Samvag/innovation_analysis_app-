import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Sample data for operational performance
data = {
    'Category': ['Production Output', 'Energy Consumption', 'Safety Incidents', 'Product Quality'],
    'Target': [10000, 500, 0, 1],
    'Actual': [9000, 550, 2, 2],
    'Status': ['Delayed', 'Issue', 'Issue', 'Issue'],
    'Problem Area': ['Downtime', 'High energy use in curing', 'Safety protocols', 'Incorrect mixing ratios'],
    'Potential Solution': ['Increase maintenance', 'Energy-efficient equipment', 'Train staff', 'Automate batch monitoring']
}

# Data for productivity improvements
productivity_data = {
    'Training Needs': [],
    'Suggested Workflow Changes': [],
    'Due Date': [],
    'Assigned User': [],
    'Status': [],
}

# DataFrame creation
df = pd.DataFrame(data)
prod_df = pd.DataFrame(productivity_data)

# Sample action item tracking
action_data = {
    'Action Item': ['Reduce downtime', 'Optimize energy use', 'Improve safety', 'Enhance quality control'],
    'Assigned To': ['Maintenance Lead', 'Energy Manager', 'Safety Officer', 'Quality Manager'],
    'Due Date': [datetime.now() + timedelta(days=30), datetime.now() + timedelta(days=20),
                 datetime.now() + timedelta(days=15), datetime.now() + timedelta(days=25)],
    'Status': ['Open', 'Open', 'In Progress', 'Open'],
    'Projected Benefit': ['Increased uptime', 'Lower costs', 'Fewer incidents', 'Better product consistency'],
}

action_df = pd.DataFrame(action_data)

# Title and description
st.title("Production Plant Health Check and Productivity Improvement Dashboard")
st.write("""
This dashboard tracks key performance metrics, identifies problem areas, tracks productivity improvement initiatives, and helps plant managers manage tasks with action items, deadlines, and potential benefits.
""")

# Filter options
category_filter = st.selectbox("Select Category to Focus On", df['Category'].unique())

# Display filtered data
filtered_df = df[df['Category'] == category_filter]

st.write("### Current Status for", category_filter)
st.write(filtered_df)

# Data Visualization: Bar Chart for Actual vs Target
st.write("### Actual vs Target Comparison")
fig, ax = plt.subplots()
ax.barh(filtered_df['Category'], filtered_df['Actual'], label='Actual', color='orange')
ax.barh(filtered_df['Category'], filtered_df['Target'], label='Target', color='green', alpha=0.5)
ax.set_xlabel('Value')
ax.set_title(f'Performance for {category_filter}')
ax.legend()
st.pyplot(fig)

# Action Plan Section
st.write("### Action Plan")
st.write("Problem Area:", filtered_df['Problem Area'].values[0])
st.write("Suggested Solution:", filtered_df['Potential Solution'].values[0])

# Productivity Improvement Section
st.write("### Productivity Improvement")
st.write("#### Add Training Needs and Workflow Suggestions")

with st.form("productivity_form"):
    training_needs = st.text_input("Training Needs (Individual/Group)")
    workflow_suggestion = st.text_input("Suggested Workflow Change")
    due_date = st.date_input("Due Date")
    assigned_user = st.text_input("Assigned User")
    action_status = st.selectbox("Status", ['Open', 'In Progress', 'Completed'])
    
    submitted_prod = st.form_submit_button("Add Productivity Improvement")

    if submitted_prod:
        new_prod_entry = {
            'Training Needs': training_needs,
            'Suggested Workflow Changes': workflow_suggestion,
            'Due Date': due_date,
            'Assigned User': assigned_user,
            'Status': action_status
        }
        prod_df = prod_df.append(new_prod_entry, ignore_index=True)
        st.success("New productivity improvement data added successfully!")

# Display Productivity Improvement Data
st.write("### Current Productivity Improvements")
st.write(prod_df)

# Send Alert Notifications (dummy for now, could be linked to email or messaging service)
st.write("#### Alert Notifications")
for index, row in prod_df.iterrows():
    if row['Due Date'] <= datetime.now().date() and row['Status'] != 'Completed':
        st.warning(f"Action '{row['Training Needs']}' assigned to {row['Assigned User']} is overdue!")

# Action Item Tracker Section
st.write("### Action Item Tracker")

st.write("Action items assigned to team members with due dates and projected benefits:")
st.write(action_df)

# Dashboard Section: Metrics
st.write("### Dashboard: Action Items and Productivity Metrics")

# Calculate the number of open, closed, and in-progress items
open_items = len(action_df[action_df['Status'] == 'Open'])
in_progress_items = len(action_df[action_df['Status'] == 'In Progress'])
completed_items = len(action_df[action_df['Status'] == 'Completed'])

# Calculate the projected benefits and performance metrics
st.write(f"**Number of Action Items Planned:** {len(action_df)}")
st.write(f"**Number of Action Items Open:** {open_items}")
st.write(f"**Number of Action Items In Progress:** {in_progress_items}")
st.write(f"**Number of Action Items Closed:** {completed_items}")

# Projected benefits: This can be further expanded as the project grows
st.write("#### Projected Benefits for the Current Month")
st.write("1. Increased outputs: 10%")
st.write("2. Lower costs: 8% reduction in energy costs")
st.write("3. Reduced time: 12% decrease in downtime")

# Visualization for Action Items Status
st.write("### Action Items Status Distribution")
fig, ax = plt.subplots()
ax.pie([open_items, in_progress_items, completed_items], labels=['Open', 'In Progress', 'Completed'], autopct='%1.1f%%', colors=['orange', 'blue', 'green'])
ax.set_title("Action Items Status Distribution")
st.pyplot(fig)