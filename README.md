# VegasRushBot

A professional Telegram gambling bot using emoji games, OxaPay for crypto payments, and Supabase for user/balance management.

## Features
- Telegram emoji games betting (Dice, Bowling, Darts, Football, Basketball, Slots)
- OxaPay crypto deposits/withdrawals (manual admin confirmation)
- Supabase (PostgreSQL) for balances, bets, transactions, referrals
- Referral system with 10% commission on referred losses
- Secure, modular, production-ready codebase

## Project Structure
```
bot/
  handlers/    # Telegram command handlers
  db/          # Supabase database functions
  payments/    # OxaPay integration
main.py        # Entry point
.env.example   # Environment variable template
```

## Setup
1. `cp .env.example .env` and fill in your secrets
2. Install dependencies: `pip install -r requirements.txt`
3. Create Supabase tables (see below)
4. Run the bot: `python main.py`

## Supabase SQL Schema
```
-- USERS TABLE
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	telegram_id BIGINT UNIQUE NOT NULL,
	username TEXT,
	balance NUMERIC(18, 8) DEFAULT 0 CHECK (balance >= 0),
	referrer_id INT REFERENCES users(id) ON DELETE SET NULL,
	created_at TIMESTAMP DEFAULT NOW()
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
	id SERIAL PRIMARY KEY,
	user_id INT REFERENCES users(id) ON DELETE CASCADE,
	type VARCHAR(20) CHECK (type IN ('deposit', 'withdraw')),
	amount NUMERIC(18, 8) NOT NULL CHECK (amount > 0),
	status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','confirmed','rejected')),
	oxapay_tx_id TEXT,
	wallet_address TEXT,
	created_at TIMESTAMP DEFAULT NOW()
);

-- BETS TABLE
CREATE TABLE bets (
	id SERIAL PRIMARY KEY,
	user_id INT REFERENCES users(id) ON DELETE CASCADE,
	game_type VARCHAR(20) NOT NULL,        -- dice, bowl, darts, etc
	bet_amount NUMERIC(18, 8) NOT NULL CHECK (bet_amount > 0),
	result TEXT,
	payout NUMERIC(18, 8),
	created_at TIMESTAMP DEFAULT NOW()
);

-- REFERRALS TABLE
CREATE TABLE referrals (
	id SERIAL PRIMARY KEY,
	referrer_id INT REFERENCES users(id) ON DELETE CASCADE,
	referred_id INT REFERENCES users(id) ON DELETE CASCADE,
	earnings NUMERIC(18, 8) DEFAULT 0
);
```

---

## License
MIT
# sturdy-doodle