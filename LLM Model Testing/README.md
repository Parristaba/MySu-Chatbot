# **LLM Response Generation for User Queries**

## **Overview**  
This module uses **Large Language Models (LLMs)** to generate formal responses to user queries based on retrieved information (e.g., announcements or documents). The retrieved data is provided by the **RAG (Retrieval-Augmented Generation)** and **NER (Named Entity Recognition)** components. The goal is to identify the best-performing LLM for response generation and further fine-tune it for the task.

---

## **Process**  

1. **Input Format**  
   The input passed to the LLM is structured in JSON format with the following template:  
   ```plaintext
   Generate a formal response for the Query, only based on the information inside Announcement:

   Query: {query}
   Announcement: {announcement}
   Response:
   ```
   - **Query**: The user's question.  
   - **Announcement**: Relevant data retrieved from the Vector Database using NER and RAG.  

2. **Model Evaluation**  
   - We tested multiple LLMs with synthetically generated data to compare their response quality.  

3. **Output Example**  
   A sample output with responses from different models:  
   ```json
   {
       "Query": "Do we have internship openings this year?",
       "Announcement": "Internship openings are available for the 2024 academic year. Visit [careerportal.university.edu](http://careerportal.university.edu) for current listings and application details.",
       "Response_T5": "",
       "Response_BART": "No, no...No...Yes... No... Yes......no...Query...",
       "Response_GPT-2": "We have a job opening for a new intern in the fall of 2018. Please contact us for more information.",
       "Response_GPT-Neo": "Yes, we do have internships available this fall. Please visit [univ-portals.com](https://universities.portaldata.org/portalsearch/univer/en/home) to apply. We are also accepting applications for summer intern positions. For more information, please visit the [Summer Interns page](#interns).\nRequest: Please send your resume and cover letter to [porta.david@universe.ac.uk](mailto:portadavid.p@portalde.uni.ca). Please include your name, email address, and phone number."
   }
   ```

4. **Model Selection**  
   After evaluating the performance of the models, **GPT-Neo** was selected as the most suitable LLM for the task due to its:  
   - Coherent and contextually accurate responses.  
   - Better alignment with the input query and retrieved announcements.  

---

## **Models Tested**  
The following models were tested for response generation:  
- **T5**  
- **BART**  
- **GPT-2**  
- **GPT-Neo**  

---

## **Conclusion**  
Based on the results, **GPT-Neo** was chosen for its superior performance in generating accurate and formal responses. Further fine-tuning can be conducted to enhance the model's capabilities for domain-specific tasks.
