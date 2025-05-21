/**
 * Pre-made item form JS to handle the dynamic inputs and displays for the user.
 */

document.addEventListener("DOMContentLoaded", function () {
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );
  const infillSlider = document.querySelector(".infill-range");
  const infillValue = document.getElementById("infill-value");
  const colorSwatch = document.getElementById("color-swatch");
  const priceValue = document.getElementById("price-value");
  const priceEstimate = document.getElementById("price-estimate");
  const priceError = document.getElementById("price-error");
  const submitButton = document.getElementById("submit-button");
  const selectedFilamentInput = document.getElementById("selected-filament");
  const modelIdInput = document.getElementById("model-id");
  const modelThumbnailContainer = document.getElementById(
    "model-thumbnail-container"
  );
  const modelThumbnail = document.getElementById("model-thumbnail");

  function updateFormState() {
    const modelId = modelSelect.value;
    const selectedOption = modelSelect.options[modelSelect.selectedIndex];
    if (modelId && selectedOption.dataset.thumbnail) {
      modelThumbnail.src = selectedOption.dataset.thumbnail;
      modelThumbnailContainer.classList.remove("hidden");
    } else {
      modelThumbnailContainer.classList.add("hidden");
    }

    modelIdInput.value = modelId;

    if (!modelId) {
      materialSelect.disabled = true;
      materialSelect.value = "";
      filamentSelect.disabled = true;
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentContainer.classList.add("hidden");
      infillSlider.disabled = true;
      updatePriceDisplay(null);
      updateSubmitButtonState();
      return;
    }
    materialSelect.disabled = false;
    if (materialSelect.value) {
      updateFilaments(modelId, materialSelect.value);
    } else {
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentSelect.disabled = true;
      filamentContainer.classList.add("hidden");
      updatePriceDisplay(null);
    }

    const baseInfill =
      parseInt(
        modelSelect.options[modelSelect.selectedIndex].dataset.baseInfill * 100
      ) || 30;

    infillSlider.value = baseInfill;
    infillValue.textContent = `${baseInfill}%`;
    infillSlider.disabled = false;

    if (filamentSelect.value) {
      calculatePrice();
    } else {
      updatePriceDisplay(null);
    }
  }

  /**
   * Fetches and updates the filaments dropdown based on selected model and material.
   * Takes in modelId and materialId.
   * Uses the shared fetchFilaments function from order_item.js
   */
  async function updateFilaments(modelId, materialId) {
    if (!materialId) {
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentSelect.disabled = true;
      filamentContainer.classList.add("hidden");
      updateSubmitButtonState();
      return;
    }

    try {
      const data = await fetchFilaments(modelId, materialId);

      filamentSelect.innerHTML = '<option value="">Select a color</option>';
      data.filaments.forEach((filament) => {
        const option = document.createElement("option");
        option.value = filament.id;
        option.textContent = `${filament.color_code} - ${filament.name}`;
        option.dataset.color = filament.color_code;
        filamentSelect.appendChild(option);
      });

      filamentSelect.disabled = false;
      filamentContainer.classList.remove("hidden");

      if (data.filaments.length === 1) {
        filamentSelect.value = data.filaments[0].id;
        updateColorSwatch(filamentSelect);
        calculatePrice();
      }

      updateSubmitButtonState();
    } catch (error) {
      console.error("Error fetching filaments:", error);
      filamentSelect.innerHTML =
        '<option value="">Error loading filaments</option>';
      filamentSelect.disabled = true;
      updatePriceDisplay(null);
    }
  }

  /**
   * Updates the color swatch based on the selected filament.
   * Uses the shared updateColorSwatch function from order_item.js
   */
  function updateColorSwatch(select) {
    const colorSwatch = document.getElementById("color-swatch");
    const selectedOption = select.options[select.selectedIndex];
    if (selectedOption && selectedOption.dataset.color) {
      colorSwatch.style.backgroundColor = selectedOption.dataset.color;
    } else {
      colorSwatch.style.backgroundColor = "transparent";
    }

    if (selectedOption && selectedOption.value) {
      selectedFilamentInput.value = selectedOption.value;
    } else {
      selectedFilamentInput.value = "";
    }
    updateSubmitButtonState();
  }

  /**
   * Calculates the price based on current selections by making an API call.
   * Updates the UI with the calculated price or error message.
   * Uses the shared calculateItemPrice function from order_item.js
   */
  async function calculatePrice() {
    const modelId = modelSelect?.value;
    const filamentId = filamentSelect?.value;
    const infillValueRaw = infillSlider?.value;
    let infillValue;
    try {
      infillValue = new Decimal(infillValueRaw || "0");
    } catch (err) {
      updatePriceDisplay(null);
      return;
    }

    if (!modelId || !filamentId || infillValue.isZero()) {
      updatePriceDisplay(null);
      return;
    }

    updatePriceDisplay("loading");

    try {
      const data = await calculateItemPrice({
        modelId,
        filamentId,
        infill: infillValue.toString(),
        quantity: "1",
      });

      if (data.status === "success") {
        updatePriceDisplay(data.price);
        const inventoryIdInput = document.getElementById("inventory-id");
        if (inventoryIdInput && data.inventory_id) {
          inventoryIdInput.value = data.inventory_id;
        }
        if (priceError) {
          priceError.classList.add("hidden");
        }
      } else {
        const errorMsg = data.message || "Error calculating price";
        console.error("Error in response:", errorMsg);
        throw new Error(errorMsg);
      }
    } catch (error) {
      console.error("Error calculating price:", error);
      updatePriceDisplay(null);

      if (priceError) {
        priceError.textContent = error.message || "Error calculating price";
        priceError.classList.remove("hidden");
      }
    }
  }

  /**
   * Updates the submit button state based on form validity.
   */
  function updateSubmitButtonState() {
    const isFormValid =
      modelSelect.value &&
      materialSelect.value &&
      filamentSelect.value &&
      infillSlider.value;

    submitButton.disabled = !isFormValid;
  }

  const debouncedCalculatePrice = debounce(calculatePrice, 300);

  modelSelect.addEventListener("change", updateFormState);

  materialSelect.addEventListener("change", function () {
    const modelId = modelSelect.value;
    const materialId = this.value;
    updateFilaments(modelId, materialId);
  });

  filamentSelect.addEventListener("change", function () {
    updateColorSwatch(this);
    calculatePrice();
  });

  if (infillSlider) {
    infillSlider.addEventListener("input", function (e) {
      const value = e.target.value;
      if (infillValue) {
        infillValue.textContent = `${value}%`;
      }
      if (modelSelect?.value && filamentSelect?.value) {
        debouncedCalculatePrice();
      }
    });
  }

  updateFormState();
  const form = document.getElementById("premade-item-form");

  if (form) {
    if (!form.action) {
      const currentUrl = window.location.href;
      form.action = currentUrl;
    }

    form.addEventListener("submit", handleFormSubmit);
    const submitButton = document.querySelector("#submit-button");
    if (submitButton) {
      submitButton.addEventListener("click", function (event) {});
    }
  }
});

/**
 * Handles the form submission via AJAX.
 * Prepares form data, sends it to the server, and handles the response.
 */
async function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const submitButton = form.querySelector('button[type="submit"]');
  const buttonText = submitButton?.querySelector(".button-text");
  const loadingText = submitButton?.querySelector(".loading-text");
  const priceError = document.getElementById("price-error");
  const modelSelect = document.getElementById("model-select");
  const filamentSelect = document.getElementById("filament-select");
  const infillSlider = document.querySelector(".infill-range");

  if (priceError) {
    priceError.classList.add("hidden");
  }

  if (modelSelect?.value) {
    formData.set("Model", modelSelect.value);
  }

  if (filamentSelect?.value) {
    formData.set("InventoryChange", filamentSelect.value);
  }

  formData.set("ItemQuantity", "1");
  formData.set("IsCustom", "False");

  if (
    infillSlider?.value &&
    modelSelect?.selectedOptions[0]?.dataset?.baseInfill
  ) {
    const baseInfill = parseFloat(
      modelSelect.selectedOptions[0].dataset.baseInfill || "0.3"
    );
    const infillPercentage = parseFloat(infillSlider.value);
    const infillMultiplier = infillPercentage / (baseInfill * 100);
    formData.set("InfillMultiplier", infillMultiplier.toFixed(2));
  }

  if (submitButton) {
    submitButton.disabled = true;
    if (buttonText) buttonText.classList.add("hidden");
    if (loadingText) loadingText.classList.remove("hidden");
  }

  try {
    const response = await fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (response.redirected) {
      window.location.href = response.url;
      return;
    }

    const responseText = await response.text();
    const data = responseText ? JSON.parse(responseText) : {};
    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else if (data.success) {
      window.location.href =
        data.redirect || "{{ url 'product-admin-premade-items' }}";
    } else {
      showFormErrors(form, data.errors || {});
    }
  } catch (error) {
    const errorMessage =
      document.getElementById("error-message") || document.createElement("div");
    errorMessage.className = "text-red-500 text-sm mt-2";
    errorMessage.textContent = "An error occurred while saving the item.";
    if (!errorMessage.parentNode) {
      form.appendChild(errorMessage);
    }
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      if (buttonText) buttonText.classList.remove("hidden");
      if (loadingText) loadingText.classList.add("hidden");
    }
  }
}

/**
 * Display form errors
 */
function showFormErrors(form, errors) {
  const errorElements = form.querySelectorAll(".error-message");
  errorElements.forEach((el) => el.remove());
  for (const [field, messages] of Object.entries(errors)) {
    const input = form.querySelector(`[name="${field}"]`);
    if (input) {
      const errorDiv = document.createElement("div");
      errorDiv.className = "text-red-500 text-sm mt-1 error-message";
      errorDiv.textContent = Array.isArray(messages) ? messages[0] : messages;
      input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
  }
}
