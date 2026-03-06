# Reviews API Documentation (JWT Authentication)

This document explains how to test the **Reviews API** using **Postman** with **JWT Authentication**.

Base URL:

```
http://127.0.0.1:8000
```

---

## 1. Start Server

Run the Django server:

```
python manage.py runserver
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 2. JWT Authentication

All APIs require authentication.

First generate an access token.

### Login API

**Method**

```
POST
```

**URL**

```
http://127.0.0.1:8000/api/token/
```

**Body → Raw → JSON**

```
{
 "email": "admin@gmail.com",
 "password": "admin123"
}
```

### Response Example

```
{
 "refresh": "REFRESH_TOKEN",
 "access": "ACCESS_TOKEN"
}
```

Copy the **ACCESS_TOKEN**.

---

## 3. Add Token in Postman

For every API request:

Go to **Headers**

Add:

```
Key: Authorization
Value: Bearer ACCESS_TOKEN
```

Example:

```
Authorization : Bearer eyJhbGciOiJIUzI1Ni...
```

---

## 4. Create Review

Creates a new review.

**Method**

```
POST
```

**URL**

```
http://127.0.0.1:8000/api/reviews/
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
Content-Type : application/json
```

**Body**

```
{
 "property": "PROPERTY_UUID",
 "reviewer": "USER_UUID",
 "rating": 4,
 "comment": "Very good property with nice location"
}
```

---

## 5. Get All Reviews

Returns all reviews.

**Method**

```
GET
```

**URL**

```
http://127.0.0.1:8000/api/reviews/
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
```

---

## 6. Get Reviews by Property

Returns reviews for a specific property.

**Method**

```
GET
```

**URL**

```
http://127.0.0.1:8000/api/reviews/?property_id=PROPERTY_UUID
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
```

---

## 7. Get Single Review

Returns one review.

**Method**

```
GET
```

**URL**

```
http://127.0.0.1:8000/api/reviews/REVIEW_UUID/
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
```

---

## 8. Update Review

Updates a review.

**Method**

```
PUT
```

**URL**

```
http://127.0.0.1:8000/api/reviews/REVIEW_UUID/
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
Content-Type : application/json
```

**Body**

```
{
 "property": "PROPERTY_UUID",
 "reviewer": "USER_UUID",
 "rating": 5,
 "comment": "Updated review"
}
```

---

## 9. Delete Review

Deletes a review.

**Method**

```
DELETE
```

**URL**

```
http://127.0.0.1:8000/api/reviews/REVIEW_UUID/
```

**Headers**

```
Authorization : Bearer ACCESS_TOKEN
```

---

## 10. Refresh Token

Generate a new access token if expired.

**Method**

```
POST
```

**URL**

```
http://127.0.0.1:8000/api/token/refresh/
```

**Body**

```
{
 "refresh": "REFRESH_TOKEN"
}
```

---

## 11. Important Notes

* JWT Authentication is required for all APIs.
* Token must be included in request headers.
* Rating must be an integer value.
* Reviewer ID must match the logged-in user.
* Access token expires after configured time.
* Generate a new token if expired.

---

## 12. API Endpoints Summary

```
POST   /api/token/
POST   /api/token/refresh/

GET    /api/reviews/
POST   /api/reviews/

GET    /api/reviews/{id}/
PUT    /api/reviews/{id}/
DELETE /api/reviews/{id}/
```

---

## 13. Example Test Data

Example Property ID:

```
96f69b10-7bb5-493a-b62e-6b5e13dc6146
```

Example User ID:

```
5dec5a9a-5149-4f91-bacd-44190636a69d
```

---

## 14. Authentication Settings

Authentication is enabled using JWT:

```
REST_FRAMEWORK = {
 "DEFAULT_AUTHENTICATION_CLASSES": (
  "rest_framework_simplejwt.authentication.JWTAuthentication",
 ),
 "DEFAULT_PERMISSION_CLASSES": (
  "rest_framework.permissions.IsAuthenticated",
 )
}
```

---

## 15. Token Lifetime Settings

```
SIMPLE_JWT = {
 "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
 "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
```

---

## 16. Testing Order

Recommended testing sequence:

1. Start server
2. Generate token
3. Add token in headers
4. Create review
5. Get reviews
6. Update review
7. Delete review
8. Refresh token if expired

---
