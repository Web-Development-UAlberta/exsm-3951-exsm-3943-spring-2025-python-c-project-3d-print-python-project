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
+ Frontend: React 18+, Next.js 13+

## 6. Test Cases

### 6.1 Customer Facing pages

#### Home Page

| Test ID     | Description                 | Expected Result                                                                 | Priority |
|-------------|-----------------------------|---------------------------------------------------------------------------------|---------|
| CF-HOME-01  | Load homepage successfully  | Homepage loads with hero banner, featured products, and navigation              | High     |
| CF-HOME-02  | Navigation links work       | Clicking Shop / Catalog / Customization / Cart / Orders / Profile redirects correctly | High     |
| CF-HOME-03  | Logo redirects to Home      | Clicking Logo button redirects to Home page                                     | Medium   |
| CF-HOME-04  | Profile link works          | Clicking Profile button redirects to Login page correctly                       | High     |
| CF-HOME-05  | Search                      | Search fetches the result accurately                                            | Medium  | 

---

#### Product Catalog / Customization Page

| Test ID     | Description                        | Expected Result                               | Priority |
|-------------|------------------------------------|-----------------------------------------------|----------|
| CF-CAT-01   | Display product list               | All products appear with name, price, and image  | High     |
| CF-CAT-02   | Search                             | Able to search products and the correct products load   | Medium   |
| CF-CAT-03   | Logo redirects to Home             | Clicking Logo button redirects to Home page             | Medium   |
| CF-CAT-04   | Navigation link works              | Clicking Home / Products / About Us / Contact Us redirects correctly   | High     |
| CF-CAT-05   | Size, color and material works   | Able to select Size, color and material by clicking on the appropriate buutons | High |
| CF-CAT-06   | Add to cart                  | Clicking add to cart adds the product with the selected Size, color and material | High   |

---

#### Cart / Checkout Page

| Test ID            | Description                            | Expected Result                              | Priority |
|--------------------|----------------------------------------|----------------------------------------------|----------|
| CF-CHECKOUT-01   | Page loads with items in bag     | Checkout page displays product(s), subtotal, and checkout button   | High     |
| CF-CHECKOUT-02   | Increase quantity           | Quantity increases by 1; subtotal updates                    | High     |
| CF-CHECKOUT-03   | Decrease quantity           | Quantity decreases by 1 (not below 1); subtotal updates      | High     |
| CF-CHECKOUT-04   | Subtotal calculation        | Subtotal correctly reflects total cost                       | High     |
| CF-CHECKOUT-05   | Proceed to checkout         | Redirects to payment (Mock)                                  | High     |
| CF-CHECKOUT-06   | Responsive layout           | Page remains readable and interactive                        | Medium   |
| CF-CHECKOUT-07   | Newsletter subscription - valid email  | Confirmation message displayed                    | Medium   |
| CF-CHECKOUT-08   | Newsletter subscription - invalid email| Error message displayed                           | Medium   |
| CF-CHECKOUT-09   | Brand Name                             | Brand Name loads correctly                        | High  |
| CF-CHECKOUT-10   | Search                                 | Search loads the result accurately                | Medium   |
| CF-CHECKOUT-11   | Subscribe newsletter | Clicking on subscribe button sends an email with a successful subscription message | Medium  |

---

#### Profile / Orders Page

| Test ID            | Description                            | Expected Result                                  | Priority |
|--------------------|----------------------------------------|--------------------------------------------------|----------|
| CF-ORDERS-01  | Page loads successfully       | Displays user name and list of past orders                                  | High     |
| CF-ORDERS-02  | Display processing orders     | Shows "Processing" section with items and total                             | High     |
| CF-ORDERS-03  | Display shipping orders       | Shows "Shipping" section with items and total                               | High     |
| CF-ORDERS-04  | Display completed orders      | Shows "Completed" section with items and total                              | High     |
| CF-ORDERS-05  | Sign out link                 | User is logged out and redirected to login page                             | High     |
| CF-ORDERS-06  | Responsive layout             | Page layout adjusts properly                                                | Medium   |
| CF-ORDERS-07  | Newsletter subscription       | Confirmation shown for valid email, error for invalid                       | Medium   |
| CF-ORDERS-08  | Navigation links              | All navigation links work                                                   | Medium   |
| CF-ORDERS-09  | Subscribe newsletter   | Clicking on subscribe button sends an email with a successful subscription message | Medium   |

---

#### Login Page

| Test ID       | Description                    | Expected Result                                                  | Priority |
|---------------|--------------------------------|------------------------------------------------------------------|----------|
| CF-LOGIN-01   | Load login page                | Login page loads with logo, nav bar, login form, and sign-up link   | High     |
| CF-LOGIN-02   | Valid login credentials        | Redirect to user dashboard or home page                             | High     |
| CF-LOGIN-03   | Invalid credentials            | Show error message "Invalid credentials"                            | High     |
| CF-LOGIN-04   | Empty fields and click sign in | Show validation errors for both fields                              | High     |
| CF-LOGIN-05   | Only username filled           | Show validation error for password                                  | High     |
| CF-LOGIN-06   | Only password filled           | Show validation error for username                                  | High     |
| CF-LOGIN-07   | Password masking               | Password should be hidden (masked with dots/asterisks)              | High     |
| CF-LOGIN-08   | Sign Up redirection            | Redirects to create account page                                    | High     |
| CF-LOGIN-09   | Navigation links               | Correct pages open in the same tab                                  | Medium   |

---

#### Sign up Page

| Test ID        | Description                   | Expected Result                                     | Priority |
|----------------|-------------------------------|-----------------------------------------------------|----------|
| CF-ACCT-01     | Load account creation page    | Account creation page loads with logo, navigation bar, form fields (First Name, Last Name, Email, Password), newsletter checkbox, and buttons | High |
| CF-ACCT-02     | Valid account creation        | New account is created and user is redirected to appropriate page | High |
| CF-ACCT-03     | Empty form submission         | Show validation errors for all required fields           | High |
| CF-ACCT-04     | Email format validation       | Show error for invalid email format                      | High |
| CF-ACCT-05     | Password complexity validation | Show error if password doesn't meet complexity requirements | High |
| CF-ACCT-06     | Duplicate email submission     | Show error that account with email already exists             | High |
| CF-ACCT-07     | Newsletter checkbox functionality | Newsletter preference is saved correctly with account | Medium |
| CF-ACCT-08     | Navigation to Sign In          | "Sign in" button redirects to login page                  | High |
| CF-ACCT-09     | Field character limits         | Form accepts appropriate length for all fields            | Medium |
| CF-ACCT-10     | Navigation bar functionality   | All navigation links work correctly                       | Medium |
| CF-ACCT-11     | Logo clickability              | Logo redirects to homepage                                | Medium |
| CF-ACCT-12     | Search functionality           | Search icon opens search functionality                    | Medium |
| CF-ACCT-13     | Form field focus               | Proper visual indication when field is selected/focused   | Low    |
| CF-ACCT-14     | Form accessibility             | Form is navigable via keyboard and works with screen readers | High |
| CF-ACCT-15     | Responsive design              | Form displays properly on different screen sizes          | Medium |

---

#### Order History Page

| Test ID        | Description                    | Expected Result                                           | Priority |
|----------------|--------------------------------|-----------------------------------------------------------|----------|
| CF-OH-01 | Load order history page | Page loads with navigation menu, order details, and order summary | High |
| CF-OH-02 | Navigation menu functionality | All navigation links (Home, Catalog, Customization, Cart, Profile) work correctly | High |
| CF-OH-03 | Logo functionality | Clicking logo redirects to homepage | Medium |
| CF-OH-04 | Search functionality | Search icon opens search functionality | Medium |
| CF-OH-05 | Order number display | Order number displays correctly | High |
| CF-OH-06 | Order date display | Order date displays correctly in expected format | High |
| CF-OH-07 | Shipping tier display | Shipping tier displays correctly | High |
| CF-OH-08 | Payment method display | Payment method (E-Transfer) displays correctly | High |
| CF-OH-09 | Order summary display | Order summary section shows product image, quantity, and price | High |
| CF-OH-10 | Product image display | Product image loads properly in order summary | Medium |
| CF-OH-11 | Delivery address display | Complete delivery address displays with proper formatting | High |
| CF-OH-12 | Order subtotal display | Order subtotal displays with correct currency format | High |
| CF-OH-13 | Shipping cost display | Shipping cost displays with correct currency format | High |
| CF-OH-14 | Order total display | Order total displays with correct currency format | High |
| CF-OH-15 | Page responsiveness | Order history page displays correctly on different screen sizes | Medium |


### 6.2 Admin Pages

#### CSV Upload Page

| Test ID        | Description                    | Expected Result                                            | Priority |
|----------------|--------------------------------|------------------------------------------------------------|----------|
| AD-CSV-01 | Load CSV upload page | Page loads with header, upload type dropdown, drag-drop area, browse button, and action buttons | High |
| AD-CSV-02      | Upload type selection          | Dropdown opens and displays available upload types         |  High    |
| AD-CSV-03      | Drag and drop functionality    | File can be successfully uploaded via drag and drop        |  High     |
| AD-CSV-04      | Browse button functionality    | File explorer opens and allows file selection              |  High |
| AD-CSV-05      | Upload invalid file format     | Error message displayed for non-CSV file types             |  High |
| AD-CSV-06      | Upload valid CSV               | File accepted and prepared for validation                  |  High |
| AD-CSV-07      | Simple CSV download            | Template CSV file downloads with correct format            | Medium |
| AD-CSV-08      | Validate button functionality  | CSV validation process runs and displays results           | High |
| AD-CSV-09      | Upload button functionality    | Validated CSV uploads to the system                        | High |
| AD-CSV-10      | File size limit                | Error message for files exceeding size limit               | Medium |
| AD-CSV-11      | Upload with no file selected   | Error message indicating no file is selected               | Medium |
| AD-CSV-12      | Upload with network interruption | Appropriate error handling and retry options             | Medium |

---

#### User Management Page

| Test ID        | Description                    | Expected Result                                            | Priority |
|----------------|--------------------------------|------------------------------------------------------------|----------|
| AD-USR-01 | Load user management page | Page loads with header, search field, filters, user table, and invite button | High |
| AD-USR-02 | Search functionality                | Search returns matching users based on input criteria       | High |
| AD-USR-03 | Filter by text input                | User list filtered according to text input                  | High |
| AD-USR-04 | Filter by action                    | User list displays based on available actions               | Medium |
| AD-USR-05 | Display user details       | All user columns (ID, Name, Email, Status, Action) display correct information | High |
| AD-USR-06 | Invite user button                  | Opens invite user form/modal                                | High |
| AD-USR-07 | Table pagination                    | Table pages through multiple users if applicable            | Medium |
| AD-USR-08 | Action buttons in table             | Action buttons in the table function correctly              | High |
| AD-USR-09 | Empty table state                   | Appropriate message shown when no users match criteria      | Medium |

---

#### Order Management Page

| Test ID        | Description                    | Expected Result                                              | Priority |
|----------------|--------------------------------|--------------------------------------------------------------|----------|
| AD-ORD-01     | Load order management page | Page loads with header, search field, filters, order table, and create button | High |
| AD-ORD-02     | Search functionality            | Search returns matching orders based on input criteria       | High |
| AD-ORD-03     | Filter by text input            | Order list filtered according to text input                  | High |
| AD-ORD-04     | Filter by material              | Order list shows only orders with selected material          | High |
| AD-ORD-05     | Filter by status                | Order list shows only orders with selected status            | High |
| AD-ORD-06     | Filter by priority              | Order list shows only orders with selected priority          | High |
| AD-ORD-07     | Display order details | All order columns (ID, Model Name, Material, Qty, Status, Priority, Actions) display correctly | High |
| AD-ORD-08     | Table pagination                | Table pages through multiple orders if applicable            | Medium |
| AD-ORD-09     | Action buttons in table         | Action buttons in the Actions column function correctly      | High |
| AD-ORD-10     | Empty table state               | Appropriate message shown when no orders match criteria      | Medium |

---

#### Inventory Management Page

| Test ID         | Description                    | Expected Result                                            | Priority |
|-----------------|--------------------------------|------------------------------------------------------------|----------|
| AD-INV-01 | Load inventory management page | Page loads with header, search field, filters, inventory table, and add button | High |
| AD-INV-02 | Search functionality          | Search returns matching inventory items based on input criteria    | High |
| AD-INV-03 | Filter by text input          | Inventory list filtered according to text input                    | High |
| AD-INV-04 | Filter by material            | Inventory list shows only items with selected material             | High |
| AD-INV-05 | Filter by quantity            | Inventory list shows only items within selected quantity range     | High |
| AD-INV-06 | Display inventory details     | All inventory columns (Item ID, Material Type, Qty, Cost, Action) display correctly | High |
| AD-INV-07 | Add new material button       | Opens the CSV upload interface                                      | High |
| AD-INV-08 | Table pagination              | Table pages through multiple inventory items if applicable         | Medium |
| AD-INV-09 | Action buttons in table       | Action buttons in the Action column function correctly             | High |
| AD-INV-10 | Empty table state             | Appropriate message shown when no inventory items match criteria   | Medium |
| AD-INV-11 | Low inventory warning         | Visual indicator for inventory items below threshold              | Medium |

---

#### Dashboard Page

| Test ID        | Description                     | Expected Result                                               | Priority |
|----------------|---------------------------------|---------------------------------------------------------------|----------|
| AD-DASH-01     | Load dashboard page             | Dashboard loads with navigation menu and all widgets/statistics | High |
| AD-DASH-02     | Navigation menu                 | All navigation links function correctly                        | High |
| AD-DASH-03     | Total Orders display            | Shows accurate count of total orders                           | High |
| AD-DASH-04     | Active Orders display           | Shows accurate count of active orders                          | High |
| AD-DASH-05     | Pending Uploads display         | Shows accurate count of pending uploads                        | High |
| AD-DASH-06     | Inventory Warnings display      | Shows accurate count of inventory warnings                     | High |
| AD-DASH-07     | Navigation to Order Management  | Clicking Order Management navigates to order page              | High |
| AD-DASH-08     | Navigation to Inventory Management | Clicking Inventory Management navigates to inventory page | High |
| AD-DASH-09     | Navigation to User Management   | Clicking User Management navigates to user page              | High |
| AD-DASH-10     | Navigation to CSV Upload        | Clicking CSV Upload navigates to upload page                  | High |
| AD-DASH-11     | Mail/notification icon          | Opens notifications or mail interface                          | Low |
| AD-DASH-12     | Dashboard responsiveness        | Dashboard displays correctly on various screen sizes           | Medium |


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