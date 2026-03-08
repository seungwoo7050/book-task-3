import { describe, it, expect, beforeEach, vi } from "vitest";
import { Test } from "@nestjs/testing";
import { getRepositoryToken } from "@nestjs/typeorm";
import { JwtService } from "@nestjs/jwt";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { ConflictException, UnauthorizedException } from "@nestjs/common";
import * as bcrypt from "bcryptjs";
import { AuthService } from "../../src/auth/auth.service";
import { User, Role } from "../../src/auth/entities/user.entity";
import { UserRegisteredEvent } from "../../src/events/events";

describe("AuthService", () => {
  let service: AuthService;
  let mockEmitter: { emit: ReturnType<typeof vi.fn> };
  let mockJwtService: { sign: ReturnType<typeof vi.fn> };
  let mockUserRepo: Record<string, ReturnType<typeof vi.fn>>;

  const mockUser: User = {
    id: "user-id",
    username: "admin",
    password: "",
    role: Role.ADMIN,
    createdAt: new Date(),
  };

  beforeEach(async () => {
    mockUser.password = await bcrypt.hash("password123", 10);

    mockEmitter = { emit: vi.fn() };
    mockJwtService = { sign: vi.fn().mockReturnValue("jwt-token") };
    mockUserRepo = {
      findOneBy: vi.fn().mockResolvedValue(null),
      create: vi.fn().mockReturnValue(mockUser),
      save: vi.fn().mockResolvedValue(mockUser),
    };

    const module = await Test.createTestingModule({
      providers: [
        AuthService,
        { provide: getRepositoryToken(User), useValue: mockUserRepo },
        { provide: JwtService, useValue: mockJwtService },
        { provide: EventEmitter2, useValue: mockEmitter },
      ],
    }).compile();

    service = module.get(AuthService);
  });

  it("should register a new user and emit event", async () => {
    const result = await service.register({ username: "newuser", password: "password123" });

    expect(result.username).toBe("admin");
    expect(mockEmitter.emit).toHaveBeenCalledWith("user.registered", expect.any(UserRegisteredEvent));
  });

  it("should throw ConflictException if user exists", async () => {
    mockUserRepo.findOneBy.mockResolvedValue(mockUser);

    await expect(
      service.register({ username: "admin", password: "password123" }),
    ).rejects.toThrow(ConflictException);
  });

  it("should login with valid credentials", async () => {
    mockUserRepo.findOneBy.mockResolvedValue(mockUser);

    const result = await service.login("admin", "password123");

    expect(result.token).toBe("jwt-token");
    expect(result.user.username).toBe("admin");
  });

  it("should throw UnauthorizedException for wrong password", async () => {
    mockUserRepo.findOneBy.mockResolvedValue(mockUser);

    await expect(service.login("admin", "wrongpassword")).rejects.toThrow(
      UnauthorizedException,
    );
  });

  it("should throw UnauthorizedException for missing user", async () => {
    await expect(service.login("nobody", "password")).rejects.toThrow(
      UnauthorizedException,
    );
  });
});
