import { Injectable } from "@nestjs/common";
import { PassportStrategy } from "@nestjs/passport";
import { ExtractJwt, Strategy } from "passport-jwt";

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: "super-secret",
    });
  }

  /**
   * Called after JWT signature is verified.
   * The return value is attached to req.user.
   */
  validate(payload: { sub: string; username: string; role: string }) {
    return { sub: payload.sub, username: payload.username, role: payload.role };
  }
}
