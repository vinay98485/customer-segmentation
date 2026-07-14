""" import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px

# 1. Dashboard UI Setup
st.set_page_config(page_title="Customer Segmentation Engine", layout="wide")
st.title("🛍️ Intelligent Customer Segmentation")
st.markdown("Discovering hidden customer personas using Unsupervised Machine Learning (K-Means).")

# 2. Load the Data
@st.cache_data
def load_data():
    return pd.read_csv("Mall_Customers.csv")

df = load_data()

# 3. The Sidebar Control Panel
st.sidebar.header("Model Settings")
st.sidebar.markdown("Drag the slider to tell the AI how many personas (clusters) to look for.")
k_clusters = st.sidebar.slider("Number of Clusters (K)", min_value=2, max_value=10, value=5)

# 4. The Machine Learning Logic
features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(features)
df['Cluster'] = df['Cluster'].astype(str)

#  # 5. The 3D Visualization
# st.subheader("Interactive 3D Cluster Map")
# st.markdown("Rotate and zoom to explore how the AI grouped the customers.")

# fig = px.scatter_3d(
#     df, 
#     x='Age', 
#     y='Annual Income (k$)', 
#     z='Spending Score (1-100)',
#     color='Cluster',
#     title=f"Customer Base Split into {k_clusters} Segments",
#     opacity=0.8,
#     color_discrete_sequence=px.colors.qualitative.Bold
# )

# fig.update_layout(margin=dict(l=0, r=0, b=0, t=40), height=600)
# st.plotly_chart(fig, use_container_width=True) 

# 5. The 2D Visualization (Clean and Professional)
st.subheader("2D Cluster Map (Income vs. Spending Score)")
st.markdown("This 2D view makes it instantly clear who our customer personas are. (Dot size represents Age).")

fig = px.scatter(
    df, 
    x='Annual Income (k$)', 
    y='Spending Score (1-100)',
    color='Cluster',
    size='Age', 
    hover_data=['Gender', 'Age'],
    title=f"Customer Base Split into {k_clusters} Segments",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# 6. Show the raw data with the AI's new column
with st.expander("View Raw Data with Cluster Assignments"):
    st.dataframe(df) """

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px

# 1. Dashboard UI Setup
st.set_page_config(page_title="Customer Segmentation Engine", layout="wide")
st.title("🛍️ Intelligent Customer Segmentation")
st.markdown("Discovering hidden customer personas using Unsupervised Machine Learning (K-Means).")

# 2. Load the Data
@st.cache_data
def load_data():
    return pd.read_csv("Mall_Customers.csv")

df = load_data()

# 3. The Sidebar Control Panel
st.sidebar.header("Model Settings")
st.sidebar.markdown("Drag the slider to tell the AI how many personas (clusters) to look for.")
k_clusters = st.sidebar.slider("Number of Clusters (K)", min_value=2, max_value=10, value=5)

# We will feed the AI three dimensions: Age, Income, and Spending Score
features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]

# 4. NEW: The Elbow Curve Calculator (Hidden in Expander)
with st.expander("🔍 View Mathematical Proof (Elbow Method)"):
    st.markdown("This graph runs the AI 10 times in the background to find the optimal number of groups. Look for the 'elbow' where the line flattens out.")
    
    wcss = []
    for i in range(1, 11):
        kmeans_test = KMeans(n_clusters=i, random_state=42, n_init=10)
        kmeans_test.fit(features)
        wcss.append(kmeans_test.inertia_)
        
    elbow_fig = px.line(
        x=list(range(1, 11)), 
        y=wcss, 
        markers=True,
        title="Inertia (WCSS) vs. Number of Clusters",
        labels={'x': 'Number of Clusters (K)', 'y': 'Inertia Score'}
    )
    st.plotly_chart(elbow_fig, use_container_width=True)

st.markdown("---")

# 5. The Machine Learning Logic
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df['Cluster_ID'] = kmeans.fit_predict(features)
df['Cluster_ID'] = df['Cluster_ID'].astype(str)

# Map the numbers to our Business Personas (Only works perfectly if K=5)
if k_clusters == 5:
    # Note: Depending on your exact package versions, K-Means might swap these numbers. 
    # Look at your graph and rearrange these names if they don't match the corners!
    persona_map = {
        '0': 'The Budget-Conscious (Low Spend/Low Income)',
        '1': 'The Core Base (Average Spend/Average Income)',
        '2': 'The VIPs (High Spend/High Income)',
        '3': 'The Frugal Wealthy (Low Spend/High Income)',
        '4': 'The Impulse Buyers (High Spend/Low Income)',
    }
    df['Persona'] = df['Cluster_ID'].map(persona_map)
else:
    # If the user slides the slider to 3 or 7, default back to generic names
    df['Persona'] = "Segment " + df['Cluster_ID']

# 6. The 2D Visualization
st.subheader("1. 2D Cluster Map (Income vs. Spending Score)")
st.markdown("This 2D view makes it instantly clear who our customer personas are.")

fig = px.scatter(
    df, 
    x='Annual Income (k$)', 
    y='Spending Score (1-100)',
    color='Persona', # We updated this to use our new names!
    size='Age', 
    hover_data=['Gender', 'Age', 'Cluster_ID'],
    title=f"Customer Base Split into {k_clusters} Segments",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# 7. Raw Data & CSV Export Feature
st.markdown("---")
st.subheader("2. Export Segmented Data")
st.markdown("Download the assigned customer list for the marketing team.")

with st.expander("View Raw Data with Cluster Assignments"):
    st.dataframe(df)
    
# Convert the updated dataframe into a CSV file in memory
csv_data = df.to_csv(index=False).encode('utf-8')

# Create the download button
st.download_button(
    label="📥 Download Segmented Data (CSV)",
    data=csv_data,
    file_name='customer_segments_ai.csv',
    mime='text/csv'
)