CREATE TABLE users(
    chat_id BIGINT PRIMARY KEY,
    lang CHAR(5) DEFAULT 'eng',
    gender CHAR(6) CHECK(gender='Male' or gender='Female'),
    partner_gender CHAR(6) DEFAULT 'None' CHECK(gender='Male' or gender='Female' or gender='None'),
    nickname VARCHAR(25) DEFAULT 'unknown',
    location CHAR(25) DEFAULT 'Addis Ababa',
    partner_location CHAR(25) DEFAULT 'None',
    horoscope CHAR(15) DEFAULT 'unknown',
    partner_horoscope CHAR(15) DEFAULT 'None',
    interest VARCHAR(25) DEFAULT 'Anything',
    conversations INT DEFAULT 0,
    rate FLOAT DEFAULT 0,
    invites INT DEFAULT 0,
    searching_partner BOOL DEFAULT FALSE,
    partner_id BIGINT DEFAULT -1,
    status CHAR(10) DEFAULT 'active' CHECK(status='active' or status='banned'),
    membership SMALLINT DEFAULT 0,
    start_time TIMESTAMP,
    nickname_time TIMESTAMP,
    expire_date TIMESTAMP,
    last_active TIMESTAMP DEFAULT NOW(),
    registered_at TIMESTAMP DEFAULT NOW());

CREATE TABLE admins(
    chat_id BIGINT PRIMARY KEY REFERENCES users,
    is_super BOOL DEFAULT FALSE);
