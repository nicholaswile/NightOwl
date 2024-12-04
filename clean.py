import json
import nltk
import re

from nltk.corpus import stopwords

def read_json(filename):
    with open(filename, "rb") as f:
        content = f.read()
        data = json.loads(content)
    return data
    
def normalize(doc):
    '''
    In: body text of a web page
    Out: list of normalized tokens from page
    '''
    # Converts to lowercase and removes non-word characters
    doc = doc.lower()
    rule = r'[^\w\s]'
    doc = re.sub(rule, '', doc)
    return doc.split()

def remove_stops(tokens):
    '''
    In: a list of word tokens
    Out: a list of tokens with NLTK stopwords removed
    '''
    stops = set(stopwords.words("english"))
    return [token for token in tokens if token not in stops]

def nltk_download():
    try:
        nltk.data.find("corpora/stopwords.zip")
    except:
        nltk.download("stopwords")

def format_json(docs):
    formatted_docs = json.dumps(docs, indent=4)
    formatted_docs = formatted_docs.replace("\n", "\n    ")  
    return formatted_docs

def main():
    nltk_download()
    
    # Load data from JSON file
    filename = "ksucrawler/ksucrawler/spiders/ksudocs_reduced01.json"
    data = read_json(filename)

    # For storing cleaned dataset
    clean_data = data.copy()

    docs = {}
    reduced = {}
    word_count = 0

    f = open("vault1000.txt", "a", encoding="utf-8")

    for page, _page in zip(data, clean_data):

        # Convert body text to tokens
        doc = normalize(page["body"])
        
        for word in doc:
            f.write(word + " ")
        
        f.write("\n\n")

        docs[page["pageid"]] = doc
        reduced_doc = remove_stops(doc)

        # Remove stopwords from dataset
        reduced[page["pageid"]] = reduced_doc
        _page["body"] = reduced_doc
        word_count += len(reduced_doc)

    f.close()

    # Display dataset stats
    page_count = len(docs)
    avg_wc = int(word_count/page_count)
    print(f"Total words: {word_count}\nTotal documents: {page_count}\nAvg words per page: {avg_wc}\n")

    # Save cleaned dataset
    with open("clean_docs_1000.json", "w") as output_file:
        json.dump(clean_data, output_file, indent=5)

    # Create vocabulary
    vocabulary = {}
    for doc in reduced.values():
        for word in doc:
            vocabulary[word] = vocabulary.get(word, 0) + 1
    
    sorted_vocab = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)

    # Num words to display
    disp = 500
    max_word_len = max(len(word) for word, _ in sorted_vocab[:disp])
    max_count_len = len(str(sorted_vocab[0][1]))

    formatted_vocab = format_json(sorted_vocab)
    with open("vocab.json", "w") as f:
        f.write(formatted_vocab)

    print(f"{disp} most occurring words:")
    for i, (word, count) in enumerate(sorted_vocab[:disp], 1):
        print(f"{i:2}. {word:<{max_word_len}} : {count:>{max_count_len}}")

if __name__ == "__main__":
    main()