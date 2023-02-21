from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "email" VARCHAR(64) NOT NULL UNIQUE,
    "name" VARCHAR(128) NOT NULL UNIQUE,
    "password_hash" VARCHAR(60)
);
COMMENT ON TABLE "users" IS 'Users model';
CREATE TABLE IF NOT EXISTS "authtokens" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "token" VARCHAR(64) NOT NULL UNIQUE,
    "renew_token" VARCHAR(64) NOT NULL UNIQUE,
    "expiration" TIMESTAMPTZ NOT NULL,
    "renew_expiration" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "authtokens" IS 'Model for storing users token';;
CREATE TABLE IF NOT EXISTS "oauthclient" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "service" VARCHAR(64) NOT NULL,
    "client_id" VARCHAR(128) NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "oauthclient" IS 'User''s OAuth  authentications';;;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "authtokens";
        DROP TABLE IF EXISTS "oauthclient";
        DROP TABLE IF EXISTS "users";"""
