import os

from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .graph import rag_graph
from .models import Document
from .rag import build_vector_store
from .serializers import DocumentSerializer


class HealthView(APIView):
    def get(self, request):
        return Response({'status': 'ok'})


class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return Response({'error': 'Please upload a PDF file.'}, status=400)

        if not uploaded_file.name.lower().endswith('.pdf'):
            return Response({'error': 'Only PDF files are supported.'}, status=400)

        document = Document.objects.create(
            name=uploaded_file.name,
            file=uploaded_file,
        )

        try:
            build_vector_store(document)
        except Exception as exc:
            document.file.delete(save=False)
            document.delete()
            return Response({'error': str(exc)}, status=400)

        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)


class AskView(APIView):
    def post(self, request):
        document_id = request.data.get('document_id')
        question = request.data.get('question', '').strip()

        if not document_id or not question:
            return Response(
                {'error': 'document_id and question are required.'},
                status=400,
            )

        try:
            document_id = int(document_id)
            Document.objects.get(id=document_id)
        except (ValueError, TypeError, Document.DoesNotExist):
            return Response({'error': 'Document not found.'}, status=404)

        if not settings.GEMINI_API_KEY:
            return Response(
                {'error': 'GEMINI_API_KEY is not configured.'},
                status=500
            )

        try:
            result = rag_graph.invoke({
                'question': question,
                'document_id': document_id,
                'context': [],
                'answer': '',
                'sources': [],
            })
        except Exception as exc:
            return Response({'error': str(exc)}, status=500)

        return Response({
            'answer': result['answer'],
            'sources': result['sources'],
        })
