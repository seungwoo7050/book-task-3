import { Injectable, Inject, ConflictException, UnauthorizedException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { JwtService } from "@nestjs/jwt";
import { EventEmitter2 } from "@nestjs/event-emitter";
import { Repository } from "typeorm";
import { randomUUID } from "crypto";
import * as bcrypt from "bcryptjs";
import { User, Role } from "./entities/user.entity";
import { RegisterDto } from "./dto/register.dto";
import { UserRegisteredEvent } from "../events/events";

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    @Inject(JwtService)
    private readonly jwtService: JwtService,
    @Inject(EventEmitter2)
    private readonly eventEmitter: EventEmitter2,
  ) {}

  async register(dto: RegisterDto) {
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

  async login(username: string, password: string) {
    const user = await this.userRepository.findOneBy({ username });
    if (!user) {
      throw new UnauthorizedException("Invalid credentials");
    }

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new UnauthorizedException("Invalid credentials");
    }

    const payload = { sub: user.id, username: user.username, role: user.role };
    const token = this.jwtService.sign(payload);

    return {
      token,
      user: { id: user.id, username: user.username, role: user.role },
    };
  }
}
