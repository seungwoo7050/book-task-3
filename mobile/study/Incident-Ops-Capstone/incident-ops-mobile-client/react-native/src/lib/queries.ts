export const incidentKeys = {
  all: ['incidents'] as const,
  feed: (baseUrl: string, userId: string) =>
    ['incidents', baseUrl, userId] as const,
};

export const auditKeys = {
  all: ['audit'] as const,
  detail: (baseUrl: string, incidentId: string) =>
    ['audit', baseUrl, incidentId] as const,
};
