import { z } from 'zod';

import { APPROVAL_DECISIONS, INCIDENT_SEVERITIES, USER_ROLES } from '../contracts';

export const loginSchema = z.object({
  userId: z.string().trim().min(3, 'user id는 최소 3자여야 합니다.'),
  role: z.enum(USER_ROLES),
  baseUrl: z.string().url('http(s) base URL을 입력하세요.'),
});

export type LoginFormValues = z.infer<typeof loginSchema>;

export const createIncidentSchema = z.object({
  title: z.string().trim().min(4, '제목은 최소 4자여야 합니다.'),
  description: z.string().trim().max(280, '설명은 280자 이하여야 합니다.'),
  severity: z.enum(INCIDENT_SEVERITIES),
});

export type CreateIncidentFormValues = z.infer<typeof createIncidentSchema>;

export const resolutionSchema = z.object({
  reason: z.string().trim().min(4, '승인 요청 이유를 4자 이상 입력하세요.'),
});

export const approvalDecisionSchema = z.object({
  decision: z.enum(APPROVAL_DECISIONS),
  note: z.string().trim().max(120, '메모는 120자 이하여야 합니다.').optional(),
});
