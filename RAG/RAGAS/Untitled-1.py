# %%
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chat_models.ollama import ChatOllama 
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader

# %%
generator_llm = ChatOllama(model = "qwen2:7b",callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
critic_llm = ChatOllama(model = "qwen2:7b",callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
embeddings = OllamaEmbeddings(
    model="qwen2:7b",
)

# %%
generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)

# %%

loader = DirectoryLoader("data/")
documents = loader.load()
for document in documents:
    document.metadata['filename'] = document.metadata['source']

# %%
testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25},raise_exceptions=False)

# %%
print(testset)


