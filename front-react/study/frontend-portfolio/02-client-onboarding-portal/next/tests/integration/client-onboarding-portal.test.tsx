import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import { ClientOnboardingPortal } from "@/components/portal/client-onboarding-portal";
import { signIn } from "@/lib/service";
import type { OnboardingStep } from "@/lib/types";

function renderPortal(step: OnboardingStep = "workspace") {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  function Wrapper() {
    const [currentStep, setCurrentStep] = useState<OnboardingStep>(step);
    return (
      <QueryClientProvider client={queryClient}>
        <ClientOnboardingPortal step={currentStep} onStepChange={setCurrentStep} />
      </QueryClientProvider>
    );
  }

  return render(<Wrapper />);
}

describe("ClientOnboardingPortal", () => {
  it("shows the route guard when no session exists", async () => {
    renderPortal();
    expect(await screen.findByText(/Sign in before opening the onboarding flow/i)).toBeInTheDocument();
  });

  it("supports step progression, invite creation, and submit retry", async () => {
    await signIn({
      email: "owner@latticecloud.dev",
      password: "launch-ready",
    });

    renderPortal();
    const user = userEvent.setup();

    expect(await screen.findByText(/Capture the launch-ready workspace profile/i)).toBeInTheDocument();

    await user.clear(screen.getByLabelText(/Workspace name/i));
    await user.type(screen.getByLabelText(/Workspace name/i), "Lattice Cloud");
    await user.clear(screen.getByLabelText(/Industry/i));
    await user.type(screen.getByLabelText(/Industry/i), "Developer tooling");
    await user.selectOptions(screen.getByLabelText(/Region/i), "Seoul");
    await user.selectOptions(screen.getByLabelText(/Team size/i), "11-50");
    await user.clear(screen.getByLabelText(/Compliance contact/i));
    await user.type(screen.getByLabelText(/Compliance contact/i), "compliance@latticecloud.dev");
    await user.click(screen.getByRole("button", { name: /Save draft/i }));

    await screen.findByText(/Draft saved to the local demo workspace/i);

    await user.click(screen.getByRole("button", { name: /Go to invites/i }));
    await screen.findByText(/Bring the first operators into the workspace/i);

    await user.type(screen.getByLabelText(/Invite email/i), "ops@latticecloud.dev");
    await user.selectOptions(screen.getByLabelText(/^Role$/i), "Admin");
    await user.click(screen.getByRole("button", { name: /Add invite/i }));
    await screen.findByText(/ops@latticecloud.dev/i);

    await user.click(screen.getByRole("button", { name: /Continue to review/i }));
    await screen.findByText(/Confirm readiness and submit the onboarding packet/i);

    const failToggle = screen.getByRole("checkbox", {
      name: /Simulate the next submit failure/i,
    });
    await user.click(failToggle);
    expect(failToggle).toBeChecked();

    const submitButton = screen.getByRole("button", { name: /Submit onboarding/i });
    expect(submitButton).toBeDisabled();

    await user.click(screen.getByRole("button", { name: /Mark review complete/i }));

    await waitFor(() => {
      expect(submitButton).toBeEnabled();
    });

    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Submission failed/i)).toBeInTheDocument();
    });

    await user.click(submitButton);

    await waitFor(() => {
      expect(
        screen.getByText(/Submitted Lattice Cloud at/i),
      ).toBeInTheDocument();
    });
  });
});
