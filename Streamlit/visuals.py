import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = {
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Value': [15, 30, 10, 25, 20]
}

# Create a DataFrame from the sample data
df = pd.DataFrame(data)

st.write(df)

# Now plot the visual
st.bar_chart(df.set_index('Category'))
st.line_chart(df.set_index('Category'))

# can we create it via plotlty and then insert in streamlit
# Create some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a Matplotlib figure
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Matplotlib Plot in Streamlit')

# Display the Matplotlib figure in Streamlit
st.pyplot(fig)