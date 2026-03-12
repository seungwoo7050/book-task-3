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
   * JWT 서명이 검증된 뒤에 호출된다.
   * 반환값은 req.user에 붙는다.
   */
  validate(payload: { sub: string; username: string; role: string }) {
    return { sub: payload.sub, username: payload.username, role: payload.role };
  }
}
