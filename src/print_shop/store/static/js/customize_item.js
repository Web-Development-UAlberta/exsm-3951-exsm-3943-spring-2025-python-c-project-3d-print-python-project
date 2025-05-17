/**
 * Update form based on selected value.
 */
function updateFormState(selectedValue) {
  const submitButton = document.querySelector('button[type="submit"]');
  const errorMessage = document.getElementById("filament-error");

  if (selectedValue) {
    submitButton.disabled = false;
    if (errorMessage) errorMessage.classList.add("hidden");
  } else {
    submitButton.disabled = true;
    if (errorMessage) errorMessage.classList.remove("hidden");
  }
}

/**
 * Update the color swatch based on selected filament
 */
function updateColorSwatch(select) {
  const selectedOption = select.options[select.selectedIndex];
  const colorSwatch = document.getElementById("color-swatch");

  if (selectedOption && selectedOption.dataset.color) {
    colorSwatch.style.backgroundColor = selectedOption.dataset.color;
  } else {
    colorSwatch.style.backgroundColor = "transparent";
  }
}

/**
 * Fetch filaments for the selected material and update the UI
 * Use the custom API endpoint to get the filaments for the selected material
 * that have available inventory.
 */
async function handleMaterialChange(event) {
  const modelId = document.querySelector('input[name="Model"]')?.value;
  const materialId = event.target.value;
  const filamentSelect = document.getElementById("filament-select");
  const filamentContainer = document.getElementById(
    "filament-select-container"
  );

  if (!modelId || !filamentSelect) {
    console.error("Required elements not found");
    return;
  }
  filamentSelect.innerHTML = '<option value="">Loading colors...</option>';
  filamentSelect.disabled = true;
  updateFormState(false);

  if (!materialId) {
    filamentSelect.innerHTML =
      '<option value="">Select a material first</option>';
    updateColorSwatch(filamentSelect);
    return;
  }
  filamentContainer.classList.remove("hidden");
  try {
    const response = await fetch(
      `/store/api/model/${modelId}/material/${materialId}/filaments/`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
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
    } else {
      throw new Error(data.message || "No filaments available");
    }
  } catch (error) {
    console.error("Error loading filaments:", error);
    const errorMessage = error.message || "Error loading colors";
    filamentSelect.innerHTML = `<option value="" disabled>${errorMessage}</option>`;
    updateFormState(false);
  }
}
/**
 * Initialize event listeners and UI state
 */
document.addEventListener("DOMContentLoaded", () => {
  const materialSelect = document.getElementById("material-select");
  const filamentSelect = document.getElementById("filament-select");
  if (!materialSelect || !filamentSelect) {
    console.warn("Required select elements not found");
    return;
  }

  updateColorSwatch(filamentSelect);
  filamentSelect.addEventListener("change", (e) => {
    updateColorSwatch(e.target);
    updateFormState(!!e.target.value);
  });
  materialSelect.addEventListener("change", handleMaterialChange);
  if (materialSelect.value) {
    handleMaterialChange({ target: materialSelect });
  }
});
