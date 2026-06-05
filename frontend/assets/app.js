function formatAuthError(data) {
    if (!data) {
        return "Login failed";
    }

    if (data.message) {
        return data.message;
    }

    if (typeof data.detail === "string") {
        return data.detail;
    }

    return "Login failed";
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function clearToken() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_role");
}

function showError(message) {
    const errorBox = document.getElementById("errorBox");

    if (errorBox) {
        errorBox.style.display = "block";
        errorBox.innerText = message;
    }
}

async function login(email, password) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData
    });

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = null;
    }

    if (!response.ok) {
        throw new Error(formatAuthError(data));
    }

    setToken(data.access_token);
    localStorage.setItem("user_email", data.user.email);
    localStorage.setItem("user_role", data.user.role);

    window.location.href = "/site/dashboard_v2.html";
}

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                await login(email, password);
            } catch (error) {
                showError(error.message);
            }
        });
    }
});
