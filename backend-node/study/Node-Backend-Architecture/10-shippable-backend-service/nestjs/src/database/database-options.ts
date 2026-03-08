import { type TypeOrmModuleOptions } from "@nestjs/typeorm";
import { type DataSourceOptions } from "typeorm";

import { User } from "../auth/entities/user.entity";
import { Book } from "../books/entities/book.entity";
import { type RuntimeConfig } from "../runtime/runtime-config";
import { InitialSchema1710000000000 } from "./migrations/1710000000000-initial-schema";

export function createDatabaseOptions(config: RuntimeConfig): DataSourceOptions {
  return {
    type: "postgres",
    url: config.databaseUrl,
    entities: [Book, User],
    migrations: [InitialSchema1710000000000],
    synchronize: false,
    logging: false,
  };
}

export function createTypeOrmModuleOptions(config: RuntimeConfig): TypeOrmModuleOptions {
  return {
    ...createDatabaseOptions(config),
    autoLoadEntities: false,
  };
}
