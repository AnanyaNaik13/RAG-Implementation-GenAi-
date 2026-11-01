from langchain_groq import ChatGroq
import re
import chromadb
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model='openai/gpt-oss-120b')


def load_pdf(filename):
    reader = PdfReader(filename)
    text = ''
    for page in reader.pages:
        text = text + page.extract_text()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    client = chromadb.Client()
    name = re.sub(r'[^a-zA-Z0-9._-]', '_', filename.name.rsplit('.', 1)[0]).strip('._-')
    if len(name) < 3:
        name = 'doc_' + name
    collection = client.get_or_create_collection(name)
    collection.add(documents=chunks,
                   ids=['c' + str(i) for i in range(len(chunks))])
    return collection


def get_answer(question, collection):
    result = collection.query(query_texts=[question], n_results=2)
    context = result['documents'][0]
    prompt = '''
    I will provide you question and the context which may have answer of given question.
    You have to generate answer in 2 lines with respect to given context. If you dont find answer in given context, just reply "Answer Not found in given context".
    question:{}
    context:{}
    '''.format(question, context)
    # Along with chunks we also need to provide previous messages as a context
    result = llm.invoke(prompt)
    return result.content, context