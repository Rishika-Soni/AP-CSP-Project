function toggleDarkMode() {
  document.body.classList.toggle("dark");
  localStorage.setItem("mode",
    document.body.classList.contains("dark") ? "dark" : "light"
  );
}

if (localStorage.getItem("mode") === "dark") {
  document.body.classList.add("dark");
}
