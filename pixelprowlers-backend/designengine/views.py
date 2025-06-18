from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DesignTheme
from .serializers import DesignThemeSerializer

@api_view(['GET'])
def get_default_theme(request):
    theme = DesignTheme.objects.filter(is_default=True).first()
    return Response(DesignThemeSerializer(theme).data)

@api_view(['GET'])
def get_theme_by_slug(request, slug):
    try:
        theme = DesignTheme.objects.get(slug=slug)
    except DesignTheme.DoesNotExist:
        return Response({'error': 'Theme not found'}, status=404)
    return Response(DesignThemeSerializer(theme).data)
