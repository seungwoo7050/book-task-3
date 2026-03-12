# Debug Log — App Distribution

## env 키 불일치 검증 실패

처음 `.env.*.example` 파일을 만들 때 `development`에만 `DEBUG_MODE=true`를 넣었다가 `validate-release.mjs`가 실패했다. 검증 스크립트는 세 env 파일의 키 집합이 정확히 동일한지를 `JSON.stringify` 비교로 확인하기 때문에, 키 하나라도 다르면 즉시 실패한다.

이 경험은 "환경별로 다른 설정이 필요하면 모든 환경에 키를 두되 값만 다르게 해야 한다"는 원칙을 체감시켰다. `DEBUG_MODE`를 세 파일 모두에 넣되, production에서는 `false`로 설정하는 식으로 해결했다. 최종적으로는 학습 범위를 단순하게 유지하기 위해 네 가지 키(`API_BASE_URL`, `WS_BASE_URL`, `RELEASE_CHANNEL`, `SENTRY_DSN`)만 남겼다.

## Fastlane Ruby 버전 충돌

macOS에서 Fastlane을 처음 실행할 때 시스템 Ruby와 Bundler Ruby 간 버전 충돌이 발생할 수 있다. `Gemfile`에 Fastlane을 명시하고 `bundle exec fastlane`으로 실행해야 안정적이다. 이 프로젝트에서는 Fastlane lane이 `node scripts/validate-release.mjs`만 호출하므로, 실제로 Fastlane의 네이티브 기능(match, gym 등)은 쓰지 않는다.

## release-rehearsal.mjs 경로 문제

`releaseConfig.mjs`에서 `projectRoot`를 `import.meta.url` 기반으로 계산할 때, Node.js 버전에 따라 URL 해석이 달라질 수 있다. `path.resolve(new URL('..', import.meta.url).pathname)`으로 한 단계 상위 디렉토리를 정확히 가리키도록 했다.

## rehearsal-summary.json 커밋 여부

이 파일을 git에 커밋할 것인지 논의가 있었다. 결론은 "커밋한다". 이유는 이 파일이 재현 가능한 검증 결과물이고, CI에서 생성/비교할 수 있는 artifact이기 때문이다. `.gitignore`에서 `release/` 디렉토리를 제외하지 않은 것은 의도적이다.
