const form = document.querySelector("#waitlist-form");
const emailInput = document.querySelector("#email");
const phoneInput = document.querySelector("#phone");
const statusField = document.querySelector("#form-status");
const submitButton = form.querySelector("button");
const popup = document.querySelector("#success-popup");
const popupMessage = document.querySelector("#popup-message");
const popupCloseButton = document.querySelector("#popup-close");

function setStatus(message, tone) {
  statusField.textContent = message;
  statusField.className = `form-status ${tone}`;
}

function openPopup(message) {
  popupMessage.textContent = message;
  popup.hidden = false;
  popupCloseButton.focus();
}

function closePopup() {
  popup.hidden = true;
}

function limitPhoneDigits(value) {
  let digitCount = 0;
  let result = "";

  for (const char of value) {
    if (/\d/.test(char)) {
      if (digitCount >= 12) {
        continue;
      }
      digitCount += 1;
      result += char;
      continue;
    }

    if (char === "+" && result.length === 0) {
      result += char;
      continue;
    }

    if ("-() ".includes(char)) {
      result += char;
    }
  }

  return result;
}

popupCloseButton.addEventListener("click", closePopup);

phoneInput.addEventListener("input", () => {
  const limitedValue = limitPhoneDigits(phoneInput.value);
  if (phoneInput.value !== limitedValue) {
    phoneInput.value = limitedValue;
  }
});

popup.addEventListener("click", (event) => {
  if (event.target === popup) {
    closePopup();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !popup.hidden) {
    closePopup();
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("", "");

  const email = emailInput.value.trim();
  const phone = phoneInput.value.trim();

  if (!email) {
    setStatus("Please enter your email address.", "error");
    emailInput.focus();
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Saving your spot...";

  try {
    const response = await fetch("/api/waitlist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, phone })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Something went wrong.");
    }

    form.reset();
    setStatus(result.message, "success");
    openPopup(result.message);
  } catch (error) {
    setStatus(error.message || "We couldn't save your details. Please try again.", "error");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Join the waitlist";
  }
});
