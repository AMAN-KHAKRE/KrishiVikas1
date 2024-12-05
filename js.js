document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("feedback-form");
    const formMessage = document.getElementById("formMessage");

    // Form submission handling
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const name = document.getElementById("name").value;
        formMessage.textContent = `Thank you, ${name}! Your message has been sent.`;
        form.reset();
    });

    // Smooth scrolling for Projects, About, and Feedback sections
    document.querySelector('a[href="#services"]').addEventListener("click", (event) => {
        event.preventDefault();
        document.querySelector("#services").scrollIntoView({ behavior: "smooth" });
    });

    document.querySelector('a[href="#about"]').addEventListener("click", (event) => {
        event.preventDefault();
        document.querySelector("#about").scrollIntoView({ behavior: "smooth" });
    });

    document.querySelector('a[href="#feedback"]').addEventListener("click", (event) => {
        event.preventDefault();
        document.querySelector("#feedback").scrollIntoView({ behavior: "smooth" });
    });
});
