# Industrial Use Cases with Advanced AI Models Project

## Introduction

This project showcases the application of advanced AI and generative models across various industrial domains, including data analysis, insurance, healthcare, retail, and education. Utilizing cutting-edge technologies like Google's generative AI models, Hugging Face datasets, and the innovative PandasAI library, we aim to solve real-world problems by enhancing data interaction, analysis, and visualization capabilities.

## Data Analysis and Visualization Chatbot

### Overview

This use case demonstrates a chatbot powered by Google's generative AI model and PandasAI for analyzing and visualizing data from an Excel spreadsheet. Users can interact with their data in natural language to generate insights and visual representations.

### Technology Stack

- **Google Generative AI (Gemini-Pro model)**: Offers precise answers with a low temperature setting. Explore more about Google Generative AI models [here](https://python.langchain.com/docs/integrations/llms/google_ai).
- **PandasAI**: Facilitates natural language queries for data analysis and visualization across various sources. Learn more about PandasAI [here](https://docs.pandas-ai.com/en/latest/).

### Implementation

A SmartDataframe object is created from an Excel data sheet, allowing for advanced data analysis and visualization through natural language commands.

```python
df = pd.read_excel("orders.xlsx", sheet_name="Sheet1", engine="openpyxl")
llm = GoogleGenerativeAI(
    google_api_key=os.environ.get("GOOGLE_API_KEY"), model="gemini-pro", temperature=0.1
)
df_chain = SmartDataframe(df, config={"llm": llm})
df_chain.chat("""
              Visualize that over the period placement of order is increasing or decreasing.
              Consider the month columns and based on that plot a graph that shows the orders placement
              over the month. Ex: in jane if 25 Orders are placed, in february 20 orders are placed, so orders
              has decaresed, so plot a graph that shows this clearly.
              
              Plot a line chart starting with the January month and showing the placement of orders. 
              Consider the label as vertical on x-axis.

              Visualise the data month number wise, plecment of order of 1 month, then of 2 month, and so on..
              use the dt.month method and then sort it in ascending order, and based on that visualize the data
              """)

```

### Output

[Order Placement Line Chart](https://drive.google.com/file/d/1yS_3m6ecB6tAQtcQIvBatLc7LILW-jk6/view?usp=sharing)

Visualizations are generated as specified by the user's query, demonstrating the powerful integration of AI in data analysis tasks.

## Insurance Data Analysis

### Overview

Analyzes insurance datasets from Hugging Face with different AI models to determine the best performer for specific tasks, focusing on the `create_pandas_dataframe` concept for efficient data handling.

### Technology Stack

- **Hugging Face Models**: For initial data analysis.
- **HuggingFaceEmbeddings and Google Palm**: Tested for performance across different scenarios.

### Implementation

Data from an Excel workbook with multiple sheets is loaded and analyzed, utilizing the RAG framework for enhanced processing and insights.

## Medical Symptoms Chatbot (Incomplete)

### Overview

Plans for a chatbot to assist in identifying and understanding medical symptoms, with a ready flow but implementation pending.

## Retail

### Overview

Introduces the `SQLDatabaseChain` concept, allowing models to understand and query database context, ideal for users unfamiliar with SQL syntax.

### Technology Stack

- **Google Palm Model**: Used for generating insights from the database.
- **SQLDatabaseChain**: Facilitates model access to database context for query execution. Explore more about SQLDatabaseChain [here](https://python.langchain.com/docs/integrations/toolkits/sql_database).

### Safety Note

Ensure only read access is provided to the LLM to prevent unintended data modifications.

## Quiz Generator

### Overview

A fun application that generates quiz questions based on user-selected categories, such as Art, Science, and Geography, showcasing the model's capability to tailor content to specific interests.

```python
prompt_template = """
......

If human provide any other catagory then simply reply "Sorry, I can't generate quiz for this category"

.....

"""
```

### Response for Unsupported Categories

```plaintext
Sorry, I can't generate a quiz for this category.
```

## Conclusion

This project highlights the versatility and potential of generative AI across various industries. By leveraging advanced models and libraries, we demonstrate how AI can transform data interaction, analysis, and decision-making processes, making sophisticated analytics accessible to a broader audience.