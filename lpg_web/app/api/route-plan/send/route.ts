import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const payload = await req.json().catch(() => ({}))
    // Mock: pretend to dispatch to driver app or SMS gateway
    const id = Math.random().toString(36).slice(2, 10)
    return NextResponse.json({ status: 'ok', dispatchId: id, at: new Date().toISOString(), echo: payload })
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || 'unknown error' }, { status: 500 })
  }
}
