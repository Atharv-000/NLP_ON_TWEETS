from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import traceback


def home(request):
    """Render home page; handle POST for tweet prediction."""
    results = None
    error = None

    if request.method == 'POST':
        try:
            from predictor.ml.predict import predict_tweets, predict_from_csv

            if 'csv_submit' in request.POST:
                # CSV upload
                csv_file = request.FILES.get('csv_file')
                if not csv_file:
                    error = 'Please upload a CSV file.'
                elif not csv_file.name.endswith('.csv'):
                    error = 'File must be a .csv file.'
                else:
                    results = predict_from_csv(csv_file)

            elif 'text_submit' in request.POST:
                # Manual tweet input
                raw = request.POST.get('tweets', '').strip()
                if not raw:
                    error = 'Please enter at least one tweet.'
                else:
                    tweets = [t.strip() for t in raw.splitlines() if t.strip()]
                    results = predict_tweets(tweets)

        except Exception as e:
            error = f'Prediction error: {str(e)}'
            print(traceback.format_exc())

    return render(request, 'predictor/home.html', {'results': results, 'error': error})


@csrf_exempt
@api_view(['POST'])
def predict_api(request):
    """API endpoint for single tweet or multiple tweets prediction."""
    try:
        from predictor.ml.predict import predict_tweets
        tweets = request.data.get('tweets', [])
        if not tweets or not isinstance(tweets, list):
            return Response({'error': 'Please provide a list of tweets'}, status=status.HTTP_400_BAD_REQUEST)
        results = predict_tweets(tweets)
        if not results:
            return Response({'error': 'No results returned'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'results': results})
    except Exception as e:
        print(traceback.format_exc())
        return Response({'error': f'Prediction error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def predict_csv_api(request):
    """API endpoint for CSV file upload and prediction."""
    try:
        from predictor.ml.predict import predict_from_csv
        if 'file' not in request.FILES:
            return Response({'error': 'CSV file is required'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return Response({'error': 'File must be a CSV file'}, status=status.HTTP_400_BAD_REQUEST)
        results = predict_from_csv(file)
        return Response({'results': results})
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(traceback.format_exc())
        return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
