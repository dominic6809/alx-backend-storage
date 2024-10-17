-- Script to create a trigger that resets valid_email when email changes
-- DELIMITER //: Changes the statement delimiter to allow for multi-line statements
-- BEFORE UPDATE ON users: This trigger fires before an update occurs on the users table.
-- FOR EACH ROW: The trigger will execute for each row that is updated.
-- IF OLD.email <> NEW.email THEN: Checks if the old email is different from the new email.
-- SET NEW.valid_email = 0;: Resets the valid_email field to 0 if the email has changed.

DELIMITER //

CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END; //

DELIMITER ;
