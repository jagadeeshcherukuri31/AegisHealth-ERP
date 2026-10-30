const $ = (s, r = document) => r.querySelector(s);
const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const money = (n) => "$" + Number(n || 0).toFixed(2);
const fmtDT = (s) => (s ? new Date(s).toLocaleString([], { dateStyle: "medium", timeStyle: "short" }) : "");

const UI = {
  toast(msg, bad) {
    const t = $("#toast");
    t.textContent = msg; t.className = "toast show" + (bad ? " bad" : "");
    clearTimeout(UI._t); UI._t = setTimeout(() => (t.className = "toast"), 2800);
  },
  badge(s) {
    const cls = { paid: "ok", completed: "ok", scheduled: "", checked_in: "warn", partial: "warn", unpaid: "warn", cancelled: "warn", no_show: "warn" }[s] ?? "";
    return `<span class="badge ${cls}">${esc(String(s).replace("_", " "))}</span>`;
  },
  // cols: [{key,label,render?}], actions: (row)=>html string, wired via data-act buttons
  table(cols, rows, actions) {
    if (!rows.length) return `<div class="empty">Nothing here yet.</div>`;
    const head = cols.map((c) => `<th>${esc(c.label)}</th>`).join("") + (actions ? "<th></th>" : "");
    const body = rows.map((r) => `<tr>${cols.map((c) => `<td>${c.render ? c.render(r) : esc(r[c.key])}</td>`).join("")}${actions ? `<td>${actions(r)}</td>` : ""}</tr>`).join("");
    return `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
  },
  // fields: [{name,label,type?,options?,required?,value?}] -> resolves with values, or null if cancelled
  form(title, fields, submitLabel = "Save") {
    return new Promise((resolve) => {
      const m = document.createElement("div");
      m.className = "modal";
      const inputs = fields.map((f) => {
        const base = `name="${f.name}" ${f.required ? "required" : ""}`;
        const val = f.value ?? "";
        if (f.options) return `<label>${esc(f.label)}<select ${base}>${f.options.map((o) => { const [v, l] = Array.isArray(o) ? o : [o, o]; return `<option value="${esc(v)}" ${String(v) === String(val) ? "selected" : ""}>${esc(l)}</option>`; }).join("")}</select></label>`;
        if (f.type === "textarea") return `<label>${esc(f.label)}<textarea rows="3" ${base}>${esc(val)}</textarea></label>`;
        return `<label>${esc(f.label)}<input type="${f.type || "text"}" ${base} value="${esc(val)}" ${f.step ? `step="${f.step}"` : ""}></label>`;
      }).join("");
      m.innerHTML = `<form><h2>${esc(title)}</h2>${inputs}<div class="actions"><button type="button" class="btn" data-x>Cancel</button><button class="btn primary">${esc(submitLabel)}</button></div></form>`;
      document.body.appendChild(m);
      const close = (v) => { m.remove(); resolve(v); };
      $("[data-x]", m).onclick = () => close(null);
      m.onclick = (e) => e.target === m && close(null);
      $("form", m).onsubmit = (e) => { e.preventDefault(); close(Object.fromEntries(new FormData(e.target))); };
      const first = $("input,select,textarea", m); first && first.focus();
    });
  },
  // Wraps an async action: toasts errors and re-renders on success.
  async run(fn, ok) {
    try { const r = await fn(); if (ok) UI.toast(ok); return r; }
    catch (e) { UI.toast(e.message, true); }
  },
  page(title, toolsHtml, bodyHtml) {
    return `<div class="head"><h2>${esc(title)}</h2><div class="tools">${toolsHtml || ""}</div></div><div class="card" id="body">${bodyHtml || ""}</div>`;
  },
};

const Aegis = {
  modules: {}, user: null,
  register(id, mod) { Aegis.modules[id] = mod; },
  boot() {
    $("#login-form").onsubmit = async (e) => {
      e.preventDefault();
      const f = Object.fromEntries(new FormData(e.target));
      try {
        const r = await Api.post("/auth/login", f);
        localStorage.setItem("aegis_token", r.token);
        localStorage.setItem("aegis_user", JSON.stringify(r.user));
        Aegis.start();
      } catch (err) { $("#login-error").textContent = err.message; }
    };
    $("#logout").onclick = () => Aegis.logout();
    window.addEventListener("hashchange", () => Aegis.route());
    Api.token() ? Aegis.start() : Aegis.showLogin();
  },
  showLogin() { $("#shell").hidden = true; $("#login").hidden = false; },
  logout() { localStorage.removeItem("aegis_token"); localStorage.removeItem("aegis_user"); Aegis.showLogin(); },
  start() {
    Aegis.user = JSON.parse(localStorage.getItem("aegis_user") || "null");
    $("#login").hidden = true; $("#shell").hidden = false;
    $("#me-name").textContent = `${Aegis.user.name} (${Aegis.user.role})`;
    const ok = (m) => !m.roles || Aegis.user.role === "admin" || m.roles.includes(Aegis.user.role);
    $("#nav").innerHTML = Object.entries(Aegis.modules).filter(([, m]) => ok(m))
      .map(([id, m]) => `<a href="#/${id}" data-id="${id}">${esc(m.label)}</a>`).join("");
    Aegis.route();
  },
  async route() {
    if (!Aegis.user) return;
    let id = location.hash.replace("#/", "") || "dashboard";
    const mod = Aegis.modules[id];
    if (!mod || (mod.roles && Aegis.user.role !== "admin" && !mod.roles.includes(Aegis.user.role))) id = "dashboard";
    document.querySelectorAll("nav a").forEach((a) => a.classList.toggle("active", a.dataset.id === id));
    const root = $("#view");
    root.innerHTML = `<p class="muted">Loading…</p>`;
    try { await Aegis.modules[id].render(root); } catch (e) { root.innerHTML = `<p class="error">${esc(e.message)}</p>`; }
  },
  reload() { return Aegis.route(); },
};
