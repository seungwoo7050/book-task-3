import { Injectable, Inject, ConflictException, HttpException, HttpStatus, UnauthorizedException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { JwtService } from "@nestjs/jwt";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { Repository } from "typeorm";
import { randomUUID } from "crypto";
import * as bcrypt from "bcryptjs";
import { User, Role } from "./entities/user.entity";
import { RegisterDto } from "./dto/register.dto";
import { UserRegisteredEvent } from "../events/events";
import { AuthRateLimitService } from "./auth-rate-limit.service";

export type AuthenticatedUser = {
  id: string;
  username: string;
  role: Role;
};

export type LoginResult = {
  token: string;
  user: AuthenticatedUser;
};

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    @Inject(JwtService)
    private readonly jwtService: JwtService,
    @Inject(EventEmitter2)
    private readonly eventEmitter: EventEmitter2,
    @Inject(AuthRateLimitService)
    private readonly authRateLimitService: AuthRateLimitService,
  ) {}

  async register(dto: RegisterDto): Promise<AuthenticatedUser> {
    const existing = await this.userRepository.findOneBy({ username: dto.username });
    if (existing) {
      throw new ConflictException("Username already exists");
    }

    const hashed = await bcrypt.hash(dto.password, 10);
    const user = this.userRepository.create({
      id: randomUUID(),
      username: dto.username,
      password: hashed,
      role: dto.role || Role.USER,
    });
    const saved = await this.userRepository.save(user);

    this.eventEmitter.emit(
      "user.registered",
      new UserRegisteredEvent(saved.id, saved.username, saved.role),
    );

    return { id: saved.id, username: saved.username, role: saved.role };
  }

  async login(username: string, password: string, clientId: string): Promise<LoginResult> {
    await this.authRateLimitService.ensureLoginAllowed(clientId);

    const user = await this.userRepository.findOneBy({ username });
    if (!user) {
      const attempts = await this.authRateLimitService.recordFailedAttempt(clientId);
      if (this.authRateLimitService.isBlockedAttemptCount(attempts)) {
        throw new HttpException("Too many login attempts", HttpStatus.TOO_MANY_REQUESTS);
      }
      throw new UnauthorizedException("Invalid credentials");
    }

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      const attempts = await this.authRateLimitService.recordFailedAttempt(clientId);
      if (this.authRateLimitService.isBlockedAttemptCount(attempts)) {
        throw new HttpException("Too many login attempts", HttpStatus.TOO_MANY_REQUESTS);
      }
      throw new UnauthorizedException("Invalid credentials");
    }

    await this.authRateLimitService.clearAttempts(clientId);

    const payload = { sub: user.id, username: user.username, role: user.role };
    const token = this.jwtService.sign(payload);

    return {
      token,
      user: { id: user.id, username: user.username, role: user.role },
    };
  }
}
