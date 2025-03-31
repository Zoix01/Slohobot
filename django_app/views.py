import string
from collections import Counter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from spellchecker import SpellChecker
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request, jsonify

spell = SpellChecker(language='en')

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
app = Flask(__name__)

def zkontroluj_slova(text):
    for znak in ["’", "‘", "´"]:
        text = text.replace(znak, "'")
    slova = text.split()
    vysledky = {}
    id_counter = 0
    for slovo in slova:
        ciste_slovo = slovo.strip(string.punctuation)
        if ciste_slovo and ciste_slovo not in vysledky:
            if ciste_slovo not in spell:
                navrh = spell.correction(ciste_slovo)
                vysledky[ciste_slovo] = {
                    "oprava": navrh if navrh else "Nebylo nalezeno",
                    "id": id_counter
                }
            else:
                vysledky[ciste_slovo] = {"id": id_counter}
            id_counter += 1
    return vysledky



@swagger_auto_schema(
    method='post',
    operation_description="Zkontroluje pravopis slov ve větě a vrátí původní větu spolu s výsledky kontroly.",
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
                description="Výsledky kontroly jednotlivých slov s případnými opravami."
            )
        }
    )}
)
@api_view(['POST'])
def process_sentence(request):
    sentence = request.data.get('sentence')
    if not sentence:
        return Response({"error": "Nic není zadáno."}, status=400)

    opravy = zkontroluj_slova(sentence)
    return Response({
        "sentence": sentence,
        "check": opravy
    })


@swagger_auto_schema(
    method='post',
    operation_description="Detekuje opakování slov ve větě a vrací počet výskytů a poměr opakování.",
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
            'opakovana_slova': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Slova, která se opakují, s jejich počtem a poměrem."
            )
        }
    )}
)
@api_view(['POST'])
def detect_repeated_words(request):
    sentence = request.data.get('sentence')
    if not sentence:
        return Response({"error": "Nic není zadáno."}, status=400)

    words = sentence.split()
    words_cleaned = [word.strip(string.punctuation) for word in words]
    total_words = len(words_cleaned)
    word_counts = Counter(words_cleaned)
    repeated_words = {}
    for index, word in enumerate(words):
        clean_word = word.strip(string.punctuation)
        if word_counts[clean_word] > 1 and clean_word not in repeated_words:
            repeated_words[clean_word] = {
                "count": word_counts[clean_word],
                "ratio": round(word_counts[clean_word] / total_words, 2)
            }
    return Response({"opakovana_slova": repeated_words})


@api_view(['POST'])
def ai_response(request):
    sentence = request.data.get('sentence')
    if not sentence:
        return Response({'error': 'Žádný vstup nebyl poskytnut'}, status=400)
    generated = generator(sentence, max_length=100, num_return_sequences=1)
    answer = generated[0]['generated_text']
    return Response({'response': answer})

@api_view(['POST'])
def ai_text_continue(request):
    sentence = request.data.get('sentence')
    if not sentence:
        return Response({'error': 'Žádný vstup nebyl poskytnut'}, status=400)

    prefix = "finish this text: "
    full_prompt = prefix + sentence
    generated = generator(full_prompt, max_length=150, num_return_sequences=1)
    answer = generated[0]['generated_text']
    return Response({'response': answer})

