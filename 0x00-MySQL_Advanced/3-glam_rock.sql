-- Create a temporary table to store the lifespan calculation
CREATE TEMPORARY TABLE temp_bands (
    band_name VARCHAR(100),
    formed INT,
    split INT,
    lifespan INT
);

-- Populate the temporary table by calculating the lifespan for each band
INSERT INTO temp_bands (band_name, formed, split, lifespan)
SELECT band_name, formed, split, (2022 - formed) - split AS lifespan
FROM metal_bands
WHERE style = 'Glam rock';

-- Retrieve the bands ranked by longevity
SELECT band_name, lifespan
FROM temp_bands
ORDER BY lifespan DESC;
