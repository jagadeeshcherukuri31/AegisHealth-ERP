# Architecture

```
Browser (static SPA)  --JSON/JWT-->  Flask app  -->  SQLAlchemy  -->  SQLite (swap via DATABASE_URL)
```

- **frontend/**: hash-routed single page app. `app.js` provides the router, modal forms and table helper; each
  feature file (`patients.js`, `billing.js`, ...) registers itself with `Aegis.register(id, {label, roles, render})`.
- **backend/app/routes**: thin HTTP layer. Validates input, checks role with `@roles_required`, calls a service.
- **backend/app/services**: business rules (double-booking check, payment totals, stock and expiry checks).
- **backend/app/models**: one file per aggregate. `Serializable.to_dict()` handles JSON output.
- **database/**: `schema.sql` mirrors the models for manual setup; `seed.sql` loads demo data.

## Data model

users 1-1 doctors; patients 1-n appointments, medical_records, invoices; doctors 1-n appointments, medical_records;
invoices 1-n invoice_items; medicines stand alone.

## Rules enforced server-side

- A doctor cannot have overlapping `scheduled`/`checked_in` appointments.
- Payments cannot exceed the invoice balance; status moves unpaid -> partial -> paid.
- Dispensing fails on insufficient stock or expired batches.
- Only doctors (and admin) may write medical records.
