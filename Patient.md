# 🧍‍♂️ Patient

## 📖 Overview

A **patient** represents an individual receiving care, testing, or consultation within the system. Patients are core entities tracked across clinics, booths, and providers. They can be associated with appointments, test results, care plans, and other clinical records.

Patient records are designed to support extensibility, regulatory compliance, and localization, including support for multiple identifiers, emergency contacts, visitation logs, and geospatial metadata.

---

## 🧬 Patient Database Table

| Field                      | Type          | Required | Description                                      |
| -------------------------- | ------------- | -------- | ------------------------------------------------ |
| `_id`                      | ObjectId      | ✅        | MongoDB auto-generated unique identifier         |
| `firstName`                | String        | ✅        | Legal first name                                 |
| `lastName`                 | String        | ✅        | Legal last name                                  |
| `dob`                      | Date          | ✅        | Date of birth                                    |
| `gender`                   | String (enum) | ✅        | `male`, `female`, `other`, `unknown`             |
| `phone`                    | String        | ✅        | E.164 format preferred (e.g., `+15551234567`)    |
| `email`                    | String        |          | Optional email address                           |
| `address`                  | Object        | ✅        | Structured address with coordinates              |
| `identifiers`              | \[Object]     |          | External IDs (e.g., national ID, insurance, MRN) |
| `emergencyContact`         | Object        |          | Contact info of emergency contact                |
| `preferredLanguage`        | String        |          | ISO 639-1 language code (e.g., `en`, `es`)       |
| `status`                   | String (enum) | ✅        | `active`, `inactive`, `deceased`, `archived`     |
| `metadata`                 | Object        |          | Extensible field for notes, tags, or custom data |
| `digitInNoise`             | \[ObjectId]   |          | Linked Digit-In-Noise test records               |
| `digitInNoiseAntiphasic`   | \[ObjectId]   |          | Linked Antiphasic test records                   |
| `questionnaires`           | \[ObjectId]   |          | Linked detailed questionnaire responses          |
| `yesnoquestionnaires`      | \[ObjectId]   |          | Linked Yes/No-style questionnaires               |
| `audiogram`                | \[ObjectId]   |          | Linked audiogram results                         |
| `role`                     | String        | ✅        | Role within the system (`Patient` by default)    |
| `socialSecurityNumber`     | String        | ✅ Unique | Encrypted or raw SSN, must be stored securely    |
| `socialSecurityNumberHash` | String        | ✅ Unique | One-way hash of SSN, used for lookup/uniqueness  |
| `visitationRecords`        | \[Date]       |          | Log of all login timestamps                      |
| `latestVisitation`         | Date          |          | Most recent login timestamp                      |
| `createdAt` / `updatedAt`  | Date          | ✅        | Auto-managed timestamps                          |

---

## 🔗 Embedded Fields

### 📍 Address

```json
{
  "line1": "string",
  "line2": "string",
  "city": "string",
  "state": "string",
  "postalCode": "string",
  "country": "string",
  "coordinates": {
    "type": "Point",
    "coordinates": [longitude, latitude]
  }
}
```

### 🆔 Identifier

```json
{
  "type": "string",   // e.g. "national_id", "insurance_id", "mrn"
  "value": "string",  // actual ID value
  "issuer": "string"  // optional source or authority
}
```

### 🆘 Emergency Contact

```json
{
  "name": "string",
  "relationship": "string",
  "phone": "string",
  "email": "string"
}
```

---

## 🧾 Mongoose Schema: `patientSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const patientSchema = new Schema({
  firstName: { type: String, required: true },
  lastName:  { type: String, required: true },
  dob:       { type: Date, required: true },

  gender: {
    type: String,
    enum: ['male', 'female', 'other', 'unknown'],
    required: true
  },

  phone: { type: String, required: true },
  email: { type: String },

  address: {
    line1: String,
    line2: String,
    city: String,
    state: String,
    postalCode: String,
    country: String,
    coordinates: {
      type: {
        type: String,
        enum: ['Point'],
        default: 'Point'
      },
      coordinates: {
        type: [Number], // [longitude, latitude]
        index: '2dsphere'
      }
    }
  },

  identifiers: [{
    type: {
      type: String,
      required: true
    },
    value: {
      type: String,
      required: true
    },
    issuer: String
  }],

  emergencyContact: {
    name: String,
    relationship: String,
    phone: String,
    email: String
  },

  preferredLanguage: String,

  status: {
    type: String,
    enum: ['active', 'inactive', 'deceased', 'archived'],
    default: 'active'
  },

  metadata: { type: Object, default: {} },

  digitInNoise: [{
    type: Schema.Types.ObjectId,
    ref: 'DigitInNoise'
  }],

  digitInNoiseAntiphasic: [{
    type: Schema.Types.ObjectId,
    ref: 'DigitInNoiseAntiphasic'
  }],

  questionnaires: [{
    type: Schema.Types.ObjectId,
    ref: 'Questionnaire'
  }],

  yesnoquestionnaires: [{
    type: Schema.Types.ObjectId,
    ref: 'YesNoQuestionnaire'
  }],

  audiogram: [{
    type: Schema.Types.ObjectId,
    ref: 'Audiogram'
  }],

  role: {
    type: String,
    default: 'Patient'
  },

  socialSecurityNumber: {
    type: String,
    unique: true,
    required: true,
    // set: ssn => encdec.encryptPayload(ssn),
    // get: encrypted => encdec.decryptPayload(encrypted)
  },

  socialSecurityNumberHash: {
    type: String,
    unique: true
  },

  visitationRecords: [{
    type: Date,
    default: Date.now
  }],

  latestVisitation: {
    type: Date,
    default: Date.now
  }

}, { timestamps: true });

module.exports = mongoose.model('Patient', patientSchema);
```

---
