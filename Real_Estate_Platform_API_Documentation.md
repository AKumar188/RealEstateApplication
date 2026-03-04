# 🏠 Real Estate Platform API

Production-Grade Scalable Backend API (Django + DRF)

------------------------------------------------------------------------

# 📌 Overview

A production-ready real estate platform backend supporting:

-   JWT Authentication
-   Role-based Users (Buyer, Owner, Agent)
-   Property Listings & Advanced Filtering
-   Favorites System
-   Reviews & Ratings
-   Real-Time Chat System
-   Property Inquiries
-   Notifications
-   Subscription & Payments
-   Admin Moderation System

------------------------------------------------------------------------

# 🌐 Base URL

Development:

    http://127.0.0.1:8000/api

Production:

    https://api.yourdomain.com/api/v1

------------------------------------------------------------------------

# 🔐 Authentication

Uses JWT Bearer Token Authentication.

Add header:

    Authorization: Bearer <access_token>

------------------------------------------------------------------------

# 🔑 AUTH APIs

  Method   Endpoint                Description
  -------- ----------------------- -----------------
  POST     /auth/register          Register user
  POST     /auth/login             Login
  POST     /auth/refresh-token     Refresh token
  POST     /auth/logout            Logout
  POST     /auth/forgot-password   Forgot password
  POST     /auth/reset-password    Reset password

------------------------------------------------------------------------

# 👤 USER APIs

  Method   Endpoint      Description
  -------- ------------- ------------------
  GET      /users/me     Get current user
  PUT      /users/me     Update profile
  GET      /users/{id}   Public profile

------------------------------------------------------------------------

# 🏡 PROPERTY APIs

  Method   Endpoint                  Description
  -------- ------------------------- -------------------
  GET      /properties               Search properties
  POST     /properties               Create property
  GET      /properties/my-listings   My listings
  GET      /properties/{id}          Property detail
  PUT      /properties/{id}          Update property
  DELETE   /properties/{id}          Delete property
  PATCH    /properties/{id}/status   Change status

------------------------------------------------------------------------

# ⭐ FAVORITES

  Method   Endpoint
  -------- --------------------------
  GET      /favorites
  POST     /favorites/{property_id}
  DELETE   /favorites/{property_id}

------------------------------------------------------------------------

# ⭐ REVIEWS SYSTEM

## Rules

-   Only verified buyers can review
-   One review per user per property
-   Rating required (1--5)
-   Owner cannot review own property

## Endpoints

  Method   Endpoint
  -------- --------------------------
  POST     /properties/{id}/reviews
  GET      /properties/{id}/reviews
  GET      /reviews/my
  PUT      /reviews/{id}
  DELETE   /reviews/{id}

## Review Model

-   id (UUID)
-   property (FK)
-   user (FK)
-   rating (1--5)
-   comment
-   created_at
-   updated_at

------------------------------------------------------------------------

# 💬 CHAT SYSTEM

Secure buyer-owner communication.

## Endpoints

  Method   Endpoint
  -------- ---------------------------------------
  GET      /chat/conversations
  POST     /chat/conversations
  DELETE   /chat/conversations/{id}
  GET      /chat/conversations/{id}/messages
  POST     /chat/conversations/{id}/send-message
  PATCH    /chat/conversations/{id}/mark-read

## Conversation Model

-   id (UUID)
-   property (FK)
-   buyer (FK)
-   owner (FK)
-   created_at

## Message Model

-   id (UUID)
-   conversation (FK)
-   sender (FK)
-   message_type (text/image/video)
-   content
-   media_url
-   is_read
-   created_at

------------------------------------------------------------------------

# 📩 INQUIRIES

  Method   Endpoint
  -------- ----------------------------
  POST     /properties/{id}/inquiries
  GET      /properties/{id}/inquiries
  GET      /inquiries/my

------------------------------------------------------------------------

# 🔔 NOTIFICATIONS

  Method   Endpoint
  -------- --------------------------
  GET      /notifications
  PATCH    /notifications/{id}/read

------------------------------------------------------------------------

# 💳 SUBSCRIPTIONS

  Method   Endpoint
  -------- -------------------------
  GET      /subscription/plans
  POST     /subscription/subscribe

------------------------------------------------------------------------

# 💰 PAYMENTS

  Method   Endpoint
  -------- ------------------------
  POST     /payments/create-order
  POST     /payments/webhook

------------------------------------------------------------------------

# 🛠 ADMIN APIs

  Method   Endpoint
  -------- --------------------------------
  GET      /admin/users
  PATCH    /admin/users/{id}/block
  GET      /admin/properties
  PATCH    /admin/properties/{id}/approve
  PATCH    /admin/properties/{id}/reject

------------------------------------------------------------------------

# 🗂 Data Models Overview

## 👤 User

-   id (UUID)
-   email
-   phone
-   role (buyer, owner, agent)
-   is_verified

## 🏡 Property

-   id (UUID)
-   title
-   description
-   price
-   bedrooms
-   bathrooms
-   listing_type (sale, rent)
-   property_type (apartment, villa, plot, commercial)

------------------------------------------------------------------------

# 🧱 Architecture

-   Django
-   Django REST Framework
-   PostgreSQL (Recommended for production)
-   JWT Authentication
-   Scalable App-Based Structure
-   Role-Based Permissions
-   Production-Ready Design

------------------------------------------------------------------------

# 🚀 Testing Guide (Quick)

1.  Register user
2.  Login → Get access token
3.  Add Authorization header
4.  Create property
5.  Start chat
6.  Add review
7.  Test subscription
8.  Verify admin moderation

------------------------------------------------------------------------

# 📈 Future Enhancements

-   Real-time WebSocket chat (Django Channels)
-   Redis caching
-   Elasticsearch property search
-   Background tasks (Celery)
-   Docker + CI/CD
-   API Documentation via Swagger

------------------------------------------------------------------------

© 2026 Real Estate Platform API Production-Ready Backend System
