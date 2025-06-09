# 👨‍⚕️ Employee

## 🧬 Employee Database Table

| Field                     | Type         | Required | Notes                                                   |
| ------------------------- | ------------ | -------- | ------------------------------------------------------- |
| `_id`                     | ObjectId     | ✅        | MongoDB default                                         |
| `employeeId`              | String       | ✅ Unique | Slug, UUID, or internal employee code                   |
| `firstName`               | String       | ✅        | First name                                              |
| `lastName`                | String       | ✅        | Last name                                               |
| `email`                   | String       | ✅ Unique | Primary email for login or contact                      |
| `phone`                   | String       |          | Optional contact number                                 |
| `assignments`             | Array        | ✅        | List of `{ entityType, entityId, role }` per assignment |
| `status`                  | String       | ✅        | `active`, `inactive`, or `archived`                     |
| `metadata`                | Mixed Object |          | Flexible object for permissions, notes, or HR data      |
| `createdAt` / `updatedAt` | Date         | ✅        | Managed by Mongoose                                     |

---

## 🧾 Mongoose Schema: `employeeSchema.js`

```js
const mongoose = require('mongoose');
const { Schema } = mongoose;

const assignmentSchema = new Schema({
  entityType: {
    type: String,
    enum: ['provider', 'clinic', 'booth'],
    required: true
  },
  entityId: {
    type: Schema.Types.ObjectId,
    required: true,
    refPath: 'assignments.entityType'
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
  }
}, { _id: false });

const employeeSchema = new Schema({
  employeeId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },

  firstName: {
    type: String,
    required: true
  },

  lastName: {
    type: String,
    required: true
  },

  email: {
    type: String,
    required: true,
    unique: true
  },

  phone: {
    type: String
  },

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
