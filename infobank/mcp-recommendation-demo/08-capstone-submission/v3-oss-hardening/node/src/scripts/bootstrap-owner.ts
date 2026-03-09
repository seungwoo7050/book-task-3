import { randomUUID } from "node:crypto";
import { config } from "../config.js";
import { pool } from "../db/client.js";
import { getInstanceSettings, getStoredUserByEmail, saveInstanceSettings, saveStoredUser } from "../repositories/catalog-repository.js";
import { buildStoredUser, hashPassword } from "../services/auth-service.js";
import { buildDefaultInstanceSettings } from "../services/instance-service.js";

async function main() {
  const existing = await getStoredUserByEmail(config.bootstrapOwnerEmail);
  const now = new Date().toISOString();
  const passwordHash = await hashPassword(config.bootstrapOwnerPassword);

  const user = buildStoredUser(
    {
      id: existing?.id ?? randomUUID(),
      email: config.bootstrapOwnerEmail,
      name: existing?.name ?? "Bootstrap Owner",
      role: "owner",
      isActive: true,
      createdAt: existing?.createdAt ?? now,
      updatedAt: now
    },
    passwordHash
  );

  await saveStoredUser(user);

  const settings = (await getInstanceSettings()) ?? buildDefaultInstanceSettings(user.email);
  if (!settings.updatedBy) {
    await saveInstanceSettings({
      ...settings,
      updatedBy: user.email,
      updatedAt: now
    });
  }

  console.log(
    JSON.stringify(
      {
        ownerEmail: user.email,
        ownerId: user.id,
        role: user.role,
        updatedAt: user.updatedAt
      },
      null,
      2
    )
  );
}

await main()
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await pool.end();
  });
