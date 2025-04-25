# Python Project - 3D Print-On-Demand Estore - ERD

## The Manufactoring vs Retail Challenge

As the 3D print store owner wants to auto calculate the cost of a customized 3D printed item - the ERD has to bridge manufacturing and inventory management processes with retail practices.

### Base assumptions and philosophies

- Raw materials and inventory will be calculated on a first in first out basis.
- The cost of goods sold is calculated by:
  - Fixed Costs + ((Starting Volume * Infill Multiplier) * Material Wieght * WearAndTear Multiplier)

## Tables

### Filament
A filament is defined by: Name, Color (in Hex Value), and Material Type

### Supplier
A supplier is a place to purchase a filament. It could be Amazon, direct from a manufactorer, or a local retailer. Each supplier may carry one or more brands of filament **and** two suppliers could carry the same filament by definition but vary greatly in cost and quality.

### Raw Materials
Each raw material entry could be any number of combinations between a filament and a supplier. Because each supplier may carry the same filament by defintion (eg, Red ABS) but their quality and cost can vary greatly, it is important to keep track of distinct raw materials and not lump all similar filaments into the same raw material entry. Lastly, it is not just material type that impacts the wear and tear it has on your machine but also the quality and color of a filament can noticably impact the wear of a machine. The unit to track quantity in raw materials is weight in grams.

### Inventory Change 
Based on our assumption of first in first out inventory cost calculations this table tracks the current unit cost and how much material is left based at this price point. As orders are created, the volume of materials can not only be decucted from invenotry but the price can be calculated from that specific material.

### 3D Models
This table defines the digital 3D model (name, description, image, where that file is stored on the server) **and** the estimated volume of a model given a preset infill for a standardized print, as well as, the fixed costs required to print the model. Fixed costs is the flat rate used to incorporate labour, consumables, and overhead into the cost of goods sold.

### Orders Items
This table tracks each item added to an order and is where the magic of cost calculations comes together. By linking the Inventory Change table to get the current cost per gram of the raw materials with 3D Models Table to get the volume of a model we can calculated the total weight based off the infill the customer sets and the wear and tear multiplier indeirectly from the Raw Materials Table.

### Users
This table tracks each unique customer profile so that it can be tied to thier orders

### Orders
This table combines all Order Items along with the Customer to calculate total cost and allows both a customer and the store owner to track order history.

### Fulfillment Status
This table tracks the change in status over time of an order as it moves through fulfillment.
- Draft Order, Pending Payment, Paid, Printing, Ready to Ship, Shipped, Refunded
