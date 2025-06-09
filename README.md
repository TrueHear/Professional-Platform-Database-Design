# 🧾 System Data Model Overview

```plaintext
Provider → Clinic → Booth → Employee
```

Each level represents a physical or virtual component of your operational network, with employees optionally assigned at any layer.

---

## 🏗️ Entity Relationship Diagram

```plaintext
Provider
├── Clinics
│   ├── Booths
│   │   └── Employees
│   └── Employees
└── Employees
```

---

## 📦 Core Models Overview

### 1. 🧠 **Provider**

Represents the top-level institution or organization, such as a hospital chain, NGO, or national agency.

* Can manage multiple **Clinics**
* Can employ **Employees** at the organization-wide level
* Has an address and metadata for configuration and compliance

🔗 [View Provider Schema →](./provider.md)

---

### 2. 🏥 **Clinic**

Represents a location or branch under a Provider. Can be physical (e.g. building) or virtual (e.g. telehealth service unit).

* Belongs to a **Provider**
* Can include multiple **Booths**
* Can have **Employees** scoped to the clinic

🔗 [View Clinic Schema →](./clinic.md)

---

### 3. 🎧 **Booth**

Represents a dedicated service point for testing, diagnosis, or care delivery. Can be a room, mobile unit, kiosk, or digital station.

* Belongs to a **Clinic**
* Configurable with test settings and limits
* May include hardware-specific configurations
* Supports dedicated **Employees**

🔗 [View Booth Schema →](./booth.md)

---

### 4. 👨‍⚕️ **Employee**

Represents any system user responsible for operations, care, or administration.

* Can be assigned to a **Provider**, **Clinic**, or **Booth**
* Assignment includes a **Role** and **Permissions**
* Supports multiple active assignments
* Centralized `Role` model enables reusable role definitions

🔗 [View Employee Schema →](./employee.md)

---

### 5. 🛡️ **Role**

Central definition for titles, access levels, and scope applicability.

* Defines what each employee *can do* based on their assignment
* Supports predefined **permissions** like `read`, `write`, and `manage`
* Scoped per level: `provider`, `clinic`, or `booth`

🔗 [View Role Schema →](./role.md)

---

## ⚙️ Reference Table

| Model    | References                      | Referenced By               |
| -------- | ------------------------------- | --------------------------- |
| Provider | —                               | Clinics, Employees          |
| Clinic   | `provider`                      | Booths, Employees           |
| Booth    | `clinic`                        | Employees                   |
| Employee | `assignments → entityId + role` | —                           |
| Role     | —                               | Employees (via assignments) |

---

## 🧩 Shared Field Conventions

| Field         | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `status`      | Common status for lifecycle control (`active`, `inactive`, `archived`)      |
| `metadata`    | Open field for extensibility (flags, tags, notes, integrations)             |
| `coordinates` | GeoJSON used in address fields for geospatial indexing and location queries |

---
