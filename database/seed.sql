-- Demo data. Every demo account uses the password: Aegis@123
INSERT INTO users (name,email,password_hash,role) VALUES
 ('Ada Admin','admin@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','admin'),
 ('Dr. Maya Rao','doctor@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','doctor'),
 ('Dr. Leo Park','leo@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','doctor'),
 ('Nora Nurse','nurse@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','nurse'),
 ('Rita Reception','reception@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','receptionist'),
 ('Paul Pharma','pharmacy@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','pharmacist'),
 ('Bill Accounts','billing@aegis.test','scrypt:32768:8:1$Y9uKwRqYKaOeLuHc$06551e3e4ba3ac4deeb20c0578f7cfafe13e19e2a4d358f9770f1804172355e9652019b81bd36dc8d8fc91e21f98171a5533510571fc35907443f82a99c7e564','billing');
INSERT INTO doctors (user_id,specialization,license_no,department) VALUES
 (2,'Cardiology','LIC-1001','Cardiology'),(3,'General Medicine','LIC-1002','OPD');
INSERT INTO patients (mrn,first_name,last_name,dob,gender,phone,blood_group,allergies) VALUES
 ('MRN000001','Sam','Carter','1985-04-12','Male','555-0101','O+','Penicillin'),
 ('MRN000002','Priya','Nair','1992-09-30','Female','555-0102','A+',NULL),
 ('MRN000003','John','Okafor','1970-01-05','Male','555-0103','B-','Latex'),
 ('MRN000004','Elena','Rossi','2001-11-21','Female','555-0104','AB+',NULL);
INSERT INTO appointments (patient_id,doctor_id,scheduled_at,duration_min,status,reason) VALUES
 (1,1,datetime('now','start of day','+9 hours'),30,'checked_in','Chest pain follow-up'),
 (2,2,datetime('now','start of day','+10 hours'),30,'scheduled','Routine check-up'),
 (3,1,datetime('now','start of day','+11 hours'),45,'scheduled','ECG review'),
 (4,2,datetime('now','start of day','+1 day','+9 hours'),30,'scheduled','Vaccination');
INSERT INTO medical_records (patient_id,doctor_id,appointment_id,diagnosis,notes,prescription,bp,heart_rate,temperature_c) VALUES
 (1,1,1,'Stable angina','Advised lifestyle changes.','Aspirin 75mg daily','130/85',78,36.8);
INSERT INTO invoices (patient_id,appointment_id,total,paid,status) VALUES (1,1,180,0,'unpaid'),(2,NULL,60,60,'paid');
INSERT INTO invoice_items (invoice_id,description,quantity,unit_price) VALUES
 (1,'Cardiology consultation',1,150),(1,'ECG',1,30),(2,'General consultation',1,60);
INSERT INTO medicines (name,sku,stock,reorder_level,unit_price,expiry_date) VALUES
 ('Paracetamol 500mg','MED-001',240,50,0.10,'2027-08-01'),
 ('Amoxicillin 250mg','MED-002',18,30,0.45,'2027-02-01'),
 ('Aspirin 75mg','MED-003',120,40,0.08,'2027-05-01'),
 ('Metformin 500mg','MED-004',8,25,0.20,'2026-12-01');
