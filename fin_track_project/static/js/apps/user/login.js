const togglePasswordButton = document.getElementById("togglePassword");

if (togglePasswordButton) {
    togglePasswordButton.addEventListener("click", function () {
        const passwordInput = document.getElementById("id_password");
        const icon = this.querySelector("i");

        if (!passwordInput || !icon) {
            return;
        }

        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            icon.classList.remove("bi-eye");
            icon.classList.add("bi-eye-slash");
        } else {
            passwordInput.type = "password";
            icon.classList.remove("bi-eye-slash");
            icon.classList.add("bi-eye");
        }
    });
}

const pendingEmailTimer = document.getElementById("pending-email-timer");
const updateEmailLink = document.querySelector("[data-update-email-link]");

function formatCountdown(totalSeconds) {
    const safeSeconds = Math.max(0, totalSeconds);
    const minutes = Math.floor(safeSeconds / 60);
    const seconds = safeSeconds % 60;
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function setUpdateEmailLinkState(isAvailable) {
    if (!updateEmailLink) {
        return;
    }

    updateEmailLink.classList.toggle("pe-none", !isAvailable);
    updateEmailLink.classList.toggle("opacity-50", !isAvailable);

    if (isAvailable) {
        updateEmailLink.removeAttribute("aria-disabled");
        updateEmailLink.textContent = "Nao confirmou o e-mail? Corrija o endereco agora.";
    } else {
        updateEmailLink.setAttribute("aria-disabled", "true");
        updateEmailLink.textContent = "Nao confirmou o e-mail? Aguarde o timer para corrigir o endereco.";
    }
}

if (pendingEmailTimer) {
    const timerText = pendingEmailTimer.querySelector("[data-timer-text]");
    let remainingSeconds = Number.parseInt(
        pendingEmailTimer.dataset.remainingSeconds || "0",
        10,
    );

    const updateTimer = () => {
        if (!timerText) {
            return;
        }

        if (remainingSeconds > 0) {
            timerText.textContent = `Correcao do e-mail disponivel em ${formatCountdown(remainingSeconds)}.`;
            setUpdateEmailLinkState(false);
            remainingSeconds -= 1;
            return;
        }

        timerText.textContent = "Voce ja pode corrigir o e-mail pendente.";
        setUpdateEmailLinkState(true);
        window.clearInterval(timerInterval);
    };

    const timerInterval = window.setInterval(updateTimer, 1000);
    updateTimer();
}
