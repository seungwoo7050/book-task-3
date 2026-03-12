import { type MigrationInterface, type QueryRunner } from "typeorm";

export class InitialSchema1710000000000 implements MigrationInterface {
  name = "InitialSchema1710000000000";

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query('CREATE EXTENSION IF NOT EXISTS "pgcrypto"');
    await queryRunner.query(`
      CREATE TABLE "users" (
        "id" uuid NOT NULL DEFAULT gen_random_uuid(),
        "username" character varying(30) NOT NULL,
        "password" character varying(100) NOT NULL,
        "role" character varying(10) NOT NULL DEFAULT 'USER',
        "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT "PK_users_id" PRIMARY KEY ("id"),
        CONSTRAINT "UQ_users_username" UNIQUE ("username")
      )
    `);
    await queryRunner.query(`
      CREATE TABLE "books" (
        "id" uuid NOT NULL DEFAULT gen_random_uuid(),
        "title" character varying(200) NOT NULL,
        "author" character varying(100) NOT NULL,
        "publishedYear" integer NOT NULL,
        "genre" character varying(50) NOT NULL,
        "price" double precision NOT NULL,
        "createdAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
        "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT "PK_books_id" PRIMARY KEY ("id")
      )
    `);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query('DROP TABLE IF EXISTS "books"');
    await queryRunner.query('DROP TABLE IF EXISTS "users"');
  }
}
