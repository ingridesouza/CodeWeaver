# api/serializers.py

from rest_framework import serializers

class PromptInputSerializer(serializers.Serializer):
    prompt = serializers.CharField(
        max_length=1000,
        required=True,
        help_text="Descreva a landing page que deseja gerar"
    )
