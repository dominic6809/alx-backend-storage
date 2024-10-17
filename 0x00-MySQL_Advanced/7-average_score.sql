-- Script to create the stored procedure ComputeAverageScoreForUser

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (
    IN user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Calculate the average score for the user
    SELECT AVG(score) INTO avg_score 
    FROM corrections 
    WHERE user_id = user_id;

    -- Update the user's average score
    UPDATE users 
    SET average_score = COALESCE(avg_score, 0) 
    WHERE id = user_id;
END; //

DELIMITER ;
