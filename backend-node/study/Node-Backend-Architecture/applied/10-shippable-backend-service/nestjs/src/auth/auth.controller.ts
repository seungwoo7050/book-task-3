import { Body, Controller, Headers, HttpCode, Inject, Post } from "@nestjs/common";
import { ApiBody, ApiOperation, ApiTags } from "@nestjs/swagger";
import { AuthService } from "./auth.service";
import { RegisterDto } from "./dto/register.dto";
import { LoginDto } from "./dto/login.dto";

@ApiTags("auth")
@Controller("auth")
export class AuthController {
  constructor(@Inject(AuthService) private readonly authService: AuthService) {}

  @ApiOperation({ summary: "Register a new user" })
  @ApiBody({ type: RegisterDto })
  @Post("register")
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  @ApiOperation({ summary: "Issue a JWT token" })
  @ApiBody({ type: LoginDto })
  @Post("login")
  @HttpCode(200)
  login(@Body() dto: LoginDto, @Headers("x-forwarded-for") forwardedFor?: string) {
    const clientId = forwardedFor?.split(",")[0]?.trim() || `username:${dto.username}`;
    return this.authService.login(dto.username, dto.password, clientId);
  }
}
