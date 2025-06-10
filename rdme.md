# 🗃️ TrueHear Database Design

## Revision: 2025-06-09

This document provides an architectural overview of the **TrueHear backend data model**, consolidating all core schemas across operational, user, and clinical domains. The goal is to enable consistent implementation, maintenance, and onboarding for teams working with the TrueHear system.

---

## 📚 Table of Contents

- [🗃️ TrueHear Database Design](#️-truehear-database-design)
  - [Revision: 2025-06-09](#revision-2025-06-09)
  - [📚 Table of Contents](#-table-of-contents)
  - [🏗️ Entity Relationship Summary](#️-entity-relationship-summary)
  - [📦 Core Data Models](#-core-data-models)
    - [1. 🧠 **Provider**](#1--provider)
    - [2. 🏥 **Clinic**](#2--clinic)
    - [3. 🎧 **Booth**](#3--booth)
    - [4. 👨‍⚕️ **Employee**](#4-️-employee)
    - [5. 🛡️ **Role**](#5-️-role)
    - [6. 🧍‍♂️ **Patient**](#6-️-patient)
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

Top-level institution (e.g., a hospital chain, NGO, or public health agency).

🔗 [View Schema →](./provider.md)

---

### 2. 🏥 **Clinic**

Represents a physical or virtual branch under a provider.

🔗 [View Schema →](./clinic.md)

---

### 3. 🎧 **Booth**

A dedicated point of care delivery (e.g., room, kiosk, or remote unit).

🔗 [View Schema →](./Booth.md)

---

### 4. 👨‍⚕️ **Employee**

System users with roles and permissions. Can be assigned to any level: provider, clinic, or booth.

🔗 [View Schema →](./Employee.md)

---

### 5. 🛡️ **Role**

Defines permission levels (`read`, `write`, `manage`) for various scopes.

🔗 [View Schema →](./Role.md)

---

### 6. 🧍‍♂️ **Patient**

Represents an individual receiving care, testing, or participating in assessments.

🔗 [View Schema →](./Patient.md)

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
