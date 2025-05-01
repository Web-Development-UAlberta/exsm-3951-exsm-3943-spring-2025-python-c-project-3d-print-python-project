# Custom 3D Products Store – Test Plan

## 1. Introduction

This test plan outlines the testing strategy for the 3D Printing E-Commerce Platform to ensure all in-scope features operate correctly and meet requirements. The plan covers both customer-facing and admin features while respecting the defined scope limitations. 

### 1.1 Testing Objectives
+	Verify all in-scope features function as expected
+	Ensure the system handles normal and boundary conditions appropriately
+	Confirm integration between frontend, backend, and database components
+	Validate that out-of-scope features are properly excluded

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
+ View order history

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
+ Frontend: React 18+, Next.js 13+

## 6. Test Cases

### 6.1 Customer Facing pages

#### Home Page

##### Normal Cases

| Test ID     | Description                 | Expected Result                                                                 | Priority |
|-------------|-----------------------------|---------------------------------------------------------------------------------|---------|
| CF-HOME-01  | Load homepage successfully  | Homepage loads with hero banner, featured products, and navigation              | High     |
| CF-HOME-02  | Navigation links work       | Clicking Shop / Catalog / Customization / Cart / Orders / Profile redirects correctly | High     |
| CF-HOME-03  | Logo redirects to Home      | Clicking Logo button redirects to Home page                                     | Medium   |
| CF-HOME-04  | Profile link works          | Clicking Profile button redirects to Login page correctly                       | High     |
| CF-HOME-05  | Search                      | Search fetches the result accurately                                            | Medium  | 

---

##### Edge Cases

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-HOME-06 | Search with special characters | System handles special characters appropriately | Medium |
| CF-HOME-07 | Very long search query | System truncates or properly handles very long search queries | Medium |
| CF-HOME-08 | Rapid navigation clicking | System handles rapid navigation clicks without errors | Low |

---

##### Fail Cases

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-HOME-09 | Network disconnection | Appropriate offline message displayed when network disconnects | Medium | 
| CF-HOME-10 | Server error on page load | Appropriate error message displayed for server errors | High |

---


#### Product Catalog / Customization Page

##### Normal Cases

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-CAT-01   | Display product list               | All products appear with name, price, and image  | High     |
| CF-CAT-02   | Search                             | Able to search products and the correct products load   | Medium   |
| CF-CAT-03   | Logo redirects to Home             | Clicking Logo button redirects to Home page             | Medium   |
| CF-CAT-04   | Navigation link works              | Clicking Home / Products / About Us / Contact Us redirects correctly   | High     |
| CF-CAT-05   | Size, color and material selection works separately   | Able to select Size, color and material by clicking on the appropriate buttons | High |
| CF-CAT-06   | Add to cart                  | Clicking add to cart adds the product with the selected Size, color and material | High   |
| CF-CAT-07 | Combined customization | All three customization options are properly saved and displayed as selected | High |
| CF-CAT-08 | Price update | Price updates according to selected customization options | High |

---

##### Edge Cases

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-CAT-09 | Option compatibility verification | Incompatible combinations are disabled/unavailable | High |
| CF-CAT-10 | Default selections | Products have appropriate default selections or clear indication to select options | Medium |
| CF-CAT-11 | Navigate away and return | Previous selections are either preserved or reset as appropriate | Medium |
| CF-CAT-12 | Multiple sequential customizations | System handles rapid changes correctly  | Low | 

---

##### Fail Cases

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-CAT-13 | Out of stock customization | Out of stock indication is shown and System prevents adding out-of-stock combination to cart | High |
| CF-CAT-14 | Model size limitation message | Error message appears when model exceeds maximum size (over 300x300x300mm) | High |
| CF-CAT-15 | Unavailable combinations | System prevents selection of invalid combinations and Appropriate error message displayed | High | 
| CF-CAT-16 | Server error during customization | Appropriate error message when customization fails | High |
| CF-CAT-17 | Add to cart without selections | System either prevents action or uses defaults with clear user notification | Medium |

---


#### Cart / Checkout Page

##### Normal Cases

| Test ID            | Description                            | Expected Result                              | Priority |
|--------------------|----------------------------------------|----------------------------------------------|----------|
| CF-CHECKOUT-01   | Page loads with items in bag     | Checkout page displays product(s), subtotal, and checkout button   | High     |
| CF-CHECKOUT-02   | Increase quantity           | Quantity increases by 1; subtotal updates                    | High     |
| CF-CHECKOUT-03   | Decrease quantity           | Quantity decreases by 1 (not below 1); subtotal updates      | High     |
| CF-CHECKOUT-04   | Subtotal calculation        | Subtotal correctly reflects total cost                       | High     |
| CF-CHECKOUT-05   | Proceed to checkout         | Redirects to payment (Mock)                                  | High     |
| CF-CHECKOUT-06   | Newsletter subscription - valid email  | Confirmation message displayed                    | Medium   |
| CF-CHECKOUT-07   | Click Home button and Logo | User is redirected to homepage                           | Medium   |
| CF-CHECKOUT-08   | Brand Name                             | Brand Name loads correctly                        | High  |
| CF-CHECKOUT-09   | Search                                 | Search loads the result accurately                | Medium   |
| CF-CHECKOUT-10   | Subscribe newsletter | Clicking on subscribe button sends an email with a successful subscription message | Medium  |

---

##### Edge Cases

| Test ID            | Description                            | Expected Result                              | Priority |
|--------------------|----------------------------------------|----------------------------------------------|----------|
| CF-CHECKOUT-11 | Attempt to reduce quantity below 1 | System prevents reduction below 1 item | High |
| CF-CHECKOUT-12 | Attempt to exceed maximum order quantity | System prevents exceeding maximum allowed quantity (limit: 10 per item) | High | 
| CF-CHECKOUT-13 | Checkout with maximum allowed quantity | System allows checkout with maximum allowed quantity (10 per item) | Medium | 
| CF-CHECKOUT-14 |Rapid quantity adjustments | System handles rapid quantity changes correctly | Medium |
| CF-CHECKOUT-15 | Session timeout during checkout | System handles timeout gracefully with proper user notification | Medium |

---

##### Fail Cases

| Test ID            | Description                            | Expected Result                              | Priority |
|--------------------|----------------------------------------|----------------------------------------------|----------|
| CF-CHECKOUT-16 | Newsletter subscription - invalid email | Error message displayed | Medium | 
| CF-CHECKOUT-17 | Newsletter subscription with empty email | Error message preventing empty submission | Medium |
| CF-CHECKOUT-18 | Out of stock during checkout | Appropriate error message displayed when item becomes unavailable | High | 
| CF-CHECKOUT-19 | Empty cart checkout attempt | System prevents checkout with empty cart | High |
| CF-CHECKOUT-20 | Network disconnection during checkout | System handles connection loss gracefully with proper error handling | High |

---


#### Profile / Orders Page

##### Normal Cases

| Test ID            | Description                            | Expected Result                                  | Priority |
|--------------------|----------------------------------------|--------------------------------------------------|----------|
| CF-ORDERS-01  | Page loads successfully       | Displays user name and list of past orders                                  | High     |
| CF-ORDERS-02  | Display processing orders     | Shows "Processing" section with items and total                             | High     |
| CF-ORDERS-03  | Display shipping orders       | Shows "Shipping" section with items and total                               | High     |
| CF-ORDERS-04  | Display completed orders      | Shows "Completed" section with items and total                              | High     |
| CF-ORDERS-05  | Sign out link                 | User is logged out and redirected to login page                             | High     |
| CF-ORDERS-06  | Click on processing order arrow            | User is redirected to processing order details page                                                | High   |
| CF-ORDERS-07 | Click on shipping order arrow | User is redirected to shipping order details page | High | 
| CF-ORDERS-08 | Click on completed order arrow | User is redirected to completed order details page | High |
| CF-ORDERS-00  | Newsletter subscription email      | Confirmation shown for valid email                       | Medium   |
| CF-ORDERS-10  | Navigation links              | All navigation links work                                                   | Medium   |
| CF-ORDERS-09  | Subscribe newsletter   | Clicking on subscribe button sends an email with a successful subscription message | Medium   |
| CF-ORDERS-10 | Click logo | User is redirected to homepage | Medium | 
| CF-ORDERS-11 | Click search icon | Search functionality activates | Medium |

---

##### Edge Cases

| Test ID            | Description                            | Expected Result                                  | Priority |
|--------------------|----------------------------------------|--------------------------------------------------|----------|
| CF-ORDERS-12 | No processing orders | "Processing" section either hidden or displays "No orders in processing" message | Medium | 
| CF-ORDERS-13 | No shipping orders | "Shipping" section either hidden or displays "No orders in shipping" message | Medium | 
| CF-ORDERS-14 | No completed orders | "Completed" section either hidden or displays "No completed orders" message | Medium | 
| CF-ORDERS-15 | No orders at all | Page displays appropriate "No orders found" message | Medium |
| CF-ORDERS-16 | Large number of orders in a category | System properly handles pagination or scrolling for many orders | Medium| 
| CF-ORDERS-17 | Very long order history | Page loads efficiently even with extensive order history| Medium |
| CF-ORDERS-18 | Orders with very high totals | Currency values display correctly for large amounts | Low |

---

##### Fail Cases

| Test ID            | Description                            | Expected Result                                  | Priority |
|--------------------|----------------------------------------|--------------------------------------------------|----------|
| CF-ORDERS-19 | Newsletter subscription with invalid email | Error shown for invalid email | Medium | 
| CF-ORDERS-20 | Server error while loading orders | Appropriate error message when orders fail to load | High | 
| CF-ORDERS-21 | Newsletter subscription with empty email | Error message preventing empty submission | Medium| 
| CF-ORDERS-22 | Session timeout | User is redirected to login page with appropriate message | High | 
| CF-ORDERS-23 | Network disconnection while on page | System handles connection loss gracefully | Medium | 
| CF-ORDERS-24 | Access profile page without authentication | User is redirected to login page | High |

---

#### Login Page

##### Normal Cases

| Test ID       | Description                    | Expected Result                                                  | Priority |
|---------------|--------------------------------|------------------------------------------------------------------|----------|
| CF-LOGIN-01   | Load login page                | Login page loads with logo, nav bar, login form, and create account link   | High     |
| CF-LOGIN-02   | Valid login credentials        | Redirect to user dashboard or home page                             | High     |
| CF-LOGIN-03   | Click logo | User is redirected to homepage | Medium |
| CF-LOGIN-04   | Click search icon | Search functionality activates | Medium | 
| CF-LOGIN-05   | Newsletter subscription with valid email | Subscription confirmation message displayed | Medium | 
| CF-LOGIN-06   | Password masking               | Password should be hidden (masked with dots/asterisks)              | High     |
| CF-LOGIN-07   | Create account redirection            | Redirects to create account page                                    | High     |
| CF-LOGIN-08   | Navigation links               | Each navigation item (Home, Catalog, Customization, Cart, Orders) redirects to correct page | Medium |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-LOGIN-09 | Tab key navigation | Form fields and buttons can be navigated in logical order using Tab key| Medium | 
| CF-LOGIN-10 | Enter key submission | Pressing Enter key while focus is in email/password field submits the form | Medium | 
| CF-LOGIN-11 | Password autocomplete | Browser's password autocomplete functions correctly | Medium | 
| CF-LOGIN-12 | Form field validation | Email field validates proper email format | High | 
| CF-LOGIN-13 | Very long email address | System handles very long email addresses appropriately | Medium | 
| CF-LOGIN-14 | Copy-paste credentials | System handles copy-paste of credentials correctly | Medium | 
| CF-LOGIN-15 | Session persistence | Login state persists appropriately according to system requirements | High | 

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-LOGIN-16 | Invalid credentials | Appropriate error message displayed for incorrect email/password | High | 
| CF-LOGIN-17 | Empty email field | Validation error shown for empty email field | High | 
| CF-LOGIN-18 | Empty password field | Validation error shown for empty password field | High | 
| CF-LOGIN-19 | Empty all fields | Validation errors shown for all required fields | High | 
| CF-LOGIN-20 | Invalid email format | Validation error shown for incorrectly formatted email | High | 
| CF-LOGIN-21 | Newsletter subscription with invalid email | Error message displayed for invalid email format | Medium | 
| CF-LOGIN-22 | Server error during authentication | Appropriate error message when login process fails | High | 
| CF-LOGIN-23 | Network disconnection during login | System handles connection loss gracefully | Medium | 

---


#### Sign up Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-ACCT-01 | Load account creation page | Page loads with logo, navigation menu (Home, Catalog, Customization, Cart, Orders), "Create Account" heading, form fields (First Name, Last Name, Email, Password), newsletter checkbox, "Create" button, and "Sign in" button | High |
| CF-ACCT-02 | Valid account creation | Account is created successfully when all fields are filled correctly and "Create" button is clicked | High |
| CF-ACCT-03 | Click "Sign in" button | User is redirected to login page | High |
| CF-ACCT-04 | Click logo | User is redirected to homepage | Medium |
| CF-ACCT-05 | Click navigation links | Each navigation item (Home, Catalog, Customization, Cart, Orders) redirects to correct page | Medium |
| CF-ACCT-06 | Click search icon | Search functionality activates | Medium |
| CF-ACCT-07 | Newsletter checkbox functionality | Checkbox toggles between checked and unchecked states | Medium |
| CF-ACCT-08 | Password field masking | Password input is masked (hidden with asterisks/dots) | High |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-ACCT-09 | Tab key navigation | Form fields and buttons can be navigated in logical order using Tab key | Medium |
| CF-ACCT-10 | Enter key submission | Pressing Enter key while focus is in any field submits the form | Medium |
| CF-ACCT-11 | Field character limits | System handles appropriate length for all fields (First Name: 2-50, Last Name: 2-50, Email: 5-100, Password: 8-64) | Medium |
| CF-ACCT-12 | Form field focus | Proper visual indication when field is selected/focused | Low |
| CF-ACCT-13 | Form accessibility | Form is navigable via keyboard and works with screen readers | High |
| CF-ACCT-14 | Special characters in name fields | System handles special characters in name fields appropriately | Medium |
| CF-ACCT-15 | Password with special characters | System accepts passwords with special characters | High |
| CF-ACCT-16 | Password with minimum/maximum length | System validates password length requirements | High |
| CF-ACCT-17 | Copy-paste functionality | System handles copy-paste into form fields correctly | Medium |
| CF-ACCT-18 | Double submission prevention | System prevents double form submission when Create button is clicked multiple times rapidly | Medium |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-ACCT-19 | Empty form submission | Validation errors shown for all required fields | High |
| CF-ACCT-20 | Empty first name field | Validation error shown for empty first name field | High |
| CF-ACCT-21 | Empty last name field | Validation error shown for empty last name field | High |
| CF-ACCT-22 | Empty email field | Validation error shown for empty email field | High |
| CF-ACCT-23 | Empty password field | Validation error shown for empty password field | High |
| CF-ACCT-24 | Invalid email format | Validation error shown for incorrectly formatted email | High |
| CF-ACCT-25 | Password too short | Validation error when password doesn't meet minimum length requirement | High |
| CF-ACCT-26 | Password complexity validation | Error if password doesn't meet complexity requirements (uppercase, number, special character) | High |
| CF-ACCT-27 | Duplicate email submission | Error message that account with email already exists | High |
| CF-ACCT-28 | First/last name too short | Error for names shorter than minimum required length | Medium |
| CF-ACCT-29 | Server error during account creation | Appropriate error message when account creation process fails | High |
| CF-ACCT-30 | Network disconnection during submission | System handles connection loss gracefully | Medium |
| CF-ACCT-31 | XSS attempt in form fields | Form sanitizes inputs and prevents XSS attacks | High |

---


#### Order Tracking Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-TRACK-01 | Load order tracking page | Page loads with logo, navigation menu (Home, Catalog, Customization, Cart, Profile), "Order History" heading, order details (number, date, shipping tier, payment method), order summary with product image and quantity, delivery address, and order cost breakdown | High |
| CF-TRACK-02 | Order number display | Order number (12345678) displays correctly | High |
| CF-TRACK-03 | Order date display | Order date (1/11/2025) displays correctly | High |
| CF-TRACK-04 | Shipping tier display | Shipping tier (Basic) displays correctly | High |
| CF-TRACK-05 | Payment method display | Payment method (E-Transfer) displays correctly | High |
| CF-TRACK-06 | Order summary display | Order summary shows product image, quantity indicator, and price | High |
| CF-TRACK-07 | Delivery address display | Delivery address shows correctly with proper formatting (name, street, city, province, country) | High |
| CF-TRACK-08 | Cost breakdown display | Order subtotal, shipping cost, and total all display with correct currency format | High |
| CF-TRACK-09 | Click logo | User is redirected to homepage | Medium |
| CF-TRACK-10 | Click navigation links | Each navigation item redirects to correct page | Medium |
| CF-TRACK-11 | Click search icon | Search functionality activates | Medium |
| CF-TRACK-12 | Product image display | Product image loads properly in order summary | Medium |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-TRACK-13 | Very long order number | System handles and displays very long order number appropriately | Medium |
| CF-TRACK-14 | Multiple items in order | System correctly displays orders with multiple items | High |
| CF-TRACK-15 | Very long product name | System handles very long product names appropriately | Medium |
| CF-TRACK-16 | Very long delivery address | System handles very long delivery addresses appropriately | Medium |
| CF-TRACK-17 | Large order total | System correctly formats and displays large monetary values | Medium |
| CF-TRACK-18 | International address format | System handles international address formats correctly | Medium |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-TRACK-19 | Invalid order number access | Appropriate error message when accessing non-existent order | High |
| CF-TRACK-20 | Access order without authentication | Redirect to login page with appropriate message | High |
| CF-TRACK-21 | Server error while loading order | Appropriate error message when order details fail to load | High |
| CF-TRACK-22 | Broken product image | Placeholder image or appropriate error when product image fails to load | Medium |
| CF-TRACK-23 | Missing order details | System handles gracefully if certain order details are missing | Medium |
| CF-TRACK-24 | Network disconnection while viewing | System handles connection loss gracefully | Medium |
| CF-TRACK-25 | Session timeout while viewing | User is redirected to login page with appropriate message | High |

---


### 6.2 Admin Pages

#### CSV Upload Page

##### Normal Cases

| Test ID        | Description                    | Expected Result                                            | Priority |
|----------------|--------------------------------|------------------------------------------------------------|----------|
| AD-CSV-01 | Load CSV upload page | Page loads with header, upload type dropdown, drag-drop area, browse button, and action buttons | High |
| AD-CSV-02      | Upload type selection          | Dropdown opens and displays available upload types         |  High    |
| AD-CSV-03      | Drag and drop functionality    | File can be successfully uploaded via drag and drop        |  High     |
| AD-CSV-04      | Browse button functionality    | File explorer opens and allows file selection              |  High |
| AD-CSV-05      | Upload valid CSV               | File accepted and prepared for validation                  |  High |
| AD-CSV-06      | Simple CSV download            | Template CSV file downloads with correct format            | Medium |
| AD-CSV-07      | Validate button functionality  | CSV validation process runs and displays results           | High |
| AD-CSV-08      | Upload button functionality    | Validated CSV uploads to the system                        | High |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-CSV-09   | CSV with maximum allowed file size       | System accepts CSV at maximum allowed size (10MB)                               | Medium   |
| AD-CSV-10   | CSV with maximum number of rows          | System handles CSV with maximum number of rows (5000)                           | Medium   |
| AD-CSV-11   | CSV with maximum number of columns       | System handles CSV with maximum number of columns (50)                          | Medium   |
| AD-CSV-12   | Different CSV delimiters                 | System correctly identifies and processes different delimiters (comma, semicolon) | Medium   |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-CSV-13   | Upload invalid file format               | Error message displayed for non-CSV file types                                  | High     |
| AD-CSV-14   | File size limit                          | Error message for files exceeding size limit (>10MB)                            | High     |
| AD-CSV-15   | Upload with no file selected             | Error message indicating no file is selected                                    | Medium   |
| AD-CSV-16   | Upload with network interruption         | Appropriate error handling and retry options                                    | Medium   |
| AD-CSV-17   | CSV with missing required fields         | Validation error highlighting missing required fields                           | High     |
| AD-CSV-18  | CSV with invalid data format             | Validation error highlighting incorrect data formats                            | High     |
| AD-CSV-19   | CSV with duplicate entries               | System identifies and reports duplicate entries                                 | Medium   |
| AD-CSV-20   | CSV with too many rows                   | Error message when CSV exceeds maximum row limit (>5000)                        | High     |
| AD-CSV-21   | CSV with corrupt data                    | Error message for corrupt or unparseable CSV                                    | High     |

---


#### User Management Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-USR-01  | Load user management page           | Page loads completely with the "User Management" header, search field, "Filter" section (with text input, Role dropdown, and Action dropdown), user table with columns "User ID", "Name", "Email", "Role", "Status", "Action", and the "Invite User" button visible. | High     |
| AD-USR-02  | Search for existing user by name    | Table displays only users whose names partially or fully match the search term.                                 | High     |
| AD-USR-03  | Search for existing user by email   | Table displays only users whose emails partially or fully match the search term.                                | High     |
| AD-USR-04  | Filter user list by text input      | Table displays only users matching the text entered in the "Filter" text field.                                 | High     |
| AD-USR-05  | Filter user list by Role            | Table displays only users whose role matches the selected option in the "Role" dropdown.                         | Medium   |
| AD-USR-06  | Filter user list by Action          | Table displays only users for whom the selected action in the "Action" dropdown is available.                     | Medium   |
| AD-USR-07  | Display details of a user           | Each row in the user table correctly displays the user's ID, Name, Email, Role, Status, and available Actions.    | High     |
| AD-USR-08  | Click the 'Invite User' button      | An 'Invite User' form or modal is displayed to the user.                                                        | High     |
| AD-USR-09  | Navigate through table pages        | When multiple users exist, the table paginates correctly, allowing navigation to different pages of users.        | Medium   |
| AD-USR-10  | Click a valid action button (e.g., 'Edit') | The corresponding action (e.g., opens the edit user form/modal for that user) is initiated.                  | High     |
| AD-USR-11  | Successfully create a new user      | A new user is created and appears in the user table with the correct details (including Role).                   | High     |
| AD-USR-12  | Edit an existing user's details     | The user's details, including Role, are updated correctly and reflected in the user table.                      | High     |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-USR-13  | Search with a very long string              | The search functionality handles the long input without errors and returns no results if no match is found.        | Medium   |
| AD-USR-14  | Search with special characters               | The search functionality handles special characters appropriately (e.g., ignores them or uses them in the search).  | Medium   |
| AD-USR-15  | Filter with a very long text input           | The filter functionality handles the long input without errors and returns no results if no match is found.          | Medium   |
| AD-USR-16  | Filter with special characters               | The filter functionality handles special characters appropriately.                                                 | Medium   |
| AD-USR-17  | Filter by a Role that has no users          | The user table displays no users, or a "No matching users found" message is shown.                               | Medium   |
| AD-USR-18  | Filter by an Action that is not available for any users | The user table displays no users, or a "No matching users found" message is shown.                      | Medium   |
| AD-USR-19  | Navigate to the last page of a long user list | The last page of users loads correctly.                                                                        | Medium   |
| AD-USR-20  | Attempt to navigate beyond the last page     | The application prevents navigation beyond the last available page (e.g., disables the 'Next' button).        | Medium   |
| AD-USR-21  | Attempt to navigate before the first page    | The application prevents navigation before the first page (e.g., disables the 'Previous' button).             | Medium   |
| AD-USR-22  | No users match the initial load criteria     | The user table area displays an appropriate message indicating that no users are currently available.             | Medium   |
| AD-USR-23  | Edit a user's details with maximum length inputs | The updated details (including Role) are saved correctly up to the maximum allowed length for each field.      | Medium   |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-USR-24  | Search for a non-existent user                   | No users are displayed in the table, or a clear "No matching users found" message is shown.                      | High     |
| AD-USR-25  | Filter by text input that matches no users       | The user table displays no users, or a clear "No matching users found" message is shown.                        | High     |
| AD-USR-26  | Filter by a Role that does not exist in the system | The "Role" dropdown should either not allow such a selection or display an error/no results message.           | High     |
| AD-USR-27  | Filter by an Action that is not valid            | The "Action" dropdown should either not allow such a selection or display an error/no results message.         | High     |
| AD-USR-28  | Attempt to save edits with invalid data          | The system displays appropriate and specific error messages for the invalid data fields, and the user details are not updated. | High     |
| AD-USR-29  | Attempt to save edits with missing required fields | The system displays error messages for the missing required fields, and the user details are not updated.       | High     |
| AD-USR-30  | Click an action button when no user is selected | The system either disables the action button or provides clear feedback that a user needs to be selected.      | High     |
| AD-USR-31  | Attempt to edit a user with fields exceeding maximum allowed length | The system prevents saving changes with input beyond the maximum allowed length and/or displays a clear error message. | High     |

---


#### Order Management Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-ORD-01 | Load order management page | Page loads with header, search field, filters, order table, and "Create New Order" button | High | 
| AD-ORD-02 | Search functionality | Matching orders are displayed based on the search input | High | 
| AD-ORD-03 | Filter by text input | Order list filters dynamically based on entered filter text | High |
| AD-ORD-04 | Filter by material | Only orders with the selected material are shown | High | 
| AD-ORD-05 | Filter by status | Only orders with the selected status are shown | High | 
| AD-ORD-06 | Filter by priority | Only orders with the selected priority are shown | High |
| AD-ORD-07 | Display order details | Order ID, Model Name, Material, Qty, Status, Priority, and Actions columns display correctly | High | 
| AD-ORD-08 | Table pagination | Table paginates correctly when order count exceeds page size | Medium |
| AD-ORD-09 | Action buttons in table | Action buttons (e.g., view, edit, cancel) function correctly | High |
| AD-ORD-11 | Order status update | Status can be updated and change is saved correctly | High |
| AD-ORD-12 | Order priority update | Priority can be updated and change is saved correctly | High
| AD-ORD-13 | Order cancellation | Cancelling an order prompts confirmation and cancels on confirmation | High |
| AD-ORD-14 | Inventory update on status change | Inventory is updated correctly based on the new order status | High |
| AD-ORD-15 | Order detail view | All order details are shown in a detail view | High |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-ORD-16 | Pagination with one more order than page limit | New page created for the extra order, UI handles edge correctly | Medium | 
| AD-ORD-17 | Filter with partial input | Results match any partial strings entered | High |
| AD-ORD-18 | Search with leading/trailing spaces | Spaces are trimmed and matching results are returned | Medium |
| AD-ORD-19 | Filtering by material not in any order | No results shown, appropriate empty state displayed | Medium |
| AD-ORD-20 | Long model names or large quantity values | Table adjusts layout or text is truncated elegantly | Medium |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-ORD-21 | Empty table state | Appropriate "No orders found" message shown if no orders match criteria | Medium |
| AD-ORD-22 | Order with insufficient inventory | Warning is displayed and user is prevented from placing the order | High |
| AD-ORD-23 | Search with unsupported characters | System handles input gracefully without crashing | Medium |
| AD-ORD-24 | Update status without required permissions | Error message displayed; change is not applied | High |
| AD-ORD-25 | Cancel order already completed | User is prevented with an appropriate warning message | High |

---


#### Inventory Management Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-INV-01  | Load inventory management page          | Page loads completely with the "Inventory Management" header, search field, "Filter" section (with text input, Material dropdown, and Quantity range input), inventory table with columns "Item ID", "Material Type", "Qty", "Cost", "Action", and the "Add New Material" button visible. | High     |
| AD-INV-02  | Search for existing item by Item ID       | Table displays only inventory items whose Item IDs partially or fully match the search term.                                                | High     |
| AD-INV-03  | Search for existing item by Material Type | Table displays only inventory items whose Material Types partially or fully match the search term.                                           | High     |
| AD-INV-04  | Filter inventory list by text input     | Table displays only inventory items matching the text entered in the "Filter" text field.                                                    | High     |
| AD-INV-05  | Filter inventory list by Material        | Table displays only inventory items whose Material Type matches the selected option in the "Material" dropdown.                               | High     |
| AD-INV-06  | Filter inventory list by Quantity        | Table displays only inventory items whose quantity falls within the range specified in the "Quantity" input fields (if applicable).          | High     |
| AD-INV-07  | Display details of an inventory item    | Each row in the inventory table correctly displays the Item ID, Material Type, Quantity, Cost, and available Actions for each item.             | High     |
| AD-INV-08  | Navigate through table pages            | When multiple inventory items exist, the table paginates correctly, allowing navigation to different pages of items.                            | Medium   |
| AD-INV-09  | Click a valid action button (e.g., 'Edit')| The corresponding action (e.g., opens the edit inventory item form/modal for that item) is initiated.                                       | High     |
| AD-INV-10  | No inventory items match initial load criteria | The inventory table area displays an appropriate message indicating that no inventory items are currently available.                       | Medium   |
| AD-INV-11  | Add a new inventory item successfully    | A new inventory item is added and appears in the inventory table with the correct details.                                                   | High     |
| AD-INV-12  | Edit an existing inventory item's details | The inventory item's details are updated correctly and reflected in the inventory table.                                                      | High     |
| AD-INV-13  | Adjust inventory quantity (increase)    | The inventory quantity for the selected item is increased correctly, and a reason for the adjustment can be recorded.         | High     |
| AD-INV-14  | Adjust inventory quantity (decrease)    | The inventory quantity for the selected item is decreased correctly, and a reason for the adjustment can be recorded.         | High     |
| AD-INV-15  | Delete an existing inventory item       | After confirmation, the inventory item is removed from the table.                                                                           | High     |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-INV-16  | Search with a very long string                 | The search functionality handles the long input without errors and returns no results if no match is found.          | Medium   |
| AD-INV-17  | Search with special characters                  | The search functionality handles special characters appropriately (e.g., ignores them or uses them in the search).    | Medium   |
| AD-INV-18  | Filter with a very long text input              | The filter functionality handles the long input without errors and returns no results if no match is found.            | Medium   |
| AD-INV-19  | Filter with special characters                  | The filter functionality handles special characters appropriately.                                                   | Medium   |
| AD-INV-20  | Filter by a Material that has no items         | The inventory table displays no items, or a "No matching items found" message is shown.                            | Medium   |
| AD-INV-21  | Filter by a Quantity range with no matching items | The inventory table displays no items, or a "No matching items found" message is shown.                            | Medium   |
| AD-INV-22  | Filter by a Quantity range with only one boundary | The inventory table displays items matching that single quantity value (if the range allows).                     | Medium   |
| AD-INV-23  | Navigate to the last page of a long item list   | The last page of inventory items loads correctly.                                                                 | Medium   |
| AD-INV-24  | Attempt to navigate beyond the last page        | The application prevents navigation beyond the last available page (e.g., disables the 'Next' button).            | Medium   |
| AD-INV-25  | Attempt to navigate before the first page       | The application prevents navigation before the first page (e.g., disables the 'Previous' button).                 | Medium   |
| AD-INV-26  | Inventory item at the low inventory threshold   | The visual indicator for low inventory is displayed for items exactly at the defined threshold.                   | High     |
| AD-INV-27  | Add a new item with maximum length inputs      | The form accepts the maximum allowed length for each field without errors.                                       | Medium   |
| AD-INV-28  | Edit an item with maximum length inputs         | The updated details are saved correctly up to the maximum allowed length for each field.                          | Medium   |
| AD-INV-29 | Empty table state             | Appropriate message shown when no inventory items match criteria   | Medium |
| AD-INV-30 | Low inventory warning         | Visual indicator for inventory items below threshold              | Medium |
---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-INV-31  | Search for a non-existent item                     | No items are displayed in the table, or a clear "No matching items found" message is shown.                        | High     |
| AD-INV-32  | Filter by text input that matches no items         | The inventory table displays no items, or a clear "No matching items found" message is shown.                      | High     |
| AD-INV-33  | Filter by a Material that does not exist in the system | The "Material" dropdown should either not allow such a selection or display an error/no results message.         | High     |
| AD-INV-34  | Filter by an invalid Quantity range | The system should either prevent such input or display an error message.                                         | High     |
| AD-INV-35  | Attempt to add a new item with missing required fields | The system displays specific error messages indicating the missing required fields, and the item is not added.    | High     |
| AD-INV-36  | Attempt to add/edit with invalid data format       | The system displays clear error messages for the invalid data fields, and the item is not added/edited.          | High     |
| AD-INV-37  | Attempt to manually set a negative quantity        | The system prevents the user from setting a negative quantity and displays an appropriate error message.           | High     |
| AD-INV-38  | Attempt to save edits with missing required fields  | The system displays error messages for the missing required fields, and the item details are not updated.        | High     |
| AD-INV-39  | Attempt to delete an item without confirmation     | The system should not delete the item without explicit user confirmation.                                       | High     |
| AD-INV-40  | Attempt to add an item with fields exceeding maximum allowed length | The system prevents input beyond the maximum allowed length and/or displays a clear error message.                  | High     |
| AD-INV-41  | Attempt to edit an item with fields exceeding maximum allowed length | The system prevents saving changes with input beyond the maximum allowed length and/or displays a clear error message. | High     |

---


#### Dashboard Page

##### Normal Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-DASH-01  | Load dashboard page                   | Dashboard loads completely with the "3D Printing" header, navigation menu (Dashboard, Order Management, Inventory Management, User Management, CSV Upload), mail/notification icon, "Total Orders", "Active Orders", "Pending Uploads", "Inventory Warnings" widgets displaying numerical values, "Orders Over Time" bar graph, and "Material Usage" pie chart. | High     |
| AD-DASH-02 | Navigate to Order Management          | Clicking "Order Management" in the navigation menu navigates the user to the Order Management page.                                                                                                  | High     |
| AD-DASH-03 | Navigate to Inventory Management      | Clicking "Inventory Management" in the navigation menu navigates the user to the Inventory Management page.                                                                                              | High     |
| AD-DASH-04 | Navigate to User Management             | Clicking "User Management" in the navigation menu navigates the user to the User Management page.                                                                                                     | High     |
| AD-DASH-05 | Navigate to CSV Upload                  | Clicking "CSV Upload" in the navigation menu navigates the user to the CSV Upload page.                                                                                                              | High     |
| AD-DASH-06  | Total Orders display accuracy         | The "Total Orders" widget displays the correct, up-to-date count of all orders in the system.                                                                                                          | High     |
| AD-DASH-07  | Active Orders display accuracy        | The "Active Orders" widget displays the correct, up-to-date count of all currently active orders in the system.                                                                                         | High     |
| AD-DASH-08  | Pending Uploads display accuracy      | The "Pending Uploads" widget displays the correct, up-to-date count of all files currently pending upload.                                                                                             | High     |
| AD-DASH-09  | Inventory Warnings display accuracy   | The "Inventory Warnings" widget displays the correct, up-to-date count of all active inventory warnings (items below threshold).                                                                         | High     |
| AD-DASH-10 | Dashboard display on desktop resolution | The dashboard layout and all elements are displayed correctly and are well-aligned on a standard desktop screen resolution.                                               | High     |

---

##### Edge Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-DASH-11 | Load dashboard with zero data                  | Dashboard loads without errors, and all numerical widgets display "0" or an appropriate "No data" indicator. The charts might be empty or display a "No data" message.                                       | Medium   |
| AD-DASH-12 | Load dashboard with a very large amount of data | Dashboard loads within an acceptable timeframe without performance issues. All widgets and charts display data appropriately without visual overflow or errors.                                                | Medium   |
| AD-DASH-13 | Click mail/notification icon with no new alerts  | If no new notifications or mail are present, clicking the icon might open an empty interface or indicate "No new notifications".                                                                             | Low      |

---

##### Fail Cases

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| AD-DASH-14 | Load dashboard with backend data errors         | If there are errors retrieving data from the backend, the affected widgets or charts should display an appropriate error message to the user instead of crashing or showing incorrect data.                    | High     |
| AD-DASH-15 | Navigate to a broken navigation link             | If any of the navigation links are broken or misconfigured, clicking them should either result in an error page or a clear indication that the link is not working.                                          | High     |
| AD-DASH-16 | Total Orders display shows incorrect count      | The "Total Orders" widget displays a count that does not match the actual number of total orders in the database.                                                                                            | High     |
| AD-DASH-17 | Active Orders display shows incorrect count     | The "Active Orders" widget displays a count that does not match the actual number of active orders in the database.                                                                                           | High     |
| AD-DASH-18 | Pending Uploads display shows incorrect count   | The "Pending Uploads" widget displays a count that does not match the actual number of pending uploads.                                                                                                      | High     |
| AD-DASH-19 | Inventory Warnings display shows incorrect count | The "Inventory Warnings" widget displays a count that does not match the actual number of active inventory warnings.                                                                                          | High     |
| AD-DASH-20 | Click mail/notification icon with backend error | If there's an error fetching notifications or mail, clicking the icon should display an error message instead of failing silently.                                                                            | Low      |
| AD-DASH-21 | Dashboard display breaks on specific resolution | The dashboard layout or elements break, overlap, or become unusable on specific screen resolutions.                                                                                                         | High     |

---


## 7. Test Execution

### 7.1 Test Execution Process

+ Prepare test environment
+ Execute test cases according to priority
+ Document test results
+ Report defects
+ Retest fixed defects
+ Update test status

### 7.2 Entry Criteria

+ Requirements analysis completed
+ Test environment set up
+ Test cases prepared
+ Test data available

### 7.3 Exit Criteria

+ All planned test cases executed
+ No critical or high-severity defects open
+ All requirements verified
+ Test coverage metrics met


## 8. Defect Management

### 8.1 Defect Lifecycle

+ Defect Detection
+ Defect Logging
+ Defect Triage
+ Defect Assignment
+ Defect Resolution
+ Defect Verification
+ Defect Closure

### 8.2 Defect Severity Levels

+ Critical : System crash, data loss, security breach
+ High     : Major functionality not working, workaround not available
+ Medium   : Functionality impaired, workaround available
+ Low      : Minor issues, cosmetic defects

### 8.3 Defect Priority Levels

+ P1 : Must be fixed immediately
+ P2 : Must be fixed before release
+ P3 : Should be fixed if time permits
+ P4 : Can be fixed in future releases


## 9. Test Deliverables

### 9.1 Before Testing

+ Test Plan
+ Test Cases
+ Test Scripts
+ Test Data

### 9.2 During Testing

+ Defect Reports
+ Status Reports

### 9.3 After Testing
+ Test Summary Report
+ Test Metrics
+ Recommendations