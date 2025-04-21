# 3D Printing E-Commerce Platform - Software Design Document


## 1. Introduction

### 1.1 Purpose

This document outlines the software design for an e-commerce platform specializing in 3D printed objects. The platform will allow customers to customize and order 3D object model with various materials and colors.

### 1.2 Scope

The system will handle:

+ A user registration page
+ An order management system 
+ An inventory management system 

The full scope of the 3D printing e-commerce platform is defined in the separately prepared Scope Document - Refer /docs/scope-doc.md.

This Software Design Document focuses on the platform’s technical architecture, component structure, and implementation details.


## 2. System Architecture

### 2.1 High-Level Architecture

The system will follow a three-tier architecture:

- Presentation Layer (Frontend)
- Application Layer (Backend)
- Data Storage Layer (Database)

## 2.2 Technology Stack
+ Frontend: React, Next.js
+ Backend: Python, Django
+ Database: MySQL


## 3. Database Design

### 3.1 Entity Relationship Diagram

Key entities include:
+ Users
+ Products (3D Models)
+ Materials
+ Colors
+ MaterialColors
+ Suppliers
+ Inventory
+ Orders
+ OrderItems
+ Fulfillments

Refer /docs/ERD.drawio for detailed ERD diagram with relationship


## 4. Component Design

### 4.1 User Management
+ Registration system
+ User profile management
+ Order history tracking
+ Address management

### 4.2 Product Customization
+ 3D model selection interface
+ Material and color selection
+ Infill percentage adjustment
+ Base plate customization options
+ Quote calculation
  
### 4.3 Inventory Management
+ CSV upload for materials and 3D objects
+ Automatic inventory deduction on order approval
+ Low-stock notifications
+ Reorder recommendations

### 4.4 Order Processing
+ Shopping cart functionality
+ Checkout process
+ Fake checkout confirmation page
+ Order confirmation

### 4.5 Admin Dashboard
+ Order management
+ Inventory oversight
+ User management


## 5. User Interface Design

### 5.1 Customer-Facing Pages
+ Home Page
+ Product Catalog
+ Product Customization Page
+ Cart & Checkout
+ Order Confirmation and Tracking
+ User Profile

### 5.2 Admin Pages
+ Dashboard
+ Order Management
+ Inventory Management
+ User Management
+ CSV Upload Interface


## 6. Testing Strategy

### 6.1 Unit Testing
+ Component-level testing
+ Business logic validation

### 6.2 Integration Testing
+ Database interaction testing
+ End-to-end user flow testing
+ Admin functions testing



