-- Task 2: Rank country origins of bands by number of fans
-- Import the metal_bands table dump

SELECT origin, SUM(nb_fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
