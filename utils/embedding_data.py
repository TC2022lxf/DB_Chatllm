from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from config import EMBEDDING_MODEL, EMBEDDING_DEVICE, MODEL_PATH


def embedding_data():
    '''
    embedding 数据     使用bge large zh模型，代替 openai的embeddings = OpenAIEmbeddings()
    '''
    model_name = MODEL_PATH['embed_model'][EMBEDDING_MODEL]
    model_kwargs = {'device': EMBEDDING_DEVICE}
    encode_kwargs = {'normalize_embeddings': True}
    # self.model = sentence_transformers.SentenceTransformer(model_name)
    model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return model

if __name__ == '__main__':
    print(MODEL_PATH['embed_model'][EMBEDDING_MODEL])