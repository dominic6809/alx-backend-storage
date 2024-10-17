-- Script to list bands with Glam rock as their main style, ranked by longevity

SELECT band_name, 
       (IFNULL(split, 2022) - formed) AS lifespan -- Calculate lifespan using split or default to 2022
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, '')) > 0 -- Use FIND_IN_SET for style checking
ORDER BY lifespan DESC;
