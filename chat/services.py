from properties.models import Property
from favorites.models import Favorite
from enquiries.models import Enquiry


def chatbot_reply(user, message):

    msg = message.lower()

    # PROPERTY SEARCH
    if "search property" in msg or "find property" in msg:

        properties = Property.objects.all()[:5]

        data = []

        for p in properties:
            data.append({
                "title": p.title,
                "price": p.price,
                "bedrooms": p.bedrooms
            })

        return {
            "type": "property_list",
            "data": data
        }


    # FAVORITES
    elif "my favorites" in msg:

        favs = Favorite.objects.filter(user=user)

        data = []

        for f in favs:
            data.append({
                "title": f.property.title,
                "price": f.property.price
            })

        return {
            "type": "favorites",
            "data": data
        }


    # INQUIRY HELP
    elif "send inquiry" in msg:

        return {
            "type": "text",
            "message": "To send inquiry open property detail and click 'Send Inquiry'."
        }


    # SUBSCRIPTION
    elif "subscription" in msg:

        return {
            "type": "text",
            "message": "You can subscribe to premium plan from Subscription section."
        }


    # PAYMENT
    elif "payment" in msg:

        return {
            "type": "text",
            "message": "Payments are processed securely using our payment gateway."
        }


    # DEFAULT RESPONSE
    return {
        "type": "text",
        "message": "Hello 👋 I can help you with property search, favorites, inquiries, subscriptions and payments."
    }