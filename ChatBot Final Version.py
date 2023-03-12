#-*- coding:'utf8'-*-

from textblob import TextBlob
import json
import nltk
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Carregar dados de conversas anteriores de um arquivo JSON
with open("conversations.json", "r", encoding = 'utf8') as file:
    data = json.load(file)

# Inicializar o vetorizador
vectorizer = TfidfVectorizer()

# Inicializar o modelo de agrupamento
model = KMeans(n_clusters=2)

# Criar colunas para pergunta e resposta
conversations = []
for item in data:
    conversation = item["conversation"].split(";")
    conversations.append({"question": conversation[0], "answer": conversation[1]})

# Criar o vetor das perguntas
questions = [conversation["question"] for conversation in conversations]
X = vectorizer.fit_transform(questions)

# Ajustar o modelo aos dados
model.fit(X)

# Função para identificar a intenção do usuário
def get_intent(question):
    # Aplicar o vetorizador à pergunta
    x = vectorizer.transform([question])
    # Prever o cluster da pergunta
    cluster = model.predict(x)[0]
    return cluster

# Exibir algumas linhas dos dados
print(conversations[:2])

# Escrever dados em um arquivo JSON
with open("conversations.json", "w", encoding = 'utf8') as file:
    json.dump(conversations, file)

# Para cada conversa, adicionar um cluster
for i, conversation in enumerate(conversations):
    x = vectorizer.transform([conversation["question"]])
    cluster = model.predict(x)[0]
    conversations[i]["cluster"] = cluster

# pergunta original
original_question = input("Usuário: ")

#remover stopwords e aplicar stemming em português
nltk.download('rslp')
nltk.download("stopwords")
stemmer = RSLPStemmer()
stopwords = set(stopwords.words("portuguese"))

def preprocess_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word not in stopwords]
    text = [stemmer.stem(word) for word in text]
    return text

#aplicando remoção de stopwords e stemming na pergunta original
preprocessed_question = preprocess_text(original_question)

#Identificar a intenção do usuário
cluster = get_intent(preprocessed_question)
    
#Procurar respostas relacionadas à intenção do usuário
related_conversations = [conversation for conversation in conversations if conversation["cluster"] == cluster]

#Escolha a resposta com base na semelhança da pergunta
best_match = max(related_conversations, key=lambda conversation: TextBlob(preprocessed_question).similarity(preprocess_text(conversation["question"])))
answer = best_match["answer"]

#Função para tratar perguntas incomuns
def handle_unknown(original_question):
    question = preprocess_text(original_question)
    # Tokenizar a pergunta
    tokens = nltk.word_tokenize(question)
    # Identificar as palavras-chave
    tagged = nltk.pos_tag(tokens)
    keywords = [word for word, pos in tagged if pos in ["NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP"]]
    # Procurar respostas relacionadas às palavras-chave
    related_conversations = [conversation for conversation in conversations if any(keyword in conversation["question"] for keyword in keywords)]
    # Escolha a resposta com base na semelhança da pergunta
    best_match = max(related_conversations, key=lambda conversation: TextBlob(question).similarity(conversation["question"]))
    return best_match["answer"]

#Tratar perguntas incomuns
if not answer:
    answer = handle_unknown(original_question)

print("Resposta: ", answer)

#Salvar a pergunta e a resposta
conversations.append({"question": original_question, "answer": answer})

#Escrever dados em um arquivo JSON
with open("conversations.json", "w", encoding = 'utf8') as file:
    json.dump(conversations, file)