# 👨‍⚕️ Employee

## 🧬 Employee Database Table

| Field                     | Type         | Required | Notes                                                             |
| ------------------------- | ------------ | -------- | ----------------------------------------------------------------- |
| `_id`                     | ObjectId     | ✅        | MongoDB default                                                   |
| `employeeId`              | String       | ✅ Unique | Slug, UUID, or internal employee code                             |
| `firstName`               | String       | ✅        | First name                                                        |
| `lastName`                | String       | ✅        | Last name                                                         |
| `email`                   | String       | ✅ Unique | Primary email for login or contact                                |
| `phone`                   | String       |          | Optional contact number                                           |
| `assignments`             | Array        | ✅        | Roles scoped to `provider`, `clinic`, or `booth` with permissions |
| `status`                  | String       | ✅        | `active`, `inactive`, or `archived`                               |
| `metadata`                | Mixed Object |          | Flexible object for permissions, notes, or HR data                |
| `createdAt` / `updatedAt` | Date         | ✅        | Managed by Mongoose                                               |

---

## 📦 Assignment Structure

Each object inside the `assignments` array:

| Field         | Type      | Required | Notes                                                       |
| ------------- | --------- | -------- | ----------------------------------------------------------- |
| `scopeType`   | String    | ✅        | `provider`, `clinic`, or `booth`                            |
| `entityId`    | ObjectId  | ✅        | Refers to the corresponding `scopeType` model               |
| `scopeName`   | String    |          | Optional name (denormalized) for display/logging            |
| `role`        | String    | ✅        | Role within the entity: `super_admin`, `clinic_admin`, etc. |
| `permissions` | \[String] |          | Optional: `read`, `write`, `manage` (action-level access)   |
| `assignedBy`  | ObjectId  |          | Ref: `Employee` who made the assignment                     |
| `assignedAt`  | Date      |          | Auto timestamp when the assignment was created              |
| `expiresAt`   | Date      |          | Optional expiration timestamp for temporary access          |

---

## 🧾 Mongoose Schema: `employeeSchema.js`

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
    type: String // optional for UI/logging
  },
  role: {
    type: String,
    enum: [
      'super_admin',
      'clinic_admin',
      'professional',
      'technician',
      'support',
      'other'
    ],
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
