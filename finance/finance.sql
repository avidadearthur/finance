-- Query used to create the table
CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'cash' NUMERIC NOT NULL DEFAULT 10000.00 );
-- Query used to create a table that tracks users transactions
CREATE TABLE 'transactions' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INT, 'amount' INT, 'price' NUMERIC NOT NULL, 'symbol' TEXT NOT NULL, 'timestamp' NUMERIC DEFAULT CURRENT_TIMESTAMP  ,FOREIGN KEY('user_id') REFERENCES users('id'));
-- Query used to create a table that tracks user's owned stocks
CREATE TABLE 'portfolios' ('last_trans_id' INT,'user_id' INT, 'symbol' TEXT NOT NULL, 'shares' INT, FOREIGN KEY('user_id') REFERENCES users('id'), FOREIGN KEY('last_trans_id') REFERENCES transactions('id'));