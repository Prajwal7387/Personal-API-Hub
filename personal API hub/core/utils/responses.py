from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK) -> Response:
    """
    Standard successful response structure.
    """
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status_code)

def error_response(message: str = "An error occurred", status_code: int = status.HTTP_400_BAD_REQUEST, errors: Optional[Any] = None) -> Response:
    """
    Standard error response structure.
    """
    response_data = {
        "status": "error",
        "message": message
    }
    if errors:
        response_data["errors"] = errors
        
    return Response(response_data, status=status_code)
