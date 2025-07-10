from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

class QASystem:
    def __init__(self):
        try:
            self.llm = Ollama(model="phi:2.7b", temperature=0.3)
            self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            self.db = None
        except Exception as e:
            raise Exception(f"Failed to initialize QA system: {str(e)}")

    def process_content(self, text):
        """Safe content processing"""
        try:
            chunks = self.text_splitter.split_text(text)
            self.db = Chroma.from_texts(
                chunks,
                self.embeddings,
                persist_directory="./chroma_db"
            )
        except Exception as e:
            raise Exception(f"Content processing failed: {str(e)}")

    def ask(self, question):
        """Error-handled question answering"""
        if not self.db:
            raise Exception("Content not processed yet")
        
        try:
            docs = self.db.similarity_search(question, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            prompt = f"""
            Answer truthfully using ONLY this context:
            {context}
            
            Question: {question}
            Answer concisely in 20-30 words:
            """
            return self.llm(prompt)
        except Exception as e:
            raise Exception(f"Failed to generate answer: {str(e)}")