CREATE TABLE users(
    chat_id BIGINT PRIMARY KEY,
    phone_number BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(25) DEFAULT 'unknown',
    username VARCHAR(25) DEFAULT 'unknown',
    balance DOUBLE PRECISION DEFAULT 0 CHECK(balance >= 0), 
    money_made DOUBLE PRECISION DEFAULT 0 CHECK(money_made >= 0),
    company VARCHAR(50) DEFAULT 'unknown',
    verified BOOL DEFAULT FALSE,
    lang CHAR(10) DEFAULT 'eng',
    coin SMALLINT DEFAULT 10 CHECK(coin >= 0),
    jobs_completed SMALLINT DEFAULT 0,
    jobs_posted INT DEFAULT 0,
    rate FLOAT DEFAULT 0, 
    level SMALLINT DEFAULT 0 CHECK(level <= 2),
    status CHAR(10) DEFAULT 'active',
    warning SMALLINT DEFAULT 0,
    opened_jobs SMALLINT DEFAULT 0,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE admins(
    chat_id BIGINT PRIMARY KEY REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    super bool DEFAULT FALSE,
    ban BOOL DEFAULT TRUE,
    approve BOOL DEFAULT TRUE,
    configure BOOL DEFAULT FALSE,
    process_deposit BOOL DEFAULT FALSE,
    process_payment BOOL DEFAULT FALSE);

CREATE TABLE jobs(
    job_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(50)  DEFAULT 'unknown',
    company VARCHAR(50) DEFAULT 'unknown',
    discription TEXT  DEFAULT 'unknown',
    cat CHAR(15)  DEFAULT 'unknown',
    type CHAR(15)  DEFAULT 'unknown',
    deposit BOOL DEFAULT FALSE,
    price DOUBLE PRECISION DEFAULT 0,
    level SMALLINT DEFAULT 0,
    coin SMALLINT DEFAULT 1, 
    freelancer BIGINT DEFAULT -1,
    escrow_id BIGINT DEFAULT -1, 
    status CHAR(10) DEFAULT 'edit' CHECK(status='edit' or status='pending' or status='opened' or status='declined' or status='closed'),
    message_id BIGINT,
    proposal_limit SMALLINT DEFAULT 1 CHECK(proposal_limit > 0),
    counter SMALLINT DEFAULT 0,
    counter_f SMALLINT DEFAULT 0, 
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE proposals(
    proposal_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    job_id INT NOT NULL REFERENCES jobs ON DELETE CASCADE ON UPDATE CASCADE,
    discription VARCHAR(250) DEFAULT 'unknown',
    price DOUBLE PRECISION DEFAULT 0,
    days SMALLINT DEFAULT 1,
    status CHAR(10) DEFAULT 'edit',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE escrow(
    escrow_id BIGSERIAL PRIMARY KEY,
    job_id INT NOT NULL UNIQUE REFERENCES jobs ON DELETE CASCADE ON UPDATE CASCADE,
    proposal_id INT NOT NULL UNIQUE REFERENCES proposals ON DELETE CASCADE ON UPDATE CASCADE,
    working bool DEFAULT FALSE,
    paid bool DEFAULT FALSE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE verify(
    verify_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    photo_id TEXT NOT NULL,
    company VARCHAR(50) DEFAULT 'unknown',
    status CHAR(10) DEFAULT 'edit',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE deposit(
    deposit_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    price DOUBLE PRECISION  NOT NULL,
    paid BOOL DEFAULT FALSE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE cashout(
    cashout_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    price DOUBLE PRECISION  NOT NULL,
    status CHAR(15) DEFAULT 'pending',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE update(
    update_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    status CHAR(15) DEFAULT 'pending',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE bot(
    bot VARCHAR(25) NOT NULL,
    channel VARCHAR(25) NOT NULL,
    s_channel VARCHAR(25) NOT NULL,
    p_channel VARCHAR(25) NOT NULL,
    s_admin VARCHAR(25)NOT NULL,
    s_group VARCHAR(25)NOT NULL,
    check_level BOOL DEFAULT FALSE,
    job_coin INT DEFAULT 0,
    proposal_coin INT DEFAULT 0,
    application_fee INT DEFAULT 0,
    minimum_deposit INT DEFAULT 1,
    maximum_deposit INT DEFAULT 2000,
    minimum_cashout INT DEFAULT 1,
    maximum_cashout INT DEFAULT 500,
    yenepay_cut INT DEFAULT 0,
    merchant_id INT DEFAULT 0,
    delete_declined BOOL DEFAULT TRUE);


INSERT INTO bot(bot, channel, s_channel, p_channel, s_admin, s_group) VALUES('freelance321bot', 'freelance321', 'freelance321_support', 'freelance321_payment', 'freelance321_admin', 'freelance321_group');