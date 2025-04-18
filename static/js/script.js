function validateEmail() {
    const email = document.getElementById('email').value;
    if (!email.includes('@')) {
        alert("Email must contain '@' character.");
        return false;
    }
    return true;
}

function validateSignup() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (!email.includes('@')) {
        alert("Email must contain '@' character.");
        return false;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }

    const recaptcha = document.querySelector('input[name="recaptcha"]');
    if (!recaptcha.checked) {
        alert("Please confirm you are not a robot.");
        return false;
    }

    return true;
}

function validatePasswordMatch() {
    const email = document.getElementById('email').value;
    const newPassword = document.getElementById('new_password').value;
    const confirmNewPassword = document.getElementById('confirm_new_password').value;

    if (!email.includes('@')) {
        alert("Email must contain '@' character.");
        return false;
    }

    if (newPassword !== confirmNewPassword) {
        alert("New passwords do not match.");
        return false;
    }

    return true;
}