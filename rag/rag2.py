import torch
import ollama
import os
from openai import OpenAI
import numpy as np

PINK = '\033[95m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
DEFAULT = '\033[0m'

# Body text of each web page is stored on a separate line
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

# Retrieve relevant context from dataset based on user query
def retrieve_context(query, embeddings, dataset, k=3):
    
    # Ensure tensor has embeddings
    if embeddings.nelement() == 0:  
        return []
    
    # Query encoding
    query_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=query)["embedding"]

    # Compute cosine similarity between query and web pages
    cos_scores = torch.cosine_similarity(torch.tensor(query_embedding).unsqueeze(0), embeddings)

    # If less docs than k, set k to the number of documents
    k = min(k, len(cos_scores))

    # Sort docs by relevance and retrieve top k docs by their ID
    idxes = torch.topk(cos_scores, k=k)[1].tolist()

    # Retrieve context from relevant docs
    context = [dataset[idx].strip() for idx in idxes]

    return context

# Interacts with Llama3
def interact(query, system_message, embeddings, dataset, model, convo_history):

    context = retrieve_context(query, embeddings, dataset, k=3)

    if context:
        context_str = "\n".join(context)

    # Concatenate query with relevant context
    query_w_context = query

    if context:
        query_w_context = context_str + "\n\n" + query
    
    # Append query to convo history
    convo_history.append({"role": "user", "content": query_w_context})
    
    # Create a message history
    messages = [
        {"role": "system", "content": system_message},
        *convo_history
    ]
    
    # Send the completion request to the Ollama model
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    # Append the model's response to convo history
    convo_history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    # Return response
    return response.choices[0].message.content

# Config for Ollama API client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='dolphin-llama3'
)

dataset = []
filepath = "texts/ksu5000.txt"

# Load dataset content
if os.path.exists(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        dataset = f.readlines()

embeddings = []
embeddings_tensor = None
embeddings_path = "embeddings/vault_embeddings_5000.npy"

if os.path.exists(embeddings_path):
    print('Found embeddings.')

    # Load embeddings from a NumPy file
    embeddings_loaded = np.load(embeddings_path)
    embeddings_tensor = torch.tensor(embeddings_loaded, dtype=torch.float32)

else:
    print('Creating embeddings.')
    
    # Generate embeddings for the vault content using Ollama
    for content in dataset:
        response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
        embeddings.append(response["embedding"])

    # Convert to tensor and print embeddings
    embeddings_tensor = torch.tensor(embeddings) 

    # Save the embeddings to a NumPy file
    embeddings_numpy = embeddings_tensor.numpy()
    np.save(embeddings_path, embeddings_numpy)

print("Embeddings for each web page in dataset:")
print(embeddings_tensor)

convo_history = []
system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text"

print(PINK + "Hello! I am NightOwl, your 24/7 AI Student Assistant. I'm here to help with all things KSU. How may I help you today?" + DEFAULT)

while True:

    query = input(YELLOW + "How may I help you today? (type 'exit' to quit): " + DEFAULT)
    if query.lower() == 'exit':
        break

    response = interact(query, system_message, embeddings_tensor, dataset, model="llama3", convo_history=convo_history)
    print(GREEN + "Ans: \n" + response + DEFAULT)