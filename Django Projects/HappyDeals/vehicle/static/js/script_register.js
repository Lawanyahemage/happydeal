     var passwordInput = document.getElementById("password");
            var passwordEye = document.querySelector(".password-eye span");
            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                passwordEye.textContent = "🙈";
            } else {
                passwordInput.type = "password";
                passwordEye.textContent = "👁️";
            }
        }