from transformers import AutoModel, AutoTokenizer
from spellchecker import SpellChecker
import torch


spell = SpellChecker(language='en')


def zkontroluj_slova(text):
    slova = text.split()
    vysledky = {}

    for slovo in slova:
        if slovo not in spell:
            navrh = spell.correction(slovo)
            vysledky[slovo] = navrh if navrh else "Nebylo nalezeno"
        else:
            vysledky[slovo] = "Správné"

    return vysledky


def main():
    text = input("Zadejte text ke kontrole: ")
    vysledky = zkontroluj_slova(text)

    for slovo, stav in vysledky.items():
        if stav == "Správné":
            print(f"{slovo} - správné")
        else:
            print(f"{slovo} - špatně, návrh: {stav}")


if __name__ == "__main__":
    main()
