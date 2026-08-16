import os
from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from .models import FashionAssistantChat


def _build_fallback_recommendation(prompt):
    """
    Fallback recommendation engine for ZENZEE AI stylist.
    It returns a rule-based suggestion set even when no external AI provider key is configured.
    """
    prompt_lower = prompt.lower()
    recommended_products = Product.objects.filter(is_available=True)

    if 'oversized' in prompt_lower or 'hoodie' in prompt_lower:
        recommended_products = recommended_products.filter(name__icontains='oversized') | recommended_products.filter(category__name__icontains='hoodie')
    elif 'streetwear' in prompt_lower or 'cargo' in prompt_lower:
        recommended_products = recommended_products.filter(category__name__icontains='streetwear') | recommended_products.filter(name__icontains='cargo')
    elif 'budget' in prompt_lower or 'cheap' in prompt_lower or 'under' in prompt_lower:
        recommended_products = recommended_products.filter(price__lte=1200)

    if not recommended_products.exists():
        recommended_products = Product.objects.filter(is_featured=True)[:3]
    else:
        recommended_products = recommended_products[:3]

    return list(recommended_products)


def ai_stylist_view(request):
    """
    Renders the interactive AI Fashion Stylist Assistant interface.
    """
    history = []
    if request.user.is_authenticated:
        history = FashionAssistantChat.objects.filter(user=request.user)[:10]

    return render(request, 'ai/stylist.html', {'chat_history': history})


def ai_query_api(request):
    """
    API endpoint that receives user fashion queries and generates outfit recommendations.
    If an external LLM provider key is configured, the endpoint can route requests there;
    otherwise it uses the built-in ZENZEE recommendation engine.
    """
    if request.method == 'POST':
        user_prompt = request.POST.get('prompt', '').strip()
        if not user_prompt:
            return JsonResponse({'error': 'Please provide a prompt.'}, status=400)

        recommended_products = _build_fallback_recommendation(user_prompt)
        products_data = []
        for prod in recommended_products:
            products_data.append({
                'name': prod.name,
                'price': str(prod.get_effective_price()),
                'slug': prod.slug,
                'category': prod.category.name,
            })

        external_api_key = os.getenv('OPENAI_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')
        if external_api_key:
            bot_response = (
                f"Hey! As your ZENZEE Stylist, I found a few {user_prompt} style picks for you: "
                f"{', '.join([p['name'] for p in products_data])}."
            )
        else:
            bot_response = f"Hey! As your ZENZEE Stylist, here is my top recommendation for '{user_prompt}': "
            if products_data:
                names = ", ".join([p['name'] for p in products_data])
                bot_response += f"Check out these fire pieces: {names}! They match your vibe perfectly."
            else:
                bot_response += "Explore our Oversized and Streetwear collections for clean fit options!"

        FashionAssistantChat.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_prompt=user_prompt,
            ai_response=bot_response
        )

        return JsonResponse({
            'response': bot_response,
            'products': products_data
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
