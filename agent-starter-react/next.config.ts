import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Optimize for production
  compress: true,
  
  // Enable experimental features for better performance
  experimental: {
    optimizePackageImports: ['@livekit/components-react', 'livekit-client']
  },
  
  // Configure headers for better security and performance
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },
  
  // Environment variables to expose to the client
  env: {
    NEXT_PUBLIC_APP_CONFIG_ENDPOINT: process.env.NEXT_PUBLIC_APP_CONFIG_ENDPOINT,
  },
};

export default nextConfig;
