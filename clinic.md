# 🏥 Clinic

## 📖 Overview

A **clinic** represents a physical or operational location managed by a provider. Clinics serve as intermediate facilities where services are delivered — typically housing one or more **booths** and **employees**, and are associated with a single **provider** (organization or network). Each clinic stores location, contact, and structural data to support day-to-day operations, staff assignments, and patient interactions.

---

## 📦 Clinic Database Table

| Field                     | Type             | Required | Description                                                                |
| ------------------------- | ---------------- | -------- | -------------------------------------------------------------------------- |
| `_id`                     | ObjectId         | ✅        | MongoDB auto-generated unique identifier                                   |
| `clinicId`                | String           | ✅ Unique | Internal or external unique identifier (e.g., slug, UUID, short code)      |
| `provider`                | ObjectId         | ✅        | Reference to the parent `Provider` document                                |
| `name`                    | String           | ✅        | Display name of the clinic                                                 |
| `status`                  | String           | ✅        | Operational state: `active`, `inactive`, or `archived`                     |
| `phone`                   | String           |          | Optional contact phone number                                              |
| `email`                   | String           |          | Optional contact email address                                             |
| `address`                 | Object (GeoJSON) | ✅        | Structured address with geolocation fields for mapping and spatial queries |
| `booths`                  | \[ObjectId]      |          | Optional array of references to `Booth` documents                          |
| `employees`               | \[ObjectId]      |          | Optional array of references to `Employee` documents                       |
| `metadata`                | Mixed Object     |          | Flexible key-value object for storing additional clinic-specific data      |
| `createdAt` / `updatedAt` | Date             | ✅        | Automatically managed timestamps                                           |

---

## 🧾 Mongoose Schema: `clinicSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const clinicSchema = new Schema({
  clinicId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },

  provider: {
    type: Schema.Types.ObjectId,
    ref: 'Provider',
    required: true
  },

  name: {
    type: String,
    required: true
  },

  status: {
    type: String,
    enum: ['active', 'inactive', 'archived'],
    default: 'active'
  },

  phone: {
    type: String
  },

  email: {
    type: String
  },

  address: {
    country: { type: String, required: true },
    state: { type: String },
    city: { type: String, required: true },
    streetName: { type: String, required: true },
    streetNumber: { type: String },
    postalCode: { type: String },
    additionalInfo: { type: String },
    coordinates: {
      type: {
        type: String,
        enum: ['Point'],
        default: 'Point',
        required: true
      },
      coordinates: {
        type: [Number], // [lng, lat]
        required: true
      }
    }
  },

  booths: [{ type: Schema.Types.ObjectId, ref: 'Booth' }],
  employees: [{ type: Schema.Types.ObjectId, ref: 'Employee' }],

  metadata: {
    type: Schema.Types.Mixed,
    default: {}
  }

}, { timestamps: true });

clinicSchema.index({ 'address.coordinates': '2dsphere' });

module.exports = mongoose.model('Clinic', clinicSchema);
```

---
