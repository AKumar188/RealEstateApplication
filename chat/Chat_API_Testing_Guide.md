# Chat API Testing Guide (Postman + JWT Authentication)

## Base URL

    http://127.0.0.1:8000/

------------------------------------------------------------------------

# 1️⃣ Get JWT Access Token (Login)

### Endpoint

    POST /api/token/

### Body (JSON)

``` json
{
    "email": "your_email_here",
    "password": "your_password_here"
}
```

### Response

``` json
{
    "refresh": "xxxx",
    "access": "yyyy"
}
```

👉 Copy the **access token**.

------------------------------------------------------------------------

# 2️⃣ Add Authorization Header in Postman

Go to **Headers** tab:

    Key: Authorization
    Value: Bearer your_access_token_here

Example:

    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

------------------------------------------------------------------------

# 3️⃣ Create Conversation

### Endpoint

    POST /api/chat/conversations/

### Body

``` json
{
    "property": "property_uuid_here",
    "owner": "owner_uuid_here"
}
```

------------------------------------------------------------------------

# 4️⃣ List Conversations

### Endpoint

    GET /api/chat/conversations/

------------------------------------------------------------------------

# 5️⃣ Send Message

### Endpoint

    POST /api/chat/conversations/{conversation_id}/send_message/

### Body

``` json
{
    "message_type": "text",
    "content": "Is the property still available?"
}
```

------------------------------------------------------------------------

# 6️⃣ Get Messages

### Endpoint

    GET /api/chat/conversations/{conversation_id}/messages/

------------------------------------------------------------------------

# 7️⃣ Mark Messages as Read

### Endpoint

    PATCH /api/chat/conversations/{conversation_id}/mark_read/

------------------------------------------------------------------------

# 8️⃣ Delete Conversation

### Endpoint

    DELETE /api/chat/conversations/{conversation_id}/

------------------------------------------------------------------------

# 🔥 Proper Testing Flow

1.  Login as Buyer → Get token\
2.  Create conversation\
3.  Send message\
4.  Login as Owner → Get token\
5.  List conversations\
6.  Get messages\
7.  Mark as read

------------------------------------------------------------------------

# ⚠ Common Errors

  Error              Reason
  ------------------ --------------------------
  401 Unauthorized   Missing or invalid token
  403 Forbidden      Not buyer or owner
  404 Not Found      Invalid conversation ID
  400 Bad Request    Missing required field

------------------------------------------------------------------------

Your Chat API is now fully testable using Postman with JWT
authentication.
