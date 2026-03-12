import { Inject, Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";

import { RuntimeConfigService } from "../../runtime/runtime-config.service";

export interface JwtPayload {
  sub: string;
  username: string;
  role: string;
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    @Inject(RuntimeConfigService)
    runtimeConfig: RuntimeConfigService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: runtimeConfig.jwtSecret,
    });
  }

  validate(payload: JwtPayload) {
    return { sub: payload.sub, username: payload.username, role: payload.role };
  }
}
