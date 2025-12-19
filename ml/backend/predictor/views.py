from predictor.ml.predict import predict_tweets, predict_from_csv
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .ml.predict import predict_tweets
import pandas as pd

@api_view(['POST'])
def predict_api(request):
    tweets = request.data.get("tweets", [])

    if not tweets or not isinstance(tweets, list):
        return Response(
            {"error": "Please provide a list of tweets"},
            status=status.HTTP_400_BAD_REQUEST
        )

    results = predict_tweets(tweets)
    return Response({"results": results})


@api_view(['POST'])
def predict_csv_api(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "CSV file is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']

    try:
        results = predict_from_csv(file)
        return Response({"results": results})
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def predict_csv_api(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "CSV file is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    file = request.FILES['file']

    try:
        results = predict_from_csv(file)
        return Response({"results": results})
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )



def home(request):
    results = None

    if request.method == "POST":

        # Text input
        if "text_submit" in request.POST:
            text = request.POST.get("tweets", "")
            tweets = [t for t in text.split("\n") if t.strip()]
            results = predict_tweets(tweets)

        # CSV upload
        elif "csv_submit" in request.POST and request.FILES.get("csv_file"):
            df = pd.read_csv(request.FILES["csv_file"])
            tweets = df.iloc[:, 0].astype(str).tolist()
            results = predict_tweets(tweets)

    return render(request, "index.html", {"results": results})

