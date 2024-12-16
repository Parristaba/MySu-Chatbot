# MySu-Chatbot
Here’s the updated **README.md** with a **Versions** section and the **License** section removed:

---

# **MySu ChatBot**

## **Overview**  
MySu ChatBot is a modular, context-aware chatbot designed for university systems. It enables students to easily access dynamic and static information, such as daily food menus, announcements, and documents. Built with a combination of **Session Management**, **NLU (Natural Language Understanding)**, **RAG (Retrieval-Augmented Generation)**, and advanced **LLM (Large Language Model)** integration, the chatbot ensures efficient, accurate, and seamless interactions.

---

## **Key Features**  
- **Session Management**: Maintains user sessions for multi-turn, context-aware conversations.  
- **Query Filtering**: Focuses on school-related queries using keyword matching and semantic analysis.  
- **NLU Module**: Recognizes user intent (e.g., food menus, announcements, or documents) and extracts relevant entities.  
- **Dynamic and Static Data Handling**: Retrieves up-to-date data using similarity searches in vectorized databases.  
- **RAG Block**: Bridges data retrieval and response generation for relevant and accurate answers.  
- **LLM Integration**: Generates natural, human-like responses using models like GPT-2 or LLaMa.  

---

## **Architecture**  
The chatbot architecture consists of the following key modules:  

1. **Session Manager**: Creates and manages user sessions, ensuring smooth multi-turn interactions.  
2. **Query Filter**: Filters school-related queries and routes them appropriately.  
3. **NLU Block**: Composed of Intent and NER layers to identify query topics and extract entities.  
4. **Database**: Handles dynamic data (e.g., food menus, announcements) and static data (e.g., policies, documents).  
5. **RAG Block**: Retrieves relevant information and feeds it into the LLM for final response generation.  
6. **LLM Module**: Processes refined inputs and generates coherent, contextually accurate responses.  

For a detailed architecture overview, refer to the **[Architecture Overview](docs/Architecture_Overview.pdf)** document.

---

## **Versions**  
- **v0.1**: Initial architecture refinement with defined components and modules.
- **v0.2**: Added data generation scripts for announcements and documents using templates and dictionaries.
- **v0.3**: Implemented and tested Free-to-Use LLM models with simple, predefined instructions.


---
