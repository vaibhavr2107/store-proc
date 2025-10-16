CREATE PROCEDURE dbo.OrderFulfillmentProc
AS
BEGIN
    SELECT
        o.order_id,
        o.order_date,
        c.customer_id,
        c.customer_name,
        pmn.method_name,
        pay.payment_id,
        pay.status,
        d.delivery_id,
        d.delivery_status
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN payments pay ON o.order_id = pay.order_id
    JOIN payment_methods pmn ON pay.method_id = pmn.method_id
    LEFT JOIN delivery d ON o.order_id = d.order_id
    LEFT JOIN invoices inv ON o.order_id = inv.order_id
    WHERE pay.status = 'APPROVED';
END;
