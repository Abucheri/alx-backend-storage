-- Task 7: Create stored procedure ComputeAverageScoreForUser to compute and store
-- the average score for a student
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser$$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE avg_score DECIMAL(10, 2);

    -- Calculate average score for the user
    SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = p_user_id;

    -- Update the average score for the user
    UPDATE users SET average_score = avg_score WHERE id = p_user_id;
END$$

DELIMITER ;
