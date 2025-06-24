// Show flash messages for a few seconds
window.onload = () => {
    const messages = document.querySelectorAll(".flash-msg");
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.display = "none";
        }, 3000); // 3 seconds
    });
};

// Optional: Confirm before deleting a note
function confirmDelete() {
    return confirm("Are you sure you want to delete this note?");
}

// Optional: Validate registration form
function validateRegisterForm() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !password) {
        alert("All fields are required!");
        return false;
    }
    return true;
}

// Optional: Validate login form
function validateLoginForm() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please enter both email and password.");
        return false;
    }
    return true;
}
