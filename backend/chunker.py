from langchain_text_splitters import RecursiveCharacterTextSplitter #splits large text into smaller chunks while keeping related information together
import re #cleaning the text before splitting

def clean_text(text: str): #Clean unnecessary spaces.
    text = re.sub(r'\s+', ' ', text) #coverts unreleated words toegether
    return text.strip() #Removes spaces from the beginning and end


def split_text(text: str): #This is the main chunking function.
    text = clean_text(text) #First clean the website text.

    splitter = RecursiveCharacterTextSplitter( #This object is responsible for dividing the text.
        chunk_size=800,        #  800 charcter in each chunk = 1-2 paragraphs
        chunk_overlap=200,     #  repeats the last 200 characters of the previous chunk
        separators=["\n\n", "\n", ". ", "? ", "! ", "; ", " "] #These tell LangChain where to split first.
    )

    chunks = splitter.split_text(text) #Now one large document becomes many chunks.

    final_chunks = [] #store the final cleaned chunks

    for chunk in chunks:
        chunk = chunk.strip() #checks chunks and removes spaces

        
        if len(chunk) < 30:  #Ignore very small chunks
            continue

        # remove junk like single lines
        if len(chunk.split()) < 8: #Ignore chunks with very few words
            continue

        final_chunks.append(chunk)

    return final_chunks