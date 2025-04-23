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
