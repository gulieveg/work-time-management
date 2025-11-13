IF OBJECT_ID('departments', 'U') IS NULL
CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    is_production BIT NOT NULL DEFAULT 0
);

IF OBJECT_ID('employees', 'U') IS NULL
CREATE TABLE employees (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255),
    personnel_number NVARCHAR(100) UNIQUE,
    department NVARCHAR(100),
    category NVARCHAR(50),
    CONSTRAINT check_employee_category
        CHECK (category IN (N'worker', N'specialist', N'manager'))
);

IF OBJECT_ID('orders', 'U') IS NULL
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    number NVARCHAR(100) UNIQUE
);

IF OBJECT_ID('tasks', 'U') IS NULL
CREATE TABLE tasks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    employee_name NVARCHAR(100),
    personnel_number NVARCHAR(100),
    department NVARCHAR(100),
    operation_type NVARCHAR(100),
    hours DECIMAL(3,2),
    order_number NVARCHAR(100),
    order_name NVARCHAR(100),
    operation_date DATE DEFAULT GETDATE(),
    employee_category NVARCHAR(50)
);

IF OBJECT_ID('users', 'U') IS NULL
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    login NVARCHAR(100) UNIQUE,
    password_hash NVARCHAR(255),
    permissions_level NVARCHAR(50) DEFAULT 'standard',
    is_enabled BIT NOT NULL DEFAULT 0,
    is_factory_worker BIT NOT NULL DEFAULT 0,
    CONSTRAINT check_permissions_level
        CHECK (permissions_level IN ('minimal', 'standard', 'advanced'))
);

IF OBJECT_ID('works', 'U') IS NULL
CREATE TABLE works (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    name NVARCHAR(255) NOT NULL,
    planned_hours DECIMAL(10,2) NOT NULL,
    spent_hours DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- UPDATE employees
-- SET category = CASE category
--     WHEN N'Руководитель' THEN 'manager'
--     WHEN N'Специалист' THEN 'specialist'
--     WHEN N'Рабочий' THEN 'worker'
--     ELSE NULL
-- END;

-- ALTER TABLE employees
-- DROP CONSTRAINT check_employee_category;

-- ALTER TABLE employees
-- ADD CONSTRAINT check_employee_category
-- CHECK (category IN (N'worker', N'specialist', N'manager'));
