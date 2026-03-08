import Link from "next/link";

const sections = [
  {
    title: "Problem framing",
    body:
      "The app simulates a SaaS customer who must pass from sign-in into workspace setup, teammate invite, and final review without losing draft state or trust in the flow.",
  },
  {
    title: "Product judgment",
    body:
      "The onboarding wizard uses compact steps, strong validation feedback, and a visible checklist so the user always knows what remains before submission.",
  },
  {
    title: "Quality bar",
    body:
      "Verification covers schema and guard helpers, storage persistence, integration around step progression and submission retry, and E2E coverage for route guard plus draft restore.",
  },
];

export default function CaseStudyPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <section className="rounded-[2rem] border border-white/80 bg-[rgba(255,251,245,0.92)] px-6 py-6 shadow-[0_30px_80px_-60px_rgba(24,34,24,0.6)] backdrop-blur">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-stone-500">
          Case Study / Client Onboarding Portal
        </p>
        <h1 className="mt-3 text-4xl font-semibold tracking-[-0.04em] text-stone-950">
          Customer-facing flow with validation, draft restore, and retry handling
        </h1>
        <p className="mt-4 max-w-3xl text-sm leading-7 text-stone-600">
          This route is written for hiring review. It focuses on product decisions, route
          guards, form behavior, and trust-building UX rather than implementation trivia.
        </p>
      </section>

      <section className="mt-6 grid gap-4">
        {sections.map((section) => (
          <article
            key={section.title}
            className="rounded-[1.6rem] border border-white/80 bg-[rgba(255,251,245,0.92)] p-6 shadow-[0_20px_50px_-40px_rgba(24,34,24,0.55)]"
          >
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-stone-500">
              {section.title}
            </p>
            <p className="mt-3 text-sm leading-7 text-stone-700">{section.body}</p>
          </article>
        ))}
      </section>

      <div className="mt-8">
        <Link
          href="/"
          className="inline-flex rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800"
        >
          Back to sign-in
        </Link>
      </div>
    </main>
  );
}
