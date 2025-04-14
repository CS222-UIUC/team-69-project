
DROP TABLE IF EXISTS users CASCADE; -- hack to keep things declarative for now since I will need to update columns as requirements change and theres no data in the db
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  display_name TEXT NOT NULL, -- set as a default when signing up with gmail account, then allow the user to change it
  email VARCHAR(255) UNIQUE NOT NULL,
  major VARCHAR(255),
  rating DECIMAL(3, 2) DEFAULT 0.00,
  total_ratings INT DEFAULT 0, -- counter for number of times rated
  rating_history INT[] DEFAULT '{}', -- last 50 ratings

  show_as_backup BOOLEAN DEFAULT TRUE,
  classes_can_tutor TEXT[] DEFAULT '{}',
  classes_needed TEXT[] DEFAULT '{}',
  recent_interactions TIMESTAMP[], -- last 10 interaction timestamps
  class_ratings JSONB DEFAULT '{}',

  password_hash VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS oauth_users (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- if user gets deleted, delete their session
  provider VARCHAR(50) NOT NULL, -- ex: google, 
  access_token TEXT,
  refresh_token TEXT,
  expires_at TIMESTAMP
);
