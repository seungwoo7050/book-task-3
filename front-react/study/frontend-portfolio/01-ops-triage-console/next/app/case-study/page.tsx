import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const sections = [
  {
    title: "Problem framing",
    body:
      "The product simulates a single operator who must classify a mixed queue of support, QA, feedback, and monitoring issues. The design goal is decision speed with enough context to avoid incorrect routing.",
  },
  {
    title: "UX and information architecture",
    body:
      "The dashboard compresses queue pressure into a short scan, while the main inbox keeps saved views, search, filters, and bulk action controls on one screen. Detail editing moves into a dialog so the queue never disappears from the operator's mental model.",
  },
  {
    title: "State and service realism",
    body:
      "All data stays local, but the app still behaves like a networked product: requests have latency, writes can fail, optimistic updates can roll back, and retry or undo flows are explicit rather than hidden.",
  },
  {
    title: "Quality bar",
    body:
      "The verification target includes unit tests for query and async helpers, integration coverage for sync between queue and detail, E2E coverage for triage and rollback, and a11y smoke checks on the main operator flow.",
  },
];

export default function CaseStudyPage() {
  return (
    <main className="mx-auto min-h-screen max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="rounded-[2rem] border border-white/80 bg-white/90 px-6 py-6 shadow-[0_30px_80px_-60px_rgba(15,23,42,0.6)] backdrop-blur">
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <div className="max-w-3xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-slate-500">
              Case Study / Ops Triage Console
            </p>
            <h1 className="mt-3 text-4xl font-semibold tracking-[-0.04em] text-slate-950">
              Hiring-focused product narrative
            </h1>
            <p className="mt-4 text-sm leading-7 text-slate-600">
              This route is written for review conversations. It focuses on product
              judgment, UX tradeoffs, reliability signals, and testing intent instead of
              code walkthroughs.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge tone="neutral">Korean docs track</Badge>
            <Badge tone="ink">English product UI</Badge>
          </div>
        </div>
      </div>

      <section className="mt-6 grid gap-4">
        {sections.map((section) => (
          <Card key={section.title} className="p-6">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
              {section.title}
            </p>
            <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-700">
              {section.body}
            </p>
          </Card>
        ))}
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-3">
        <Card className="p-5">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
            Product signals
          </p>
          <div className="mt-4 space-y-3 text-sm text-slate-700">
            <p>Dense but readable grid instead of a marketing-style landing page.</p>
            <p>Explicit error, retry, and undo flows around optimistic mutations.</p>
            <p>Keyboard-reachable actions and compact operator notes.</p>
          </div>
        </Card>
        <Card className="p-5">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
            Study linkage
          </p>
          <div className="mt-4 space-y-3 text-sm text-slate-700">
            <p>
              The React internals track remains a supporting proof of depth, not the main
              execution path for this portfolio.
            </p>
            <p>
              This app is the product-facing artifact that hiring managers can run and
              evaluate directly.
            </p>
          </div>
        </Card>
        <Card className="p-5">
          <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
            Next review path
          </p>
          <div className="mt-4 space-y-3 text-sm text-slate-700">
            <p>Run the main app, inspect the queue, and trigger a failed mutation.</p>
            <p>Review the repository docs for positioning and quality criteria.</p>
            <p>Use the E2E flows as a quick confidence check before demoing.</p>
          </div>
        </Card>
      </section>

      <div className="mt-8">
        <Link href="/">
          <Button variant="primary">Back to console</Button>
        </Link>
      </div>
    </main>
  );
}
