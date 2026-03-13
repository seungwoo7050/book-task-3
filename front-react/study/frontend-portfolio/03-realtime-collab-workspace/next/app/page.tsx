import { WorkspaceShell } from "@/components/workspace-shell";

type HomePageProps = {
  searchParams?: Promise<{ viewer?: string }>;
};

export default async function HomePage({ searchParams }: HomePageProps) {
  const resolved = searchParams ? await searchParams : undefined;
  return <WorkspaceShell viewerHint={resolved?.viewer} />;
}
