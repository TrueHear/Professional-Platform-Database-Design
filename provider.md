# 🏥 **Provider**

## 📘 What is a Provider?

A **Provider** is the top-level organization in system — like a **hospital network**, **NGO**, or **private agency**. It manages one or more **clinics**, and through them, operates **booths** where services (like testing or treatment) are provided to **patients**.

Analogy of it could be "parent company" or "headquarters" in system’s hierarchy.

---

## 📦 Recommended Fields (What Makes Up a Provider?)

| Field                     | Type        | Required | Description                                                      |
| ------------------------- | ----------- | -------- | ---------------------------------------------------------------- |
| `_id`                     | ObjectId    | ✅        | Auto-generated unique ID from MongoDB                            |
| `providerId`              | String      | ✅ Unique | Custom internal ID (slug, code, or UUID)                         |
| `name`                    | String      | ✅        | Public-facing name (brand or facility name)                      |
| `legalName`               | String      |          | Official legal name (for documents, billing, compliance)         |
| `type`                    | String      | ✅        | Organization type: `hospital`, `school`, `NGO`, `company`, etc.  |
| `description`             | String      |          | Short blurb or about section                                     |
| `status`                  | String      | ✅        | Operational state: `active`, `inactive`, `archived`              |
| `website`                 | String      |          | Website link (if applicable)                                     |
| `email`                   | String      | ✅        | Main contact email                                               |
| `phone`                   | String      | ✅        | Phone number for support/admin                                   |
| `address`                 | Object      | ✅        | Full address including GPS coordinates (used for mapping/search) |
| `clinics`                 | \[ObjectId] |          | List of connected clinics (facilities operated by this provider) |
| `employees`               | \[ObjectId] |          | Staff members working under this provider                        |
| `patients`                | \[ObjectId] |          | Patients registered in this provider’s system                    |
| `metadata`                | Object      |          | Any extra data (e.g., billing codes, integrations, tags)         |
| `createdAt` / `updatedAt` | Date        | ✅        | Auto-managed timestamps (created/last modified)                  |

---

## 🗺️ Address Format (GeoJSON)

The `address` includes a **GeoJSON `Point`** object which stores latitude and longitude. This allows features like:

* "Find nearest provider"
* Map views
* Spatial queries

---

## 🧾 Mongoose Schema

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

  legalName: String,

  type: {
    type: String,
    enum: ['hospital', 'school', 'NGO', 'company', 'gov_agency', 'other'],
    required: true,
  },

  description: String,

  status: {
    type: String,
    enum: ['active', 'inactive', 'archived'],
    default: 'active',
  },

  website: String,
  email: { type: String, required: true },
  phone: { type: String, required: true },

  address: {
    country: { type: String, required: true },
    state: String,
    city: { type: String, required: true },
    streetName: { type: String, required: true },
    streetNumber: String,
    postalCode: String,
    additionalInfo: String,
    coordinates: {
      type: {
        type: String,
        enum: ['Point'],
        default: 'Point',
        required: true,
      },
      coordinates: {
        type: [Number], // Format: [longitude, latitude]
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

// For geospatial queries
providerSchema.index({ 'address.coordinates': '2dsphere' });

module.exports = mongoose.model('Provider', providerSchema);
```

---

## 📌 Summary

* A **Provider** is the "owner" of all its **clinics**, **booths**, **employees**, and **patients**.
* It's the top-level entity in your system.
* It supports **location-based queries**, **multi-site operations**, and **integrated data tracking**.

---
