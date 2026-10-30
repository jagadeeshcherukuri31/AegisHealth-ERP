const API_BASE = window.API_BASE || "http://localhost:5000/api";

const Api = {
  token: () => localStorage.getItem("aegis_token"),
  async request(method, path, body) {
    const res = await fetch(API_BASE + path, {
      method,
      headers: { "Content-Type": "application/json", ...(Api.token() ? { Authorization: "Bearer " + Api.token() } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (res.status === 401 && path !== "/auth/login") { Aegis.logout(); throw new Error("Session expired"); }
    const data = res.status === 204 ? null : await res.json().catch(() => ({}));
    if (!res.ok) throw new Error((data && (data.error || data.msg)) || "Request failed (" + res.status + ")");
    return data;
  },
  get: (p) => Api.request("GET", p),
  post: (p, b) => Api.request("POST", p, b || {}),
  put: (p, b) => Api.request("PUT", p, b),
  patch: (p, b) => Api.request("PATCH", p, b),
  del: (p) => Api.request("DELETE", p),
};
