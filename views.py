from django.http import JsonResponse
from django.contrib.auth.models import User

def get_user(request):
    
    
    user_id = request.GET.get('id') 
    
    
    if user_id and user_id.strip().isdigit():
        user_id = int(user_id.strip()) 
        user = User.objects.filter(id=user_id).first()  
        if user:
            return JsonResponse({'username': user.username, 'email': user.email})
        return JsonResponse({'error'})
    
    return JsonResponse({'error': 'Sorry Invalid user ID'})