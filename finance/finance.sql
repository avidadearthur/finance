-- Query used to create the table
CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'cash' NUMERIC NOT NULL DEFAULT 10000.00 );
-- Query used to create a table that track user transactions
CREATE TABLE 'transactions' ('user_id' INT, 'amount' INT, 'price' NUMERIC NOT NULL, 'symbol' TEXT NOT NULL, 'timestamp' NUMERIC DEFAULT CURRENT_TIMESTAMP  ,FOREIGN KEY('user_id') REFERENCES users('id'));