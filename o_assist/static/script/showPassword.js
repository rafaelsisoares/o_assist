const btnShowPassword = document.getElementById("show-password");
    const passwordInput = document.querySelector(".pass");

    btnShowPassword.addEventListener(
        "click", (e) => {
            passwordInput.type === "text"
            ? passwordInput.type = "password"
            : passwordInput.type = "text";
        }
    );