from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,      # slightly smaller = better retrieval
        chunk_overlap=150    # overlap improves context
    )
    return splitter.split_documents(documents)