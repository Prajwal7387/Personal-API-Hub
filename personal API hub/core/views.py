from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class LandingView(APIView):
    """
    Renders the premium hub landing page or redirects to dashboard if authenticated.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('ui_overview')
        return render(request, 'core/landing.html')

class PingView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"status": "ok", "message": "Personal API Hub is running"})
