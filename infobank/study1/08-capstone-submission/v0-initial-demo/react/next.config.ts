import { fileURLToPath } from "node:url";
import type { NextConfig } from "next";

const root = fileURLToPath(new URL("..", import.meta.url));

const nextConfig: NextConfig = {
  transpilePackages: ["@study1-v0/shared"],
  allowedDevOrigins: ["127.0.0.1"],
  turbopack: {
    root
  }
};

export default nextConfig;
