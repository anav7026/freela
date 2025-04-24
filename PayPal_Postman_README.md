
# 🧾 Freela x PayPal Sandbox Integration – Developer Update for Andrew

Hi Andrew 👋,

This document outlines the progress I've made integrating **PayPal Sandbox** into our **Freela** project, how it connects with Postman and our tech stack (Flask, PostgreSQL via Docker/DBeaver).

---

## 🔧 Tools Used
- **Flask** – Handles backend logic for endpoints and PayPal token requests
- **Docker** – Running our services and PostgreSQL containerized
- **DBeaver** – Visual DB tool for managing PostgreSQL schemas and testing queries
- **Postman** – Used to simulate PayPal API calls and debug requests
- **PayPal Developer Dashboard** – Managing sandbox credentials and test accounts

---

## 🔐 PayPal Sandbox App Setup

I created a PayPal **Sandbox app** in the developer portal.

- **Client ID**: AS65CQOi1NgNfqFsEdrSWxOww7AOiV6EtR3A2H8BVQisHBQ7ratHjABN7mI4s3XHC_UcZwRREMXZE4I6
- **Secret ID**: EHnAi6d-XyQDKXAB-pjL0IljAohrRbfUjSE10q7h7uDx04MZspfsxtBbL04j5_ezx6NuaGCeLwp0pPxc

These credentials allow us to authenticate with the API and retrieve `access_token`s for test users and transactions.

---

## 📬 Postman API Testing Workflow

I configured Postman with a complete testing flow:

### 1. 🌟 Generate Access Token
**Endpoint:**  
`POST https://api-m.sandbox.paypal.com/v1/oauth2/token`

**Authorization:**
- Type: Paypal
- Username: Your **Client ID**
- Password: Your **Secret ID**

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
```

**Body (x-www-form-urlencoded):**
```
grant_type=client_credentials
```

**Result:** Returns `access_token`, which is used in all other calls.

---

### 2. 👤 Get Basic User Info (from Sandbox)
**Endpoint:**  
`GET https://api-m.sandbox.paypal.com/v1/identity/oauth2/userinfo?schema=paypalv1.1`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Returns:**
- `user_id`
- `sub`
- "payer_id": "KEWBKRRFHLYA2",
- "businessName": "",
- "businessCategory": "",
- "businessSubCategory": "",
- "business_address": {}
---


## 👤 Sandbox Test Accounts Created 
Samples in PDF Format inside Sandbox Test Account Folder 


---

## 🧠 How This Will Work in Freela?? 

Question:  Unclear how much information I can use from PAYPAL Sandbox? I had some errors with names and other attributes. 

Question: Sandbox had an invoicing system, which I thought was cool/useful. 

Question: Will all accounts be sandbox personal accounts, and then there is one business account they run under? 




## 🗃️ PostgreSQL Integration Plan / Questions

We'll use Postgres (via Docker) to persist:

- User details (including PayPal sandbox mappings)
  -  **To Do** have to change user details in class and database

- Transactions and payment history
  -  **To Do** : Edit/ Change attritubes in Transaction/Payments History
  
- Client/freelancer role associations
  -  **To Do** : Add this to user attributes
  
- Financial metadata for analytics/tax reporting
  -  **Question**: How much information do I have access to with PayPalAPI?
  
---

---

Thanks again for reviewing!  
Let me know if you want to go over anything in more detail.  
— **Ana**
