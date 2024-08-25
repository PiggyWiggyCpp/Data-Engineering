CREATE TABLE Customers_Log (
    log_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    column_name VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50)
);

CREATE OR REPLACE FUNCTION log_sensitive_data_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.first_name IS DISTINCT FROM NEW.first_name THEN
        INSERT INTO Customers_Log(customer_id, column_name, old_value, new_value, changed_by)
        VALUES(OLD.customer_id, 'first_name', OLD.first_name, NEW.first_name, SESSION_USER);
    END IF;

    IF OLD.last_name IS DISTINCT FROM NEW.last_name THEN
        INSERT INTO Customers_Log(customer_id, column_name, old_value, new_value, changed_by)
        VALUES(OLD.customer_id, 'last_name', OLD.last_name, NEW.last_name, SESSION_USER);
    END IF;

    IF OLD.email IS DISTINCT FROM NEW.email THEN
        INSERT INTO Customers_Log(customer_id, column_name, old_value, new_value, changed_by)
        VALUES(OLD.customer_id, 'email', OLD.email, NEW.email, SESSION_USER);
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_log_sensitive_data_changes
AFTER UPDATE ON Customers
FOR EACH ROW
EXECUTE FUNCTION log_sensitive_data_changes();



INSERT INTO Customers (first_name, last_name, email, join_date)
VALUES ('Alex', 'Bone', 'alexb@google.com', '2024-08-20');

UPDATE Customers
SET first_name = 'Jon', last_name = 'Smith', email = 'jonsmith@google.com'
WHERE email = 'alexb@google.com';

SELECT * FROM Customers_Log;
