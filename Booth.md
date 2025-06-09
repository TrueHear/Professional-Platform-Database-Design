# 📦 Booth

## 🧩 Booth Database Table

| Field                                   | Type             | Required | Notes                                                       |
| --------------------------------------- | ---------------- | -------- | ----------------------------------------------------------- |
| `_id`                                   | ObjectId         | ✅        | MongoDB default                                             |
| `boothId`                               | Number           | ✅ Unique | Internal numeric booth identifier                           |
| `boothName`                             | String           | ✅        | Display name of the booth                                   |
| `clinic`                                | ObjectId         | ✅        | Reference to parent Clinic                                  |
| `userName`                              | String           | ✅ Unique | Login username                                              |
| `password`                              | String           | ✅        | Hashed password                                             |
| `boothAddress`                          | String           | ✅        | Display address for humans                                  |
| `status`                                | String           | ✅        | `active`, `inactive`, `maintenance`, or `archived`          |
| `type`                                  | String           |          | `room`, `kiosk`, `mobile`, `outdoor`, `virtual`, or `other` |
| `services`                              | \[String]        |          | List of services offered (e.g. `["audiometry"]`)            |
| `capacity`                              | Number           |          | Optional maximum throughput or occupancy                    |
| `role`                                  | String           |          | Default: `"Booth"`                                          |
| `tests`                                 | \[Object]        |          | Array of test configs with `testId` and `included` flag     |
| `employees`                             | \[ObjectId]      |          | Staff assigned to this booth                                |
| `dinSettings`                           | \[ObjectId]      |          | Ref: `DigitInNoiseSettingv1`                                |
| `dinSettingsRound1Constant`             | \[ObjectId]      |          | Ref: `DigitInNoiseSettingv1`                                |
| `dinSettingsRound2Adaptive`             | \[ObjectId]      |          | Ref: `DigitInNoiseSettingv1`                                |
| `dinSettingsRound3Adaptive`             | \[ObjectId]      |          | Ref: `DigitInNoiseSettingv1`                                |
| `antiphasicDinSettings`                 | \[ObjectId]      |          | Ref: `AntiphasicDigitInNoiseSettingv1`                      |
| `questionaireSettings`                  | \[ObjectId]      |          | Ref: `QuestionaireSetting`                                  |
| `yesNoQuestionnaireSettings`            | \[ObjectId]      |          | Ref: `YesNoQuestionnaireSetting`                            |
| `audiogramSettings`                     | \[ObjectId]      |          | Ref: `AudiogramSettings`                                    |
| `defaultDinSettingsIndex`               | Number           |          | Index into `dinSettings`                                    |
| `defaultDinSettingsRound1ConstantIndex` | Number           |          | Index into `dinSettingsRound1Constant`                      |
| `defaultDinSettingsRound2AdaptiveIndex` | Number           |          | Index into `dinSettingsRound2Adaptive`                      |
| `defaultDinSettingsRound3AdaptiveIndex` | Number           |          | Index into `dinSettingsRound3Adaptive`                      |
| `defaultAntiphasicDinSettingsIndex`     | Number           |          | Index into `antiphasicDinSettings`                          |
| `defaultQuestionaireIndex`              | Number           |          | Index into `questionaireSettings`                           |
| `defaultYesNoQuestionnaireIndex`        | Number           |          | Index into `yesNoQuestionnaireSettings`                     |
| `defaultAudiogramSettingsIndex`         | Number           |          | Index into `audiogramSettings`                              |
| `address`                               | Object (GeoJSON) |          | Geolocation + address details                               |
| `metadata`                              | Mixed Object     |          | For booth-specific custom data                              |
| `createdAt` / `updatedAt`               | Date             | ✅        | Mongoose timestamps                                         |

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
