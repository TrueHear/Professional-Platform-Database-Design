# 📦 Booth

## 📖 Overview

A **booth** represents a testing, diagnostic, or service station within a clinic. Booths are tied to a single **clinic** and often serve patients for specific services such as audiometry or questionnaire-based assessments. Each booth can be configured with its own settings, test options, hardware limits, and staff assignments.

Booths support local customization of diagnostic workflows, employee assignments, and test settings. They can be physical (e.g., a soundproof room), semi-mobile (e.g., a kiosk), or virtual (e.g., telehealth setups).

---

## 🧩 Booth Database Table

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

## 🧾 Mongoose Schema: `boothSchema.js`

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
