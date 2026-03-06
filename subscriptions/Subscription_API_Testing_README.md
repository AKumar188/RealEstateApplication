# RealEstate Subscription API – Postman Testing Guide

This README explains **step-by-step** how to test the complete Subscription module:

- List Subscription Plans
- Subscribe to a Plan (Creates Payment)
- Activate Subscription via Payment Webhook

---

## 1. Start the Django Server

Run:

```powershell
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```

---

## 2. Create Subscription Plans in Database (Required)

Before testing, plans must exist.

Run:

```powershell
python manage.py shell
```

Then:

```python
from subscriptions.models import SubscriptionPlan

SubscriptionPlan.objects.create(
    name="Basic Plan",
    price=999,
    duration_days=30,
    property_limit=5,
    is_active=True
)

SubscriptionPlan.objects.create(
    name="Premium Plan",
    price=1999,
    duration_days=90,
    property_limit=20,
    is_active=True
)

print("Plans Created Successfully!")
```

Exit shell:

```python
exit()
```

---

## 3. Get JWT Token (Login)

Subscribe API requires authentication.

### Request

**POST**

```
http://127.0.0.1:8000/api/token/
```

### Body → raw JSON

```json
{
  "email": "admin@gmail.com",
  "password": "yourpassword"
}
```

### Response

```json
{
  "access": "xxxxx",
  "refresh": "yyyyy"
}
```

Copy the **access token**.

---

## 4. List Subscription Plans API

### Request

**GET**

```
http://127.0.0.1:8000/subscription/plans/
```

### Authorization

No Auth required.

### Response

```json
{
  "success": true,
  "plans": [
    {
      "id": "PLAN_UUID",
      "name": "Basic Plan",
      "price": "999.00",
      "duration_days": 30
    }
  ]
}
```

Copy one plan id.

---

## 5. Subscribe to Plan API

This API creates:

- Subscription (pending)
- Payment (pending)

### Request

**POST**

```
http://127.0.0.1:8000/subscription/subscribe/
```

### Authorization

Bearer Token required.

### Body

```json
{
  "plan_id": "PLAN_UUID"
}
```

### Response

```json
{
  "success": true,
  "message": "Subscription created. Complete payment to activate.",
  "subscription": {
    "id": "SUBSCRIPTION_UUID",
    "status": "pending"
  },
  "payment": {
    "id": "PAYMENT_UUID",
    "status": "pending"
  }
}
```

Copy the payment id.

---

## 6. Activate Subscription via Payment Webhook

Webhook simulates payment gateway confirmation.

### Request

**POST**

```
http://127.0.0.1:8000/api/v1/payments/webhook/
```

### Authorization

Webhook uses No Auth.

### Headers

Add:

| Key | Value |
|-----|------|
| Content-Type | application/json |
| X-WEBHOOK-SECRET | mydemo123 |

### Body

```json
{
  "payment_id": "PAYMENT_UUID",
  "status": "success"
}
```

### Response

```json
{
  "success": true,
  "message": "Webhook processed successfully",
  "payment": {
    "status": "success"
  }
}
```

Now the subscription becomes active.

---

## 7. Verify Subscription Status in Database (Optional)

Run:

```powershell
python manage.py shell
```

```python
from subscriptions.models import Subscription

s = Subscription.objects.last()
print(s.status)
```

Output:

```
active
```

---

## Common Errors

### Authentication credentials not provided

You forgot:

```
Authorization: Bearer <token>
```

### Plan not found or inactive

The plan_id is wrong or is_active=False.

### Invalid webhook secret

Missing header:

```
X-WEBHOOK-SECRET: mydemo123
```

---

## Done ✅

Now you can fully test:

- Subscription Plans Listing
- Subscription + Payment Creation
- Payment Webhook Activation Flow
