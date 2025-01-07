from langchain_community.document_loaders import PDFLoader, DOCXLoader, XLSXLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

# Load the documents
pdf_loader = PDFLoader("path/to/pdf.pdf")
docx_loader = DOCXLoader("path/to/docx.docx")
xlsx_loader = XLSXLoader("path/to/xlsx.xlsx")

pdf_documents = pdf_loader.load()
docx_documents = docx_loader.load()
xlsx_documents = xlsx_loader.load()

# Split the documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
pdf_docs = text_splitter.split_documents(pdf_documents)
docx_docs = text_splitter.split_documents(docx_documents)
xlsx_docs = text_splitter.split_documents(xlsx_documents)

# Initialize the vector store
embeddings = OpenAIEmbeddings()
vector_store = MongoDBAtlasVectorSearch(
    collection=MongoClient("mongodb://localhost:27017")["langchain_test_db"]["langchain_test_vectorstores"],
    embedding=embeddings,
    index_name="langchain-test-index-vectorstores",
)

# Add the documents to the vector store
vector_store.add_documents(documents=pdf_docs + docx_docs + xlsx_docs)

# Search the vector store
query = "What is the meaning of life?"
found_docs = vector_store.similarity_search(query)

# Print the results
for doc in found_docs:
    print(doc)