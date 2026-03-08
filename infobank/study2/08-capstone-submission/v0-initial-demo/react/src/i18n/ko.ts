const FAILURE_TYPE_LABELS: Record<string, string> = {
  FORBIDDEN_PROMISE: "금지된 약속",
  PII_EXPOSURE: "개인정보 노출",
  MISSING_MANDATORY_STEP: "필수 절차 누락",
  CONTRADICTED_BY_SOURCE: "근거 문서와 모순",
  UNSUPPORTED_CLAIM: "근거 없는 주장",
  RETRIEVAL_MISS: "검색 누락",
  ESCALATION_MISS: "상담원 이관 누락",
};

const GRADE_LABELS: Record<string, string> = {
  A: "A (우수)",
  B: "B (양호)",
  C: "C (보통)",
  D: "D (미흡)",
  F: "F (실패)",
  CRITICAL: "CRITICAL (치명)",
};

export function failureTypeKo(code: string): string {
  const label = FAILURE_TYPE_LABELS[code];
  return label ? `${label} (${code})` : code;
}

export function gradeKo(grade: string | null | undefined): string {
  if (!grade) return "-";
  return GRADE_LABELS[grade] ?? grade;
}
