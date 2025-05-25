/**
 * Premade Item Form JS
 * Handles the dynamic functionality for the admin premade item form
 * Uses shared functionality from order_item.js
 */

/**
 * Handle model selection change
 */
function handleModelChange(event) {
  const modelSelect = event.target;
  const modelId = modelSelect.value;
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");

  updateModelThumbnail();

  if (materialSelect) {
    materialSelect.value = "";
    materialSelect.disabled = !modelId;
  }

  if (filamentSelect) {
    filamentSelect.innerHTML =
      '<option value="">Select a material first</option>';
    filamentSelect.disabled = true;
  }

  updateInfillSlider(modelSelect);

  updateFormState(modelId);

  updatePriceDisplay(null);
}

/**
 * Update form state based on selected value
 */
function updateFormState(selectedValue) {
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );
  const infillSlider = document.querySelector(".infill-range");
  const priceError = document.getElementById("price-error");
  const submitButton = document.getElementById("submit-button");
  const formError = document.getElementById("form-error");

  updateModelThumbnail();

  if (selectedValue) {
    if (materialSelect) materialSelect.disabled = false;
    if (infillSlider) {
      infillSlider.disabled = false;
      updateInfillSlider(modelSelect);
    }

    if (filamentContainer && materialSelect?.value) {
      filamentContainer.classList.remove("hidden");
    }
    if (filamentSelect) filamentSelect.required = true;
    if (priceError) priceError.classList.add("hidden");

    if (submitButton) {
      const modelSelect = document.getElementById("model-select");
      const materialSelect = document.getElementById("material-select");
      const filamentSelect = document.getElementById("filament-select");

      const isFormValid =
        modelSelect?.value && materialSelect?.value && filamentSelect?.value;

      submitButton.disabled = !isFormValid;

      if (formError) {
        formError.style.display = isFormValid ? "none" : "block";
      }
    }

    if (modelSelect?.value && filamentSelect?.value) calculatePrice();
  } else {
    if (materialSelect) {
      materialSelect.disabled = true;
      materialSelect.value = "";
    }
    if (filamentSelect) {
      filamentSelect.disabled = true;
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentSelect.required = false;
    }
    if (filamentContainer) filamentContainer.classList.add("hidden");
    if (infillSlider) infillSlider.disabled = true;
    if (priceError) priceError.classList.add("hidden");
    if (submitButton) {
      submitButton.disabled = true;
      if (formError) formError.style.display = "block";
    }
    updatePriceDisplay(null);
  }
}

/**
 * Update the model thumbnail and hidden model ID input
 */
function updateModelThumbnail() {
  const modelSelect = document.getElementById("model-select");
  const modelIdInput = document.getElementById("model-id");
  const modelThumbnailContainer = document.getElementById(
    "model-thumbnail-container"
  );
  const modelThumbnail = document.getElementById("model-thumbnail");

  if (modelSelect && modelSelect.value) {
    const selectedOption = modelSelect.options[modelSelect.selectedIndex];
    if (selectedOption.dataset.thumbnail) {
      modelThumbnail.src = selectedOption.dataset.thumbnail;
      modelThumbnailContainer.classList.remove("hidden");
    }
    if (modelIdInput) {
      modelIdInput.value = modelSelect.value;
    }
  } else if (modelThumbnailContainer) {
    modelThumbnailContainer.classList.add("hidden");
  }
}

/**
 * Calculate the estimated price based on current selections
 * Uses the shared calculateItemPrice function from order_item.js
 */
async function calculatePrice() {
  try {
    const modelSelect = document.getElementById("model-select");
    const filamentSelect = document.getElementById("filament-select");
    const infillRange = document.querySelector(".infill-range");
    const priceError = document.getElementById("price-error");
    const modelId = modelSelect?.value;
    const filamentId = filamentSelect?.value;
    const infillValueRaw = infillRange?.value;
    const quantity = "1";

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
        quantity,
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
        throw new Error(errorMsg);
      }
    } catch (error) {
      updatePriceDisplay(null);

      if (priceError) {
        priceError.textContent = error.message || "Error calculating price";
        priceError.classList.remove("hidden");
      }
    }
  } catch (error) {
    updatePriceDisplay(null);
  }
}

/**
 * Debounced version of calculatePrice
 */
const debouncedCalculatePrice = debounce(calculatePrice, 300);
window.debouncedCalculatePrice = debouncedCalculatePrice;

/**
 * Handle material selection change
 * Fetches available filaments for the selected material and updates the UI
 */
async function handleMaterialChange(event) {
  try {
    const modelSelect = document.getElementById("model-select");
    const filamentSelect = document.getElementById("filament-select");
    const filamentContainer = document.getElementById(
      "filament-select-container"
    );

    const modelId = modelSelect?.value;
    const materialId = event.target.value;

    if (!modelId || !materialId) {
      if (filamentSelect) {
        filamentSelect.innerHTML =
          '<option value="">Select a material first</option>';
        filamentSelect.disabled = true;
      }
      if (filamentContainer) {
        filamentContainer.classList.add("hidden");
      }
      updateFormState(false);
      return;
    }

    if (filamentSelect) {
      filamentSelect.innerHTML = '<option value="">Loading colors...</option>';
      filamentSelect.disabled = true;
    }

    const data = await fetchFilaments(modelId, materialId);
    if (!filamentSelect) return;
    filamentSelect.innerHTML = '<option value="">Select a color</option>';
    if (
      data.status === "success" &&
      data.filaments &&
      data.filaments.length > 0
    ) {
      data.filaments.forEach((filament) => {
        const option = new Option(
          `${filament.color_code} - ${filament.name}`,
          filament.id,
          false,
          false
        );
        option.dataset.color = filament.color_code;
        filamentSelect.add(option);
      });
      filamentSelect.disabled = false;
      updateFormState(true);
      updateColorSwatch(filamentSelect);
      if (filamentContainer) {
        filamentContainer.classList.remove("hidden");
      }
      if (filamentSelect.value) {
        debouncedCalculatePrice();
      }
    } else {
      throw new Error(
        data.message || "No filaments available for the selected material"
      );
    }
  } catch (error) {
    const filamentSelect = document.getElementById("filament-select");
    if (filamentSelect) {
      filamentSelect.innerHTML =
        '<option value="">Error loading colors</option>';
      filamentSelect.disabled = false;
    }
    updateFormState(false);

    const priceError = document.getElementById("price-error");
    if (priceError) {
      priceError.textContent =
        error.message || "Error loading filament options";
      priceError.classList.remove("hidden");
    }
  }
}

/**
 * Update the visibility of the filament error message
 */
function updateFilamentErrorVisibility() {
  const errorMessage = document.getElementById("filament-error");
  const filamentSelect = document.getElementById("filament-select");
  if (!errorMessage) return;
  const hasSelection = filamentSelect && filamentSelect.value;
  if (hasSelection) {
    errorMessage.classList.add("hidden");
  } else {
    errorMessage.classList.remove("hidden");
  }
}

/**
 * Handle filament selection change
 */
function handleFilamentChange(event) {
  const selectedFilamentInput = document.getElementById("selected-filament");
  const filamentSelect = event.target;
  const modelSelect = document.getElementById("model-select");

  updateColorSwatch(filamentSelect);
  updateFilamentErrorVisibility();

  if (selectedFilamentInput && filamentSelect.value) {
    selectedFilamentInput.value = filamentSelect.value;
  }

  updateFormState(modelSelect?.value);
  debouncedCalculatePrice();
}

/**
 * Initialize the page when DOM is fully loaded
 */
function initializePage() {
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const infillSlider = document.querySelector(".infill-range");
  const form = document.getElementById("premade-item-form");

  if (!modelSelect || !materialSelect || !filamentSelect) {
    alert("Required elements not found");
    return;
  }

  updateFormState(modelSelect.value !== "" && filamentSelect.value !== "");

  const handleInfillChange = (e) => {
    updateInfillDisplay(e.target.value);
    if (modelSelect?.value && filamentSelect?.value) {
      debouncedCalculatePrice();
    }
  };

  try {
    if (modelSelect) {
      modelSelect.addEventListener("change", handleModelChange);
    }

    if (materialSelect) {
      materialSelect.addEventListener("change", handleMaterialChange);
    }

    if (filamentSelect) {
      filamentSelect.addEventListener("change", handleFilamentChange);
    }

    if (infillSlider) {
      infillSlider.addEventListener("input", handleInfillChange);
    }

    if (form) {
      if (!form.action) {
        const currentUrl = window.location.href;
        form.action = currentUrl;
      }
      form.addEventListener("submit", handleFormSubmit);
    }
  } catch (error) {
    alert("An error occurred while loading the page");
  }

  window._premadeItemEventHandlers = {
    modelSelect: { element: modelSelect, handler: handleModelChange },
    materialSelect: { element: materialSelect, handler: handleMaterialChange },
    filamentSelect: { element: filamentSelect, handler: handleFilamentChange },
    infillSlider: { element: infillSlider, handler: handleInfillChange },
  };

  if (modelSelect.value) {
    handleModelChange({ target: modelSelect });
  }

  if (materialSelect.value) {
    handleMaterialChange({ target: materialSelect });
  }

  if (modelSelect.value && filamentSelect.value) {
    debouncedCalculatePrice();
  }

  return () => {
    Object.values(window._premadeItemEventHandlers || {}).forEach(
      ({ element, handler }) => {
        if (element && handler) {
          element.removeEventListener("input", handler);
          element.removeEventListener("change", handler);
        }
      }
    );
    delete window._premadeItemEventHandlers;
  };
}

/**
 * Handle form submission via AJAX
 */
async function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const submitButton = form.querySelector('button[type="submit"]');
  const originalButtonText = submitButton?.textContent || "Create Premade Item";
  const existingError = form.querySelector(".form-error");
  if (existingError) {
    existingError.remove();
  }
  const priceElement = document.getElementById("price-value");
  if (priceElement && priceElement.textContent !== "--") {
    formData.append("calculated_price", priceElement.textContent);
  }

  const modelSelect = document.getElementById("model-select");
  const inventoryIdInput = document.getElementById("inventory-id");

  if (modelSelect?.value) {
    formData.set("Model", modelSelect.value);
  }

  if (inventoryIdInput?.value) {
    formData.set("InventoryChange", inventoryIdInput.value);
  }

  const infillSlider = document.querySelector(".infill-range");
  if (
    infillSlider?.value &&
    modelSelect?.selectedOptions[0]?.dataset?.baseInfill
  ) {
    const baseInfill = Decimal(
      modelSelect.selectedOptions[0].dataset.baseInfill || "0.3"
    );
    const infillPercentage = Decimal(infillSlider.value);
    const infillMultiplier = infillPercentage / (baseInfill * 100);
    formData.set("InfillMultiplier", infillMultiplier.toFixed(2));
  }

  formData.set("ItemQuantity", "1");
  formData.set("IsCustom", "False");

  if (submitButton?.disabled) {
    return;
  }

  try {
    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Creating Premade Item...";
    }

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

    const data = await response.json();

    if (data.status === "success" || data.success) {
      window.location.href = data.redirect_url || "/store/admin/premade-items/";
    } else {
      const errorDiv = document.createElement("div");
      errorDiv.className = "text-red-500 text-sm mt-2 form-error";
      errorDiv.textContent = data.message || "Error creating premade item";
      form.appendChild(errorDiv);
    }
  } catch (error) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "text-red-500 text-sm mt-2 form-error";
    errorDiv.textContent =
      error.message ||
      "An error occurred while creating the premade item. Please try again.";

    form.appendChild(errorDiv);
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = originalButtonText;
    }
  }
}

document.addEventListener("DOMContentLoaded", initializePage);
