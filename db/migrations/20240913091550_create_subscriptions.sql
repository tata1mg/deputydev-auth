-- 005_create_subscriptions.sql

-- migrate:up
CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    plan_id BIGINT NOT NULL,
    user_team_id BIGINT NOT NULL UNIQUE,
    current_status VARCHAR NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES subscription_plans(id) ,
    FOREIGN KEY (user_team_id) REFERENCES user_teams(id)
);

-- migrate:down
DROP TABLE IF EXISTS subscriptions;
