from django.http import JsonResponse
from django.contrib.auth.models import User

def get_user(request):
    """
    View to retrieve a user by ID. Normalizes and validates input.
    """
    user_id = request.GET.get('id')  # Incoming user input
    
    # Input normalization: Strip whitespace and validate numeric input
    if user_id and user_id.strip().isdigit():
        user_id = int(user_id.strip())  # Normalize input by converting to integer
        user = User.objects.filter(id=user_id).first()  # Safe query using ORM
        if user:
            return JsonResponse({'username': user.username, 'email': user.email})
        return JsonResponse({'error': 'User not found'})
    
    # Return error for invalid input
    return JsonResponse({'error': 'Sorry Invalid user ID'})