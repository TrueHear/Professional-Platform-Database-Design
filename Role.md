# 📘 `Role.md`

## 🧬 Role Database Table

| Field                     | Type      | Required | Notes                                                              |
| ------------------------- | --------- | -------- | ------------------------------------------------------------------ |
| `_id`                     | ObjectId  | ✅        | MongoDB default                                                    |
| `roleKey`                 | String    | ✅ Unique | Internal key (e.g. `super_admin`, `technician`)                    |
| `label`                   | String    | ✅        | Human-readable display name (e.g. "Super Admin")                   |
| `description`             | String    |          | What this role does or controls                                    |
| `scopeType`               | String    | ✅        | Entity this role can be assigned to: `provider`, `clinic`, `booth` |
| `defaultPermissions`      | \[String] | ✅        | Access rights: `read`, `write`, `manage`                           |
| `createdAt` / `updatedAt` | Date      | ✅        | Mongoose timestamps                                                |

---

## 🧾 Mongoose Schema: `roleSchema.js`

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

# 👨‍⚕️ `Employee.md` (With Centralized Role Model)

## 🧬 Employee Database Table

| Field                     | Type         | Required | Notes                                                          |
| ------------------------- | ------------ | -------- | -------------------------------------------------------------- |
| `_id`                     | ObjectId     | ✅        | MongoDB default                                                |
| `employeeId`              | String       | ✅ Unique | Slug, UUID, or internal employee code                          |
| `firstName`               | String       | ✅        | First name                                                     |
| `lastName`                | String       | ✅        | Last name                                                      |
| `email`                   | String       | ✅ Unique | Primary email for login or contact                             |
| `phone`                   | String       |          | Optional contact number                                        |
| `assignments`             | Array        | ✅        | Role assignments, each referencing a role, entity, permissions |
| `status`                  | String       | ✅        | `active`, `inactive`, or `archived`                            |
| `metadata`                | Mixed Object |          | Flexible object for HR data, tags, notes, etc.                 |
| `createdAt` / `updatedAt` | Date         | ✅        | Managed by Mongoose                                            |

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
