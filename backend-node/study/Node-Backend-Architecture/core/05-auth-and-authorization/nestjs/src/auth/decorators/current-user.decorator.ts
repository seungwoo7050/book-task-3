import { createParamDecorator, ExecutionContext } from "@nestjs/common";

/**
 * 요청에서 인증된 사용자를 추출하는 커스텀 파라미터 decorator.
 * 사용 예: @CurrentUser() user: JwtPayload
 */
export const CurrentUser = createParamDecorator(
  (_data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
