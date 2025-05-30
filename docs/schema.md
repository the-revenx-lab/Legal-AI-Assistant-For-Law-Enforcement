# Database Schema Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core Tables](#core-tables)
3. [Authentication Tables](#authentication-tables)
4. [FIR Management Tables](#fir-management-tables)
5. [IPC Database Tables](#ipc-database-tables)
6. [Chat History Tables](#chat-history-tables)
7. [Audit Tables](#audit-tables)
8. [Relationships](#relationships)
9. [Indexes](#indexes)

## Overview

The database is designed to support the Legal AI Assistant system with the following key features:
- User authentication and authorization
- FIR management and tracking
- IPC sections and crime classification
- Chat history and conversation tracking
- Audit logging and system monitoring

## Core Tables

### Users
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    badge_number VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    role VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    CONSTRAINT chk_role CHECK (role IN ('admin', 'officer', 'supervisor'))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_badge ON users(badge_number);
```

### Departments
```sql
CREATE TABLE departments (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    jurisdiction VARCHAR(100),
    contact_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Authentication Tables

### Sessions
```sql
CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_expiry ON sessions(expires_at);
```

### Password_Reset_Tokens
```sql
CREATE TABLE password_reset_tokens (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## FIR Management Tables

### FIR
```sql
CREATE TABLE fir (
    id VARCHAR(36) PRIMARY KEY,
    fir_number VARCHAR(50) UNIQUE NOT NULL,
    complainant_name VARCHAR(100) NOT NULL,
    complainant_contact VARCHAR(20),
    complainant_address TEXT,
    incident_date DATE NOT NULL,
    incident_time TIME,
    incident_location TEXT,
    incident_description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    officer_id VARCHAR(36) NOT NULL,
    department_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (officer_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    CONSTRAINT chk_status CHECK (status IN ('pending', 'active', 'closed', 'transferred'))
);

CREATE INDEX idx_fir_number ON fir(fir_number);
CREATE INDEX idx_fir_date ON fir(incident_date);
CREATE INDEX idx_fir_status ON fir(status);
```

### FIR_Sections
```sql
CREATE TABLE fir_sections (
    id VARCHAR(36) PRIMARY KEY,
    fir_id VARCHAR(36) NOT NULL,
    section_id VARCHAR(36) NOT NULL,
    added_by VARCHAR(36) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fir_id) REFERENCES fir(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES ipc_sections(id),
    FOREIGN KEY (added_by) REFERENCES users(id)
);

CREATE INDEX idx_fir_sections ON fir_sections(fir_id, section_id);
```

### FIR_Witnesses
```sql
CREATE TABLE fir_witnesses (
    id VARCHAR(36) PRIMARY KEY,
    fir_id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    address TEXT,
    statement TEXT,
    recorded_by VARCHAR(36) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fir_id) REFERENCES fir(id) ON DELETE CASCADE,
    FOREIGN KEY (recorded_by) REFERENCES users(id)
);
```

### FIR_Evidence
```sql
CREATE TABLE fir_evidence (
    id VARCHAR(36) PRIMARY KEY,
    fir_id VARCHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    location TEXT,
    collected_by VARCHAR(36) NOT NULL,
    collected_at TIMESTAMP,
    chain_of_custody TEXT,
    status VARCHAR(20) DEFAULT 'collected',
    FOREIGN KEY (fir_id) REFERENCES fir(id) ON DELETE CASCADE,
    FOREIGN KEY (collected_by) REFERENCES users(id)
);
```

## IPC Database Tables

### IPC_Sections
```sql
CREATE TABLE ipc_sections (
    id VARCHAR(36) PRIMARY KEY,
    section_number VARCHAR(20) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    punishment TEXT,
    category VARCHAR(50),
    is_cognizable BOOLEAN DEFAULT FALSE,
    is_bailable BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_section_number ON ipc_sections(section_number);
CREATE INDEX idx_category ON ipc_sections(category);
```

### Related_Sections
```sql
CREATE TABLE related_sections (
    id VARCHAR(36) PRIMARY KEY,
    section_id VARCHAR(36) NOT NULL,
    related_section_id VARCHAR(36) NOT NULL,
    relationship_type VARCHAR(50),
    FOREIGN KEY (section_id) REFERENCES ipc_sections(id),
    FOREIGN KEY (related_section_id) REFERENCES ipc_sections(id),
    CONSTRAINT unique_relation UNIQUE (section_id, related_section_id)
);
```

### Case_Precedents
```sql
CREATE TABLE case_precedents (
    id VARCHAR(36) PRIMARY KEY,
    section_id VARCHAR(36) NOT NULL,
    case_title VARCHAR(255) NOT NULL,
    case_number VARCHAR(100),
    court VARCHAR(100),
    judgment_date DATE,
    summary TEXT,
    citation TEXT,
    FOREIGN KEY (section_id) REFERENCES ipc_sections(id)
);

CREATE INDEX idx_case_precedents ON case_precedents(section_id);
```

## Chat History Tables

### Chat_Sessions
```sql
CREATE TABLE chat_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_chat_user ON chat_sessions(user_id);
```

### Chat_Messages
```sql
CREATE TABLE chat_messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    sender_type ENUM('user', 'bot') NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intent VARCHAR(100),
    confidence DECIMAL(5,4),
    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) ON DELETE CASCADE
);

CREATE INDEX idx_chat_session ON chat_messages(session_id);
CREATE INDEX idx_message_time ON chat_messages(timestamp);
```

## Audit Tables

### Activity_Log
```sql
CREATE TABLE activity_log (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    action VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id VARCHAR(36),
    details JSON,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_activity_time ON activity_log(timestamp);
CREATE INDEX idx_activity_user ON activity_log(user_id);
```

### Error_Log
```sql
CREATE TABLE error_log (
    id VARCHAR(36) PRIMARY KEY,
    error_type VARCHAR(50) NOT NULL,
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    user_id VARCHAR(36),
    ip_address VARCHAR(45),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_error_time ON error_log(timestamp);
```

## Relationships

### Key Relationships
1. Users → Departments (Many-to-One)
2. FIR → Users (Many-to-One)
3. FIR → Departments (Many-to-One)
4. FIR_Sections → FIR (Many-to-One)
5. FIR_Sections → IPC_Sections (Many-to-One)
6. Chat_Sessions → Users (Many-to-One)
7. Chat_Messages → Chat_Sessions (Many-to-One)

## Indexes

### Performance Indexes
1. Users table:
   - Email (for login)
   - Badge number (for queries)

2. FIR table:
   - FIR number (for lookups)
   - Status (for filtering)
   - Incident date (for date-based queries)

3. IPC_Sections table:
   - Section number (for direct lookups)
   - Category (for filtering)

4. Chat tables:
   - Session timestamps (for time-based queries)
   - User ID (for user history)

### Foreign Key Indexes
All foreign key columns have corresponding indexes for improved join performance.

## Views

### Active_Cases_View
```sql
CREATE VIEW active_cases_view AS
SELECT 
    f.id,
    f.fir_number,
    f.complainant_name,
    f.incident_date,
    f.status,
    u.name as officer_name,
    d.name as department_name,
    GROUP_CONCAT(DISTINCT is.section_number) as sections
FROM fir f
JOIN users u ON f.officer_id = u.id
JOIN departments d ON f.department_id = d.id
LEFT JOIN fir_sections fs ON f.id = fs.fir_id
LEFT JOIN ipc_sections is ON fs.section_id = is.id
WHERE f.status = 'active'
GROUP BY f.id;
```

### Case_Statistics_View
```sql
CREATE VIEW case_statistics_view AS
SELECT 
    d.name as department,
    COUNT(f.id) as total_cases,
    SUM(CASE WHEN f.status = 'active' THEN 1 ELSE 0 END) as active_cases,
    SUM(CASE WHEN f.status = 'closed' THEN 1 ELSE 0 END) as closed_cases,
    AVG(DATEDIFF(CASE 
        WHEN f.status = 'closed' THEN f.updated_at 
        ELSE CURRENT_TIMESTAMP 
    END, f.created_at)) as avg_resolution_days
FROM departments d
LEFT JOIN fir f ON d.id = f.department_id
GROUP BY d.id;
``` 