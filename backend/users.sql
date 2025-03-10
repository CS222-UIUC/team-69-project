CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  display_name TEXT NOT NULL, -- set as a default when signing up with gmail account, then allow the user to change it
  email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS oauth_users (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- if user gets deleted, delete their session
  provider VARCHAR(50) NOT NULL, -- ex: google, 
  access_token TEXT,
  refresh_token TEXT,
  expires_at TIMESTAMP
);