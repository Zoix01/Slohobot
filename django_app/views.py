from rest_framework.decorators import api_view
from rest_framework.response import Response
from spellchecker import SpellChecker
from collections import Counter
spell = SpellChecker(language='en')

def zkontroluj_slova(text):
    slova = text.split()
    vysledky = {}
    for index, slovo in enumerate(slova):
        if slovo not in spell:
            navrh = spell.correction(slovo)
            vysledky[slovo] = {
                "oprava": navrh if navrh else "Nebylo nalezeno",
                "id": index

            }
        else:
            vysledky[slovo] = {
                "id": index
            }

    return vysledky



@api_view(['POST'])
def process_sentence(request):
    sentence = request.data.get('sentence')

    if not sentence:
        return Response({"error": "nic neni zadáno"}, status=400)

    opravy = zkontroluj_slova(sentence)

    return Response({
        "sentence": sentence,
        "check": opravy
    })

#Kontrola textu -- opakování slov, správnost smyslu věty
@api_view(['POST'])
def detect_repeated_words(request):
    sentence = request.data.get('sentence')

    if not sentence:
        return Response({"error": "nic není zadáno"}, status=400)

    words = sentence.split()
    total_words = len(words)
    word_counts = Counter(words)

    repeated_words = {
        word: {
            "count": count,
            "ratio": round(count / total_words, 2)
        }
        for word, count in word_counts.items() if count > 1
    }

    return Response({"opakovaná_slova": repeated_words})


#interakce s AI