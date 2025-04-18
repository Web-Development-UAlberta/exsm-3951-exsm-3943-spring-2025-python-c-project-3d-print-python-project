# 3D Printing E-Commerce Platform - Software Design Document

## 1. Introduction

### 1.1 Purpose

This document outlines the software design for an e-commerce platform specializing in 3D printed objects. The platform will allow customers to customize and order 3D object model with various materials and colors.

### 1.2 Scope

The system will handle:

A user registration, allowing customers to create accounts, save their preferences, and track their order history.

An order management system that handles order processing, pseudo payment integration (always approved), order tracking, and order status updates.

An inventory management system that tracks the available filament materials and colors, automatically updates stock levels based on orders, and generates low-stock notifications for reordering.

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
+ Inventory
+ Orders
+ OrderItems

### 3.2 Key Tables

#### Users
+ UserID (PK)
+ Email
+ PasswordHash
+ Name
+ Address
+ Phone
+ CreatedAt

#### Products
+ ProductID (PK)
+ Name
+ Description
+ FilePath
+ Thumbnail
+ BasePrice
+ EstimatedPrintTime
+ CreatedAt
  
#### Materials
+ MaterialID (PK)
+ Name
+ CostPerUnit
+ LeadTime
+ WearandTear

#### Colors
+ ColorID (PK)
+ MaterialID (FK)
+ Name
+ HexCode

#### Inventory
+ InventoryID (PK)
+ MaterialID (FK)
+ ColorID (FK)
+ QuantityAvailable

#### Orders
+ OrderID (PK)
+ UserID (FK)
+ TotalPrice
+ Status
+ CreatedAt
+ EstimatedShipDate
+ ExpediteService
+ PaymentStatus


## 4. Component Design

## 4.1 User Management
+ Registration system
+ User profile management
+ Order history tracking
+ Address management

## 4.2 Product Customization
+ 3D model selection interface
+ Material and color selection
+ Infill percentage adjustment
+ Base plate customization options
+ Quote calculation
  
## 4.3 Inventory Management
+ CSV upload for materials and 3D objects
+ Automatic inventory deduction on order approval
+ Low-stock notifications
+ Reorder recommendations

## 4.4 Order Processing
+ Shopping cart functionality
+ Checkout process
+ Fake checkout confirmation page
+ Order confirmation

## 4.5 Admin Dashboard
+ Order management
+ Inventory oversight
+ User management


# Conclusion
This software design document provides the blueprint for developing the 3D printing e-commerce platform. The system will enable customers to customize and order 3D printed products while providing the entrepreneur with the tools needed to manage inventory, process orders, and manage users.

