# References

## 1. Helm Docs

- Title: Helm Documentation
- URL: https://helm.sh/docs/
- Checked date: 2026-03-07
- Why: lint와 template 검증 기준을 정리하기 위해 확인했다.
- Learned: cluster 없이도 chart 품질의 상당 부분은 로컬에서 검증 가능하다.
- Effect: `verified` 최소 기준을 `helm-lint`와 `helm-template`로 고정했다.

## 2. Argo CD Docs

- Title: Argo CD Documentation
- URL: https://argo-cd.readthedocs.io/
- Checked date: 2026-03-07
- Why: Application manifest의 역할과 범위를 정리하기 위해 확인했다.
- Learned: 입문 단계에서는 sync policy와 source path 설명만으로도 충분히 가치가 있다.
- Effect: apply를 필수 검증에서 제외하고 문서화 대상으로 남겼다.

