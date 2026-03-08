"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { signInSchema, type SignInSchema } from "@/lib/schemas";
import { getSession, signIn, signOut } from "@/lib/service";

export function SignInPanel() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const sessionQuery = useQuery({
    queryKey: ["session"],
    queryFn: getSession,
  });
  const form = useForm<SignInSchema>({
    resolver: zodResolver(signInSchema),
    defaultValues: {
      email: "owner@latticecloud.dev",
      password: "launch-ready",
    },
  });

  const signInMutation = useMutation({
    mutationFn: signIn,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["session"] });
      router.push("/onboarding?step=workspace");
    },
  });

  const signOutMutation = useMutation({
    mutationFn: signOut,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["session"] });
    },
  });

  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col justify-center gap-6 px-4 py-10 sm:px-6 lg:flex-row lg:items-center lg:px-8">
      <section className="max-w-xl rounded-[2rem] border border-white/80 bg-[rgba(255,251,245,0.9)] px-6 py-8 shadow-[0_30px_80px_-60px_rgba(24,34,24,0.65)]">
        <p className="font-mono text-xs uppercase tracking-[0.28em] text-stone-500">
          Client Onboarding Portal
        </p>
        <h1 className="mt-4 text-4xl font-semibold tracking-[-0.05em] text-stone-950">
          Build trust before the first workspace goes live
        </h1>
        <p className="mt-4 text-sm leading-7 text-stone-600">
          This portfolio project focuses on customer-facing sign-in, wizard progression,
          draft save, route guard, and submit retry handling.
        </p>
        <div className="mt-6 rounded-[1.4rem] border border-stone-200 bg-white/70 p-4 text-sm text-stone-700">
          <p className="font-semibold text-stone-900">Demo credentials</p>
          <p className="mt-2">Email: any valid work email</p>
          <p>Password: at least 8 characters</p>
        </div>
      </section>

      <section className="w-full max-w-xl rounded-[2rem] border border-white/80 bg-[rgba(255,251,245,0.9)] px-6 py-8 shadow-[0_30px_80px_-60px_rgba(24,34,24,0.65)]">
        {sessionQuery.data ? (
          <div className="space-y-5">
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.24em] text-stone-500">
                Active Session
              </p>
              <h2 className="mt-2 text-2xl font-semibold text-stone-950">
                {sessionQuery.data.email}
              </h2>
              <p className="mt-2 text-sm leading-7 text-stone-600">
                Continue the onboarding flow or sign out to test the route guard again.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => router.push("/onboarding?step=workspace")}
                className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800"
              >
                Continue onboarding
              </button>
              <button
                type="button"
                onClick={() => signOutMutation.mutate()}
                className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700 transition hover:border-stone-500"
              >
                Sign out
              </button>
              <Link
                href="/case-study"
                className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700 transition hover:border-stone-500"
              >
                Open case study
              </Link>
            </div>
          </div>
        ) : (
          <form
            className="space-y-5"
            onSubmit={form.handleSubmit((values) => signInMutation.mutate(values))}
          >
            <div>
              <p className="font-mono text-xs uppercase tracking-[0.24em] text-stone-500">
                Sign In
              </p>
              <h2 className="mt-2 text-2xl font-semibold text-stone-950">
                Start the onboarding journey
              </h2>
            </div>

            <label className="grid gap-2 text-sm font-semibold text-stone-800">
              Work email
              <input
                {...form.register("email")}
                className="rounded-2xl border border-stone-300 bg-white px-4 py-3 text-sm outline-none ring-0 transition focus:border-stone-500"
              />
              {form.formState.errors.email ? (
                <span className="text-sm text-red-700">{form.formState.errors.email.message}</span>
              ) : null}
            </label>

            <label className="grid gap-2 text-sm font-semibold text-stone-800">
              Password
              <input
                type="password"
                {...form.register("password")}
                className="rounded-2xl border border-stone-300 bg-white px-4 py-3 text-sm outline-none ring-0 transition focus:border-stone-500"
              />
              {form.formState.errors.password ? (
                <span className="text-sm text-red-700">
                  {form.formState.errors.password.message}
                </span>
              ) : null}
            </label>

            {signInMutation.error ? (
              <p className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {signInMutation.error.message}
              </p>
            ) : null}

            <div className="flex flex-wrap gap-3">
              <button
                type="submit"
                className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800"
              >
                {signInMutation.isPending ? "Signing in..." : "Sign in"}
              </button>
              <Link
                href="/case-study"
                className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700 transition hover:border-stone-500"
              >
                Open case study
              </Link>
            </div>
          </form>
        )}
      </section>
    </main>
  );
}
