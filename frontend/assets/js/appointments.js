Aegis.register("appointments", {
  label: "Appointments",
  roles: ["doctor", "nurse", "receptionist", "billing"],
  async render(root) {
    const today = new Date().toISOString().slice(0, 10);
    root.innerHTML = UI.page("Appointments", `<input id="day" type="date" value="${today}"><button class="btn primary" id="add">Book appointment</button>`);
    const draw = async () => {
      const rows = await Api.get("/appointments?date=" + $("#day").value);
      $("#body").innerHTML = UI.table(
        [{ key: "scheduled_at", label: "Time", render: (a) => new Date(a.scheduled_at).toLocaleTimeString([], { timeStyle: "short" }) },
         { key: "patient_name", label: "Patient" }, { key: "doctor_name", label: "Doctor" }, { key: "reason", label: "Reason" },
         { key: "status", label: "Status", render: (a) => UI.badge(a.status) }],
        rows, (a) => ["checked_in", "completed", "cancelled"].filter((s) => s !== a.status && a.status !== "completed" && a.status !== "cancelled")
          .map((s) => `<button class="btn sm" data-id="${a.id}" data-s="${s}">${s.replace("_", " ")}</button>`).join(" "));
    };
    $("#day").onchange = draw;
    $("#add").onclick = async () => {
      const [patients, doctors] = await Promise.all([Api.get("/patients"), Api.get("/appointments/doctors")]);
      const v = await UI.form("Book appointment", [
        { name: "patient_id", label: "Patient", options: patients.map((p) => [p.id, `${p.first_name} ${p.last_name} (${p.mrn})`]) },
        { name: "doctor_id", label: "Doctor", options: doctors.map((d) => [d.id, `${d.name} – ${d.specialization || "General"}`]) },
        { name: "scheduled_at", label: "Date & time", type: "datetime-local", required: true, value: today + "T09:00" },
        { name: "duration_min", label: "Duration (minutes)", type: "number", value: 30 },
        { name: "reason", label: "Reason" }]);
      if (v && (await UI.run(() => Api.post("/appointments", v), "Appointment booked"))) draw();
    };
    root.onclick = async (e) => {
      const { id, s } = e.target.dataset; if (!s) return;
      if (await UI.run(() => Api.patch(`/appointments/${id}/status`, { status: s }), "Status updated")) draw();
    };
    draw();
  },
});
