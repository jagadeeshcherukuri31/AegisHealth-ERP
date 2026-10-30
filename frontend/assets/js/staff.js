Aegis.register("staff", {
  label: "Staff",
  roles: [], // admin only (admin always passes the role check)
  async render(root) {
    const doctors = await Api.get("/appointments/doctors");
    root.innerHTML = UI.page("Staff", `<button class="btn primary" id="add">Add user</button>`,
      UI.table([{ key: "name", label: "Doctor" }, { key: "specialization", label: "Specialization" }, { key: "department", label: "Department" }, { key: "license_no", label: "License" }], doctors));
    $("#add").onclick = async () => {
      const v = await UI.form("Add user", [{ name: "name", label: "Full name", required: true }, { name: "email", label: "Email", type: "email", required: true },
        { name: "password", label: "Temporary password", type: "password", required: true },
        { name: "role", label: "Role", options: ["doctor", "nurse", "receptionist", "pharmacist", "billing", "admin"] }]);
      if (v) await UI.run(() => Api.post("/auth/register", v), "User created");
    };
  },
});
