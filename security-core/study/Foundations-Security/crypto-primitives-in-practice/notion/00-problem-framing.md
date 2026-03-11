# 문제 프레이밍

보안 문서에서 가장 자주 흐려지는 지점은 “digest를 만들었다”와 “sender를 인증했다”와 “새 키를 만들었다”를 같은
문장에 섞는 순간입니다. 이 프로젝트는 그 혼선을 줄이기 위해 hash, MAC, KDF를 각각 다른 입력 모델과 검증 기준으로
분리합니다.

이번 v1에서는 reference vector가 있는 primitive만 다룹니다. production auth 시스템 전체를 만들지 않고, 먼저
primitive 경계를 설명 가능한 상태로 만드는 것이 목표입니다.

