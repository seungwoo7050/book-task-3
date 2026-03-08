import { Module } from "@nestjs/common";
import { JwtModule } from "@nestjs/jwt";
import { PassportModule } from "@nestjs/passport";
import { TypeOrmModule } from "@nestjs/typeorm";
import { AuthController } from "./auth.controller";
import { AuthService } from "./auth.service";
import { JwtStrategy } from "./strategies/jwt.strategy";
import { User } from "./entities/user.entity";
import { RuntimeConfigService } from "../runtime/runtime-config.service";
import { AuthRateLimitService } from "./auth-rate-limit.service";

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),
    PassportModule,
    JwtModule.registerAsync({
      inject: [RuntimeConfigService],
      useFactory: (runtimeConfig: RuntimeConfigService) => ({
        secret: runtimeConfig.jwtSecret,
        signOptions: { expiresIn: "1h" },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy, AuthRateLimitService],
})
export class AuthModule {}
