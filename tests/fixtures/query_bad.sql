-- Fixture: SQL with detectable anti-patterns

SELECT * FROM orders;

SELECT o.id FROM orders o
WHERE o.total = (SELECT MAX(total) FROM orders);

SELECT * FROM users WHERE LOWER(email) = 'x';

INSERT INTO logs VALUES (1, 'x');

SELECT id, name, created_at FROM users
WHERE created_at >= '2026-01-01'
ORDER BY id
LIMIT 50;
