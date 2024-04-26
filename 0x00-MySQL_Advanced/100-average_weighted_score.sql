-- Task 12: Create a stored procedure to compute the average
-- weighted score for a student
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_average FLOAT DEFAULT 0;

    -- Calculate the total weighted score
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Compute the weighted average
    IF total_weight > 0 THEN
        SET weighted_average = total_score / total_weight;
    ELSE
        SET weighted_average = 0;
    END IF;

    -- Update the average_score for the user
    UPDATE users
    SET average_score = weighted_average
    WHERE id = user_id;
END $$

DELIMITER ;
