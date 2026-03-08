import { z } from "zod";
import {
  issueLabels,
  issuePriorities,
  issueStatuses,
  teamRoutes,
} from "@/lib/constants";

export const noteSchema = z
  .string()
  .trim()
  .max(180, "Keep notes short enough to scan from the timeline.")
  .optional();

export const issuePatchSchema = z.object({
  status: z.enum(issueStatuses).optional(),
  priority: z.enum(issuePriorities).optional(),
  labels: z.array(z.enum(issueLabels)).optional(),
  routeTeam: z.enum(teamRoutes).optional(),
  operatorNote: noteSchema,
});

export const bulkIssuePatchSchema = z.object({
  status: z.enum(issueStatuses).optional(),
  priority: z.enum(issuePriorities).optional(),
  addLabel: z.enum(issueLabels).optional(),
  routeTeam: z.enum(teamRoutes).optional(),
});

