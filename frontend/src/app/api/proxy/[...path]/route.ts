import type { NextRequest } from "next/server";

const API_URL = (process.env.SEMANTIQ_API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/+$/, "");
const API_KEY = process.env.SEMANTIQ_API_KEY || process.env.NEXT_PUBLIC_API_KEY || "dev-key";

export async function GET(req: NextRequest, { params }: { params: { path: string[] } }) {
  const urlPath = `/${(params.path || []).join("/")}`;
  const target = `${API_URL}${urlPath}${req.nextUrl.search || ""}`;
  const res = await fetch(target, {
    headers: {
      "x-api-key": API_KEY,
      "accept": "application/json",
    },
    cache: "no-store",
  });
  return new Response(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" } });
}

export async function POST(req: NextRequest, { params }: { params: { path: string[] } }) {
  const urlPath = `/${(params.path || []).join("/")}`;
  const target = `${API_URL}${urlPath}${req.nextUrl.search || ""}`;
  const body = await req.text();
  const res = await fetch(target, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "content-type": req.headers.get("content-type") || "application/json",
      "accept": "application/json",
    },
    body,
    cache: "no-store",
  });
  return new Response(await res.text(), { status: res.status, headers: { "content-type": res.headers.get("content-type") || "application/json" } });
}
