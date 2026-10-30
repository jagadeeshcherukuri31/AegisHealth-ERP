Aegis.register("dashboard", {
  label: "Dashboard",
  async render(root) {
    const d = await Api.get("/dashboard");
    const stat = (l, v, cls = "") => `<div class="stat ${cls}">${l}<b>${v}</b></div>`;
    const rows = UI.table(
      [{ key: "scheduled_at", label: "Time", render: (a) => fmtDT(a.scheduled_at) }, { key: "patient_name", label: "Patient" },
       { key: "doctor_name", label: "Doctor" }, { key: "status", label: "Status", render: (a) => UI.badge(a.status) }],
      d.upcoming);
    root.innerHTML = `<div class="head"><h2>Today at the hospital</h2></div>
      <div class="stats">${stat("Registered patients", d.patients)}${stat("Appointments today", d.appointments_today)}
      ${stat("Waiting now", d.waiting)}${stat("Outstanding billing", money(d.outstanding))}
      ${stat("Low-stock medicines", d.low_stock, d.low_stock ? "alert" : "")}</div>
      <h3 style="margin-bottom:10px">Upcoming today</h3><div class="card">${rows}</div>`;
  },
});
