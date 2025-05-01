USE rentoo;

-- Add property_name column
ALTER TABLE property ADD COLUMN property_name VARCHAR(255) NOT NULL;

-- Add unique constraint on owner_id and property_name
ALTER TABLE property ADD CONSTRAINT unique_owner_property_name UNIQUE (owner_id, property_name); 