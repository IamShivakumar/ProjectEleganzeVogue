document.addEventListener('DOMContentLoaded', function () {
    const sendOtpButton = document.getElementById('sendOtp');
    const emailInput = document.getElementById('email');
    const otpSection = document.getElementById('otpSection');
    const otpDigits = document.querySelectorAll('.otp__digit');
    const resendOtp = document.getElementById('resendOtp');
    const resendOtpLink = resendOtp.querySelector('a');
    let timer = document.getElementById('timer');

    sendOtpButton.addEventListener('click', function () {
        if (sendOtpButton.textContent === 'Send OTP') {
            emailInput.disabled = true;
            otpSection.style.display = 'flex';
            otpDigits.forEach(input => input.disabled = false);
            sendOtpButton.textContent = 'Verify';
            startTimer();
        } else {
            // Verify OTP logic here
        }
    });

    otpDigits.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            if (value) {
                if (index < otpDigits.length - 1) {
                    otpDigits[index + 1].focus();
                }
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value) {
                if (index > 0) {
                    otpDigits[index - 1].focus();
                }
            }
        });
    });

    function startTimer() {
        let timeLeft = 60;
        resendLink.style.pointerEvents = 'none';
        resendLink.style.color="white";
        resendLink.style.textDecoration = 'none';
        const countdown = setInterval(() => {
            timer.textContent = timeLeft;
            if (timeLeft === 0) {
                clearInterval(countdown);
                resendLink.style.pointerEvents = 'auto';
                resendLink.style.textDecoration = 'underline';
                resendLink.textContent = 'Resend OTP';
                resendLink.addEventListener('click', function () {
                    // Redirect logic
                    window.location.href = 'changepassword.html';
                });
            }
            timeLeft--;
        }, 1000);
    }
});


