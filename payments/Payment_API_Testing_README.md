# RealEstate Payment API – Postman Testing Guide

This README explains **step-by-step** how to test the complete Payment module:

- JWT Authentication Token
- Create Payment (Pending)
- My Payments (History)
- Admin Update Payment Status
- Payment Webhook Simulation

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

## 2. Get JWT Token (Login)

Payment APIs require authentication.

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

## 3. Create Payment API (Status = Pending)

### Request

**POST**

```
http://127.0.0.1:8000/api/v1/payments/create/
```

### Authorization Tab

Type:

```
Bearer Token
```

Paste your access token.

### Body → raw JSON

```json
{
  "subscription_id": "YOUR_SUBSCRIPTION_UUID",
  "amount": 999,
  "currency": "INR",
  "gateway": "demo"
}
```

### Response

```json
{
  "payment": {
    "id": "PAYMENT_UUID",
    "status": "pending"
  }
}
```

Copy the payment id.

---

## 4. View My Payments (History)

### Request

**GET**

```
http://127.0.0.1:8000/api/v1/payments/my/
```

### Authorization

Bearer Token required.

### Response

```json
[
  {
    "id": "PAYMENT_UUID",
  "amount": "999.00",
    "status": "pending"
  }
]
```

---

## 5. Admin Update Payment Status API

Only admin users can update status manually.

### Request

**PATCH**

```
http://127.0.0.1:8000/api/v1/payments/<payment_id>/status/
```

### Authorization

Use **Admin Bearer Token**

### Body

```json
{
  "status": "success"
}
```

Allowed values:

- pending
- success
- failed
- refunded

---

## 6. Payment Webhook API (Gateway Simulation)

Webhook simulates Razorpay/Stripe confirmation.

### Request

**POST**

```
http://127.0.0.1:8000/api/v1/payments/webhook/
```

### Authorization

Webhook uses:

```
No Auth
```

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
  "new_status": "success"
}
```

---

## 7. Verify Payment Status in Database (Optional)

Run:

```powershell
python manage.py shell
```

```python
from payments.models import Payment

p = Payment.objects.last()
print(p.id, p.status)
```

---

## Common Errors

### Authentication credentials not provided

You forgot:

```
Authorization: Bearer <token>
```

### Invalid webhook secret

Missing header:

```
X-WEBHOOK-SECRET: mydemo123
```

### Payment not found

Wrong payment_id or payment does not exist.

---

## Done ✅

Now you can fully test:

- Payment creation
- Payment history
- Admin status update
- Webhook confirmation flow
