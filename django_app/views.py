from rest_framework.decorators import api_view
from rest_framework.response import Response
from spellchecker import SpellChecker
from collections import Counter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
spell = SpellChecker(language='en')

@swagger_auto_schema(
    method='post',
    operation_description="Zpracuje větu a vrátí upravenou verzi.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sentence': openapi.Schema(type=openapi.TYPE_STRING, description="Vstupní věta")
        },
        required=['sentence']
    ),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'processed_sentence': openapi.Schema(type=openapi.TYPE_STRING, description="Upravená věta")
        }
    )}
)
@api_view(['POST'])
def process_sentence(request):
    sentence = request.data.get('sentence', '')
    processed_sentence = sentence.upper()  # Například převod na velká písmena
    return Response({'processed_sentence': processed_sentence})


@swagger_auto_schema(
    method='post',
    operation_description="Detekuje opakující se slova ve větě.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'sentence': openapi.Schema(type=openapi.TYPE_STRING, description="Vstupní věta")
        },
        required=['sentence']
    ),
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'repeated_words': openapi.Schema(type=openapi.TYPE_ARRAY,
                                             items=openapi.Items(type=openapi.TYPE_STRING),
                                             description="Seznam opakujících se slov")
        }
    )}
)
@api_view(['POST'])
def detect_repeated_words(request):
    sentence = request.data.get('sentence', '')
    words = sentence.lower().split()
    repeated = list(set([word for word in words if words.count(word) > 1]))
    return Response({'repeated_words': repeated})

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


#opravit ignorování teček u slov (slovo. vyhodnotí špatně) opravit připisování pořadí
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