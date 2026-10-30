-- AegisHealth ERP schema (SQLite flavour; swap AUTOINCREMENT for SERIAL/IDENTITY on Postgres/MySQL)
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'receptionist',
  active BOOLEAN DEFAULT 1
);
CREATE TABLE patients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mrn VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(80) NOT NULL,
  last_name VARCHAR(80) NOT NULL,
  dob DATE NOT NULL,
  gender VARCHAR(10),
  phone VARCHAR(30),
  email VARCHAR(120),
  address VARCHAR(255),
  blood_group VARCHAR(5),
  allergies VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE doctors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
  specialization VARCHAR(80),
  license_no VARCHAR(40),
  department VARCHAR(80)
);
CREATE TABLE appointments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  doctor_id INTEGER NOT NULL REFERENCES doctors(id),
  scheduled_at DATETIME NOT NULL,
  duration_min INTEGER DEFAULT 30,
  status VARCHAR(20) DEFAULT 'scheduled',
  reason VARCHAR(255)
);
CREATE INDEX ix_appt_doctor_time ON appointments(doctor_id, scheduled_at);
CREATE TABLE medical_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  doctor_id INTEGER NOT NULL REFERENCES doctors(id),
  appointment_id INTEGER REFERENCES appointments(id),
  diagnosis VARCHAR(255) NOT NULL,
  notes TEXT,
  prescription TEXT,
  bp VARCHAR(10),
  heart_rate INTEGER,
  temperature_c FLOAT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE invoices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  appointment_id INTEGER REFERENCES appointments(id),
  total FLOAT DEFAULT 0,
  paid FLOAT DEFAULT 0,
  status VARCHAR(10) DEFAULT 'unpaid',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE invoice_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  description VARCHAR(200) NOT NULL,
  quantity INTEGER DEFAULT 1,
  unit_price FLOAT NOT NULL
);
CREATE TABLE medicines (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(120) NOT NULL,
  sku VARCHAR(40) NOT NULL UNIQUE,
  stock INTEGER DEFAULT 0,
  reorder_level INTEGER DEFAULT 20,
  unit_price FLOAT DEFAULT 0,
  expiry_date DATE
);
