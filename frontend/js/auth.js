// Auth forms handler
document.addEventListener('DOMContentLoaded', function () {

    // ── Register ─────────────────────────────────────────────────────────────
    var regForm = document.getElementById('register-form');
    if (regForm) {
        regForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var btn = document.getElementById('reg-btn');
            var alert = document.getElementById('reg-alert');
            var name = document.getElementById('reg-name').value.trim();
            var email = document.getElementById('reg-email').value.trim();
            var pass = document.getElementById('reg-pass').value;
            var confirm = document.getElementById('reg-confirm').value;

            if (pass !== confirm) {
                showAlert(alert, 'Passwords do not match.', 'error');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Creating account...';

            fetch((window.SARA_API || API) + '/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name: name, email: email, password: pass })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.access_token) {
                        setAuth(data.access_token, data.name);
                        window.location.href = '/';
                    } else {
                        showAlert(alert, data.detail || 'Registration failed.', 'error');
                    }
                })
                .catch(function () {
                    showAlert(alert, 'Server error. Please try again.', 'error');
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = 'Create Account';
                });
        });
    }

    // ── Login ─────────────────────────────────────────────────────────────────
    var loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var btn = document.getElementById('login-btn');
            var alert = document.getElementById('login-alert');
            var email = document.getElementById('login-email').value.trim();
            var pass = document.getElementById('login-pass').value;

            btn.disabled = true;
            btn.textContent = 'Signing in...';

            fetch((window.SARA_API || API) + '/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: pass })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.access_token) {
                        setAuth(data.access_token, data.name);
                        var next = new URLSearchParams(window.location.search).get('next') || '/';
                        window.location.href = next;
                    } else {
                        showAlert(alert, data.detail || 'Invalid email or password.', 'error');
                    }
                })
                .catch(function () {
                    showAlert(alert, 'Server error. Please try again.', 'error');
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = 'Sign In';
                });
        });
    }

    // ── Forgot Password ───────────────────────────────────────────────────────
    var forgotForm = document.getElementById('forgot-form');
    if (forgotForm) {
        forgotForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var btn = document.getElementById('forgot-btn');
            var alert = document.getElementById('forgot-alert');
            var email = document.getElementById('forgot-email').value.trim();

            btn.disabled = true;
            btn.textContent = 'Sending...';

            fetch((window.SARA_API || API) + '/auth/forgot-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    showAlert(alert, data.message || 'Check your email for the reset link.', 'success');
                })
                .catch(function () {
                    showAlert(alert, 'Server error. Please try again.', 'error');
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = 'Send Reset Link';
                });
        });
    }

    // ── Reset Password ────────────────────────────────────────────────────────
    var resetForm = document.getElementById('reset-form');
    if (resetForm) {
        var token = new URLSearchParams(window.location.search).get('token');

        resetForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var btn = document.getElementById('reset-btn');
            var alert = document.getElementById('reset-alert');
            var pass = document.getElementById('reset-pass').value;
            var confirm = document.getElementById('reset-confirm').value;

            if (pass !== confirm) {
                showAlert(alert, 'Passwords do not match.', 'error');
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Resetting...';

            fetch((window.SARA_API || API) + '/auth/reset-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: token, new_password: pass })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.message) {
                        showAlert(alert, data.message + ' Redirecting to login...', 'success');
                        setTimeout(function () { window.location.href = '/login.html'; }, 2000);
                    } else {
                        showAlert(alert, data.detail || 'Reset failed.', 'error');
                    }
                })
                .catch(function () {
                    showAlert(alert, 'Server error. Please try again.', 'error');
                })
                .finally(function () {
                    btn.disabled = false;
                    btn.textContent = 'Reset Password';
                });
        });
    }

    // ── Google Login buttons ──────────────────────────────────────────────────
    document.querySelectorAll('.btn-google').forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.location.href = (window.SARA_API || API) + '/auth/google';
        });
    });
});

function showAlert(el, msg, type) {
    if (!el) return;
    el.textContent = msg;
    el.className = 'alert ' + type;
    el.style.display = 'block';
}

