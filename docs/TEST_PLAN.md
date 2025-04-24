# Custom 3D Products Store – Test Plan

## 1. Introduction

This test plan outlines the testing strategy for the 3D Printing E-Commerce Platform to ensure all in-scope features operate correctly and meet requirements. The plan covers both customer-facing and admin features while respecting the defined scope limitations. 

### 1.1 Testing Objectives
+	Verify all in-scope features function as expected
+	Ensure the system handles normal and boundary conditions appropriately
+	Confirm integration between frontend, backend, and database components
+	Validate that out-of-scope features are properly exclude

### 1.2 References
+ Design Document
+ Scope Document
+ Project Requirements
+ ERD


## 2. Test Scope

### 2.1 Features to be Tested

Testing the features and functionalities as designed in the Scope and design document which includes: 

+ User Management 
+ Product Customization
+ Inventory Management
+ Order Processing
+ Admin Dashboard

### 2.2 Features Not to be Tested
+	Third-party integrations with actual payment gateways
+	Physical printing process
+	Shipping carrier integrations
+	Physical hardware compatibility


## 3. Test Strategy

### 3.1 Testing Levels and types

The following testing levels will be implemented:
+ Unit Testing: Testing individual components or functions
+ Integration Testing: Testing the interaction between integrated components
+ System Testing: Testing the entire system as a whole.
+ Functional Testing: Verifying that each function operates according to requirements
+ Usability Testing: Evaluating the user interface and user experience

### 3.2 Testing Approach

+ Test cases will be developed based on the requirements, considering the design and scope documents.
+ Automated testing will be used where possible
+ Manual testing will be performed for complex scenarios and usability testing


## 4. Test Types

### 4.1 Unit Testing

#### Customer Features
	
Model Selection Library 
+ Test model loading and display
+ Verify filtering and sorting capabilities
+ Validate model details display correctly

Color and Material Selection 
+ Test color/material option rendering
+ Verify combinations are correctly applied to models

Quote Generation 
+ Test calculation formula accuracy
+ Verify price updates when options change
+ Test edge cases (very large models, special materials)

User Authentication 
+ Test registration form validation
+ Verify login/logout functionality

Order History 
+ Test order history listing and filtering

#### Admin Features

Inventory Management 
+ Test filament stock tracking
+ Verify stock deduction on order processing
+ Test low-stock warning thresholds
+ Test CSV upload for materials and 3D objects
+ Test automatic inventory deduction

Order Management 
+ Test order listing and search
+ Verify status update functionality
+ Test order detail views

User management
+ Test change/update user information
+ Test add/delete user

### 4.2 Integration Testing

End-to-End User Flow 
+ Complete user registration
+ Browse and select 3D models
+ Customize with colors/materials
+ Receive quote and proceed to checkout
+ Complete pseudo-checkout
+ View order in history

Admin Order Processing Flow 
+ New order notification
+ Order status updates
+ Inventory adjustments when fulfilling orders
+ Order shipment marking

Database Integration 
+ Verify data consistency across transactions
+ Test database locking and concurrency handling
+ Validate relationship integrity between entities

### 4.3 User Interface Testing

Accessibility Testing 
+ Verify WCAG 2.1 AA compliance
+ Validate screen reader compatibility


## 5. Test Environment

### 5.1 Software Requirements
+ Operating Systems: Windows, macOS
+ Browsers: Chrome, Edge
+ Backend: Python 3.9+, Django 4.0+
+ Database: MySQL 8.0+
+ Frontend: Node.js 16+, React 18+, Next.js 13+

## 6. Test Cases

### 6.1 Customer Facing pages

#### Home Page

| Test ID       | Description                    | Expected Result                                                    | Priority |
|---------------|--------------------------------|--------------------------------------------------------------------|----------|
| CF-HOME-01    | Load homepage successfully     | Homepage loads with hero banner, featured products, and navigation | High     |
| CF-HOME-02    | Navigation links work          | Clicking Shop / Catalog / Customization/ Cart / Orders/ Profile redirects correctly   | High     |
| CF-HOME-03    | Logo redirects to Home         | Clicking Logo button re-directs to Home page                       | Medium   |
| CF-HOME-04    | Login link works               | Clicking Login button redirects to Login page correctly            | High     |
---

#### Product Customization Page

| Test ID       | Description                    | Expected Result                                                | Priority |
|---------------|--------------------------------|----------------------------------------------------------------|----------|
| CF-CAT-01     | Display product list           | All products appear with name, price, image                    | High     |
| CF-CAT-02     | Search                         | Able to search the products and the correct products load      | Medium   |
| CF-CAT-03     | Logo redirects to Home         | Clicking Logo button re-directs to Home page                   | Medium   |
| CF-CAT-04     | Navigation Link works          | Clicking Home/Products/About us/ Contact us redirects correctly| High     |
| CF-CAT-05     | Products from each category loads| Clicking on products category on the left side of the page loads all the products from that category | High |
| CF-CAT-06     | Product Selection              | Selecting the products add the product to the Product selection section on the right | High |
| CF-CAT-07  | Delete selection                  | Clicking on the delete button deletes the product from the selection | High |
| CF-CAT-08  | Cart checkout                     | Clicking on cart icon redirects to the checkout page                | High |

---

#### Checkout Page

| Test ID      | Description                             | Expected Result                                              | Priority |
|--------------|-----------------------------------------|---------------------------------------------------------------|----------|
| CF-CHECKOUT-01  | Page loads with items in bag            | Checkout page displays product(s), subtotal, and checkout button | High     |
| CF-CHECKOUT-02  | Increase quantity                       | Quantity increases by 1; subtotal updates                     | High     |
| CF-CHECKOUT-03  | Decrease quantity                       | Quantity decreases by 1 (not below 1); subtotal updates       | High     |
| CF-CHECKOUT-04  | Subtotal calculation                    | Subtotal correctly reflects total cost                        | High     |
| CF-CHECKOUT-05  | Proceed to checkout                     | Redirects to payment (Mock)                        | High     |
| CF-CHECKOUT-06  | Responsive layout                       | Page remains readable and interactive                         | Medium   |
| CF-CHECKOUT-07  | Newsletter subscription - valid email   | Confirmation message displayed                                | Medium   |
| CF-CHECKOUT-08  | Newsletter subscription - invalid email | Error message displayed                                       | Medium   |

---

#### Order History Page

| Test ID       | Description                             | Expected Result                                               | Priority |
|---------------|-----------------------------------------|----------------------------------------------------------------|----------|
| CF-ORDERS-01     | Page loads successfully                 | Displays user name and list of past orders                    | High     |
| CF-ORDERS-02     | Display processing orders               | Shows "Processing" section with items and total               | High     |
| CF-ORDERS-03     | Display shipping orders                 | Shows "Shipping" section with items and total                 | High     |
| CF-ORDERS-04     | Display completed orders                | Shows "Completed" section with items and total                | High     |
| CF-ORDERS-05     | Sign out link                           | User is logged out and redirected to login page               | High     |
| CF-ORDERS-06     | Responsive layout                       | Page layout adjusts properly                                  | Medium   |
| CF-ORDERS-07     | Newsletter subscription                 | Confirmation shown for valid email, error for invalid         | Medium   |
| CF-ORDERS-08     | Navigation Links                | All Navigation links work         | Medium   |
----

#### Login Page

| Test ID       | Description                             | Expected Result                                        | Priority |
|---------------|-----------------------------------------|--------------------------------------------------------|----------|
| CF-LOGIN-01      | Load login page                      | Login page loads with logo, nav bar, login form, and sign-up link | High     |
| CF-LOGIN-02      | Valid login credentials              | Redirect to user dashboard or home page                           | High     |
| CF-LOGIN-03      | Invalid credentials                  | Show error message "Invalid credentials"                          | High     |
| CF-LOGIN-04      | Empty fields and click sign in       | Show validation errors for both fields                            | High     |
| CF-LOGIN-05      | Only username filled                 | Show validation error for password                                | High   |
| CF-LOGIN-06      | Only password filled                 | Show validation error for username                                | High   |
| CF-LOGIN-07      | Password masking                     | Password should be hidden (masked with dots/asterisks)            | High     |
| CF-LOGIN-08      | Forgot Password link                 | Redirects to password recovery page                               | Medium   |
| CF-LOGIN-09      | Sign Up redirection                  | Redirects to registration page                                    | High     |
| CF-LOGIN-10      | Navigation links                     | Correct pages open in the same tab                                | Medium   |





