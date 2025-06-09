# 🏥 Database

## Provider

## ✅ Recommended `Provider` Fields (Based on Industry Standards)

| Field                     | Type        | Required | Notes                               |
| ------------------------- | ----------- | -------- | ----------------------------------- |
| `_id`                     | ObjectId    | ✅        | MongoDB default                     |
| `providerId`              | String      | ✅ Unique | Internal ID, slug or UUID           |
| `name`                    | String      | ✅        | Legal or brand name                 |
| `legalName`               | String      |          | For compliance/documents            |
| `type`                    | String      | ✅        | e.g., hospital, NGO, school         |
| `description`             | String      |          | Optional bio or blurb               |
| `status`                  | String      | ✅        | `active`, `inactive`, `archived`    |
| `website`                 | String      |          | URL                                 |
| `email`                   | String      | ✅        | Primary contact                     |
| `phone`                   | String      | ✅        | Main contact line                   |
| `address`                 | Object      | ✅        | Same GeoJSON pattern as booth       |
| `clinics`                 | \[ObjectId] |          | Refs to Clinic schema               |
| `employees`               | \[ObjectId] |          | Refs to Employee schema             |
| `patients`                | \[ObjectId] |          | Refs to Patient schema              |
| `metadata`                | Object      |          | Flexible structure for integrations |
| `createdAt` / `updatedAt` | Date        | ✅        | Managed by Mongoose                 |

---

## 🧾 Mongoose Schema: `providerSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const providerSchema = new Schema({
  providerId: {
    type: String,
    required: true,
    unique: true,
    index: true,
  },

  name: {
    type: String,
    required: true,
  },

  legalName: {
    type: String,
  },

  type: {
    type: String,
    enum: ['hospital', 'school', 'NGO', 'company', 'gov_agency', 'other'],
    required: true,
  },

  description: {
    type: String,
  },

  status: {
    type: String,
    enum: ['active', 'inactive', 'archived'],
    default: 'active',
  },

  website: {
    type: String,
  },

  email: {
    type: String,
    required: true,
  },

  phone: {
    type: String,
    required: true,
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
        required: true,
      },
      coordinates: {
        type: [Number], // [lng, lat]
        required: true,
      }
    }
  },

  clinics: [{ type: Schema.Types.ObjectId, ref: 'Clinic' }],
  employees: [{ type: Schema.Types.ObjectId, ref: 'Employee' }],
  patients: [{ type: Schema.Types.ObjectId, ref: 'Patient' }],

  metadata: {
    type: Schema.Types.Mixed,
    default: {}
  }

}, { timestamps: true });

providerSchema.index({ 'address.coordinates': '2dsphere' });

module.exports = mongoose.model('Provider', providerSchema);
```

---
