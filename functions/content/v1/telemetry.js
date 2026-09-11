export async function onRequestPost({ request, env }) {
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, User-Agent",
  };
  let events;
  try {
    events = await request.json();
  } catch {
    return new Response("bad json", { status: 400, headers: cors });
  }
  const list = Array.isArray(events) ? events : [events];
  const token = env.GITHUB_TOKEN;
  if (!token) {
    return new Response("ingest offline", { status: 503, headers: cors });
  }
  const res = await fetch("https://api.github.com/repos/taskfather/stay-delusional/dispatches", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "staydelusional",
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: JSON.stringify({
      event_type: "guide-event",
      client_payload: { events: list.slice(0, 40) },
    }),
  });
  if (!res.ok) {
    return new Response("dispatch failed", { status: 502, headers: cors });
  }
  return new Response(null, { status: 204, headers: cors });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, User-Agent",
    },
  });
}
