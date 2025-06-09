# 🧾 System Data Model Overview

This document provides a high-level overview of the core data structure for your system, centered around:

```bash
Provider → Clinics → Booths → Employees
```

Each level builds on the previous and represents a real-world organizational or operational structure.

---

## 🏗️ Entity Relationships

```plaintext
Provider
├── has many Clinics
│   ├── has many Booths
│   │   └── has many Employees (optional)
│   └── has many Employees
└── has many Employees
```

---

## 📦 Models Overview

### 1. 🧠 **Provider**

Represents the top-level organization (e.g. a hospital group, NGO, school system).

* Has many **Clinics**
* May directly employ **Employees** at the provider level

🔗 [View Provider Schema →](./provider.md)

---

### 2. 🏥 **Clinic**

A physical or virtual facility under a Provider.

* Belongs to a **Provider**
* May host multiple **Booths**
* May have assigned **Employees**

🔗 [View Clinic Schema →](./clinic.md)

---

### 3. 🎧 **Booth**

An individual testing or service station (room, kiosk, or mobile unit).

* Belongs to a **Clinic**
* Can be configured with test settings
* May be staffed with **Employees**

🔗 [View Booth Schema →](./booth.md)

---

### 4. 👨‍⚕️ **Employee**

Staff member associated with a Provider, Clinic, or Booth.

* Can be associated with any level of the hierarchy
* Has a defined `role` and `status`
* Used for access control, scheduling, assignments

🔗 [View Employee Schema →](./employee.md)

---

## ⚙️ Relationship Summary Table

| Model    | References                    | Referenced By      |
| -------- | ----------------------------- | ------------------ |
| Provider | —                             | Clinics, Employees |
| Clinic   | `provider`                    | Booths, Employees  |
| Booth    | `clinic`                      | Employees          |
| Employee | `provider`, `clinic`, `booth` | —                  |

---

## 🔐 Common Field Conventions

* **`status`**: Used across entities to manage lifecycle (`active`, `inactive`, `archived`)
* **`metadata`**: Flexible field for custom flags, notes, or external integration data
* **`address.coordinates`**: GeoJSON used in Provider, Clinic, Booth for map-based queries

---

## 🧩 Optional Extensions

You can extend this model with:

* **Appointments** (linked to Booth, Patient, and Time)
* **Schedules** or **Shifts** for Employees
* **Audit logs** for changes
* **Permissions / Roles** at a finer level

---
