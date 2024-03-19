from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "metadata" (
            "id" BIGSERIAL NOT NULL PRIMARY KEY,
            "path" VARCHAR(255) NOT NULL,
            "file_type" VARCHAR(255) NOT NULL,
            "arch" VARCHAR(3) NOT NULL,
            "numer_of_imports" INT NOT NULL,
            "number_of_exports" INT NOT NULL,
            "hash" BIGINT NOT NULL UNIQUE
        );
        CREATE INDEX IF NOT EXISTS "idx_metadata_hash_401c4b" ON "metadata" ("hash");
        COMMENT ON COLUMN "metadata"."arch" IS 'x32: x32\nx64: x64';
        COMMENT ON TABLE "metadata" IS 'File metadata model.';
                CREATE TABLE IF NOT EXISTS "tasks" (
            "id" UUID NOT NULL  PRIMARY KEY,
            "status" SMALLINT NOT NULL  DEFAULT 1
        );
        COMMENT ON COLUMN "tasks"."status" IS 'PENDING: 1\nIN_PROGRESS: 2\nDONE: 3\nFAILED: 4';
        COMMENT ON TABLE "tasks" IS 'Task model.';
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "metadata";
        DROP TABLE IF EXISTS "tasks";
    """
