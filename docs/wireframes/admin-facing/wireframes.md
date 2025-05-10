## Dashboard Wireframe
Purpose: Overview of system activity and key metrics.

Header
Project Name: < id="project-name-header">

Notifications: < id="notification-button" class="icon-button mail-icon">

Left Sidebar Navigation
Dashboard: <id="nav-dashboard" class="sidebar-link">

Order Management: < id="nav-order-management" class="sidebar-link">

Inventory Management: < id="nav-inventory-management" class="sidebar-link">

User Management: < id="nav-user-management" class="sidebar-link">

CSV Upload: < id="nav-csv-upload" class="sidebar-link">

Quick Stats Cards
Each stat as a component:

Total Orders: < id="stat-total-orders" class="card">

Active Orders: < id="stat-active-orders" class="card">

Pending Uploads: < id="stat-pending-uploads" class="card">

Inventory Warnings: < id="stat-inventory-warnings" class="card">


## Order Management Wireframe
Purpose: View, track, and manage print orders.

Header
Title: < id="order-name-header">
Search Bar: < id="order-search-input" class="search-bar" type="text">

Filters
Status: < id="filter-status" class="filter-dropdown">

Material: < id="filter-material" class="filter-dropdown">

Priority: < id="filter-priority" class="filter-dropdown">

Orders Table
Table: < id="orders-table">

Columns (headers and cells):

Order ID: < id="col-order-id"> / < class="cell-order-id">

Model Name: < id="col-model-name"> / < class="cell-model-name">

Material: < id="col-material"> / < class="cell-material">

Quantity: < id="col-quantity"> / < class="cell-quantity">

Status: < id="col-status"> / < class="cell-status">

Priority: < id="col-priority"> / < class="cell-priority">

Actions: < class="cell-actions"> (with buttons: edit, view, delete)


## Inventory Management Wireframe
Purpose: Manage 3D printing materials and parts.

Header
Title: < id="Inventory-name-header">
Search Bar: < id="inventory-search-input" class="search-bar">

Filters
Material: < id="filter-inventory-material" class="filter-dropdown">

Quantity: < id="filter-inventory-quantity" class="filter-dropdown">

Inventory Table
Table: < id="inventory-table">

Item ID: < class="cell-item-id">

Material Type: < class="cell-material-type">

Quantity Available: < class="cell-quantity-available">

Cost: < class="cell-cost">

Actions: < class="cell-actions">

## User Management Wireframe
Purpose: Administer users and permissions.

Header
Title: < id="User-name-header">
Search Bar: < id="user-search-input" class="search-bar" type="text">

Invite User: < id="invite-user-button" class="primary-cta">

Filters
Filter by Action: < id="filter-user-action" class="filter-dropdown">

Users Table
Table: < id="users-table">

User ID: < class="cell-user-id">

Name: < class="cell-name">

Email: < class="cell-email">

Statu: < class="cell-status">

Action: < class="cell-actions">

## CSV Upload Interface Wireframe
Purpose: Upload bulk data for orders, inventory, or users.

Header
Title: < id="CSV-name-header">

Upload Type Selector
Dropdown: < id="csv-upload-type" class="upload-type-selector">

Upload Zone
Drag-and-Drop Area: < id="csv-drop-zone" class="drag-drop-area">

“Choose File” Button: < type="file" id="csv-file-input" class="file-upload-input">

Sample CSV Download: < id="download-sample-csv" class="secondary-cta">

Validation
Validate Button: < id="validate-csv-button" class="primary-cta">

Upload Button (disabled initially): < id="upload-csv-button" class="primary-cta">