import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# 1. Vectorise the sales response csv data
#CHANGE THIS TO A NEW CSV
loader = CSVLoader(file_path="carComments.csv") #ADD TEXT SPLITTER IF LONG DOCS 
documents = loader.load()

print("len documents:")
print(len(documents))

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search


def retrieve_info(query):
    similar_response = db.similarity_search(query, k=5) #are the number of results that we return

    page_contents_array = [doc.page_content for doc in similar_response]

    print("page contents array")
    print(page_contents_array)

    return page_contents_array


# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")

template = """
You are a design consultant and research analyst named "DesignResearcherAI".You are concerned with how users are navigating new products and unique ways that they are using things. 
You want to find insights into behavioral patterns. 
You are organized in the way you present the information and include the voice of the user. 
I will share a managers question with you and you will give me the best answer that 
I will share with him from your research.
Do not preface your message with "dear" or format the front of it as an email. There is no need for a regards statement at the end either. 

Below is a request I received from the manager:
{message}

Here is a list of best practies of how we normally respond to prospect in similar scenarios:
{best_practice}

Please write the best response to my managers question. 
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# 4. Retrieval augmented generation
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response


# 5. Build an app with streamlit
def main():
    st.set_page_config(
        page_title="Car forum comments consumer insights generator", page_icon=":car:")

    st.header("Design research tool with consumer insights:car:")
    message = st.text_area("Designer request:")

    if message:
        st.write("Generating response to design research inquiry...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()
