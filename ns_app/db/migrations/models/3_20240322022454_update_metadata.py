from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metadata" ALTER COLUMN "numer_of_imports" DROP NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "arch" DROP NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "number_of_exports" DROP NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "file_type" DROP NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "file_type" TYPE VARCHAR(3) USING "file_type"::VARCHAR(3);
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metadata" ALTER COLUMN "numer_of_imports" SET NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "arch" SET NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "number_of_exports" SET NOT NULL;
        ALTER TABLE "metadata" ALTER COLUMN "file_type" TYPE VARCHAR(255) USING "file_type"::VARCHAR(255);
        ALTER TABLE "metadata" ALTER COLUMN "file_type" SET NOT NULL;
    """
