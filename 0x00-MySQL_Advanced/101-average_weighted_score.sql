-- Create stored procedure to compute average weighted score for all users

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE userId INT;

    -- Cursor to iterate through all users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Declare CONTINUE handler to handle end of cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through each user
    read_loop: LOOP
        FETCH user_cursor INTO userId;

        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Declare variables for weighted score calculation
        DECLARE total_weighted_score FLOAT DEFAULT 0;
        DECLARE total_weight INT DEFAULT 0;

        -- Calculate the total weighted score and total weight for the user
        SELECT SUM(c.score * p.weight) INTO total_weighted_score,
               SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = userId;

        -- Calculate and update the average score for the user
        IF total_weight > 0 THEN
            UPDATE users
            SET average_score = total_weighted_score / total_weight
            WHERE id = userId;
        ELSE
            UPDATE users
            SET average_score = 0
            WHERE id = userId;
        END IF;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END //

DELIMITER ;
