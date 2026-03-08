import "reflect-metadata";
import "dotenv/config";

import { DataSource } from "typeorm";

import { loadRuntimeConfig, type RuntimeConfig } from "../runtime/runtime-config";
import { createDatabaseOptions } from "./database-options";

export function createAppDataSource(env: NodeJS.ProcessEnv = process.env): DataSource {
  const runtimeConfig = loadRuntimeConfig(env);
  return createAppDataSourceFromConfig(runtimeConfig);
}

export function createAppDataSourceFromConfig(config: RuntimeConfig): DataSource {
  return new DataSource(createDatabaseOptions(config));
}

export const AppDataSource = createAppDataSource();
