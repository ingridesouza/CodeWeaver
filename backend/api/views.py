from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PromptInputSerializer
from agents.crew import run_crew


class GenerateLandingPageView(APIView):
    """
    Endpoint POST /api/generate/

    Corpo esperado:
    {
      "prompt": "Quero uma landing page moderna sobre cafés especiais"
    }

    Retorno de sucesso:
    {
      "status": "success",
      "briefing": {...},
      "project_dir": "backend/output/cafes-especiais",
      "zip_path": "backend/output/cafes-especiais.zip",
      "timestamp": "2025-05-23T14:32:10Z",
      "token_usage": { ... }
    }
    """

    def post(self, request):
        serializer = PromptInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        prompt: str = serializer.validated_data["prompt"].strip()
        if not prompt:
            return Response(
                {"status": "error", "message": "O campo 'prompt' não pode estar vazio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = run_crew(prompt)          # ← executa todo o fluxo
            return Response(
                {"status": "success", **result},
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            # Logue exc se quiser (logger.error(...))
            return Response(
                {"status": "error", "message": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
