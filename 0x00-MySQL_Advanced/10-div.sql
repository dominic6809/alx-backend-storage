-- This function SafeDiv divides two integers and returns the result.
-- If the second integer is zero, it returns 0 to avoid division by zero errors.

DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT) 
RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF;
END //

DELIMITER ;
