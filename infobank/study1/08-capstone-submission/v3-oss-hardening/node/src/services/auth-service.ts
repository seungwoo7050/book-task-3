import type { Session, StoredUser, User } from "@study1-v3/shared";
import argon2 from "argon2";
import { createHash, randomBytes, randomUUID } from "node:crypto";
import { config } from "../config.js";

export const SESSION_COOKIE_NAME = "study1_v3_session";
const SESSION_TTL_MS = 1000 * 60 * 60 * 24 * 7;

export function toPublicUser(user: StoredUser): User {
  const { passwordHash: _passwordHash, ...rest } = user;
  return rest;
}

export async function hashPassword(password: string) {
  return argon2.hash(password);
}

export async function verifyPassword(passwordHash: string, password: string) {
  return argon2.verify(passwordHash, password);
}

export function hashSessionToken(token: string) {
  return createHash("sha256")
    .update(`${token}:${config.sessionSecret}`)
    .digest("hex");
}

export function issueSession(userId: string) {
  const token = randomBytes(32).toString("hex");
  const now = Date.now();
  const session: Session = {
    id: randomUUID(),
    userId,
    createdAt: new Date(now).toISOString(),
    lastSeenAt: new Date(now).toISOString(),
    expiresAt: new Date(now + SESSION_TTL_MS).toISOString()
  };

  return {
    token,
    tokenHash: hashSessionToken(token),
    session
  };
}

export function refreshSession(session: Session): Session {
  const now = Date.now();
  return {
    ...session,
    lastSeenAt: new Date(now).toISOString(),
    expiresAt: new Date(now + SESSION_TTL_MS).toISOString()
  };
}

export function buildStoredUser(user: Omit<StoredUser, "passwordHash">, passwordHash: string): StoredUser {
  return {
    ...user,
    passwordHash
  };
}
