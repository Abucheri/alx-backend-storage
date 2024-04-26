-- Task 13: Create a stored procedure to compute the average weighted
-- score for all students
DELIMITER $$

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE weighted_average FLOAT DEFAULT 0;

    -- Declare cursor for selecting user IDs
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open cursor
    OPEN cur;

    -- Loop through each user
    users_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE users_loop;
        END IF;

        -- Calculate the total weighted score for the current user
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

        -- Update the average_score for the current user
        UPDATE users
        SET average_score = weighted_average
        WHERE id = user_id;
    END LOOP;

    -- Close cursor
    CLOSE cur;
END $$

DELIMITER ;
