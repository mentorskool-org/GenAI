# Advanced RAG Chatbot Project

## Introduction

This project represents the pinnacle of Retrieval-Augmented Generation (RAG) technology, introducing advanced concepts and functionalities that extend the capabilities of traditional chatbots and document search tools. Through sophisticated integration of various tools, loaders, and AI models, this project offers a suite of applications capable of understanding and interacting with unstructured data across multiple formats, performing web searches for unanswered queries, and even visualizing data.

## Project Components

### chatbot.py

- **Functionality**: An advanced chatbot that leverages Chroma vector stores for efficient data retrieval and utilizes the Unstructured File Loader to handle various file formats including JSON, Excel, CSV, docs, and PDFs. Users can upload documents and engage in a conversational interface to query information directly related to the loaded document.
- **Key Features**:
    - **Unstructured File Loading**: Utilizes a versatile loader capable of handling multiple file types, including JSON, Excel, CSV, PDF, and docs. This feature ensures that the chatbot can serve various user needs without file format limitations.
    - **Chroma Vector Stores**: Employs Chroma vector stores for storing and retrieving document embeddings. This storage solution is optimized for speed and efficiency, enabling quick response times even with large datasets.
    - **Dynamic Query Handling**: The chatbot can understand and process user queries, fetch relevant information from the uploaded documents, and generate informative responses.

### document_search_tool_agent_with_memory.py

- **Functionality**: An end-to-end conversational chatbot that not only allows document uploads for querying but also searches the internet when it fails to find answers within the document. It seamlessly integrates DuckDuckGo Search API Wrapper and RetrievalQA chains as tools within an agent framework, storing previous conversations to maintain context.

- **Key Features**:
    - **Dual Retrieval Tools**: Incorporates the DuckDuckGo Search API Wrapper for internet searches and a RetrievalQA chain for document-based queries. This dual approach ensures comprehensive coverage of possible information sources.
    - **Memory Function**: Utilizes a conversation buffer to store past interactions, enabling the chatbot to maintain context over the course of a conversation. This feature is critical for providing coherent and relevant responses over extended dialogues.
    - **Agent Framework**: Agents are preferrable for dynamic tasks. Agents can have an access to the external tools such as search_engine, calculator, files, documents, etc. Suppose we want to find the Age of Elon Musk, so we will ask the agent for the age. We will give agent the access to 2 tools that is duck duck go search engine and the calculator. So what does agent will do. Agent will identify the steps then arrange it in order, it will first take the step and fetch the birth year of Elon Musk via duck duck go, in the next step it will take the birth year and will calculate the age of Elon Musk using calculator. Like this steps are taken by agents dynamically. It decides that which actions should be considered first. It uses the LLM as reasoning engine to decides which actions to be performed next

### document_search_tool_agent_without_memory.py

- **Functionality**: Similar to the with-memory version, but lacks the ability to store conversation history, making each interaction stateless.
**Key Features**:
    - **Stateless Interactions**: Designed for scenarios where conversation history isn't necessary or desired. It provides a simpler, more focused user experience for straightforward information retrieval tasks.
    - **Tool Integration**: Despite the absence of memory, it retains the integration of DuckDuckGo for web searches and RetrievalQA for document queries, ensuring robust response capabilities.

### rag_bots.ipynb

- **Functionality**: A Jupyter notebook introduction covering the foundational concepts of RetrievalQA, agent tools, and LangChain agents, providing a hands-on experience with the code.
**Key Features**:
    - **Interactive Learning**: Allows users to experiment with code snippets in real-time, offering a hands-on approach to understanding RAG concepts and the project's architecture.
    - **Comprehensive Coverage**: Covers a wide range of topics from RetrievalQA, tool integration, to the use of LangChain agents, offering a rounded educational experience.

### visualization_bot.py

- **Functionality**: Utilizes the pandas-ai library to analyze and visualize data from uploaded CSV files, offering users an interactive experience with data through conversational queries.
**Key Features**:
    - **Data Visualization**: Users can request visualizations of their data, such as graphs and charts, directly through chat interactions, making data analysis more accessible and user-friendly.
    - **Pandas-AI Integration**: Utilizes the pandas-ai library for data processing and visualization capabilities, showcasing the library's potential for conversational data science applications.

## Skills You'll Learn

- Integration and use of various file loaders to handle unstructured data.
- Application of vector stores for efficient data retrieval.
- Development of advanced conversational agents with and without memory capabilities.
- Utilization of external tools and APIs within an agent to extend functionality beyond document-based information retrieval.
- Implementation of data visualization within a chatbot framework.

## Getting Started

To get started with this project, follow these setup steps:

1. Install the necessary packages and dependencies:
   ```bash
   pip install "unstructured[all-docs]" pandas-ai langchain chroma-storage faiss
   ```
2. Review the `rag_bots.ipynb` notebook for an introduction to the core concepts and hands-on examples.
3. Explore the `chatbot.py`, `document_search_tool_agent_with_memory.py`, and `visualization_bot.py` scripts to understand the project's functionalities.

## Documentation and References

- **Unstructured File Loader**: [Installation and Usage](https://unstructured-io.github.io/unstructured/installation/full_installation.html)
- **Pandas AI Library**: [Documentation](https://docs.pandas-ai.com/en/latest/)
- **LangChain Agents and Tools**: [Understanding Agents and Their Tools](https://www.pinecone.io/learn/series/langchain/langchain-agents/)
- **Memory in Conversational Agents**: [Types of Memory and Their Applications](https://python.langchain.com/docs/modules/memory)
- **Few-Shot Prompt Templates**: [Guide](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples)

## Conclusion

This project showcases the advanced capabilities of RAG technology when combined with innovative data handling and retrieval techniques. By participating, you'll not only learn about the technical aspects of building sophisticated AI-driven tools but also gain insights into practical applications that can revolutionize the way we interact with information.