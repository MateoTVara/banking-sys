-- create database bankingdb;

use bankingdb;

-- === Groups ===
INSERT INTO auth_group (name) VALUES ('admins'), ('employees'), ('clients');

-- === Users ===
INSERT INTO bankingsys_user 
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, failed_attempts) 
VALUES
-- Admin
('pbkdf2_sha256$1000000$ySSH1nq1jGa8A0sSLnoiL2$UsArhNYyrVPfPxDXcX5GY8Jn7e1uOzBDi35bzjJNXqo=', NOW(), 1, 'admin', 'Carlos', 'Admin', 'admin@bank.com', 1, 1, NOW(), 0),
-- Employee
('pbkdf2_sha256$1000000$GiHq7uncU7TXLrlv3ngu2x$rjYQXed0aEiG9C2zV9xhhAk83+8DjZzozxlUvxmFyR0=', NOW(), 0, 'empleado', 'Ana', 'Empleado', 'empleado@bank.com', 1, 1, NOW(), 0);
-- Role Assignation
INSERT INTO bankingsys_user_groups (user_id, group_id) VALUES (1, 1), (2, 2);

-- === Tests ===
INSERT INTO bankingsys_test (name, created_at) VALUES
('Carga inicial', NOW()),
('Prueba movimientos', NOW());

-- === Clients ===
INSERT INTO bankingsys_client (code, client_type, dni, ruc, name, address, phone, email)
VALUES
('C001', 'natural', '12345678', NULL, 'Juan Pérez', 'Av. Siempre Viva 123', '987654321', 'juan.perez@mail.com'),
('C002', 'legal', NULL, '20123456789', 'Inversiones SAC', 'Calle Falsa 456', '912345678', 'contacto@inversiones.com'),
('C003', 'natural', '87654321', NULL, 'María López', 'Jr. Los Sauces 789', '987000111', 'maria.lopez@mail.com'),
('C004', 'legal', NULL, '20456789012', 'Servicios Globales SAC', 'Av. Central 101', '914000222', 'contacto@serviciosglobales.com'),
('C005', 'natural', '11223344', NULL, 'Carlos García', 'Av. Paz 55', '999111222', 'carlos.garcia@mail.com'),
('C006', 'legal', NULL, '20567890123', 'Constructora del Norte S.A.C.', 'Calle Real 321', '945222333', 'info@constructora-norte.com'),
('C007', 'natural', '87654321', NULL, 'Giancarlo Astoray', 'San Isidro', '966666666', 'cliente@gmail.com');

-- === Client User ===
INSERT INTO bankingsys_user 
(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, failed_attempts, client_id) 
VALUES
('pbkdf2_sha256$1000000$srb2N8tx4dEFekt3wXYQaG$DSwOyH8LCFBN0ZJPGKiWgYQ91mNYIqZsisu3oCCtC5Q=', NOW(), 0, 'juanp', 'Juan', 'Pérez', 'juan.perez@mail.com', 0, 1, NOW(), 0, 1),
('pbkdf2_sha256$1000000$A43E6wGHq9cNwMLPYGZSOK$CdrcnQjPt7ZmRszPFRxE7ha99BgrvGLslYqEpcQ6Gdw=', NOW(), 0, 'inversionessac', NULL, NULL, 'contacto@inversiones.com', 0, 1, NOW(), 0, 2),
('pbkdf2_sha256$1000000$bFnmkTvz9fNQYmRn15EmbM$mS9+RWGZJtW+LZQGDwVTKzfyi0Rby/i/CfUQeQjinMs=', NOW(), 0, 'marial', 'María', 'López', 'maria.lopez@mail.com', 0, 1, NOW(), 0, 3),
('pbkdf2_sha256$1000000$OmeBetNfyhvl2H5ummcmY4$iFaM1mAYJl8d/X90oUqLjqfzDQSotGdf8zq3muMWs+A=', NOW(), 0, 'serviciosglobales', NULL, NULL, 'contacto@serviciosglobales.com', 0, 1, NOW(), 0, 4),
('pbkdf2_sha256$1000000$gtU5QiIP3gIxtsZlrM3xih$8j5TGP+j+cpjwzuVu0AUvYX4G5uOTMOJg/HTv57CceI=', NOW(), 0, 'carlosg', 'Carlos', 'García', 'carlos.garcia@mail.com', 0, 1, NOW(), 0, 5),
('pbkdf2_sha256$1000000$Id8BljLmAU3cQaRsPGVrvr$HVNuE4GVDmBXAJ7YWISfSTBMQs4QLnydlk+2Yn3ZaNU=', NOW(), 0, 'constructoranorte', NULL, NULL, 'info@constructora-norte.com', 0, 1, NOW(), 0, 6),
('pbkdf2_sha256$1000000$Ydm1rEIlRlaYp3HfAVYsKz$ozmATQewzQSKc8/bC+8A1LBIrj5gEABerV3/POhejV0=', NOW(), 0, 'cliente', 'Giancarlo', 'Astoray', 'cliente@gmail.com', 0, 1, NOW(), 0, 7);


INSERT INTO bankingsys_user_groups (user_id, group_id) VALUES
(3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3);

-- === Exchange Rates ===
INSERT INTO bankingsys_exchangerate (date, rate)
VALUES
(CURDATE(), 3.8500);

-- === Accounts ===
INSERT INTO bankingsys_account 
(client_id, account_number, account_type, currency, balance, status, overdraft_limit, term_months, monthly_interest, opened_at, closed_at)
VALUES
-- Ahorros
(1, '191-00000001-0-01', 'savings', 'PEN', 1500.00, 'active', 0.00, NULL, NULL, NOW(), NULL), -- id = 1
-- Plazo fijo
(2, '191-00000003-0-03', 'term', 'PEN', 10000.00, 'active', 0.00, 12, 2.50, NOW(), NULL), -- id = 2
-- María López (client_id = 3)
(3, '191-00000004-0-04', 'savings', 'PEN', 2500.00, 'active', 0.00, NULL, NULL, NOW(), NULL), -- id = 3
(3, '191-00000005-0-05', 'term',    'PEN', 5000.00, 'active', 0.00, 6,    1.80, NOW(), NULL), -- id = 4
-- Carlos García (client_id = 5)
(5, '191-00000006-0-06', 'savings', 'USD', 1200.00, 'active', 0.00, NULL, NULL, NOW(), NULL), -- id = 5
(5, '191-00000007-0-07', 'term',    'USD', 3000.00, 'active', 0.00, 12,   2.00, NOW(), NULL), -- id = 6
-- Servicios Globales SAC (client_id = 4)
(4, '191-00000008-0-08', 'current', 'PEN', 15000.00, 'active', 1000.00, NULL, NULL, NOW(), NULL), -- id = 7
(4, '191-00000009-0-09', 'term',    'PEN',  40000.00, 'active', 0.00,    12,   2.75, NOW(), NULL), -- id = 8
-- Constructora del Norte S.A.C. (client_id = 6)
(6, '191-00000010-0-10', 'current', 'USD', 25000.00, 'active', 5000.00, NULL, NULL, NOW(), NULL), -- id = 9
(6, '191-00000011-0-11', 'term',    'USD', 100000.00,'active', 0.00,    24,   3.10, NOW(), NULL), -- id = 10
-- Giancarlo Astoray (client_id = 7)
(7, '191-00000012-0-12', 'savings', 'PEN', 1800.00, 'active', 0.00, NULL, NULL, NOW(), NULL), -- id = 11
(7, '191-00000013-0-13', 'term', 'USD', 5000.00, 'active', 0.00, 12, 2.40, NOW(), NULL); -- id = 12


-- === Judicial Holds ===
INSERT INTO bankingsys_judicialhold (account_id, hold_type, amount, is_active, created_at, removed_at)
VALUES
(1, 'partial', 300.00, 1, NOW(), NULL),
(2, 'total', 0.00, 1, NOW(), NULL);

-- === Account Movements ===
INSERT INTO bankingsys_accountmovement 
(account_id, movement_type, amount, currency, description, created_at, related_account_id, authorized_key, origin_of_funds)
VALUES
-- Depósito en cuenta de ahorros
(1, 'deposit', 500.00, 'PEN', 'Depósito en ventanilla', NOW(), NULL, NULL, 'Sueldo'),
-- Retiro en cuenta de ahorros
(1, 'withdrawal', 200.00, 'PEN', 'Retiro en cajero', NOW(), NULL, NULL, NULL),
-- Transferencia entre cuentas (ahorros → corriente)
(1, 'transfer', 100.00, 'PEN', 'Transferencia a cuenta corriente', NOW(), 2, NULL, NULL),
(2, 'deposit', 100.00, 'USD', 'Transferencia recibida desde ahorros', NOW(), 1, NULL, NULL),
-- Cancelación de cuenta a plazo
(3, 'cancellation', 10000.00, 'PEN', 'Cancelación anticipada', NOW(), NULL, NULL, NULL),
-- María López (savings id = 3) : deposit & withdrawal
(3, 'deposit',     800.00,  'PEN', 'Depósito por transferencia',                NOW() - INTERVAL 6 DAY, NULL, NULL, 'Venta'),
(3, 'withdrawal',  150.00,  'PEN', 'Retiro en ventanilla',                      NOW() - INTERVAL 4 DAY, NULL, NULL, NULL),
-- María López (term id = 4) : renewal recently
(4, 'renewal',    5000.00,  'PEN', 'Renovación de plazo fijo',                  NOW() - INTERVAL 2 DAY, NULL, NULL, NULL),
-- Carlos García (savings id = 5, USD): deposit and transfer to his term
(5, 'deposit',    300.00,   'USD', 'Depósito móvil',                            NOW() - INTERVAL 5 DAY, NULL, NULL, 'Ahorros personales'),
(5, 'transfer',   200.00,   'USD', 'Transferencia a plazo',                     NOW() - INTERVAL 3 DAY, 6, NULL, NULL),
-- Carlos García (term id = 6, USD): renewal
(6, 'renewal',   3000.00,   'USD', 'Renovación plazo fijo',                     NOW() - INTERVAL 1 DAY, NULL, NULL, NULL),
-- Servicios Globales (current id = 7, PEN): large deposit, withdrawal and transfer to Constructora
(7, 'deposit',  10000.00,   'PEN', 'Ingreso por cliente',                       NOW() - INTERVAL 6 DAY, NULL, NULL, 'Cobro factura'),
(7, 'withdrawal', 1200.00,  'PEN', 'Pago proveedores',                          NOW() - INTERVAL 4 DAY, NULL, NULL, 'Pago proveedores'),
(7, 'transfer', 5000.00,    'PEN', 'Transferencia a Constructora',              NOW() - INTERVAL 2 DAY, 9, NULL, NULL),
-- Servicios Globales (term id = 8, PEN): cancellation (partial example)
(8, 'cancellation', 40000.00, 'PEN', 'Cancelación anticipada',                  NOW() - INTERVAL 0 DAY, NULL, NULL, NULL),
-- Constructora del Norte (current id = 9, USD): deposit from Servicios Globales
(9, 'deposit', 5000.00,      'USD', 'Transferencia recibida desde Servicios',    NOW() - INTERVAL 2 DAY, 7, NULL, NULL),
(9, 'withdrawal', 2000.00,   'USD', 'Pago equipo',                               NOW() - INTERVAL 1 DAY, NULL, NULL, 'Compra maquinaria'),
-- Constructora del Norte (term id = 10, USD): renewal
(10, 'renewal', 100000.00,   'USD', 'Renovación de plazo',                      NOW() - INTERVAL 3 DAY, NULL, NULL, NULL),
-- Giancarlo (savings id = 11, PEN): deposit & transfer to his USD term (cross-currency kept as illustrative)
(11, 'deposit',  250.00,     'PEN', 'Depósito por ventanilla',                   NOW() - INTERVAL 5 DAY, NULL, NULL, 'Ingresos varios'),
(11, 'transfer', 300.00,     'PEN', 'Transferencia a plazo (conversión posterior)', NOW() - INTERVAL 1 DAY, 12, NULL, NULL),
-- Giancarlo (term id = 12, USD): deposit (initial placement) and renewal
(12, 'deposit',  5000.00,    'USD', 'Aporte inicial a plazo',                   NOW() - INTERVAL 6 DAY, NULL, NULL, 'Ahorros'),
(12, 'renewal',  5000.00,    'USD', 'Renovación de plazo',                      NOW() - INTERVAL 0 DAY, NULL, NULL, NULL);
