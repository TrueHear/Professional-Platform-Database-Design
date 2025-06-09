# 📘 Role

## 📖 Overview

A **role** defines the title, permissions, and scope of responsibility that an employee can have within the system. Roles are reusable across entities (e.g., a `clinic_admin` role may apply to multiple clinics) and allow centralized control over what actions different types of users can perform.

Each role is tied to a **scope type** (e.g., `provider`, `clinic`, or `booth`), and comes with a default set of **permissions** (`read`, `write`, or `manage`). These can be customized per assignment.

---

## 🧬 Role Database Table

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
