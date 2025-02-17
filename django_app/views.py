import re
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from spellchecker import SpellChecker
from collections import Counter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

spell = SpellChecker(language='en')

def zkontroluj_slova(text):
    """
    Funkce kontroluje pravopis slov ve větě.
    - Odstraní interpunkci
    - Zkontroluje správnost slov
    - Navrhne opravy
    """
    text = re.sub(r'[^\w\s]', '', text)  # Odstranění interpunkce
    slova = text.split()
    vysledky = {}

    for index, slovo in enumerate(slova):
        if slovo not in spell:
            navrhy = list(spell.candidates(slovo))
            navrh = navrhy[0] if navrhy else "Nebylo nalezeno"
            vysledky[slovo] = {
                "oprava": navrh,
                "možnosti": navrhy,
                "id": index
            }
        else:
            vysledky[slovo] = {"id": index}

    return vysledky


@swagger_auto_schema(
    method='post',
    operation_description="Zpracuje větu a vrátí upravenou verzi (například převedením na velká písmena).",
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
    sentence = request.data.get('sentence')

    if not sentence:
        return Response({"error": "Nic není zadáno"}, status=400)

    processed_sentence = sentence.upper()
    return Response({'processed_sentence': processed_sentence})


@swagger_auto_schema(
    method='post',
    operation_description="Detekuje opakující se slova a spočítá jejich výskyt.",
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
            'opakovaná_slova': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Slova, která se opakují, včetně počtu a procentuálního výskytu",
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Počet výskytů"),
                        "ratio": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", description="Podíl výskytů na celkovém počtu slov")
                    }
                )
            )
        }
    )}
)
@api_view(['POST'])
def detect_repeated_words(request):
    sentence = request.data.get('sentence')

    if not sentence:
        return Response({"error": "Nic není zadáno"}, status=400)

    words = re.sub(r'[^\w\s]', '', sentence).split()  # Odstranění interpunkce
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


@swagger_auto_schema(
    method='post',
    operation_description="Zkontroluje pravopis věty a navrhne opravy.",
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
            'sentence': openapi.Schema(type=openapi.TYPE_STRING, description="Původní věta"),
            'check': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Slova s navrženými opravami",
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "oprava": openapi.Schema(type=openapi.TYPE_STRING, description="Navrhovaná oprava"),
                        "možnosti": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_STRING),
                            description="Možnosti oprav"
                        ),
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Pořadí slova ve větě")
                    }
                )
            )
        }
    )}
)
@api_view(['POST'])
def check_spelling(request):
    """
    Endpoint pro kontrolu pravopisu ve větě.
    """
    sentence = request.data.get('sentence')

    if not sentence:
        return Response({"error": "Nic není zadáno"}, status=400)

    opravy = zkontroluj_slova(sentence)

    return Response({
        "sentence": sentence,
        "check": opravy
    })
