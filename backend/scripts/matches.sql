DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE IF NOT EXISTS matches (
  id SERIAL PRIMARY KEY,
  requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  matched_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  match_score DECIMAL(5, 3),
  UNIQUE (requester_id, matched_user_id)
);



-- DROP TABLE IF EXISTS match_requests CASCADE; -- hack to keep things declarative for now since I will need to update columns as requirements change and theres no data in the db
-- CREATE TABLE IF NOT EXISTS match_requests (
--   id SERIAL PRIMARY KEY,
--   student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
--   requested_subject TEXT,
--   request_status VARCHAR(255), -- holds if the request was deleted / fulfilled
--   created_at TIMESTAMP
-- );
--
-- DROP TABLE IF EXISTS matches CASCADE; -- hack to keep things declarative for now since I will need to update columns as requirements change and theres no data in the db
-- CREATE TABLE IF NOT EXISTS matches (
--   id SERIAL PRIMARY KEY,
--   tutor_one_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
--   tutor_two_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
--   tutor_one_subject TEXT,
--   tutor_two_subject TEXT,
--   match_status VARCHAR(255), -- holds if the match was canceled / ended
--   matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );