export async function GET() {
  return Response.json({ status: "ok", service: "web", mode: process.env.DATA_MODE ?? "mock" });
}
