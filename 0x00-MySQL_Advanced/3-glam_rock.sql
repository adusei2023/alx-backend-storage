-- SQL script that lists all bands with Glam rock as their main style
-- ranked by thier longevity (number of years they have been active)
SELECT band_name, (IFNULL(split, YEAR(CURDATE()) - 1) - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', style) > 0
ORDER BY lifespan DESC;
