IF OBJECT_ID('employees', 'U') IS NULL
CREATE TABLE dbo.employees (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255),
    personnel_number NVARCHAR(100) UNIQUE,
    department NVARCHAR(100),
    operation_type NVARCHAR(100),
    category NVARCHAR(50),
    CONSTRAINT check_employee_category
        CHECK (category IN (N'руководитель', N'специалист', N'рабочий'))
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

IF OBJECT_ID('work_types', 'U') IS NULL
CREATE TABLE work_types (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE
);
