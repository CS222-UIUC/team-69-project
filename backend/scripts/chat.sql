DROP TABLE IF EXISTS chat_messages CASCADE; -- hack to keep things declarative for now since I will need to update columns as requirements change and theres no data in the db
CREATE TABLE IF NOT EXISTS chat_messages (
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
  sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  message_text TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

