from django.shortcuts import render

# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PromptInputSerializer
from agents.crew import run_crew

class GenerateLandingPageView(APIView):
    def post(self, request):
        serializer = PromptInputSerializer(data=request.data)
        
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            
            try:
                # Executa a Crew com o prompt
                result = run_crew(prompt)

                return Response({
                    "status": "success",
                    "enhanced_prompt": result
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
