export interface SettingsValues {
  workspaceName: string;
  supportEmail: string;
  timezone: string;
}

export interface SettingsErrors {
  workspaceName?: string;
  supportEmail?: string;
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateSettings(values: SettingsValues): SettingsErrors {
  const errors: SettingsErrors = {};
  const name = values.workspaceName.trim();
  const email = values.supportEmail.trim();

  if (name.length < 3) {
    errors.workspaceName =
      "Workspace name must be at least 3 characters long.";
  }

  if (!EMAIL_PATTERN.test(email)) {
    errors.supportEmail = "Enter a valid support email address.";
  }

  return errors;
}

export function hasValidationErrors(errors: SettingsErrors): boolean {
  return Object.values(errors).some(Boolean);
}
