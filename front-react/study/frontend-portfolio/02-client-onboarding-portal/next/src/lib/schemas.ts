import { z } from "zod";

export const signInSchema = z.object({
  email: z.email("Enter a valid work email."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

export const workspaceProfileSchema = z.object({
  workspaceName: z.string().min(2, "Workspace name must be at least 2 characters."),
  industry: z.string().min(2, "Choose or enter an industry."),
  region: z.string().min(2, "Region is required."),
  teamSize: z.string().min(1, "Select a team size."),
  complianceEmail: z.email("Enter a valid compliance contact email."),
});

export const inviteInputSchema = z.object({
  email: z.email("Enter a valid teammate email."),
  role: z.enum(["Admin", "Billing", "Collaborator"]),
});

export type SignInSchema = z.infer<typeof signInSchema>;
export type WorkspaceProfileSchema = z.infer<typeof workspaceProfileSchema>;
export type InviteInputSchema = z.infer<typeof inviteInputSchema>;
