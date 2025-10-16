CREATE PROCEDURE GetCustomerOrderSummary(
   IN customer_id INT,
   IN start_date DATE,
   IN end_date DATE
)
BEGIN
   DECLARE total_orders INT DEFAULT 0;
   DECLARE total_amount DECIMAL(10,2) DEFAULT 0.00;

   -- Get customer information
SELECT
   c.customer_name,
   c.email,
   c.phone,
   c.address
FROM customers c
WHERE c.customer_id = customer_id;

-- Get order summary
SELECT
   COUNT(o.order_id) INTO total_orders,
   COALESCE(SUM(o.total_amount), 0) INTO total_amount
FROM orders o
WHERE o.customer_id = customer_id
 AND o.order_date BETWEEN start_date AND end_date;

-- Get detailed order items
SELECT
   o.order_id,
   o.order_date,
   oi.product_id,
   p.product_name,
   p.category,
   oi.quantity,
   oi.unit_price,
   (oi.quantity * oi.unit_price) as line_total,
   inv.stock_quantity,
   s.supplier_name,
   s.contact_email
FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        JOIN inventory inv ON p.product_id = inv.product_id
        JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE o.customer_id = customer_id
 AND o.order_date BETWEEN start_date AND end_date
ORDER BY o.order_date DESC, o.order_id;

-- Get payment information
SELECT
   pay.payment_id,
   pay.order_id,
   pay.payment_method,
   pay.payment_status,
   pay.payment_date,
   pay.amount
FROM payments pay
        JOIN orders o ON pay.order_id = o.order_id
WHERE o.customer_id = customer_id
 AND o.order_date BETWEEN start_date AND end_date;

-- Update customer last_access_date
UPDATE customers
SET last_access_date = NOW()
WHERE customer_id = customer_id;

-- Log the access in audit table
INSERT INTO audit_logs (table_name, operation, record_id, timestamp, user_id)
VALUES ('customers', 'SELECT', customer_id, NOW(), USER());

-- Return summary
SELECT total_orders, total_amount;

END