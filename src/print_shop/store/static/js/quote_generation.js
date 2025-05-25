/**
 * Quote Generation JS
 * Handles the dynamic functionality for the admin quote generation form
 * Uses shared functionality from order_item.js
 */

/**
 * Update form based on selected value
 */
function updateFormState(selectedValue) {
  const customerSelect = document.querySelector("select[name='customer']");
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );
  const formError = document.getElementById("form-error");
  const priceError = document.getElementById("price-error");
  const generateQuoteBtn = document.getElementById("generate-quote-btn");

  if (selectedValue) {
    if (filamentContainer) {
      filamentContainer.classList.remove("hidden");
    }
    if (filamentSelect) {
      filamentSelect.required = true;
    }
    if (priceError) {
      priceError.classList.add("hidden");
    }
    if (generateQuoteBtn) {
      const isCustomerSelected = customerSelect && customerSelect.value;
      const isModelSelected = modelSelect && modelSelect.value;
      const isMaterialSelected = materialSelect && materialSelect.value;
      const isFilamentSelected = filamentSelect && filamentSelect.value;

      const isFormValid =
        isCustomerSelected &&
        isModelSelected &&
        isMaterialSelected &&
        isFilamentSelected;
      generateQuoteBtn.disabled = !isFormValid;

      if (formError) {
        formError.style.display = isFormValid ? "none" : "block";
      }
    }
  } else {
    if (filamentContainer) {
      filamentContainer.classList.add("hidden");
    }
    if (filamentSelect) {
      filamentSelect.required = false;
      filamentSelect.value = "";
    }
    if (priceError) {
      priceError.classList.add("hidden");
    }
    if (generateQuoteBtn) {
      generateQuoteBtn.disabled = true;

      if (formError) {
        formError.style.display = "block";
      }
    }
    updatePriceDisplay(null);
  }
}

/**
 * Calculate the estimated price based on current selections
 * Uses the shared calculateItemPrice function from order_item.js
 */
async function calculatePrice() {
  try {
    const modelIdInput = document.getElementById("model-id");
    const filamentSelect = document.getElementById("filament-select");
    const infillRange = document.getElementById("infill-percentage");
    const quantityInput = document.getElementById("ItemQuantity");
    const priceError = document.getElementById("price-error");
    const modelId = modelIdInput?.value;
    const filamentId = filamentSelect?.value;
    const infillValueRaw = infillRange?.value;
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
      !filamentId ||
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
        filamentId,
        infill: infillValue.toString(),
        quantity: quantityValue.toString(),
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

  updateColorSwatch(filamentSelect);
  updateFilamentErrorVisibility();

  if (selectedFilamentInput && filamentSelect.value) {
    selectedFilamentInput.value = filamentSelect.value;
  }

  debouncedCalculatePrice();

  const generateQuoteBtn = document.getElementById("generate-quote-btn");
  if (generateQuoteBtn) {
    const isValid = filamentSelect && filamentSelect.value;
    generateQuoteBtn.disabled = !isValid;
  }

  updateFormState(filamentSelect && filamentSelect.value ? true : false);
}

/**
 * Handle model selection change
 */
function handleModelChange(event) {
  const modelSelect = event.target;
  const modelIdInput = document.getElementById("model-id");
  const materialSelect = document.getElementById("material-select");
  const customizationSection = document.getElementById("customization-section");

  if (modelIdInput) {
    modelIdInput.value = modelSelect.value || "";
  }

  if (customizationSection) {
    customizationSection.style.display = modelSelect.value ? "block" : "none";
  }

  updateModelThumbnail(modelSelect);

  updateInfillSlider(modelSelect);

  if (materialSelect) {
    materialSelect.disabled = !modelSelect.value;
    if (materialSelect.value && modelSelect.value) {
      handleMaterialChange({ target: materialSelect });
    }
  }

  updateFormState();
}

/**
 * Handle customer selection change
 */
function handleCustomerChange(event) {
  const customerSelect = event.target;
  const customerIdInput = document.getElementById("customer-id");

  if (customerIdInput) {
    customerIdInput.value = customerSelect.value || "";
  }

  updateFormState();
}

/**
 * Update the model thumbnail based on selection
 */
function updateModelThumbnail(modelSelect) {
  if (!modelSelect) return;

  const modelThumbnailContainer = document.getElementById(
    "model-thumbnail-container"
  );
  const modelThumbnail = document.getElementById("model-thumbnail");
  if (!modelThumbnailContainer || !modelThumbnail) return;

  const selectedOption = modelSelect.options[modelSelect.selectedIndex];
  if (selectedOption && selectedOption.dataset.thumbnail) {
    modelThumbnail.src = selectedOption.dataset.thumbnail;
    modelThumbnailContainer.classList.remove("hidden");
  } else {
    modelThumbnailContainer.classList.add("hidden");
  }
}

/**
 * Initialize the page when DOM is fully loaded
 */
function initializePage() {
  const customerSelect = document.querySelector("select[name='customer']");
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const infillRange = document.getElementById("infill-percentage");
  const quantityInput = document.getElementById("ItemQuantity");
  const quoteForm = document.getElementById("quote-form");

  if (!modelSelect || !materialSelect || !filamentSelect) {
    alert("Required elements not found");
    return;
  }

  updateFormState(modelSelect.value !== "" && filamentSelect.value !== "");

  const handleQuantityChange = (e) => {
    if (modelSelect?.value && filamentSelect?.value) {
      debouncedCalculatePrice();
    }
  };

  if (infillRange) {
    updateInfillDisplay(infillRange.value);
  }

  try {
    if (customerSelect) {
      customerSelect.addEventListener("change", handleCustomerChange);
    }

    if (modelSelect) {
      modelSelect.addEventListener("change", handleModelChange);
    }

    if (materialSelect) {
      materialSelect.addEventListener("change", handleMaterialChange);
    }

    if (filamentSelect) {
      filamentSelect.addEventListener("change", handleFilamentChange);
    }

    if (infillRange) {
      infillRange.addEventListener("input", handleInfillChange);
    }

    if (quantityInput) {
      quantityInput.addEventListener("input", handleQuantityChange);
    }

    if (quoteForm) {
      quoteForm.addEventListener("submit", handleFormSubmit);
    }
  } catch (error) {
    alert("Error loading page");
  }

  window._quoteEventHandlers = {
    customerSelect: { element: customerSelect, handler: handleCustomerChange },
    modelSelect: { element: modelSelect, handler: handleModelChange },
    materialSelect: { element: materialSelect, handler: handleMaterialChange },
    filamentSelect: { element: filamentSelect, handler: handleFilamentChange },
    infillRange: { element: infillRange, handler: handleInfillChange },
    quantityInput: { element: quantityInput, handler: handleQuantityChange },
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
    Object.values(window._quoteEventHandlers || {}).forEach(
      ({ element, handler }) => {
        if (element && handler) {
          element.removeEventListener("input", handler);
          element.removeEventListener("change", handler);
        }
      }
    );
    delete window._quoteEventHandlers;
  };
}

/**
 * Handle form submission via AJAX
 */
async function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const generateQuoteBtn = document.getElementById("generate-quote-btn");
  const originalButtonText = generateQuoteBtn?.textContent || "Generate Quote";
  const existingError = form.querySelector(".form-error");
  if (existingError) {
    existingError.remove();
  }

  const priceElement = document.getElementById("price-value");
  if (priceElement && priceElement.textContent !== "--") {
    formData.append("calculated_price", priceElement.textContent);
  }

  if (generateQuoteBtn?.disabled) {
    return;
  }

  try {
    if (generateQuoteBtn) {
      generateQuoteBtn.disabled = true;
      generateQuoteBtn.textContent = "Generating Quote...";
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
    } else {
      const data = await response.json();

      if (data.status === "success") {
        window.location.href = data.redirect_url || "/quotes/";
      } else {
        const errorDiv = document.createElement("div");
        errorDiv.className = "text-red-500 text-sm mt-2 form-error";
        errorDiv.textContent = data.message || "Error generating quote";

        form.appendChild(errorDiv);
      }
    }
  } catch (error) {
    const errorDiv = document.createElement("div");
    errorDiv.className = "text-red-500 text-sm mt-2 form-error";
    errorDiv.textContent =
      error.message ||
      "An error occurred while generating the quote. Please try again.";

    form.appendChild(errorDiv);
  } finally {
    if (generateQuoteBtn) {
      generateQuoteBtn.disabled = false;
      generateQuoteBtn.textContent = originalButtonText;
    }
  }
}

document.addEventListener("DOMContentLoaded", initializePage);
