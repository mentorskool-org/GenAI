import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px

load_dotenv(find_dotenv())

# Create a psycopg2 connection
conn = psycopg2.connect(
    host=os.environ.get("HOST"),
    database=os.environ.get("DBNAME"),
    user=os.environ.get("USER"),
    password=os.environ.get("PASSWORD"),
    port="5432",
)

# Create a cursor
cursor = conn.cursor()

# run a sql query
query = """
    SELECT "participant_email", "participant_name", SUM("score") AS total_scores,    
        SUM("total") as out_of_scores,    
        (SUM("score")/SUM("total"))*100 as scores_in_percentage    
        FROM "skills_fact" sk  
        join orders_dimension od   
        on sk.order_id =od.id  
        and od.description like '%FRAC-IMG-09102023%'  
        WHERE "project_name" = 'SQL Assessment' AND "is_current" = True    
        GROUP BY "participant_email", "participant_name"  
        ORDER BY scores_in_percentage DESC;
"""
cursor.execute(query)
result = cursor.fetchall()
columns = [
    desc[0] for desc in cursor.description
]  # fetch all the columns from the table


skills_df = pd.DataFrame(result, columns=columns)
# print(skills_df)


color_code = ()
st.bar_chart(
    data=skills_df,
    x="participant_name",
    y="scores_in_percentage",
    height=500,
    use_container_width=True,
    color="scores_in_percentage",
)


base = alt.Chart(skills_df).properties(width=800, height=600)

bar = base.mark_bar().encode(
    x=alt.X("scores_in_percentage", title="Learners Scores (%)"),
    y=alt.Y("participant_name", title="Participants Name"),
    color=alt.Color("scores_in_percentage", legend=None),
)
# st.write(bar.properties(width = 800, height = 600))

st.altair_chart(bar, use_container_width=True)


# Create a colormap (color range) from red to green
cmap = plt.get_cmap("RdYlGn")

# Normalize the marks to fit within the colormap's range [0, 1]
norm = plt.Normalize(
    min(skills_df["scores_in_percentage"]), max(skills_df["scores_in_percentage"])
)

# Map marks to colors using the colormap
colors = [cmap(norm(mark)) for mark in skills_df["scores_in_percentage"]]

# Create a Matplotlib bar chart
fig, ax = plt.subplots()
ax.bar(
    skills_df["participant_name"],
    skills_df["scores_in_percentage"],
    color=colors,
)
ax.set_xticklabels(skills_df["participant_name"], rotation=90)

ax.set_xlabel("Category")
ax.set_ylabel("Marks")
ax.set_title("Bar Chart with Custom Colors")

# Display the Matplotlib figure in Streamlit
st.pyplot(fig)




# Create a bar chart using Plotly
fig = px.bar(skills_df, x='participant_name', y='scores_in_percentage', color='scores_in_percentage', labels={'Participant Name': 'participant_name'}, title='Bar Chart with Custom Colors')

# Customize the color scale to match your desired colors
fig.update_traces(marker_line_color='black', marker_line_width=1.5)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)


# Have experienced an interactive plot via plotly, so either use plotly to draw visuals or draw it directly via streamlit