import {
  hasValidationErrors,
  type SettingsErrors,
  type SettingsValues,
  validateSettings,
} from "./validation";

const FIELD_IDS = ["workspaceName", "supportEmail"] as const;

function getFieldErrorId(field: typeof FIELD_IDS[number]): string {
  return `${field}-error`;
}

function getFieldInput(form: HTMLFormElement, field: typeof FIELD_IDS[number]) {
  return form.elements.namedItem(field) as HTMLInputElement;
}

function extractValues(form: HTMLFormElement): SettingsValues {
  const data = new FormData(form);

  return {
    workspaceName: String(data.get("workspaceName") ?? ""),
    supportEmail: String(data.get("supportEmail") ?? ""),
    timezone: String(data.get("timezone") ?? "Asia/Seoul"),
  };
}

function updateErrorState(form: HTMLFormElement, errors: SettingsErrors): number {
  let errorCount = 0;

  FIELD_IDS.forEach((field) => {
    const input = getFieldInput(form, field);
    const errorText = form.querySelector<HTMLElement>(`#${getFieldErrorId(field)}`);
    const message = errors[field];

    if (!input || !errorText) {
      return;
    }

    if (message) {
      input.setAttribute("aria-invalid", "true");
      errorText.hidden = false;
      errorText.textContent = message;
      errorCount += 1;
    } else {
      input.removeAttribute("aria-invalid");
      errorText.hidden = true;
      errorText.textContent = "";
    }
  });

  return errorCount;
}

function focusFirstInvalidField(form: HTMLFormElement, errors: SettingsErrors) {
  const firstField = FIELD_IDS.find((field) => Boolean(errors[field]));

  if (!firstField) {
    return;
  }

  getFieldInput(form, firstField)?.focus();
}

export function getAppMarkup(): string {
  return `
    <a class="skip-link" href="#main-content">Skip to main content</a>
    <div class="shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Foundations 01</p>
          <h1 class="title">Accessible workspace settings shell</h1>
          <p class="lede">A responsive control surface that keeps form structure, focus order, and status messaging explicit.</p>
        </div>
        <div class="pill-row" aria-label="Current learning focus">
          <span class="pill">Semantic landmarks</span>
          <span class="pill">Keyboard flow</span>
          <span class="pill">Inline guidance</span>
        </div>
      </header>

      <div class="workspace-grid" data-testid="workspace-grid">
        <nav class="nav-card" aria-label="Settings sections">
          <h2 class="section-title">Sections</h2>
          <ul class="nav-list">
            <li><a href="#identity">Workspace identity</a></li>
            <li><a href="#notifications">Notifications</a></li>
            <li><a href="#review">Review checklist</a></li>
          </ul>
        </nav>

        <main id="main-content" tabindex="-1">
          <section class="panel" aria-labelledby="identity-heading">
            <div class="section-header">
              <p class="eyebrow">Primary task</p>
              <h2 id="identity-heading" class="section-title">Workspace identity</h2>
              <p class="section-copy">Use the form below to verify labeling, inline help, error pairing, and keyboard-only navigation.</p>
            </div>

            <form id="settings-form" novalidate>
              <fieldset class="field-group" id="identity">
                <legend>Workspace details</legend>

                <div class="field">
                  <label for="workspaceName">Workspace name</label>
                  <input
                    id="workspaceName"
                    name="workspaceName"
                    type="text"
                    autocomplete="organization"
                    aria-describedby="workspaceName-help workspaceName-error"
                    value="Ops North"
                  />
                  <p id="workspaceName-help" class="field-help">Shown in internal dashboards and review queues.</p>
                  <p id="workspaceName-error" class="field-error" hidden></p>
                </div>

                <div class="field">
                  <label for="supportEmail">Support email</label>
                  <input
                    id="supportEmail"
                    name="supportEmail"
                    type="email"
                    autocomplete="email"
                    aria-describedby="supportEmail-help supportEmail-error"
                    value="ops-north@example.com"
                  />
                  <p id="supportEmail-help" class="field-help">Used for escalations and incident summaries.</p>
                  <p id="supportEmail-error" class="field-error" hidden></p>
                </div>

                <div class="field">
                  <label for="timezone">Primary timezone</label>
                  <select id="timezone" name="timezone" aria-describedby="timezone-help">
                    <option value="Asia/Seoul" selected>Asia/Seoul (UTC+09:00)</option>
                    <option value="Europe/Berlin">Europe/Berlin (UTC+01:00)</option>
                    <option value="America/Los_Angeles">America/Los_Angeles (UTC-08:00)</option>
                  </select>
                  <p id="timezone-help" class="field-help">Status pages and reports will use this timezone by default.</p>
                </div>
              </fieldset>

              <fieldset class="field-group" id="notifications">
                <legend>Delivery preferences</legend>

                <label class="toggle-row" for="incidentDigest">
                  <span>
                    <span class="toggle-title">Daily incident digest</span>
                    <span class="toggle-copy">Summaries for open incidents and unresolved alerts.</span>
                  </span>
                  <input id="incidentDigest" name="incidentDigest" type="checkbox" checked />
                </label>

                <label class="toggle-row" for="reducedMotion">
                  <span>
                    <span class="toggle-title">Reduced motion</span>
                    <span class="toggle-copy">Prefer immediate transitions over animated feedback.</span>
                  </span>
                  <input id="reducedMotion" name="reducedMotion" type="checkbox" />
                </label>
              </fieldset>

              <div class="action-row">
                <button type="submit" class="primary-action">Save settings</button>
                <p id="save-status" class="status-text" role="status" aria-live="polite">
                  No changes saved yet.
                </p>
              </div>
            </form>
          </section>
        </main>

        <aside class="panel review-panel" id="review" aria-labelledby="review-heading">
          <div class="section-header">
            <p class="eyebrow">Review checklist</p>
            <h2 id="review-heading" class="section-title">What this shell verifies</h2>
          </div>
          <ol class="checklist">
            <li>Landmarks are present and readable with role navigation.</li>
            <li>Field help and error text stay paired to their inputs.</li>
            <li>Focus states remain visible with keyboard-only navigation.</li>
            <li>Two-column layout collapses to a single readable column on smaller viewports.</li>
          </ol>
        </aside>
      </div>
    </div>
  `;
}

export function mountSettingsShell(container: HTMLElement): void {
  container.innerHTML = getAppMarkup();

  const form = container.querySelector<HTMLFormElement>("#settings-form");
  const status = container.querySelector<HTMLElement>("#save-status");

  if (!form || !status) {
    return;
  }

  const runValidation = (targetField?: typeof FIELD_IDS[number]) => {
    const errors = validateSettings(extractValues(form));

    if (targetField) {
      const targetErrors: SettingsErrors = {
        [targetField]: errors[targetField],
      };
      updateErrorState(form, targetErrors);
      return errors;
    }

    updateErrorState(form, errors);
    return errors;
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const errors = runValidation();

    if (hasValidationErrors(errors)) {
      const count = Object.values(errors).filter(Boolean).length;
      status.textContent = `Fix ${count} field${count > 1 ? "s" : ""} before saving.`;
      focusFirstInvalidField(form, errors);
      return;
    }

    const values = extractValues(form);
    status.textContent = `Settings saved for ${values.workspaceName.trim()} (${values.timezone}).`;
  });

  FIELD_IDS.forEach((field) => {
    const input = getFieldInput(form, field);

    input?.addEventListener("blur", () => {
      runValidation(field);
    });
  });
}
