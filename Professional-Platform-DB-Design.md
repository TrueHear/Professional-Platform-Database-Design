# 🗃️ TrueHear Database Design

## Revision: 2025-06-10

This document provides an architectural overview of the **TrueHear backend data model**, consolidating all core schemas across operational, user, and clinical domains. The goal is to enable consistent implementation, maintenance, and onboarding for teams working with the TrueHear system.

---

## 📚 Table of Contents

- [🗃️ TrueHear Database Design](#️-truehear-database-design)
  - [Revision: 2025-06-10](#revision-2025-06-10)
  - [📚 Table of Contents](#-table-of-contents)
  - [🏗️ Entity Relationship Summary](#️-entity-relationship-summary)
  - [📦 Core Data Models](#-core-data-models)
    - [1. 🧠 **Provider**](#1--provider)
      - [📘 What is a Provider?](#-what-is-a-provider)
      - [📦 Recommended Fields (What Makes Up a Provider?)](#-recommended-fields-what-makes-up-a-provider)
      - [🗺️ Address Format (GeoJSON)](#️-address-format-geojson)
      - [🧾 Mongoose Schema](#-mongoose-schema)
    - [2. 🏥 **Clinic**](#2--clinic)
      - [📖 Overview-Clinic](#-overview-clinic)
      - [📦 Clinic Database Table](#-clinic-database-table)
      - [🧾 Mongoose Schema: `clinicSchema.js`](#-mongoose-schema-clinicschemajs)
    - [3. 🎧 **Booth**](#3--booth)
      - [📖 Overview-Booth](#-overview-booth)
      - [🧩 Booth Database Table](#-booth-database-table)
      - [🧾 Mongoose Schema: `boothSchema.js`](#-mongoose-schema-boothschemajs)
    - [4. 👨‍⚕️ **Employee**](#4-️-employee)
      - [📖 Overview-Employee](#-overview-employee)
      - [🧬 Employee Database Table](#-employee-database-table)
      - [📘 Assignment Structure (`assignments`)](#-assignment-structure-assignments)
      - [🧾 Mongoose Schema: `employeeSchema.js`](#-mongoose-schema-employeeschemajs)
    - [5. 🛡️ **Role**](#5-️-role)
      - [📖 Overview-Role](#-overview-role)
      - [🧬 Role Database Table](#-role-database-table)
      - [🧾 Mongoose Schema: `roleSchema.js`](#-mongoose-schema-roleschemajs)
    - [6. 🧍‍♂️ **Patient**](#6-️-patient)
      - [📖 Overview-Patient](#-overview-patient)
      - [🧬 Patient Database Table](#-patient-database-table)
      - [🔗 Embedded Fields](#-embedded-fields)
      - [📍 Address](#-address)
      - [🆔 Identifier](#-identifier)
      - [🆘 Emergency Contact](#-emergency-contact)
      - [🧾 Mongoose Schema: `patientSchema.js`](#-mongoose-schema-patientschemajs)
  - [🔗 Reference Relationships](#-reference-relationships)
  - [📖 Shared Schema Conventions](#-shared-schema-conventions)

---

## 🏗️ Entity Relationship Summary

```plaintext
Provider
├── Clinics
│   ├── Booths
│   │   └── Employees
│   │       └── Patients
│   └── Employees
└── Employees
```

Patients are registered independently of staff but connect to booths, test records, and clinical outcomes.

---

## 📦 Core Data Models

### 1. 🧠 **Provider**

#### 📘 What is a Provider?

A **Provider** is the top-level organization in system — like a **hospital network**, **NGO**, or **private agency**. It manages one or more **clinics**, and through them, operates **booths** where services (like testing or treatment) are provided to **patients**.

Analogy of it could be "parent company" or "headquarters" in system’s hierarchy.

---

#### 📦 Recommended Fields (What Makes Up a Provider?)

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

#### 🗺️ Address Format (GeoJSON)

The `address` includes a **GeoJSON `Point`** object which stores latitude and longitude. This allows features like:

- "Find nearest provider"
- Map views
- Spatial queries

---

#### 🧾 Mongoose Schema

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

### 2. 🏥 **Clinic**

#### 📖 Overview-Clinic

A **clinic** represents a physical or operational location managed by a provider. Clinics serve as intermediate facilities where services are delivered — typically housing one or more **booths** and **employees**, and are associated with a single **provider** (organization or network). Each clinic stores location, contact, and structural data to support day-to-day operations, staff assignments, and patient interactions.

---

#### 📦 Clinic Database Table

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

#### 🧾 Mongoose Schema: `clinicSchema.js`

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

### 3. 🎧 **Booth**

#### 📖 Overview-Booth

A **booth** represents a testing, diagnostic, or service station within a clinic. Booths are tied to a single **clinic** and often serve patients for specific services such as audiometry or questionnaire-based assessments. Each booth can be configured with its own settings, test options, hardware limits, and staff assignments.

Booths support local customization of diagnostic workflows, employee assignments, and test settings. They can be physical (e.g., a soundproof room), semi-mobile (e.g., a kiosk), or virtual (e.g., telehealth setups).

---

#### 🧩 Booth Database Table

| Field                                   | Type             | Required | Description                                                                 |
| --------------------------------------- | ---------------- | -------- | --------------------------------------------------------------------------- |
| `_id`                                   | ObjectId         | ✅        | MongoDB auto-generated unique identifier                                    |
| `boothId`                               | Number           | ✅ Unique | Numeric internal identifier                                                 |
| `boothName`                             | String           | ✅        | Human-readable booth label                                                  |
| `clinic`                                | ObjectId         | ✅        | Reference to the clinic this booth belongs to                               |
| `userName`                              | String           | ✅ Unique | Booth-specific login username                                               |
| `password`                              | String           | ✅        | Hashed password                                                             |
| `boothAddress`                          | String           | ✅        | Display address (used for front-end or human viewing)                       |
| `status`                                | String           | ✅        | Current operational state: `active`, `inactive`, `maintenance`, `archived`  |
| `type`                                  | String           |          | Booth category: `room`, `kiosk`, `mobile`, `outdoor`, `virtual`, or `other` |
| `services`                              | \[String]        |          | Functional capabilities (e.g. `["audiometry"]`)                             |
| `capacity`                              | Number           |          | Optional maximum patient throughput or occupancy                            |
| `role`                                  | String           |          | Optional role tag for internal labeling                                     |
| `tests`                                 | \[Object]        |          | List of available tests and inclusion flags                                 |
| `employees`                             | \[ObjectId]      |          | Staff members assigned to operate or support the booth                      |
| `dinSettings`                           | \[ObjectId]      |          | Digit-in-noise test configurations                                          |
| `dinSettingsRound1Constant`             | \[ObjectId]      |          | DIN settings for round 1                                                    |
| `dinSettingsRound2Adaptive`             | \[ObjectId]      |          | DIN settings for round 2                                                    |
| `dinSettingsRound3Adaptive`             | \[ObjectId]      |          | DIN settings for round 3                                                    |
| `antiphasicDinSettings`                 | \[ObjectId]      |          | Antiphasic DIN configurations                                               |
| `questionaireSettings`                  | \[ObjectId]      |          | Linked questionnaire settings                                               |
| `yesNoQuestionnaireSettings`            | \[ObjectId]      |          | Linked yes/no questionnaire settings                                        |
| `audiogramSettings`                     | \[ObjectId]      |          | Audiogram test settings                                                     |
| `defaultDinSettingsIndex`               | Number           |          | Index of default DIN config in `dinSettings`                                |
| `defaultDinSettingsRound1ConstantIndex` | Number           |          | Index of default config in round 1 list                                     |
| `defaultDinSettingsRound2AdaptiveIndex` | Number           |          | Index of default config in round 2 list                                     |
| `defaultDinSettingsRound3AdaptiveIndex` | Number           |          | Index of default config in round 3 list                                     |
| `defaultAntiphasicDinSettingsIndex`     | Number           |          | Index into `antiphasicDinSettings`                                          |
| `defaultQuestionaireIndex`              | Number           |          | Default index in questionnaire settings                                     |
| `defaultYesNoQuestionnaireIndex`        | Number           |          | Default index in yes/no questionnaire settings                              |
| `defaultAudiogramSettingsIndex`         | Number           |          | Default index for audiogram settings                                        |
| `address`                               | Object (GeoJSON) |          | Structured geographic address with coordinates                              |
| `metadata`                              | Mixed Object     |          | Optional structure for custom integrations, UI settings, or overrides       |
| `createdAt` / `updatedAt`               | Date             | ✅        | Auto-managed creation and update timestamps                                 |

---

#### 🧾 Mongoose Schema: `boothSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const boothSchema = new Schema({
  boothId: { type: Number, unique: true, index: true },
  boothName: { type: String, required: true },
  clinic: { type: Schema.Types.ObjectId, ref: 'Clinic', required: true },

  userName: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  boothAddress: { type: String, required: true },

  status: {
    type: String,
    enum: ['active', 'inactive', 'maintenance', 'archived'],
    default: 'active',
  },

  type: {
    type: String,
    enum: ['room', 'kiosk', 'mobile', 'outdoor', 'virtual', 'other'],
  },

  services: { type: [String], default: [] },
  capacity: { type: Number },

  role: { type: String, default: "Booth" },

  tests: {
    type: [
      {
        _id: false,
        testId: { type: String, required: true },
        included: { type: Boolean, default: false }
      }
    ],
    default: []
  },

  employees: [{ type: Schema.Types.ObjectId, ref: 'Employee' }],

  dinSettings: [{ type: Schema.Types.ObjectId, ref: 'DigitInNoiseSettingv1' }],
  dinSettingsRound1Constant: [{ type: Schema.Types.ObjectId, ref: 'DigitInNoiseSettingv1' }],
  dinSettingsRound2Adaptive: [{ type: Schema.Types.ObjectId, ref: 'DigitInNoiseSettingv1' }],
  dinSettingsRound3Adaptive: [{ type: Schema.Types.ObjectId, ref: 'DigitInNoiseSettingv1' }],
  antiphasicDinSettings: [{ type: Schema.Types.ObjectId, ref: 'AntiphasicDigitInNoiseSettingv1' }],
  questionaireSettings: [{ type: Schema.Types.ObjectId, ref: 'QuestionaireSetting' }],
  yesNoQuestionnaireSettings: [{ type: Schema.Types.ObjectId, ref: 'YesNoQuestionnaireSetting' }],
  audiogramSettings: [{ type: Schema.Types.ObjectId, ref: 'AudiogramSettings' }],

  defaultDinSettingsIndex: { type: Number, default: null },
  defaultDinSettingsRound1ConstantIndex: { type: Number, default: null },
  defaultDinSettingsRound2AdaptiveIndex: { type: Number, default: null },
  defaultDinSettingsRound3AdaptiveIndex: { type: Number, default: null },
  defaultAntiphasicDinSettingsIndex: { type: Number, default: null },
  defaultQuestionaireIndex: { type: Number, default: null },
  defaultYesNoQuestionnaireIndex: { type: Number, default: null },
  defaultAudiogramSettingsIndex: { type: Number, default: null },

  address: {
    country: { type: String },
    state: { type: String },
    city: { type: String },
    streetName: { type: String },
    streetNumber: { type: String },
    postalCode: { type: String },
    additionalInfo: { type: String },
    coordinates: {
      type: {
        type: String,
        enum: ['Point'],
        default: 'Point',
      },
      coordinates: {
        type: [Number] // [lng, lat]
      }
    }
  },

  metadata: { type: Schema.Types.Mixed, default: {} }

}, { timestamps: true });

boothSchema.index({ 'address.coordinates': '2dsphere' });

module.exports = mongoose.model('Booth', boothSchema);
```

---

### 4. 👨‍⚕️ **Employee**

#### 📖 Overview-Employee

An **employee** is a system user who can work at various levels: provider, clinic, or booth. Each employee can hold multiple roles, assigned per scope (e.g., clinic or booth), and can have specific permissions based on that role. Assignments include references to the role model and allow tracking who assigned them, when, and for how long.

---

#### 🧬 Employee Database Table

| Field                     | Type         | Required | Description                                                              |
| ------------------------- | ------------ | -------- | ------------------------------------------------------------------------ |
| `_id`                     | ObjectId     | ✅        | MongoDB internal unique ID                                               |
| `employeeId`              | String       | ✅ Unique | Unique employee code or UUID                                             |
| `firstName`               | String       | ✅        | Employee’s first name                                                    |
| `lastName`                | String       | ✅        | Employee’s last name                                                     |
| `email`                   | String       | ✅ Unique | Primary email used for login or communication                            |
| `phone`                   | String       |          | Optional phone number                                                    |
| `assignments`             | Array        | ✅        | List of scope-role-permission mappings (see `assignmentSchema`)          |
| `status`                  | String       | ✅        | Employment or account status: `active`, `inactive`, or `archived`        |
| `metadata`                | Mixed Object |          | Flexible structure for tags, department info, notes, or external linkage |
| `createdAt` / `updatedAt` | Date         | ✅        | Auto-managed timestamps by Mongoose                                      |

---

#### 📘 Assignment Structure (`assignments`)

Each assignment defines where the employee works, what role they have, and what permissions come with it.

| Field         | Type      | Required | Description                                               |
| ------------- | --------- | -------- | --------------------------------------------------------- |
| `scopeType`   | String    | ✅        | Type of entity: `provider`, `clinic`, or `booth`          |
| `entityId`    | ObjectId  | ✅        | Reference to the specific entity (refPath to `scopeType`) |
| `scopeName`   | String    |          | Optional display name for the assigned entity             |
| `role`        | ObjectId  | ✅        | Reference to a role document in `Role` collection         |
| `permissions` | \[String] |          | Action types allowed: `read`, `write`, `manage`           |
| `assignedBy`  | ObjectId  |          | Employee who made the assignment                          |
| `assignedAt`  | Date      |          | Default timestamp for when the assignment was made        |
| `expiresAt`   | Date      |          | Optional expiration for time-limited roles                |

---

#### 🧾 Mongoose Schema: `employeeSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const assignmentSchema = new Schema({
  scopeType: {
    type: String,
    enum: ['provider', 'clinic', 'booth'],
    required: true
  },
  entityId: {
    type: Schema.Types.ObjectId,
    required: true,
    refPath: 'assignments.scopeType'
  },
  scopeName: {
    type: String
  },
  role: {
    type: Schema.Types.ObjectId,
    ref: 'Role',
    required: true
  },
  permissions: {
    type: [String],
    enum: ['read', 'write', 'manage'],
    default: ['read']
  },
  assignedBy: {
    type: Schema.Types.ObjectId,
    ref: 'Employee'
  },
  assignedAt: {
    type: Date,
    default: Date.now
  },
  expiresAt: {
    type: Date
  }
}, { _id: false });

const employeeSchema = new Schema({
  employeeId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },

  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  phone: { type: String },

  assignments: {
    type: [assignmentSchema],
    required: true
  },

  status: {
    type: String,
    enum: ['active', 'inactive', 'archived'],
    default: 'active'
  },

  metadata: {
    type: Schema.Types.Mixed,
    default: {}
  }

}, { timestamps: true });

module.exports = mongoose.model('Employee', employeeSchema);
```

---

### 5. 🛡️ **Role**

#### 📖 Overview-Role

A **role** defines the title, permissions, and scope of responsibility that an employee can have within the system. Roles are reusable across entities (e.g., a `clinic_admin` role may apply to multiple clinics) and allow centralized control over what actions different types of users can perform.

Each role is tied to a **scope type** (e.g., `provider`, `clinic`, or `booth`), and comes with a default set of **permissions** (`read`, `write`, or `manage`). These can be customized per assignment.

---

#### 🧬 Role Database Table

| Field                     | Type      | Required | Description                                                             |
| ------------------------- | --------- | -------- | ----------------------------------------------------------------------- |
| `_id`                     | ObjectId  | ✅        | MongoDB auto-generated unique identifier                                |
| `roleKey`                 | String    | ✅ Unique | Machine-friendly identifier (e.g. `super_admin`, `technician`)          |
| `label`                   | String    | ✅        | Human-readable title for UI (e.g. “Super Admin”, “Hearing Specialist”)  |
| `description`             | String    |          | Optional explanation of the role’s responsibilities                     |
| `scopeType`               | String    | ✅        | Context where this role is applicable: `provider`, `clinic`, or `booth` |
| `defaultPermissions`      | \[String] | ✅        | Default set of actions allowed: `read`, `write`, `manage`               |
| `createdAt` / `updatedAt` | Date      | ✅        | Auto-managed timestamps for record creation and updates                 |

---

#### 🧾 Mongoose Schema: `roleSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const roleSchema = new Schema({
  roleKey: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },

  label: {
    type: String,
    required: true
  },

  description: {
    type: String
  },

  scopeType: {
    type: String,
    enum: ['provider', 'clinic', 'booth'],
    required: true
  },

  defaultPermissions: {
    type: [String],
    enum: ['read', 'write', 'manage'],
    default: ['read']
  }

}, { timestamps: true });

module.exports = mongoose.model('Role', roleSchema);
```

---

### 6. 🧍‍♂️ **Patient**

#### 📖 Overview-Patient

A **patient** represents an individual receiving care, testing, or consultation within the system. Patients are core entities tracked across clinics, booths, and providers. They can be associated with appointments, test results, care plans, and other clinical records.

Patient records are designed to support extensibility, regulatory compliance, and localization, including support for multiple identifiers, emergency contacts, visitation logs, and geospatial metadata.

---

#### 🧬 Patient Database Table

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

#### 🔗 Embedded Fields

#### 📍 Address

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

#### 🆔 Identifier

```json
{
  "type": "string",   // e.g. "national_id", "insurance_id", "mrn"
  "value": "string",  // actual ID value
  "issuer": "string"  // optional source or authority
}
```

#### 🆘 Emergency Contact

```json
{
  "name": "string",
  "relationship": "string",
  "phone": "string",
  "email": "string"
}
```

---

#### 🧾 Mongoose Schema: `patientSchema.js`

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

## 🔗 Reference Relationships

| Model    | References                         | Referenced By                         |
| -------- | ---------------------------------- | ------------------------------------- |
| Provider | —                                  | Clinics, Employees                    |
| Clinic   | `provider`                         | Booths, Employees                     |
| Booth    | `clinic`                           | Employees, Patients (via tests)       |
| Employee | `assignments → entityId + role`    | —                                     |
| Role     | —                                  | Employees (via assignments)           |
| Patient  | `booth`, `tests`, `questionnaires` | Audiogram, DIN, Questionnaire modules |

---

## 📖 Shared Schema Conventions

| Field                     | Description                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| `status`                  | Common lifecycle marker: `active`, `inactive`, `archived`, or `deceased` |
| `metadata`                | Extensible `object` for notes, tags, or third-party integration flags    |
| `coordinates`             | GeoJSON `Point` object for spatial indexing in address models            |
| `createdAt` / `updatedAt` | Auto-managed timestamps via Mongoose schema options                      |

---
