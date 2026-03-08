import { startIncidentOpsServer } from "./server";

async function main(): Promise<void> {
  const port = Number(process.env.PORT ?? "4100");
  const server = await startIncidentOpsServer({ port });

  process.stdout.write(`incident-ops server listening on ${server.url}\n`);

  const shutdown = async (): Promise<void> => {
    await server.stop();
    process.exit(0);
  };

  process.on("SIGINT", () => {
    void shutdown();
  });

  process.on("SIGTERM", () => {
    void shutdown();
  });
}

void main();
