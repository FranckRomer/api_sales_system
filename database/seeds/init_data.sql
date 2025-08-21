-- Script de inicialización de datos básicos
-- Ejecutar después de crear las tablas

USE sales_system;

-- Insertar tipos de cliente
INSERT INTO customer_type (name) VALUES 
('VIP'),
('Regular');

-- Insertar términos de crédito
INSERT INTO credit_terms (days) VALUES 
(30),
(60),
(90),
(120),
(180),
(365);

-- Insertar tipos de producto
INSERT INTO product_type (name) VALUES 
('Electronics'),
('Clothing'),
('Books'),
('Home & Garden'),
('Sports'),
('Automotive');

-- Insertar métodos de pago
INSERT INTO payment_method (name) VALUES 
('Cash'),
('Credit Card'),
('Debit Card'),
('Store Credit'),
('Bank Transfer'),
('Digital Wallet');

-- Insertar descuentos por tipo de producto
INSERT INTO product_type_discount (product_type_id, discount_percent) VALUES 
(1, 5.00),  -- Electronics: 5%
(2, 10.00), -- Clothing: 10%
(3, 15.00), -- Books: 15%
(4, 8.00),  -- Home & Garden: 8%
(5, 12.00), -- Sports: 12%
(6, 7.00);  -- Automotive: 7%

-- Insertar descuentos por método de pago
INSERT INTO payment_method_discount (payment_method_id, discount_percent) VALUES 
(1, 5.00),  -- Cash: 5%
(2, 2.00),  -- Credit Card: 2%
(3, 3.00),  -- Debit Card: 3%
(4, 1.90),  -- Store Credit: 1.9%
(5, 0.00),  -- Bank Transfer: 0%
(6, 4.00);  -- Digital Wallet: 4%

-- Insertar clientes de ejemplo
INSERT INTO customer (name, customer_type_id, credit_terms_id) VALUES 
('Ana García', 1, 3),      -- VIP con 90 días
('Luis Rodríguez', 2, 1),  -- Regular con 30 días
('María López', 1, 4),     -- VIP con 120 días
('Carlos Pérez', 2, 2);    -- Regular con 60 días

-- Insertar productos de ejemplo
INSERT INTO product (name, product_type_id, list_price) VALUES 
('Laptop Gaming', 1, 15000.00),
('Smartphone', 1, 8000.00),
('Camiseta Casual', 2, 500.00),
('Libro de Programación', 3, 800.00),
('Mesa de Oficina', 4, 2500.00),
('Balón de Fútbol', 5, 300.00);
