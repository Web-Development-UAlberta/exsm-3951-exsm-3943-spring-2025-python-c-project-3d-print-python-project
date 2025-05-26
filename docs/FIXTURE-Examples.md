# Django Fixture Examples for 3D Print Shop

This document provides examples of fixture structures for each model in the 3D Print Shop application. Use these as templates when creating your own fixtures.

## Loading Order

When loading fixtures, follow this order to maintain proper relationships:

1. [Materials](#materials)
2. [Filament](#filament)
3. [Suppliers](#suppliers)
4. [RawMaterials](#rawmaterials)
5. [InventoryChange](#inventorychange)
6. [Models](#models)
7. [Shipping](#shipping)
8. [UserProfiles](#userprofiles) (requires User fixtures)
9. [Orders](#orders)
10. [OrderItems](#orderitems)
11. [FulfillmentStatus](#fulfillmentstatus)

## Materials

```json
[
    {
        "model": "store.materials",
        "pk": 1,
        "fields": {
            "Name": "PLA"
        }
    },
    {
        "model": "store.materials",
        "pk": 2,
        "fields": {
            "Name": "ABS"
        }
    }
]
```

## Filament

```json
[
    {
        "model": "store.filament",
        "pk": 1,
        "fields": {
            "Name": "PLA White",
            "Material": 1,
            "ColorHexCode": "FFFFFF"
        }
    },
    {
        "model": "store.filament",
        "pk": 2,
        "fields": {
            "Name": "PLA Black",
            "Material": 1,
            "ColorHexCode": "000000"
        }
    }
]
```

## Suppliers

```json
[
    {
        "model": "store.suppliers",
        "pk": 1,
        "fields": {
            "Name": "Prusa Polymers",
            "Address": "Prague, Czech Republic",
            "Phone": "+420-222-333-444",
            "Email": "info@prusa3d.com"
        }
    },
    {
        "model": "store.suppliers",
        "pk": 2,
        "fields": {
            "Name": "MatterHackers",
            "Address": "Lake Forest, CA, USA",
            "Phone": "+1-949-613-5838",
            "Email": "support@matterhackers.com"
        }
    }
]
```

## RawMaterials

```json
[
    {
        "model": "store.rawmaterials",
        "pk": 1,
        "fields": {
            "Supplier": 1,
            "Filament": 1,
            "BrandName": "Prusament",
            "Cost": "30.00",
            "MaterialWeightPurchased": 1000,
            "MaterialDensity": "1.24",
            "ReorderLeadTime": 7,
            "WearAndTearMultiplier": "1.00",
            "PurchasedDate": "2025-05-13T00:00:00Z"
        }
    }
]
```

## InventoryChange

```json
[
    {
        "model": "store.inventorychange",
        "pk": 1,
        "fields": {
            "RawMaterial": 1,
            "QuantityWeightAvailable": 1000,
            "InventoryChangeDate": "2025-05-13T00:00:00Z",
            "UnitCost": "0.03"
        }
    }
]
```

## Models

```json
[
    {
        "model": "store.models",
        "pk": 1,
        "fields": {
            "Name": "Calibration Cube",
            "Description": "A simple calibration cube for testing printer accuracy.",
            "FilePath": "models/calibration_cube.stl",
            "Thumbnail": "thumbnails/calibration_cube.png",
            "FixedCost": "3.00",
            "EstimatedPrintVolume": 20,
            "BaseInfill": "0.20",
            "CreatedAt": "2025-05-13T00:00:00Z"
        }
    }
]
```

## UserProfiles

```json
[
    {
        "model": "store.userprofiles",
        "pk": 1,
        "fields": {
            "user": 1,
            "Address": "123 Main St, Anytown, USA",
            "Phone": "+1-555-123-4567"
        }
    }
]
```

## Shipping

```json
[
    {
        "model": "store.shipping",
        "pk": 1,
        "fields": {
            "Name": "Standard Shipping",
            "Rate": "5.99",
            "ShipTime": 5
        }
    },
    {
        "model": "store.shipping",
        "pk": 2,
        "fields": {
            "Name": "Express Shipping",
            "Rate": "12.99",
            "ShipTime": 2
        }
    }
]
```

## Orders

```json
[
    {
        "model": "store.orders",
        "pk": 1,
        "fields": {
            "User": 1,
            "Shipping": 1,
            "TotalPrice": "35.99",
            "CreatedAt": "2025-05-13T00:00:00Z",
            "EstimatedShipDate": "2025-05-18T00:00:00Z",
            "ExpeditedService": false
        }
    }
]
```

## OrderItems

```json
[
    {
        "model": "store.orderitems",
        "pk": 1,
        "fields": {
            "InventoryChange": 1,
            "Order": 1,
            "Model": 1,
            "InfillMultiplier": "1.00",
            "TotalWeight": 20,
            "CostOfGoodsSold": "3.60",
            "Markup": "1.15",
            "ItemPrice": "10.00",
            "ItemQuantity": 3,
            "IsCustom": false
        }
    }
]
```

## FulfillmentStatus

```json
[
    {
        "model": "store.fulfillmentstatus",
        "pk": 1,
        "fields": {
            "Order": 1,
            "OrderStatus": "Paid",
            "StatusChangeDate": "2025-05-13T00:00:00Z"
        }
    }
]
```

## Tips for Creating Fixtures

1. **Foreign Keys**: Make sure foreign key references exist before loading dependent fixtures
2. **Date Formats**: Use ISO format for dates (YYYY-MM-DDThh:mm:ssZ)
3. **Decimal Values**: Always use quotes around decimal values ("10.99" not 10.99)
4. **File Paths**: For file fields, use relative paths from MEDIA_ROOT
5. **Testing**: Always test your fixtures in a development environment before using in production