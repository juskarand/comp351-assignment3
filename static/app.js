function app() {
  return {
    user: null,
    items: [],
    error: "",
    success: "",
    loginForm: { username: "", password: "" },
    registerForm: { username: "", email: "", password: "" },

    async init() {
      await this.fetchMe();
      if (this.user) await this.loadItems();
    },

    async fetchMe() {
      const res = await fetch("/api/me", { credentials: "include" });
      this.user = res.ok ? await res.json() : null;
    },

    async register() {
      this.error = ""; this.success = "";
      const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(this.registerForm),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) { this.error = data.detail || "Registration failed"; return; }
      this.success = "Registered. Now login.";
    },

    async login() {
      this.error = "";
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(this.loginForm),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) { this.error = data.detail || "Login failed"; return; }
      window.location.href = "/";
    },

    async logout() {
      await fetch("/api/logout", { method: "POST", credentials: "include" });
      window.location.href = "/";
    },

    async loadItems() {
      this.error = "";
      const res = await fetch("/api/items", { credentials: "include" });
      if (res.status === 401) { this.error = "Unauthorized (login first)."; this.items = []; return; }
      this.items = res.ok ? await res.json() : [];
    },
  };
}
