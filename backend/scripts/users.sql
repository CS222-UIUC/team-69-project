DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  display_name TEXT NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  major VARCHAR(255),
  year TEXT, -- Added year field here
  rating DECIMAL(3, 2) DEFAULT 0.00,
  total_ratings INT DEFAULT 0,
  rating_history INT[] DEFAULT '{}',
  show_as_backup BOOLEAN DEFAULT TRUE,
  classes_can_tutor TEXT[] DEFAULT '{}',
  classes_needed TEXT[] DEFAULT '{}',
  recent_interactions TIMESTAMP[],
  class_ratings JSONB DEFAULT '{}',
  password_hash VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS oauth_users (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider VARCHAR(50) NOT NULL,
  access_token TEXT,
  refresh_token TEXT,
  expires_at TIMESTAMP
);

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- GIN index on display_name
CREATE INDEX idx_users_display_name_trgm
ON users
USING GIN (display_name gin_trgm_ops);