# 🏥 Clinic

## 🧬 Clinic Database Table

| Field                     | Type             | Required | Notes                                 |
| ------------------------- | ---------------- | -------- | ------------------------------------- |
| `_id`                     | ObjectId         | ✅        | MongoDB default                       |
| `clinicId`                | String           | ✅ Unique | Slug, UUID, or internal ID            |
| `provider`                | ObjectId         | ✅        | Reference to parent Provider          |
| `name`                    | String           | ✅        | Clinic name (e.g., "Downtown Clinic") |
| `status`                  | String           | ✅        | `active`, `inactive`, or `archived`   |
| `phone`                   | String           |          | Contact phone number                  |
| `email`                   | String           |          | Contact email                         |
| `address`                 | Object (GeoJSON) | ✅        | Structured + geospatially queryable   |
| `booths`                  | \[ObjectId]      |          | Optional list of related Booths       |
| `employees`               | \[ObjectId]      |          | Employees assigned to this clinic     |
| `metadata`                | Mixed Object     |          | Flexible key-value config             |
| `createdAt` / `updatedAt` | Date             | ✅        | Managed by Mongoose                   |

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
