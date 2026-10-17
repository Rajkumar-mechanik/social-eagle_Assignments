# =====================================================================
# SIMPLE RAG DEMO: LangChain + HuggingFace Embeddings + FAISS + OpenAI
# with LangSmith monitoring
# =====================================================================
#
# STEP 1 - INSTALL PACKAGES (run once in your terminal)
# ---------------------------------------------------------------------
#   pip install langchain langchain-community langchain-openai \
#               langchain-huggingface langchain-text-splitters \
#               faiss-cpu sentence-transformers python-dotenv langsmith
#
# STEP 2 - CREATE A ".env" FILE in the same folder as this script
# ---------------------------------------------------------------------
#   OPENAI_API_KEY=sk-your-openai-key
#   LANGSMITH_TRACING=true
#   LANGSMITH_API_KEY=lsv2-your-langsmith-key
#   LANGSMITH_PROJECT=rag-demo
#
# STEP 3 - RUN
# ---------------------------------------------------------------------
#   python rag_langchain_demo.py
#
# Then open https://smith.langchain.com -> Projects -> "rag-demo"
# to see every retrieval + LLM call traced.
# =====================================================================


# ---------------------------------------------------------------------
# 0. SAMPLE TEXT (a little long, so chunking actually has something to do)
# ---------------------------------------------------------------------
SAMPLE_TEXT = """
The Story of Coffee

Coffee is one of the most widely consumed beverages in the world, with billions of cups enjoyed every single day. According to popular legend, coffee was discovered around the ninth century in the highlands of Ethiopia by a goat herder named Kaldi. He noticed that his goats became unusually energetic after eating the red berries from a certain bush. Curious, he shared the berries with a local monastery, and the monks soon found that a drink made from them helped them stay awake during long evening prayers. From Ethiopia, coffee travelled across the Red Sea to Yemen, where it was cultivated and traded by the fifteenth century.

By the sixteenth century, coffee had spread through Persia, Egypt, Syria and Turkey. Coffeehouses, known as qahveh khaneh, became popular social centres where people gathered to drink coffee, listen to music, play chess and discuss the news. These places were often called "schools of the wise" because of the lively conversations that took place inside them. European travellers carried stories of the dark drink back home, and by the seventeenth century coffeehouses had opened in Venice, London, Paris and Amsterdam.

Coffee grows in a belt around the equator, often called the Bean Belt, which includes countries such as Brazil, Vietnam, Colombia, Ethiopia and India. The two most important species are Arabica and Robusta. Arabica makes up about sixty percent of world production, grows at high altitudes between 600 and 2000 metres, and has a smooth, sweet and slightly acidic flavour. Robusta grows at lower altitudes, is hardier against pests, contains almost twice as much caffeine, and tastes stronger and more bitter. In India, coffee is mainly grown in the shaded hills of Karnataka, Kerala and Tamil Nadu.

After the cherries are picked, the beans must be separated from the fruit using one of three main processing methods. In the washed process, the fruit pulp is removed and the beans are fermented in water tanks before being dried, which gives a clean and bright taste. In the natural process, the whole cherries are dried in the sun with the fruit still attached, producing a fruity and heavy-bodied cup. In the honey process, only part of the fruit pulp is removed before drying, giving a balance of sweetness and clarity. Once dried, the green beans are sorted, graded and shipped to roasters around the world.

Roasting transforms green beans into the brown, aromatic beans we recognise. Light roasts keep more of the original fruity and floral flavours and have higher acidity. Medium roasts are balanced, with caramel-like sweetness. Dark roasts taste bold, smoky and bitter because the natural sugars have been heavily caramelised. A common mistake is to think dark roast has more caffeine, but in fact the roasting process slightly reduces caffeine, so light roasts often have a little more.

Brewing method and ratio strongly affect the final cup. A widely used guideline, called the golden ratio, is about one gram of coffee for every sixteen grams of water, which is roughly sixty grams of coffee per litre. The ideal water temperature is between 90 and 96 degrees Celsius, because boiling water can scorch the grounds. A pour-over takes around three minutes, a French press needs about four minutes of steeping, and an espresso shot is pulled in just twenty-five to thirty seconds under high pressure. Freshly ground beans and clean filtered water are the two simplest ways to improve any cup of coffee.
"""

# Save the sample text into a .txt file so we can load it like a real document
with open("sample.txt", "w", encoding="utf-8") as f:   # open (or create) sample.txt for writing
    f.write(SAMPLE_TEXT.strip())                       # write the text and strip leading/trailing blank lines

print(f"Sample text length: {len(SAMPLE_TEXT.strip())} characters")  # ~3,700 characters -> we use this to choose the chunk size


# ---------------------------------------------------------------------
# 1. LOAD API KEYS FROM .env  (must be done BEFORE using OpenAI / LangSmith)
# ---------------------------------------------------------------------
from dotenv import load_dotenv   # python-dotenv reads key=value pairs from the .env file

load_dotenv()                    # loads OPENAI_API_KEY, LANGSMITH_API_KEY, LANGSMITH_TRACING, LANGSMITH_PROJECT
# NOTE: LangSmith needs no extra code. Once LANGSMITH_TRACING=true and the key
# are in the environment, every LangChain call (retriever, prompt, LLM) is traced automatically.


# ---------------------------------------------------------------------
# 2. DATA INGESTION  (load the .txt file as a LangChain Document)
# ---------------------------------------------------------------------
from langchain_community.document_loaders import TextLoader   # loader for plain .txt files

loader = TextLoader("sample.txt", encoding="utf-8")   # point the loader at our file
documents = loader.load()                             # returns a list of Document objects (1 for a single .txt)

print(f"Loaded {len(documents)} document(s)")         # expect 1 document


# ---------------------------------------------------------------------
# 3. DATA SPLITTING (chunking)
# ---------------------------------------------------------------------
# THUMB RULES FOR CHUNK SIZE AND OVERLAP
# ---------------------------------------------------------------------
# 1. Chunk size: one chunk should hold roughly ONE complete idea.
#      - Short factual / FAQ text ........ 200-500 characters
#      - Articles, blogs, notes .......... 500-1000 characters  (our case)
#      - Long reports, legal, technical .. 1000-2000 characters
# 2. Never exceed the embedding model's limit. all-MiniLM-L6-v2 reads about
#    256 tokens (~1000 characters), so chunks above that get silently truncated.
# 3. Overlap: use 10-20% of chunk size. It keeps a sentence that falls on a
#    boundary visible in both neighbouring chunks. Too much overlap means
#    duplicate chunks, a bigger index and repeated results.
# 4. Sanity check: total text / chunk size should give about 6-15 chunks for a
#    small demo. Smaller chunks give precise retrieval but less context;
#    bigger chunks give more context but noisier retrieval.
#
# OUR DECISION: text is ~3,700 characters with 6 paragraphs of ~500-700
# characters each, so chunk_size=600 (about one paragraph) and
# chunk_overlap=100 (about 15%). That gives roughly 7-8 chunks.
# ---------------------------------------------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter   # splits on paragraphs, then sentences, then words

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,       # max characters per chunk
    chunk_overlap=100,    # characters shared between neighbouring chunks (~15%)
)
chunks = splitter.split_documents(documents)   # split the Document into smaller Documents

print(f"Created {len(chunks)} chunks")          # check how many chunks were produced


# ---------------------------------------------------------------------
# 4. EMBEDDINGS (HuggingFace, runs locally and free, no API key needed)
# ---------------------------------------------------------------------
from langchain_huggingface import HuggingFaceEmbeddings   # wrapper around sentence-transformers

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"   # small, fast, good general-purpose model (384 dimensions)
)
# The model is downloaded automatically the first time you run this.


# ---------------------------------------------------------------------
# 5. VECTOR DATABASE (FAISS, stored locally on disk)
# ---------------------------------------------------------------------
from langchain_community.vectorstores import FAISS   # FAISS = Facebook AI Similarity Search

vectorstore = FAISS.from_documents(chunks, embeddings)   # embed every chunk and build the index in memory
vectorstore.save_local("faiss_index")                    # save the index into a local folder called faiss_index

# To reuse the saved index later without re-embedding, you would do:
# vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

print("FAISS index saved to ./faiss_index")


# ---------------------------------------------------------------------
# 6. RETRIEVER
# ---------------------------------------------------------------------
# k = number of chunks returned for each question.
# Thumb rule: k = 3 is a good default (range 2-5). With ~600 character chunks,
# 3 chunks is about 1800 characters, so enough context without noise.
retriever = vectorstore.as_retriever(
    search_type="similarity",     # plain cosine/L2 similarity search
    search_kwargs={"k": 3},       # return the top 3 most similar chunks
)


# ---------------------------------------------------------------------
# 7. LLM (OpenAI mini model)
# ---------------------------------------------------------------------
from langchain_openai import ChatOpenAI   # OpenAI chat model wrapper

llm = ChatOpenAI(
    model="gpt-4o-mini",   # the "mini" model: cheap and fast
    temperature=0,         # 0 = factual, consistent answers (best for RAG)
)


# ---------------------------------------------------------------------
# 8. PROMPT + CHAIN (retriever -> prompt -> llm -> text)
# ---------------------------------------------------------------------
from langchain_core.prompts import ChatPromptTemplate        # build the prompt
from langchain_core.output_parsers import StrOutputParser    # turn the LLM message into a plain string
from langchain_core.runnables import RunnablePassthrough     # passes the question through unchanged

prompt = ChatPromptTemplate.from_template(
    """Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}

Answer:"""
)   # {context} and {question} are filled in at run time


def format_docs(docs):
    # join the text of the retrieved chunks into one string, separated by blank lines
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {
        "context": retriever | format_docs,    # question -> retriever -> top 3 chunks -> one text block
        "question": RunnablePassthrough(),     # the original question goes straight to the prompt
    }
    | prompt                                   # fill the prompt template
    | llm                                      # send it to gpt-4o-mini
    | StrOutputParser()                        # get the answer as a string
)


# ---------------------------------------------------------------------
# 9. ASK THREE QUESTIONS (all answers are in the sample text)
# ---------------------------------------------------------------------
questions = [
    "Who discovered coffee according to the legend, and where?",         # answer is in paragraph 1
    "What are the three coffee processing methods and how do they taste?",  # answer is in paragraph 4
    "What is the golden ratio and the ideal water temperature for brewing?",  # answer is in paragraph 6
]

for i, q in enumerate(questions, start=1):          # loop through the three questions
    print(f"\n--- Question {i}: {q}")                # show the question
    answer = rag_chain.invoke(q)                     # run the full RAG pipeline (this call is traced in LangSmith)
    print(f"Answer: {answer}")                       # show the LLM answer

    # Optional: show which chunks the retriever picked, to understand retrieval quality
    retrieved = retriever.invoke(q)                  # run only the retriever
    for j, doc in enumerate(retrieved, start=1):
        print(f"   [chunk {j}] {doc.page_content[:80]}...")   # print first 80 characters of each chunk

print("\nDone. Check your traces at https://smith.langchain.com")
