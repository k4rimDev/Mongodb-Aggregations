import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import Feedback, collection


class FeedbackGroupedView(APIView):
    def get(self, request):
        data = Feedback.group_feedback_by_branch_service()
        return Response(data)


@csrf_exempt
def fetch_and_store_feedback(request):
    if request.method == 'GET':
        try:
            response = requests.get('https://qmeter-fb-dev.s3.amazonaws.com/media/feedback.json')
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                collection.insert_one(data)

            return JsonResponse({'status': 'success', 'message': 'Data inserted successfully'}, status=200)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'status': 'error', 'message': f'Network error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'only GET method allowed'}, status=405)
