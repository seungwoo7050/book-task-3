# 회고

이번 버전이 가장 잘한 점은 “hash/MAC/KDF를 각각 다른 출력 함수”가 아니라 “다른 보안 질문에 답하는 도구”로 보이게
정리한 것입니다. 반대로 가장 큰 한계는 이 프로젝트만으로 nonce 관리, key rotation, 서명, AEAD 같은 실제 응용 계층의
더 큰 보안 설계를 보여 주지는 못한다는 점입니다.

후속으로는 Argon2id, session/JWT threat modeling, dependency triage 같은 더 상위 레벨 프로젝트가 필요합니다.

