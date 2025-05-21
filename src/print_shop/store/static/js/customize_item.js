/**
 * Update form based on selected value.
 */
function updateFormState(selectedValue) {
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );
  const filamentSelect = document.getElementById("filament-select");
  const errorMessage = document.getElementById("filament-error");
  const addToCartButton = document.querySelector('button[type="submit"]');

  if (selectedValue) {
    if (filamentContainer) {
      filamentContainer.classList.remove("hidden");
    }
    if (filamentSelect) {
      filamentSelect.required = true;
    }
    if (errorMessage) {
      errorMessage.classList.add("hidden");
    }
    if (addToCartButton) {
      addToCartButton.disabled = !filamentSelect || !filamentSelect.value;
    }
  } else {
    if (filamentContainer) {
      filamentContainer.classList.add("hidden");
    }
    if (filamentSelect) {
      filamentSelect.required = false;
      filamentSelect.value = "";
    }
    if (errorMessage) {
      errorMessage.classList.remove("hidden");
    }
    if (addToCartButton) {
      addToCartButton.disabled = true;
    }
    updatePriceDisplay(null);
  }
  updateFilamentErrorVisibility();
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
 * Update the price display with smooth transitions
 */
function updatePriceDisplay(price) {
  const priceElement = document.getElementById("price-value");
  const priceContainer = document.getElementById("price-estimate");
  const errorMessage = document.getElementById("price-error");

  if (!priceElement || !priceContainer) return;
  priceContainer.style.opacity = "0.5";
  priceContainer.style.transition = "opacity 150ms ease-in-out";
  if (errorMessage) {
    errorMessage.classList.add("hidden");
  }
  setTimeout(() => {
    if (price === null) {
      priceElement.textContent = "--";
      priceContainer.classList.remove("text-green-600", "font-bold");
    } else if (price === "loading") {
      priceElement.textContent = "Calculating...";
      priceContainer.classList.remove("text-green-600", "font-bold");
    } else {
      try {
        const formattedPrice = new Decimal(price).toFixed(2);
        priceElement.textContent = formattedPrice;
        priceContainer.classList.add("text-green-600", "font-bold");
      } catch (err) {
        priceElement.textContent = price;
        priceContainer.classList.remove("text-green-600", "font-bold");
      }
    }
    priceContainer.style.opacity = "1";
  }, 150);
}

/**
 * Calculate the estimated price based on current selections
 * Uses the shared calculateItemPrice function from order_item.js
 */
async function calculatePrice() {
  try {
    let modelId = document.querySelector('input[name="Model"]')?.value;
    if (!modelId) {
      modelId = document.getElementById("model-id")?.value;
    }

    const filamentSelect = document.getElementById("filament-select");
    const infillInput = document.querySelector(".infill-range");
    const quantityInput = document.querySelector(".quantity-input");
    const errorMessage = document.getElementById("price-error");
    const infillValueRaw = infillInput?.value;
    const quantityValueRaw = quantityInput?.value;
    let infillValue, quantityValue;
    try {
      infillValue = new Decimal(infillValueRaw || "0");
      quantityValue = new Decimal(quantityValueRaw || "1");
    } catch (err) {
      updatePriceDisplay(null);
      return;
    }

    if (
      !modelId ||
      !filamentSelect?.value ||
      infillValue.isZero() ||
      quantityValue.isZero()
    ) {
      updatePriceDisplay(null);
      return;
    }

    updatePriceDisplay("loading");

    try {
      const data = await calculateItemPrice({
        modelId,
        filamentId: filamentSelect.value,
        infill: infillValue.toString(),
        quantity: quantityValue.toString(),
      });

      if (data.status === "success") {
        updatePriceDisplay(data.price);
        const inventoryIdInput = document.getElementById("inventory-id");
        if (inventoryIdInput && data.inventory_id) {
          inventoryIdInput.value = data.inventory_id;
        }
        if (errorMessage) {
          errorMessage.classList.add("hidden");
        }
      } else {
        const errorMsg = data.message || "Error calculating price";
        console.error("Error in response:", errorMsg);
        throw new Error(errorMsg);
      }
    } catch (error) {
      console.error("Error calculating price:", error);
      updatePriceDisplay(null);

      if (errorMessage) {
        errorMessage.textContent = error.message || "Error calculating price";
        errorMessage.classList.remove("hidden");
      }
    }
  } catch (error) {
    console.error("Error in calculatePrice:", error);
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
    const modelId = document.querySelector('input[name="Model"]')?.value;
    const materialId = event.target.value;
    const filamentSelect = document.getElementById("filament-select");

    if (!modelId || !materialId) {
      updateFormState(false);
      return;
    }

    if (filamentSelect) {
      filamentSelect.innerHTML = '<option value="">Loading colors...</option>';
      filamentSelect.disabled = true;
    }
    const response = await fetch(
      `/store/api/model/${modelId}/material/${materialId}/filaments/`
    );
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `HTTP error! status: ${response.status}`
      );
    }
    const data = await response.json();
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
      if (filamentSelect.value) {
        debouncedCalculatePrice();
      }
    } else {
      throw new Error(
        data.message || "No filaments available for the selected material"
      );
    }
  } catch (error) {
    console.error("Error in handleMaterialChange:", error);
    const filamentSelect = document.getElementById("filament-select");
    if (filamentSelect) {
      filamentSelect.innerHTML =
        '<option value="">Error loading colors</option>';
      filamentSelect.disabled = false;
    }
    updateFormState(false);

    const errorMessage = document.getElementById("price-error");
    if (errorMessage) {
      errorMessage.textContent =
        error.message || "Error loading material options";
      errorMessage.classList.remove("hidden");
    }
  }
}

/**
 * Initialize the page when DOM is fully loaded
 */
function initializePage() {
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const infillRange = document.querySelector(".infill-range");
  const infillValue = document.getElementById("infill-value");
  const quantityInput = document.querySelector(".quantity-input");
  const form = document.querySelector("form");

  if (!materialSelect || !filamentSelect) {
    console.error(
      "Required elements (materialSelect or filamentSelect) not found"
    );
    return;
  }

  updateFormState(materialSelect.value !== "");

  const handleFilamentChange = (e) => {
    updateColorSwatch(e.target);
    updateFilamentErrorVisibility();
    debouncedCalculatePrice();

    const addToCartButton = document.querySelector('button[type="submit"]');
    if (addToCartButton) {
      addToCartButton.disabled = !e.target.value;
    }
  };

  const handleQuantityChange = (e) => {
    debouncedCalculatePrice();
  };

  if (infillRange) {
    updateInfillDisplay(infillRange.value);
  }

  try {
    if (materialSelect) {
      materialSelect.addEventListener("change", handleMaterialChange);
    }

    if (filamentSelect) {
      filamentSelect.addEventListener("change", handleFilamentChange);
    }

    if (infillRange) {
      infillRange.addEventListener("input", (e) => {
        updateInfillDisplay(e.target.value);
        debouncedCalculatePrice();
      });
    }

    if (quantityInput) {
      quantityInput.addEventListener("input", handleQuantityChange);
    }

    if (form) {
      form.addEventListener("submit", handleFormSubmit);
    }
  } catch (error) {
    console.error("Error adding event listeners:", error);
  }

  window._eventHandlers = {
    materialSelect: { element: materialSelect, handler: handleMaterialChange },
    filamentSelect: { element: filamentSelect, handler: handleFilamentChange },
    infillRange: { element: infillRange, handler: handleInfillChange },
    quantityInput: { element: quantityInput, handler: handleQuantityChange },
  };

  if (materialSelect.value) {
    handleMaterialChange({ target: materialSelect });
  }

  if (materialSelect.value && filamentSelect.value) {
    debouncedCalculatePrice();
  }

  return () => {
    Object.values(window._eventHandlers || {}).forEach(
      ({ element, handler }) => {
        if (element && handler) {
          element.removeEventListener("input", handler);
          element.removeEventListener("change", handler);
        }
      }
    );
    delete window._eventHandlers;
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
  const originalButtonText = submitButton.textContent;

  const priceElement = document.getElementById("price-value");
  if (priceElement && priceElement.textContent !== "--") {
    formData.append("calculated_price", priceElement.textContent);
  }

  try {
    submitButton.disabled = true;
    submitButton.textContent = "Adding to Cart...";

    const response = await fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    if (response.redirected) {
      window.location.href = response.url;
    } else {
      const data = await response.json();
      if (data.success) {
        window.location.href = data.redirect_url || "/cart/";
      } else {
        const errorDiv = document.createElement("div");
        errorDiv.className = "text-red-500 text-sm mt-2";
        errorDiv.textContent = data.message || "Error adding item to cart";
        const existingError = form.querySelector(".form-error");
        if (existingError) {
          existingError.remove();
        }

        form.appendChild(errorDiv);
      }
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while adding the item to your cart.");
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = originalButtonText;
  }
}

document.addEventListener("DOMContentLoaded", initializePage);
