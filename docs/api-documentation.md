# API

Base URL `/api`. Send `Authorization: Bearer <token>` on everything except login. Errors return `{"error": "..."}`.

| Method & path | Roles | Notes |
|---|---|---|
| POST /auth/login | public | `{email,password}` -> `{token,user}` |
| GET /auth/me | any | current user |
| POST /auth/register | admin | `{name,email,password,role}` |
| GET /patients?q= | clinical, billing, pharmacist | search name, MRN, phone |
| POST /patients | receptionist, nurse, doctor | needs first_name, last_name, dob; MRN auto-generated |
| GET/PUT /patients/:id | as above | |
| DELETE /patients/:id | admin | |
| GET /appointments?date=&doctor_id=&patient_id=&status= | doctor, nurse, receptionist, billing | |
| GET /appointments/doctors | same | |
| POST /appointments | receptionist, nurse, doctor | `{patient_id,doctor_id,scheduled_at,duration_min,reason}`; 400 on conflict |
| PATCH /appointments/:id/status | doctor, nurse, receptionist | scheduled, checked_in, completed, cancelled, no_show |
| GET /ehr?patient_id= | doctor, nurse | |
| POST /ehr | doctor | `{patient_id,doctor_id,diagnosis,notes,prescription,bp,heart_rate,temperature_c}` |
| GET /billing?status= | billing, receptionist | |
| POST /billing | billing, receptionist | `{patient_id,items:[{description,quantity,unit_price}]}` |
| POST /billing/:id/pay | billing, receptionist | `{amount}` (defaults to full balance) |
| GET /pharmacy?q= | pharmacist, doctor, nurse | |
| GET /pharmacy/alerts | pharmacist | low stock + expiring within 60 days |
| POST /pharmacy, /pharmacy/:id/restock, /pharmacy/:id/dispense | pharmacist | |
| GET /dashboard | any | summary counts and today's queue |

Admin passes every role check.
