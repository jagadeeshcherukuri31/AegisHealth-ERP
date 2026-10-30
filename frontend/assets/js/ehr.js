Aegis.register("ehr", {
  label: "Medical records",
  roles: ["doctor", "nurse"],
  async render(root) {
    const patients = await Api.get("/patients");
    const canWrite = ["doctor", "admin"].includes(Aegis.user.role);
    root.innerHTML = UI.page("Medical records",
      `<select id="pt"><option value="">Select patient…</option>${patients.map((p) => `<option value="${p.id}">${esc(p.first_name + " " + p.last_name)} (${esc(p.mrn)})</option>`).join("")}</select>` +
      (canWrite ? `<button class="btn primary" id="add">New entry</button>` : ""), `<div class="empty">Choose a patient to see their history.</div>`);
    const draw = async () => {
      if (!$("#pt").value) return;
      const rows = await Api.get("/ehr?patient_id=" + $("#pt").value);
      $("#body").innerHTML = UI.table(
        [{ key: "created_at", label: "Date", render: (r) => fmtDT(r.created_at) }, { key: "diagnosis", label: "Diagnosis" },
         { key: "doctor_name", label: "Doctor" }, { label: "Vitals", render: (r) => esc([r.bp, r.heart_rate && r.heart_rate + " bpm", r.temperature_c && r.temperature_c + " °C"].filter(Boolean).join(" · ")) },
         { key: "prescription", label: "Prescription" }, { key: "notes", label: "Notes" }], rows);
    };
    $("#pt").onchange = draw;
    if (canWrite) $("#add").onclick = async () => {
      if (!$("#pt").value) return UI.toast("Select a patient first", true);
      const doctors = await Api.get("/appointments/doctors");
      const mine = doctors.find((d) => d.user_id === Aegis.user.id);
      const v = await UI.form("New medical record", [
        { name: "doctor_id", label: "Doctor", options: doctors.map((d) => [d.id, d.name]), value: mine && mine.id },
        { name: "diagnosis", label: "Diagnosis", required: true },
        { name: "bp", label: "Blood pressure (e.g. 120/80)" }, { name: "heart_rate", label: "Heart rate (bpm)", type: "number" },
        { name: "temperature_c", label: "Temperature (°C)", type: "number", step: "0.1" },
        { name: "prescription", label: "Prescription", type: "textarea" }, { name: "notes", label: "Notes", type: "textarea" }]);
      if (v && (await UI.run(() => Api.post("/ehr", { ...v, patient_id: +$("#pt").value }), "Record saved"))) draw();
    };
  },
});
