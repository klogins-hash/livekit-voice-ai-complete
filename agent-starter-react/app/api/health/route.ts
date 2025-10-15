import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Basic health check - can be extended with more comprehensive checks
    const healthData = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV,
      version: process.env.npm_package_version || '1.0.0',
      livekit: {
        configured: !!(
          process.env.LIVEKIT_API_KEY &&
          process.env.LIVEKIT_API_SECRET &&
          process.env.LIVEKIT_URL
        ),
      },
    };

    return NextResponse.json(healthData, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString(),
      },
      { status: 500 }
    );
  }
}
