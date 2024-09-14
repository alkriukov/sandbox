CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nick VARCHAR(30) NOT NULL UNIQUE,
    passwd VARCHAR(255) NOT NULL,
    u_status ENUM('active', 'suspended', 'blocked', 'deleted') NOT NULL DEFAULT 'active',
    registered DATETIME NOT NULL,
    settings VARCHAR(255) NOT NULL);
CREATE OR REPLACE VIEW nicks AS SELECT id,nick,u_status,settings FROM users;

CREATE TABLE devices (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL UNIQUE,
    registered DATETIME NOT NULL,
    generic_info VARCHAR(255) NOT NULL,
    user_id BIGINT NOT NULL,
    CONSTRAINT fk_devices_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);
CREATE OR REPLACE VIEW device_infos AS SELECT id,generic_info,user_id FROM devices;

CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL,
    settings VARCHAR(255) NOT NULL,
    p_status ENUM('active', 'deleted') NOT NULL DEFAULT 'active');

CREATE TABLE user_projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_role ENUM('member', 'admin') NOT NULL,
    user_id BIGINT NOT NULL,
    project_id BIGINT NOT NULL,
    UNIQUE(user_id,project_id),
    CONSTRAINT fk_user_projects_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_projects_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE);
CREATE OR REPLACE VIEW user_project_view AS SELECT projects.id, projects.title, projects.settings, projects.p_status, user_projects.user_role, user_projects.user_id FROM projects, user_projects WHERE projects.id = user_projects.project_id;

CREATE TABLE labels (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL,
    project_id BIGINT NOT NULL,
    UNIQUE(title,project_id),
    CONSTRAINT fk_label_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE);

CREATE TABLE portfolios (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    pf_title VARCHAR(30) NOT NULL,
    pf_properties VARCHAR(255) NOT NULL,
    project_id BIGINT NOT NULL,
    UNIQUE(pf_title,project_id),
    CONSTRAINT fk_pf_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE);

CREATE TABLE wallets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(30) NOT NULL,
    properties VARCHAR(255) NOT NULL,
    value INTEGER NOT NULL,
    goal_value INTEGER,
    start_date DATETIME,
    goal_date DATETIME,
    portfolio_id BIGINT NOT NULL,
    UNIQUE(title,project_id),
    CONSTRAINT fk_wallets_portfolio FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE);
CREATE OR REPLACE VIEW wallets_view AS SELECT wallets.id, wallets.title, wallets.properties, wallets.value, wallets.goal_value, wallets.start_date, wallets.goal_date, wallets.portfolio_id, portfolios.project_id, portfolios.pf_title FROM wallets, portfolios WHERE wallets.portfolio_id = portfolios.id;


CREATE TABLE transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    date DATETIME NOT NULL,
    value INTEGER NOT NULL,
    comment VARCHAR(255),
    from_wallet_id BIGINT,
    to_wallet_id BIGINT,
    CONSTRAINT fk_transactions_from_wallet FOREIGN KEY (from_wallet_id) REFERENCES wallets(id) ON DELETE CASCADE,
    CONSTRAINT fk_transactions_to_wallet FOREIGN KEY (to_wallet_id) REFERENCES wallets(id) ON DELETE CASCADE);

CREATE TABLE transaction_labels (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    transaction_id BIGINT,
    label_id BIGINT,
    UNIQUE(transaction_id,label_id),
    CONSTRAINT fk_transaction_labels_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    CONSTRAINT fk_transaction_labels_label FOREIGN KEY (label_id) REFERENCES labels(id));
CREATE OR REPLACE VIEW transaction_label_view AS SELECT transaction_labels.id, transaction_labels.transaction_id, labels.title, labels.project_id FROM transaction_labels, labels WHERE transaction_labels.label_id = labels.id;

CREATE TABLE schedules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    comment VARCHAR(255) NOT NULL,
    next_date DATETIME NOT NULL,
    tz_offset_min INTEGER NOT NULL,
    repeat_rule VARCHAR(255) NOT NULL,
    value INTEGER NOT NULL,
    value_is_percent BOOLEAN NOT NULL,
    from_wallet_id BIGINT,
    to_wallet_id BIGINT,
    CONSTRAINT fk_schedules_from_wallet FOREIGN KEY (from_wallet_id) REFERENCES wallets(id) ON DELETE CASCADE,
    CONSTRAINT fk_schedules_to_wallet FOREIGN KEY (to_wallet_id) REFERENCES wallets(id) ON DELETE CASCADE);

CREATE TABLE schedule_labels (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    schedule_id BIGINT,
    label_id BIGINT,
    UNIQUE(schedule_id,label_id),
    CONSTRAINT fk_schedule_labels_schedule FOREIGN KEY (schedule_id) REFERENCES schedules(id),
    CONSTRAINT fk_schedule_labels_label FOREIGN KEY (label_id) REFERENCES labels(id));
CREATE OR REPLACE VIEW schedule_label_view AS SELECT schedule_labels.id, schedule_labels.schedule_id, labels.title, labels.project_id FROM schedule_labels, labels WHERE schedule_labels.label_id = labels.id;


