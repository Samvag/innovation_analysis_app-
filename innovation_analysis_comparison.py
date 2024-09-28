import streamlit as st
import pandas as pd

# Set up the page title and description
st.title("Enhanced Innovation Opportunity Evaluation Framework")
st.markdown("""
This tool evaluates up to 12 innovation opportunities at both the organization and plant levels by integrating financial metrics, strategic factors, 
and principles of innovation. Please input the relevant data below for each innovation idea, including resource, value, cost, and process evaluations.
""")

# Sidebar pane for selecting innovation ideas to analyze
st.sidebar.title("Select Innovation Idea")
innovation_ideas = [f"Innovation {i}" for i in range(1, 13)]
selected_innovation = st.sidebar.selectbox("Choose an Innovation Idea to Analyze", innovation_ideas)

# Initialize or retrieve stored data
if 'innovation_data' not in st.session_state:
    st.session_state.innovation_data = {idea: pd.DataFrame() for idea in innovation_ideas}  # Initialize all ideas with empty DataFrames

# Function to perform calculations for the chosen innovation idea
def calculate_metrics(data):
    # Perform calculations
    try:
        data['Incremental Market Share Gain (%)'] = ((data['Post-Innovation Market Share'] - data['Pre-Innovation Market Share']) / data['Pre-Innovation Market Share']) * 100
        data['Contribution to Sales (%)'] = ((data['Sales After Innovation'] - data['Sales Before Innovation']) / data['Sales Before Innovation']) * 100
        data['Contribution to Gross Margin (%)'] = ((data['Gross Profit After Innovation'] - data['Gross Profit Before Innovation']) / (data['Sales After Innovation'] - data['Sales Before Innovation'])) * 100
        data['Contribution to Net Profit Margin (%)'] = ((data['Net Profit After Innovation'] - data['Net Profit Before Innovation']) / (data['Sales After Innovation'] - data['Sales Before Innovation'])) * 100
        data['Inventory Velocity (Times per year)'] = data['Cost of Goods Sold'] / ((data['Beginning Inventory'] + data['Ending Inventory']) / 2)
        data['ROIC (%)'] = (data['Net Operating Profit After Taxes'] / data['Invested Capital (Market Value)']) * 100
        data['Cash Generation (in $)'] = (data['Sales After Innovation'] - data['Sales Before Innovation']) - data['Incremental Costs'] - data['Incremental Capital Expenditure']
        
        # Add critical conditions that must hold true for the analysis to be valid
        data['Critical Conditions'] = (
            f"Must achieve a market share gain > 0. Current gain: {data['Incremental Market Share Gain (%)'].iloc[0]:.2f}% | "
            f"ROIC should be > WACC. Current ROIC: {data['ROIC (%)'].iloc[0]:.2f}% | "
            f"Cash generation should be positive: ${data['Cash Generation (in $)'].iloc[0]:.2f}"
        )
    except Exception as e:
        st.error(f"Error in calculations: {e}")
    return data

# Collect input data for the selected innovation idea
st.header(f"Input Data for {selected_innovation}")

# Check if we already have data for this innovation, otherwise set default values
existing_data = st.session_state.innovation_data[selected_innovation]
if not existing_data.empty:
    # Load existing data values into input fields
    data = existing_data.iloc[0].to_dict()
else:
    # Set default values if no data exists
    data = {
        'Pre-Innovation Market Share': 0.0,
        'Post-Innovation Market Share': 0.0,
        'Sales Before Innovation': 0.0,
        'Sales After Innovation': 0.0,
        'Gross Profit Before Innovation': 0.0,
        'Gross Profit After Innovation': 0.0,
        'Net Profit Before Innovation': 0.0,
        'Net Profit After Innovation': 0.0,
        'Cost of Goods Sold': 0.0,
        'Beginning Inventory': 0.0,
        'Ending Inventory': 0.0,
        'Net Operating Profit After Taxes': 0.0,
        'Invested Capital (Market Value)': 0.0,
        'Incremental Costs': 0.0,
        'Incremental Capital Expenditure': 0.0,
        'Sales Team Availability': 'No',
        'Sales Team Challenges': '',
        'Distribution Network Readiness': 'No',
        'Distribution Network Challenges': '',
        'Value 1': '',
        'Value 1 Alignment': 'No',
        'Value 2': '',
        'Value 2 Alignment': 'No',
        'Value 3': '',
        'Value 3 Alignment': 'No',
        'Cost Feasibility': 'No',
        'Cost Challenges': '',
        'Process Capability': 'No',
        'Process Challenges': '',
        'Technology Type': 'Sustaining'  # Default value can be Sustaining or Disruptive
    }

# Collect data from user input
data['Pre-Innovation Market Share'] = st.number_input("Pre-Innovation Market Share (%)", value=data['Pre-Innovation Market Share'], key=f"{selected_innovation}_PreMS")
data['Post-Innovation Market Share'] = st.number_input("Post-Innovation Market Share (%)", value=data['Post-Innovation Market Share'], key=f"{selected_innovation}_PostMS")
data['Sales Before Innovation'] = st.number_input("Sales Before Innovation ($)", value=data['Sales Before Innovation'], key=f"{selected_innovation}_SalesBefore")
data['Sales After Innovation'] = st.number_input("Sales After Innovation ($)", value=data['Sales After Innovation'], key=f"{selected_innovation}_SalesAfter")
data['Gross Profit Before Innovation'] = st.number_input("Gross Profit Before Innovation ($)", value=data['Gross Profit Before Innovation'], key=f"{selected_innovation}_GPBefore")
data['Gross Profit After Innovation'] = st.number_input("Gross Profit After Innovation ($)", value=data['Gross Profit After Innovation'], key=f"{selected_innovation}_GPAfter")
data['Net Profit Before Innovation'] = st.number_input("Net Profit Before Innovation ($)", value=data['Net Profit Before Innovation'], key=f"{selected_innovation}_NPBefore")
data['Net Profit After Innovation'] = st.number_input("Net Profit After Innovation ($)", value=data['Net Profit After Innovation'], key=f"{selected_innovation}_NPAfter")
data['Cost of Goods Sold'] = st.number_input("Cost of Goods Sold ($)", value=data['Cost of Goods Sold'], key=f"{selected_innovation}_COGS")
data['Beginning Inventory'] = st.number_input("Beginning Inventory ($)", value=data['Beginning Inventory'], key=f"{selected_innovation}_BegInv")
data['Ending Inventory'] = st.number_input("Ending Inventory ($)", value=data['Ending Inventory'], key=f"{selected_innovation}_EndInv")
data['Net Operating Profit After Taxes'] = st.number_input("Net Operating Profit After Taxes (NOPAT) ($)", value=data['Net Operating Profit After Taxes'], key=f"{selected_innovation}_NOPAT")
data['Invested Capital (Market Value)'] = st.number_input("Invested Capital (Market Value) ($)", value=data['Invested Capital (Market Value)'], key=f"{selected_innovation}_InvestedCapital")
data['Incremental Costs'] = st.number_input("Incremental Costs ($)", value=data['Incremental Costs'], key=f"{selected_innovation}_IncrCosts")
data['Incremental Capital Expenditure'] = st.number_input("Incremental Capital Expenditure ($)", value=data['Incremental Capital Expenditure'], key=f"{selected_innovation}_IncrCapExp")

# New Resource Evaluation Fields
st.subheader("Resource Evaluation")
data['Sales Team Availability'] = st.selectbox("Sales Team Availability", ["Yes", "No"], index=1 if data['Sales Team Availability'] == "No" else 0)
data['Sales Team Challenges'] = st.text_input("Sales Team Challenges", value=data['Sales Team Challenges'])
data['Distribution Network Readiness'] = st.selectbox("Distribution Network Readiness", ["Yes", "No"], index=1 if data['Distribution Network Readiness'] == "No" else 0)
data['Distribution Network Challenges'] = st.text_input("Distribution Network Challenges", value=data['Distribution Network Challenges'])

# Value Evaluation
st.subheader("Value Evaluation")
data['Value 1'] = st.text_input("Value 1 Description", value=data['Value 1'])
data['Value 1 Alignment'] = st.selectbox("Value 1 Alignment", ["Yes", "No"], index=1 if data['Value 1 Alignment'] == "No" else 0)
data['Value 2'] = st.text_input("Value 2 Description", value=data['Value 2'])
data['Value 2 Alignment'] = st.selectbox("Value 2 Alignment", ["Yes", "No"], index=1 if data['Value 2 Alignment'] == "No" else 0)
data['Value 3'] = st.text_input("Value 3 Description", value=data['Value 3'])
data['Value 3 Alignment'] = st.selectbox("Value 3 Alignment", ["Yes", "No"], index=1 if data['Value 3 Alignment'] == "No" else 0)

# Cost Evaluation
st.subheader("Cost Evaluation")
data['Cost Feasibility'] = st.selectbox("Is the innovation feasible within the company’s cost structure?", 
                                        ["Yes", "No"], 
                                        index=1 if data['Cost Feasibility'] == "No" else 0, 
                                        key=f"{selected_innovation}_CostFeasibility")
data['Cost Challenges'] = st.text_input("Cost Challenges", value=data['Cost Challenges'], key=f"{selected_innovation}_CostChallenges")

# Process Evaluation
st.subheader("Process Evaluation")
data['Process Capability'] = st.selectbox("Are current processes capable of handling the innovation?", 
                                          ["Yes", "No"], 
                                          index=1 if data['Process Capability'] == "No" else 0, 
                                          key=f"{selected_innovation}_ProcessCapability")
data['Process Challenges'] = st.text_input("Process Challenges", value=data['Process Challenges'], key=f"{selected_innovation}_ProcessChallenges")

# Technology Type Evaluation
st.subheader("Technology Type Evaluation")
data['Technology Type'] = st.selectbox("Is it a Sustaining or Disruptive Technology?", 
                                       ["Sustaining", "Disruptive"], 
                                       index=0 if data['Technology Type'] == "Sustaining" else 1, 
                                       key=f"{selected_innovation}_TechnologyType")

# Saving the data back into the session state
df = pd.DataFrame([data])
st.session_state.innovation_data[selected_innovation] = df

# Display calculated metrics when the user clicks a button
if st.button("Calculate and Save Metrics for This Innovation"):
    metrics_df = calculate_metrics(df)
    st.write("**Calculated Metrics for this Innovation:**")
    st.dataframe(metrics_df)
    st.success(f"Metrics calculated and saved for {selected_innovation}")

# Comparison Functionality
st.sidebar.subheader("Compare Innovation Ideas")
selected_comparisons = st.sidebar.multiselect("Select up to 4 innovations to compare", innovation_ideas, default=[])

if len(selected_comparisons) > 0:
    # Display comparison of selected innovations
    comparison_df = pd.concat([st.session_state.innovation_data[idea] for idea in selected_comparisons if not st.session_state.innovation_data[idea].empty])
    
    if not comparison_df.empty:
        st.header("Innovation Comparison Analysis")
        comparison_df.index = selected_comparisons
        st.dataframe(comparison_df[[
            'Incremental Market Share Gain (%)', 
            'Contribution to Sales (%)', 
            'Contribution to Gross Margin (%)', 
            'Contribution to Net Profit Margin (%)',
            'Inventory Velocity (Times per year)', 
            'ROIC (%)', 
            'Cash Generation (in $)',
            'Critical Conditions',
            'Sales Team Availability', 
            'Sales Team Challenges', 
            'Distribution Network Readiness',
            'Distribution Network Challenges',
            'Value 1', 'Value 1 Alignment',
            'Value 2', 'Value 2 Alignment',
            'Value 3', 'Value 3 Alignment',
            'Cost Feasibility', 'Cost Challenges',
            'Process Capability', 'Process Challenges',
            'Technology Type'
        ]])
    else:
        st.warning("Selected innovations do not have any saved data for comparison.")
else:
    st.info("Select up to 4 innovations from the sidebar to compare their metrics.")

st.sidebar.markdown("---")
st.sidebar.write("**Reminder:** Ensure you save your input data by pressing the 'Calculate and Save Metrics' button.")                                   
