from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PromptInputSerializer
from agents.crew import run_crew


class GenerateLandingPageView(APIView):
    """Gera um pequeno projeto a partir de um prompt do usuário.

    O endpoint `/api/generate/` recebe um JSON com o campo `prompt` e aciona o
    fluxo de agentes (aprimoramento do prompt, planejamento, desenvolvimento,
    testes e validação final). O resultado é o caminho para um arquivo zip
    contendo o código gerado.
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
