"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { ClientOnboardingPortal } from "@/components/portal/client-onboarding-portal";
import { coerceStep } from "@/lib/guards";

export function OnboardingRoute() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const step = coerceStep(searchParams.get("step"));

  return (
    <ClientOnboardingPortal
      step={step}
      onStepChange={(nextStep) => {
        router.replace(`/onboarding?step=${nextStep}`);
      }}
    />
  );
}
