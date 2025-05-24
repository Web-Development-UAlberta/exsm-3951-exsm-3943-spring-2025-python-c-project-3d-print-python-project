/**
 * Quote Generation JS
 * Handles the dynamic functionality for the admin quote generation form
 * Uses shared functionality from order_item.js
 */

document.addEventListener("DOMContentLoaded", function () {
  const quoteForm = document.getElementById("quote-form");
  const customerSelect = document.querySelector("select[name='customer']");
  const customerIdInput = document.getElementById("customer-id");
  const modelSelect = document.getElementById("model-select");
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );
  const infillRange = document.getElementById("infill-percentage");
  const infillValue = document.getElementById("infill-value");
  const quantityInput = document.getElementById("ItemQuantity");
  const colorSwatch = document.getElementById("color-swatch");
  const generateQuoteBtn = document.getElementById("generate-quote-btn");
  const formError = document.getElementById("form-error");
  const modelIdInput = document.getElementById("model-id");
  const selectedFilamentInput = document.getElementById("selected-filament");
  const customizationSection = document.getElementById("customization-section");
  const modelThumbnailContainer = document.getElementById(
    "model-thumbnail-container"
  );
  const modelThumbnail = document.getElementById("model-thumbnail");

  function updateFormState() {
    const isCustomerSelected = customerSelect && customerSelect.value;
    const isModelSelected = modelSelect && modelSelect.value;

    if (customizationSection) {
      if (isModelSelected) {
        customizationSection.style.display = "block";
        modelIdInput.value = modelSelect.value;
      } else {
        customizationSection.style.display = "none";
        modelIdInput.value = "";
      }
    }

    if (materialSelect) {
      materialSelect.disabled = !isModelSelected;
      if (!isModelSelected) {
        materialSelect.value = "";
        updateFilaments("", "");
      }
    }

    updateSubmitButtonState();
  }

  function updateSubmitButtonState() {
    const isCustomerSelected = customerSelect && customerSelect.value;
    const isModelSelected = modelSelect && modelSelect.value;
    const isMaterialSelected = materialSelect && materialSelect.value;
    const isFilamentSelected = filamentSelect && filamentSelect.value;

    console.log(
      "Customer selected:",
      isCustomerSelected,
      customerSelect ? customerSelect.value : "No customer select"
    );
    console.log("Model selected:", isModelSelected);
    console.log("Material selected:", isMaterialSelected);
    console.log("Filament selected:", isFilamentSelected);

    if (generateQuoteBtn) {
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
  }

  function handleModelChange() {
    if (modelSelect.value) {
      modelIdInput.value = modelSelect.value;
      customizationSection.style.display = "block";
      materialSelect.disabled = false;

      const selectedOption = modelSelect.options[modelSelect.selectedIndex];
      const baseInfill =
        parseInt(selectedOption.dataset.baseInfill * 100) || 30;

      if (
        selectedOption.dataset.thumbnail &&
        modelThumbnail &&
        modelThumbnailContainer
      ) {
        modelThumbnail.src = selectedOption.dataset.thumbnail;
        modelThumbnailContainer.classList.remove("hidden");
      }

      if (infillRange) {
        infillRange.value = baseInfill;
        updateInfillDisplay(baseInfill);
      }

      if (materialSelect.value) {
        updateFilaments(modelSelect.value, materialSelect.value);
      }
    } else {
      customizationSection.style.display = "none";
      modelIdInput.value = "";
      materialSelect.disabled = true;
      materialSelect.value = "";
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentSelect.disabled = true;
      filamentContainer.classList.add("hidden");

      if (modelThumbnailContainer) {
        modelThumbnailContainer.classList.add("hidden");
      }

      updatePriceDisplay(null);
    }

    updateSubmitButtonState();
  }

  function handleMaterialChange() {
    if (modelSelect.value && materialSelect.value) {
      updateFilaments(modelSelect.value, materialSelect.value);
    } else {
      filamentSelect.innerHTML =
        '<option value="">Select a material first</option>';
      filamentSelect.disabled = true;
      filamentContainer.classList.add("hidden");
      updatePriceDisplay(null);
    }

    updateSubmitButtonState();
  }

  async function updateFilaments(modelId, materialId) {
    if (!modelId || !materialId) {
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
        handleFilamentChange();
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

  function handleFilamentChange() {
    updateColorSwatch(filamentSelect);
    selectedFilamentInput.value = filamentSelect.value;
    calculatePrice();
    updateSubmitButtonState();
  }

  async function calculatePrice() {
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

        const priceError = document.getElementById("price-error");
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

      const priceError = document.getElementById("price-error");
      if (priceError) {
        priceError.textContent = error.message || "Error calculating price";
        priceError.classList.remove("hidden");
      }
    }
  }

  async function handleFormSubmit(event) {
    event.preventDefault();

    if (generateQuoteBtn.disabled) {
      return;
    }

    const form = event.target;
    const formData = new FormData(form);
    const originalButtonText = generateQuoteBtn.innerHTML;

    try {
      generateQuoteBtn.disabled = true;
      generateQuoteBtn.innerHTML =
        '<span class="button-text">Generating Quote...</span>';

      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await response.json();

      if (data.success) {
        if (data.redirect_url) {
          window.location.href = data.redirect_url;
        } else {
          const successMessage = document.createElement("div");
          successMessage.className =
            "bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4";
          successMessage.innerHTML = `<p>${data.message}</p>`;
          form.prepend(successMessage);
          form.reset();
          updateFormState();
        }
      } else {
        const errorMessage = document.createElement("div");
        errorMessage.className =
          "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4";
        errorMessage.innerHTML = `<p>${data.message}</p>`;
        form.prepend(errorMessage);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      const errorMessage = document.createElement("div");
      errorMessage.className =
        "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4";
      errorMessage.innerHTML = `<p>An error occurred while generating the quote. Please try again.</p>`;
      form.prepend(errorMessage);
    } finally {
      generateQuoteBtn.disabled = false;
      generateQuoteBtn.innerHTML = originalButtonText;
    }
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
    infillRange.addEventListener("input", function (e) {
      const value = e.target.value;
      if (infillValue) {
        infillValue.textContent = `${value}%`;
      }
      if (modelIdInput?.value && filamentSelect?.value) {
        debouncedCalculatePrice();
      }
    });
  }

  if (quantityInput) {
    quantityInput.addEventListener("input", function () {
      if (modelIdInput?.value && filamentSelect?.value) {
        debouncedCalculatePrice();
      }
    });
  }

  function handleCustomerChange() {
    if (customerSelect && customerIdInput) {
      customerIdInput.value = customerSelect.value;
    }
    updateSubmitButtonState();
  }

  if (customerSelect) {
    customerSelect.addEventListener("change", handleCustomerChange);
  }

  if (quoteForm) {
    quoteForm.addEventListener("submit", handleFormSubmit);
  }

  const debouncedCalculatePrice = debounce(calculatePrice, 300);

  updateFormState();
});
