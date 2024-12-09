from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

# Stripe API keys
stripe.api_key = settings.STRIPE_SECRET_KEY

def subscribe(request):
    """Renders the subscription page."""
    return render(request, "sim/subscribe.html", {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    })
@csrf_exempt
def create_checkout_session(request):
    """Creates a Stripe Checkout session."""
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debugging: print the data
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': data['price_id'],  # Dynamically pass the price ID
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://127.0.0.1:8000/success/',  # Replace with your success URL
                cancel_url='http://127.0.0.1:8000/cancel/',    # Replace with your cancel URL
            )
            return JsonResponse({'url': session.url})
        except json.JSONDecodeError as e:
            print("JSON decode error:", str(e))  # Debugging: log the error
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except stripe.error.StripeError as e:
            print("Stripe error:", str(e))  # Debugging: log the error
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print("General error:", str(e))  # Debugging: log the error
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)