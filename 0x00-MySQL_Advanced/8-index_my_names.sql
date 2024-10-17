-- Add a generated column for the first letter of the name
ALTER TABLE names 
ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (LEFT(name, 1)) STORED;

-- Create the index on the generated column
CREATE INDEX idx_name_first ON names (first_letter);
