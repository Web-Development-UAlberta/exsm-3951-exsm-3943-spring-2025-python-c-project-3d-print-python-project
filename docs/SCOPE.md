# Project Scope Document

## Project Title

**Custom 3D Products Store**

## Project Duration

**6 Weeks (Part-Time, School Project)**

## Team Size

4 Members

## 🧠 Project Vision

> “I have this amazing vision for an online store that sells customized 3D printed products. Customers will be able to pick any 3D model from our library, choose the color and material they want it printed in, and get an instant quote.
>
> We need to make sure turnaround times are accurate based on what materials we have in stock. If we're low on a certain filament color, we'll need to account for the extra time to order more. Maybe there could be an option for customers to pay a fee to expedite their order too?
>
> User accounts are a must. Customers should be able to easily create profiles, save their preferences and payment info, and track their orders from start to finish.
>
> Then on the backend, we'll need a solid system for managing inventory levels, updating stock as orders come in, and flagging when we're low so we can reorder materials proactively. Fulfillment and pseudo-payment processing will be key pieces too.”

## ✅ In Scope

These features reflect the client’s core goals and are realistic to build within 6 weeks.

### Customer Features

- Select 3D models from a library (preloaded)
- Choose color and material options
- Get instant quote based on a fixed formula
- User registration and login
- View past orders and order status (e.g., Ordered → Printing → Shipped)

### 🛠️ Admin & Backend Features

- Track filament stock by color and material
- Display low-stock warnings (manual restock only)
- User dashboard to view/manage orders
- Fulfillment status updates (mark as "Shipped")
- Simple quote generation logic based on model + material
- Pseudo-checkout confirmation (no real payments)

## ❌ Out of Scope

These items are mentioned or implied in the client pitch, but are out of scope due to technical complexity and/or project time constraints.

**1. Real Payment Processing**  
Client mentioned: "Save payment info" and "Pseudo-payment processing will be key pieces too."

- We will not integrate Stripe, PayPal, or any real payment gateways.
- We will not store any sensitive payment information.
- Instead, we'll use a fake checkout confirmation page to simulate payment.

**2. Full Fulfillment & Shipping Integration**  
Client mentioned: "Fulfillment will be key pieces too."

- We will not integrate with shipping providers like UPS or FedEx.
- There will be no real-time package tracking or shipping APIs.
- For fulfillment, we will provide simple Canada Post shipping estimates within Canada based on postal code regions.
- For international orders, we’ll show a general 3+ week delivery window, subject to local shipping providers.
- Live tracking will not be available.

**3. Secure Storage of Payment Preferences**  
Client mentioned: "Save their preferences and payment info."

- We will not store any actual credit card data or secure payment tokens.
- Instead, users may optionally enter their "preferred payment method" as plain text for display only (for example, Visa, Apple Pay or PayPal).

## Notes

This scope outlines a realistic and achievable plan for our six-week timeline. Certain features have been excluded to ensure the team can focus on building a reliable, well-executed product that meets the core requirements.
