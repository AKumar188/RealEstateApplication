# 🏠 Real Estate Platform API

Production-Grade Real Estate Platform API

---

## 🚀 Features

- JWT Authentication (Register, Login, Refresh, Logout)
- User Profile Management
- Property Listing & Advanced Search
- Favorites System
- Property Inquiries
- Notifications
- Subscription Plans
- Payment Integration
- Admin Management
- Production-ready scalable structure

---

## 🌐 Base URL

```
https://api.yourdomain.com/api/v1
```

---

## 🔐 Authentication

This API uses JWT Bearer Token authentication.

Add token in request header:

```
Authorization: Bearer <access_token>
```

---

# 📌 API Endpoints

---

## 🔑 Auth

- `POST /auth/register` – Register user
- `POST /auth/login` – Login
- `POST /auth/refresh-token` – Refresh token
- `POST /auth/logout` – Logout
- `POST /auth/forgot-password` – Forgot password
- `POST /auth/reset-password` – Reset password

---

## 👤 Users

- `GET /users/me` – Get current user
- `PUT /users/me` – Update profile
- `GET /users/{id}` – Public profile

---

## 🏡 Properties

- `GET /properties` – Search properties
- `POST /properties` – Create property
- `GET /properties/my-listings` – My listings
- `GET /properties/{id}` – Property detail
- `PUT /properties/{id}` – Update property
- `DELETE /properties/{id}` – Delete property
- `PATCH /properties/{id}/status` – Change status

---

## ⭐ Favorites

- `GET /favorites` – Get my favorites
- `POST /favorites/{property_id}` – Add favorite
- `DELETE /favorites/{property_id}` – Remove favorite

---

## 📩 Inquiries

- `POST /properties/{id}/inquiries` – Create inquiry
- `GET /properties/{id}/inquiries` – Owner inquiries
- `GET /inquiries/my` – My inquiries

---

## 🔔 Notifications

- `GET /notifications` – Get notifications
- `PATCH /notifications/{id}/read` – Mark as read

---

## 💳 Subscriptions

- `GET /subscription/plans` – List plans
- `POST /subscription/subscribe` – Subscribe to plan

---

## 💰 Payments

- `POST /payments/create-order` – Create payment order
- `POST /payments/webhook` – Payment webhook endpoint

---

## 🛠 Admin

- `GET /admin/users` – List users
- `PATCH /admin/users/{id}/block` – Block user
- `GET /admin/properties` – List all properties
- `PATCH /admin/properties/{id}/approve` – Approve property
- `PATCH /admin/properties/{id}/reject` – Reject property

---

# 📊 Data Models

## 👤 User

- id (UUID)
- email
- phone
- role (buyer, owner, agent)

## 🏡 Property

- id (UUID)
- title
- description
- price
- bedrooms
- bathrooms
- listing_type (sale, rent)
- property_type (apartment, villa, plot, commercial)

---






