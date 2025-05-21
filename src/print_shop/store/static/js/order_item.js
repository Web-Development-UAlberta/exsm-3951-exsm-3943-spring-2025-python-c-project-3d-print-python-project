/**
 * Shared utility functions for 3D print shop order items
 * Used by all order item forms
 */

/**
 * Debounce function that delays invoking func until after wait milliseconds
 * have elapsed since the last time the debounced function was invoked.
 */
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Updates the price display based on the provided price
 */
function updatePriceDisplay(price) {
  const priceValue = document.getElementById("price-value");
  const priceEstimate = document.getElementById("price-estimate");
  const priceError = document.getElementById("price-error");

  if (!priceValue || !priceEstimate) {
    console.error("Required price display elements not found");
    return;
  }

  if (price === null || price === undefined) {
    priceValue.textContent = "--";
    priceEstimate.classList.remove("text-green-600", "font-bold");
    if (priceError) priceError.classList.add("hidden");
    return;
  }

  if (price === "loading") {
    priceValue.textContent = "...";
    priceEstimate.classList.remove("text-green-600", "font-bold");
    return;
  }

  priceEstimate.style.opacity = "0";
  setTimeout(() => {
    priceValue.textContent = price;
    priceEstimate.classList.add("text-green-600", "font-bold");
    priceEstimate.style.opacity = "1";
  }, 150);
}

/**
 * Updates the color swatch based on the selected filament
 */
function updateColorSwatch(select) {
  const colorSwatch = document.getElementById("color-swatch");
  if (!colorSwatch) return;

  const selectedOption = select.options[select.selectedIndex];
  if (selectedOption && selectedOption.dataset.color) {
    colorSwatch.style.backgroundColor = selectedOption.dataset.color;
  } else {
    colorSwatch.style.backgroundColor = "transparent";
  }
}

/**
 * Updates the infill display with the current value
 */
function updateInfillDisplay(value) {
  const infillValue = document.getElementById("infill-value");
  if (infillValue) {
    infillValue.textContent = `${value}%`;
  }
}

/**
 * Handles infill slider changes
 */
function handleInfillChange(e) {
  const value = e.target.value;
  updateInfillDisplay(value);

  if (typeof debouncedCalculatePrice === "function") {
    debouncedCalculatePrice();
  }
}

/**
 * Fetches filaments for a given model and material
 * from the custom API endpoint
 */
async function fetchFilaments(modelId, materialId) {
  if (!modelId || !materialId) {
    throw new Error("Model ID and Material ID are required");
  }

  const url = `/store/api/model/${modelId}/material/${materialId}/filaments/`;
  const response = await fetch(url, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch filaments");
  }

  return await response.json();
}

/**
 * Calculates the price for a given configuration
 * from the custom API endpoint
 */
async function calculateItemPrice(config) {
  const { modelId, filamentId, infill, quantity = 1 } = config;

  if (!modelId || !filamentId || !infill) {
    throw new Error("Model ID, Filament ID, and Infill are required");
  }

  const params = new URLSearchParams({
    infill: infill.toString(),
    quantity: quantity.toString(),
  });

  const url = `/store/api/model/${modelId}/filament/${filamentId}/calculate-price/?${params}`;
  const response = await fetch(url, {
    headers: {
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "same-origin",
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorData = {};
    try {
      errorData = JSON.parse(errorText);
    } catch (e) {
      console.error("Failed to parse error response as JSON");
    }
    const errorMessage =
      errorData.message || `HTTP error! status: ${response.status}`;
    throw new Error(errorMessage);
  }

  const responseText = await response.text();
  try {
    return JSON.parse(responseText);
  } catch (e) {
    throw new Error("Invalid response from server");
  }
}
