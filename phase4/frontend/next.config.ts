import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Enable hot reload in Docker
  experimental: {
    // Enable Turbopack with Docker compatibility
  },
    turbopack: {},

};

export default nextConfig;
