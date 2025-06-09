# 👨‍⚕️ Employee

## 📖 Overview

An **employee** is a system user who can work at various levels: provider, clinic, or booth. Each employee can hold multiple roles, assigned per scope (e.g., clinic or booth), and can have specific permissions based on that role. Assignments include references to the role model and allow tracking who assigned them, when, and for how long.

---

## 🧬 Employee Database Table

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

## 📘 Assignment Structure (`assignments`)

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
