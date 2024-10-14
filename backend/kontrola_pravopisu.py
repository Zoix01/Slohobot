import torch
import torch.nn as nn
import torch.nn.functional as F


def nacti_slovnik(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        slova = [line.strip() for line in f.readlines()]
    return slova


def vytvor_vocab(slova):
    word_to_idx = {word: idx for idx, word in enumerate(slova)}
    idx_to_word = {idx: word for word, idx in word_to_idx.items()}
    return word_to_idx, idx_to_word


class WordEmbeddings(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(WordEmbeddings, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, input_tensor):
        return self.embeddings(input_tensor)


def najdi_nejpodobnejsi_slovo(user_input, word_to_idx, idx_to_word, model, device, threshold=0.8):
    user_input_idx = None

    # Pokud slovo není ve slovníku, hledáme nejpodobnější
    if user_input in word_to_idx:
        user_input_idx = torch.tensor([word_to_idx[user_input]], dtype=torch.long).to(device)
    else:
        print("Slovo není ve slovníku, hledám nejpodobnější...")

    # Pokud je slovo ve slovníku, použijeme jeho embedding
    if user_input_idx is not None:
        user_embedding = model(user_input_idx)
    else:
        # Pokud není slovo ve slovníku, simulujeme embedding pro porovnání s ostatními slovy
        # Prozatím ho necháme jako nulový vektor, který budeme porovnávat
        user_embedding = torch.zeros(1, model.embeddings.embedding_dim).to(device)

    nejblizsi_slovo = None
    nejlepsi_podobnost = -1

    # Projdeme všechny embeddingy ve slovníku
    for slovo, idx in word_to_idx.items():
        word_idx_tensor = torch.tensor([idx], dtype=torch.long).to(device)
        word_embedding = model(word_idx_tensor)

        cosine_similarity = F.cosine_similarity(user_embedding, word_embedding).item()

        if cosine_similarity > nejlepsi_podobnost and cosine_similarity >= threshold:
            nejlepsi_podobnost = cosine_similarity
            nejblizsi_slovo = slovo

    return nejblizsi_slovo if nejblizsi_slovo else "Žádné podobné slovo nebylo nalezeno."


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    slovnik_file = 'slovnik.dic'
    slova = nacti_slovnik(slovnik_file)
    word_to_idx, idx_to_word = vytvor_vocab(slova)
    embedding_dim = 100
    vocab_size = len(slova)
    model = WordEmbeddings(vocab_size, embedding_dim).to(device)
    user_input = input("Zadejte slovo: ").strip()
    threshold = 0.0000000000001
    nejblizsi_slovo = najdi_nejpodobnejsi_slovo(user_input, word_to_idx, idx_to_word, model, device, threshold)

    print(f"Nejpodobnější slovo je: {nejblizsi_slovo}")


if __name__ == "__main__":
    main()
