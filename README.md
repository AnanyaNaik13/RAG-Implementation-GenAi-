# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built with Streamlit. Upload a PDF and ask questions about it. The app retrieves the most relevant parts of the document and uses an LLM to answer based only on that content.

**Live demo:** https://ragchatbotpdf.streamlit.app/

## Features

- Upload any text-based PDF from the browser
- Splits the document into overlapping chunks and stores them in a vector database
- Retrieves the most relevant chunks for each question
- Answers in two lines, grounded in the retrieved context
- Replies "Answer Not found in given context" when the PDF doesn't contain the answer
- Shows the retrieved source chunks in an expandable "Sources" section
- Keeps the chat history for the session

## How It Works

1. **Upload:** The user uploads a PDF through the Streamlit file uploader.
2. **Extract:** Text is extracted from every page with PyPDF2.
3. **Chunk:** The text is split into 1000-character chunks with 200 characters of overlap using LangChain's `RecursiveCharacterTextSplitter`.
4. **Embed and store:** The chunks are stored in a ChromaDB collection, which creates the embeddings.
5. **Retrieve:** For each question, the top 2 most similar chunks are fetched.
6. **Generate:** The question and the retrieved context go into a prompt for the LLM (`openai/gpt-oss-120b` via Groq), which returns the answer.

## Tech Stack

| Component | Tool |
|---|---|
| UI | Streamlit |
| PDF parsing | PyPDF2 |
| Text splitting | LangChain Text Splitters |
| Vector database | ChromaDB |
| LLM | Groq (`openai/gpt-oss-120b`) via `langchain-groq` |
| Config | python-dotenv |

## Project Structure

```
.
├── ragui.py            # Streamlit UI: upload, chat, sources
├── rag_pipeline.py     # load_pdf() and get_answer() RAG logic
├── requirements.txt    # Python dependencies
└── .env                # GROQ_API_KEY (local only, do not commit)
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A free Groq API key from https://console.groq.com

### Installation

```bash
git clone <your-repo-url>
cd <your-repo-folder>
python -m pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

### Run

```bash
streamlit run ragui.py
```

Open the local URL shown in the terminal, upload a PDF, and start asking questions.

## Deploying on Streamlit Cloud

1. Push the project to GitHub, including `requirements.txt`.
2. Create a new app on https://share.streamlit.io and select `ragui.py` as the main file.
3. Under **Settings → Secrets**, add:
   ```
   GROQ_API_KEY = "your_key_here"
   ```
4. Deploy. Never commit your real API key to GitHub.

## Limitations

- Scanned PDFs (images without a text layer) don't work, since there is no OCR.
- The vector database is in memory, so it resets when the app restarts.
- The chatbot answers each question independently and doesn't yet use previous messages as context.

## Future Improvements

- Use previous chat messages as context for follow-up questions
- Support multiple PDFs and other file types
- Add OCR for scanned documents
- Persist the vector database between sessions
- Cache processing so large PDFs aren't re-processed on every message

## License

This project is for educational purposes.
