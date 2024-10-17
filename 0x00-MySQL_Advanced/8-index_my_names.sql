-- Add a generated column for the first letter of the name

-- Create the index on the generated column
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
