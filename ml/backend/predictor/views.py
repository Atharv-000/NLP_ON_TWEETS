from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from predictor.ml.predict import predict_tweets, predict_from_csv
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import traceback


def home(request):
    """Render the home page with the prediction UI"""
    return render(request, 'predictor/home.html')


@api_view(['POST'])
def predict_api(request):
    """API endpoint for single tweet or multiple tweets prediction"""
    try:
        # Get tweets from request
        tweets = request.data.get("tweets", [])
        
        print(f"Received request with {len(tweets) if isinstance(tweets, list) else 1} tweet(s)")

        if not tweets or not isinstance(tweets, list):
            return Response(
                {"error": "Please provide a list of tweets"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Make predictions
        print("Calling predict_tweets...")
        results = predict_tweets(tweets)
        print(f"Prediction successful! Got {len(results)} results")
        
        if not results or len(results) == 0:
            return Response(
                {"error": "No results returned from prediction"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({"results": results})
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"❌ Error in predict_api: {str(e)}")
        print(f"Traceback: {error_trace}")
        return Response(
            {"error": f"Prediction error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def predict_csv_api(request):
    """API endpoint for CSV file upload and prediction"""
    try:
        if 'file' not in request.FILES:
            return Response(
                {"error": "CSV file is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']

        # Validate file extension
        if not file.name.endswith('.csv'):
            return Response(
                {"error": "File must be a CSV file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = predict_from_csv(file)
        return Response({"results": results})
    except ValueError as e:
        error_trace = traceback.format_exc()
        print(f"ValueError in predict_csv_api: {str(e)}")
        print(f"Traceback: {error_trace}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in predict_csv_api: {str(e)}")
        print(f"Traceback: {error_trace}")
        return Response(
            {"error": f"Error processing file: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
