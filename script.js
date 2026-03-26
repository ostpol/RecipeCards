const STORAGE_KEY = "recipe-card-current";
const LANGUAGE_KEY = "recipe-card-language";

const translations = {
  en: {
    appEyebrow: "DIN A6 Recipe Cards",
    appTitle: "Beautiful, fixed-layout recipe cards",
    appIntro: "Edit once, print reliably in landscape A6, and move recipes around with JSON import/export.",
    languageLabel: "Language",
    printButton: "Print card",
    newButton: "New recipe",
    exportButton: "Export JSON",
    importButton: "Import JSON",
    outputTitle: "Print and export",
    storageStatusReady: "",
    storageStatusRecovered: "Saving works again.",
    storageErrorQuota: "Could not save this recipe in the browser. The embedded image is probably too large. Try a smaller image or remove it, then export JSON to keep the recipe.",
    storageErrorGeneric: "Could not save this recipe in the browser. Your latest changes are still shown, but they may be lost after a refresh.",
    duplexHint: "Tip: choose duplex printing with <strong>flip on short edge</strong> for correct front/back alignment.",
    debugBorder: "Print debug border",
    printSettingsTitle: "Print Settings",
    printSettingsSummary: "Show print settings",
    printStep1: "Open the browser print dialog with <strong>Print card</strong>.",
    printStep2: "Set <strong>Paper size</strong> to <strong>A6</strong>.",
    printStep3: "Set <strong>Orientation</strong> to <strong>Landscape</strong>.",
    printStep4: "Set <strong>Scale</strong> to <strong>100%</strong> or <strong>Default</strong>, not \"Fit to page\".",
    printStep5: "Set <strong>Margins</strong> to <strong>None</strong> or <strong>Default</strong>.",
    printStep6: "Turn <strong>Headers and footers</strong> off.",
    printStep7: "For double-sided printing, use <strong>Duplex</strong> with <strong>flip on short edge</strong>.",
    printHint: "If the print is too large, the paper size is usually still set to A4 or Letter in the print dialog or printer driver.",
    frontSide: "Front side",
    titleLabel: "Title",
    titlePlaceholder: "Lemon Ricotta Pasta",
    subtitleLabel: "Subtitle",
    subtitlePlaceholder: "Bright, creamy, and ready in 20 minutes",
    coverImageLabel: "Cover image",
    removeImage: "Remove image",
    imageStatusEmpty: "No image selected",
    imageStatusEmbedded: "Embedded in recipe JSON",
    backSide: "Back side",
    layoutTitle: "Card layout",
    showCoverImage: "Show cover image",
    showSubtitle: "Show subtitle",
    showBackHeader: "Show back title",
    showMetaStrip: "Show recipe info strip",
    showPrepTime: "Show prep time",
    showCookTime: "Show cook time",
    showServings: "Show servings",
    showDifficulty: "Show difficulty",
    showIngredients: "Show ingredients",
    showInstructions: "Show instructions",
    showNotes: "Show notes",
    prepTimeLabel: "Prep time",
    prepTimePlaceholder: "15 min",
    cookTimeLabel: "Cook time",
    cookTimePlaceholder: "10 min",
    servingsLabel: "Servings",
    servingsPlaceholder: "2",
    difficultyLabel: "Difficulty",
    difficultyPlaceholder: "Easy",
    ingredientsLabel: "Ingredients",
    ingredientsPlaceholder: "250 g pasta\n200 g ricotta\n1 lemon\nParmesan",
    instructionsLabel: "Instructions",
    instructionsPlaceholder: "Cook pasta until al dente.\nMix ricotta with lemon zest and juice.\nToss with pasta and a splash of pasta water.",
    notesLabel: "Notes",
    notesPlaceholder: "Add spinach at the end for extra color.",
    previewEyebrow: "Live preview",
    previewTitle: "Landscape A6, fixed on every print",
    cardKicker: "Recipe Card",
    detailsKicker: "Recipe Details",
    metaPrep: "Prep",
    metaCook: "Cook",
    metaServes: "Serves",
    metaLevel: "Level",
    defaultSubtitle: "A beautiful recipe card ready for print",
    fallbackIngredients: "Add ingredients on the left",
    fallbackInstructions: "Add instructions on the left",
    fallbackNotes: "No notes",
    importError: "The JSON file could not be imported. Please check the file format."
  },
  de: {
    appEyebrow: "DIN A6 Rezeptkarten",
    appTitle: "Schöne Rezeptkarten mit festem Layout",
    appIntro: "Einmal bearbeiten, zuverlässig im DIN-A6-Querformat drucken und Rezepte per JSON importieren oder exportieren.",
    languageLabel: "Sprache",
    printButton: "Karte drucken",
    newButton: "Neues Rezept",
    exportButton: "JSON exportieren",
    importButton: "JSON importieren",
    outputTitle: "Drucken und exportieren",
    storageStatusReady: "",
    storageStatusRecovered: "Speichern funktioniert wieder.",
    storageErrorQuota: "Dieses Rezept konnte nicht im Browser gespeichert werden. Das eingebettete Bild ist wahrscheinlich zu gro\u00df. Verwende ein kleineres Bild oder entferne es und exportiere das Rezept anschlie\u00dfend als JSON.",
    storageErrorGeneric: "Dieses Rezept konnte nicht im Browser gespeichert werden. Die letzten \u00c4nderungen werden noch angezeigt, gehen nach einem Neuladen aber m\u00f6glicherweise verloren.",
    duplexHint: "Tipp: für den beidseitigen Druck <strong>an kurzer Kante wenden</strong> wählen, damit Vorder- und Rückseite richtig ausgerichtet sind.",
    debugBorder: "Druckrahmen zur Fehlersuche",
    printSettingsTitle: "Druckeinstellungen",
    printSettingsSummary: "Druckeinstellungen anzeigen",
    printStep1: "Öffne den Browser-Druckdialog mit <strong>Karte drucken</strong>.",
    printStep2: "Stelle <strong>Papierformat</strong> auf <strong>A6</strong>.",
    printStep3: "Stelle <strong>Ausrichtung</strong> auf <strong>Querformat</strong>.",
    printStep4: "Stelle <strong>Skalierung</strong> auf <strong>100 %</strong> oder <strong>Standard</strong>, nicht auf \"An Seite anpassen\".",
    printStep5: "Stelle <strong>Ränder</strong> auf <strong>Keine</strong> oder <strong>Standard</strong>.",
    printStep6: "Schalte <strong>Kopf- und Fußzeilen</strong> aus.",
    printStep7: "Für den beidseitigen Druck <strong>Duplex</strong> mit <strong>an kurzer Kante wenden</strong> verwenden.",
    printHint: "Wenn der Ausdruck zu groß ist, ist im Druckdialog oder Druckertreiber meist noch A4 oder Letter eingestellt.",
    frontSide: "Vorderseite",
    titleLabel: "Titel",
    titlePlaceholder: "Zitronen-Ricotta-Pasta",
    subtitleLabel: "Untertitel",
    subtitlePlaceholder: "Frisch, cremig und in 20 Minuten fertig",
    coverImageLabel: "Titelbild",
    removeImage: "Bild entfernen",
    imageStatusEmpty: "Kein Bild ausgewählt",
    imageStatusEmbedded: "Im Rezept-JSON eingebettet",
    backSide: "Rückseite",
    layoutTitle: "Kartenlayout",
    showCoverImage: "Titelbild anzeigen",
    showSubtitle: "Untertitel anzeigen",
    showBackHeader: "Rücktitel anzeigen",
    showMetaStrip: "Infoleiste anzeigen",
    showPrepTime: "Vorbereitung anzeigen",
    showCookTime: "Kochzeit anzeigen",
    showServings: "Portionen anzeigen",
    showDifficulty: "Schwierigkeit anzeigen",
    showIngredients: "Zutaten anzeigen",
    showInstructions: "Zubereitung anzeigen",
    showNotes: "Notizen anzeigen",
    prepTimeLabel: "Vorbereitung",
    prepTimePlaceholder: "15 Min.",
    cookTimeLabel: "Kochzeit",
    cookTimePlaceholder: "10 Min.",
    servingsLabel: "Portionen",
    servingsPlaceholder: "2",
    difficultyLabel: "Schwierigkeit",
    difficultyPlaceholder: "Einfach",
    ingredientsLabel: "Zutaten",
    ingredientsPlaceholder: "250 g Pasta\n200 g Ricotta\n1 Zitrone\nParmesan",
    instructionsLabel: "Zubereitung",
    instructionsPlaceholder: "Pasta al dente kochen.\nRicotta mit Zitronenschale und Saft verrühren.\nMit etwas Pastawasser unter die Pasta heben.",
    notesLabel: "Notizen",
    notesPlaceholder: "Am Ende Spinat für mehr Farbe unterheben.",
    previewEyebrow: "Live-Vorschau",
    previewTitle: "DIN A6 quer, bei jedem Druck fest",
    cardKicker: "Rezeptkarte",
    detailsKicker: "Rezeptdetails",
    metaPrep: "Vorb.",
    metaCook: "Kochen",
    metaServes: "Port.",
    metaLevel: "Niveau",
    defaultSubtitle: "Eine schöne Rezeptkarte, bereit für den Druck",
    fallbackIngredients: "Links Zutaten eintragen",
    fallbackInstructions: "Links Zubereitung eintragen",
    fallbackNotes: "Keine Notizen",
    importError: "Die JSON-Datei konnte nicht importiert werden. Bitte prüfe das Dateiformat."
  }
};

const defaultRecipe = {
  title: "Lemon Ricotta Pasta",
  subtitle: "Bright, creamy, and ready in 20 minutes",
  prepTime: "15 min",
  cookTime: "10 min",
  servings: "2",
  difficulty: "Easy",
  ingredients: [
    "250 g pasta",
    "200 g ricotta",
    "1 lemon",
    "40 g parmesan",
    "Black pepper"
  ],
  instructions: [
    "Cook the pasta until al dente.",
    "Mix ricotta with lemon zest, juice, and parmesan.",
    "Toss with pasta and a splash of pasta water.",
    "Finish with black pepper and extra parmesan."
  ],
  notes: "Add spinach or peas in the last minute for a greener version.",
  image: "",
  visibility: {
    showCoverImage: true,
    showSubtitle: true,
    showBackHeader: true,
    showMetaStrip: true,
    showPrepTime: true,
    showCookTime: true,
    showServings: true,
    showDifficulty: true,
    showIngredients: true,
    showInstructions: true,
    showNotes: true
  }
};

const form = document.querySelector("#recipe-form");
const titleInput = document.querySelector("#title");
const subtitleInput = document.querySelector("#subtitle");
const prepTimeInput = document.querySelector("#prepTime");
const cookTimeInput = document.querySelector("#cookTime");
const servingsInput = document.querySelector("#servings");
const difficultyInput = document.querySelector("#difficulty");
const ingredientsInput = document.querySelector("#ingredients");
const instructionsInput = document.querySelector("#instructions");
const notesInput = document.querySelector("#notes");
const imageUploadInput = document.querySelector("#image-upload");
const importInput = document.querySelector("#import-input");
const printButton = document.querySelector("#print-button");
const exportButton = document.querySelector("#export-button");
const newButton = document.querySelector("#new-button");
const debugPrintInput = document.querySelector("#debug-print");
const languageButtons = Array.from(document.querySelectorAll("[data-language]"));
const removeImageButton = document.querySelector("#remove-image-button");
const visibilityInputs = Array.from(document.querySelectorAll("[data-visibility-key]"));
const imageStatus = document.querySelector("#image-status");
const storageStatus = document.querySelector("#storage-status");
const previewImage = document.querySelector("#preview-image");
const imageFallback = document.querySelector("#image-fallback");
const frontOverlay = document.querySelector("#front-overlay");
const frontCard = document.querySelector(".recipe-card-front");
const backHeader = document.querySelector("#back-header");
const metaStrip = document.querySelector("#meta-strip");
const metaPrep = document.querySelector("#meta-prep");
const metaCook = document.querySelector("#meta-cook");
const metaServings = document.querySelector("#meta-servings");
const metaDifficulty = document.querySelector("#meta-difficulty");
const backColumns = document.querySelector("#back-columns");
const ingredientsBlock = document.querySelector("#ingredients-block");
const previewIngredients = document.querySelector("#preview-ingredients");
const instructionsBlock = document.querySelector("#instructions-block");
const notesBlock = document.querySelector("#notes-block");
const listItemTemplate = document.querySelector("#list-item-template");

let recipe = loadRecipe();
let currentLanguage = loadLanguage();
let storageState = "ready";

function loadLanguage() {
  const stored = localStorage.getItem(LANGUAGE_KEY);
  return stored && translations[stored] ? stored : "en";
}

function loadRecipe() {
  const stored = localStorage.getItem(STORAGE_KEY);

  if (!stored) {
    return structuredClone(defaultRecipe);
  }

  try {
    return normalizeRecipe(JSON.parse(stored));
  } catch (error) {
    console.warn("Could not parse saved recipe.", error);
    return structuredClone(defaultRecipe);
  }
}

function normalizeRecipe(raw) {
  const nextRecipe = {
    ...structuredClone(defaultRecipe),
    ...raw
  };

  nextRecipe.ingredients = normalizeList(raw.ingredients);
  nextRecipe.instructions = normalizeList(raw.instructions);
  nextRecipe.notes = normalizeText(raw.notes || "");
  nextRecipe.image = typeof raw.image === "string" ? raw.image : "";
  nextRecipe.visibility = {
    ...structuredClone(defaultRecipe.visibility),
    ...(raw.visibility || {})
  };

  return nextRecipe;
}

function normalizeList(value) {
  if (Array.isArray(value)) {
    return value.map((item) => normalizeText(item)).filter(Boolean);
  }

  if (typeof value === "string") {
    return value
      .split(/\r?\n/)
      .map((item) => normalizeText(item))
      .filter(Boolean);
  }

  return [];
}

function normalizeText(value) {
  return String(value || "").trim();
}

function fillForm(nextRecipe) {
  titleInput.value = nextRecipe.title;
  subtitleInput.value = nextRecipe.subtitle;
  prepTimeInput.value = nextRecipe.prepTime;
  cookTimeInput.value = nextRecipe.cookTime;
  servingsInput.value = nextRecipe.servings;
  difficultyInput.value = nextRecipe.difficulty;
  ingredientsInput.value = nextRecipe.ingredients.join("\n");
  instructionsInput.value = nextRecipe.instructions.join("\n");
  notesInput.value = nextRecipe.notes;
  imageUploadInput.value = "";
  visibilityInputs.forEach((input) => {
    input.checked = Boolean(nextRecipe.visibility[input.dataset.visibilityKey]);
  });
  syncImageStatus();
}

function readForm() {
  return {
    title: normalizeText(titleInput.value),
    subtitle: normalizeText(subtitleInput.value),
    prepTime: normalizeText(prepTimeInput.value),
    cookTime: normalizeText(cookTimeInput.value),
    servings: normalizeText(servingsInput.value),
    difficulty: normalizeText(difficultyInput.value),
    ingredients: normalizeList(ingredientsInput.value),
    instructions: normalizeList(instructionsInput.value),
    notes: normalizeText(notesInput.value),
    image: recipe.image || "",
    visibility: visibilityInputs.reduce((accumulator, input) => {
      accumulator[input.dataset.visibilityKey] = input.checked;
      return accumulator;
    }, {})
  };
}

function updateRecipe() {
  recipe = readForm();
  persistRecipe();
  renderRecipe();
}

function persistRecipe() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(recipe, null, 2));
    updateStorageStatus("ready");
    return true;
  } catch (error) {
    console.error("Could not save recipe.", error);
    updateStorageStatus(isQuotaExceededError(error) ? "quota-error" : "generic-error");
    return false;
  }
}

function renderRecipe() {
  const t = translations[currentLanguage];
  const visibility = recipe.visibility;
  setText("#preview-title", recipe.title || defaultRecipe.title);
  setText("#preview-subtitle", recipe.subtitle || t.defaultSubtitle);
  setText("#back-title", recipe.title || defaultRecipe.title);
  setText("#preview-prepTime", recipe.prepTime || "-");
  setText("#preview-cookTime", recipe.cookTime || "-");
  setText("#preview-servings", recipe.servings || "-");
  setText("#preview-difficulty", recipe.difficulty || "-");
  setText("#preview-notes", recipe.notes || t.fallbackNotes);

  renderList("#preview-ingredients", recipe.ingredients, false, [t.fallbackIngredients]);
  renderList("#preview-instructions", recipe.instructions, true, [t.fallbackInstructions]);

  if (recipe.image && visibility.showCoverImage) {
    previewImage.src = recipe.image;
    previewImage.style.display = "block";
    imageFallback.style.display = "none";
    frontOverlay.style.display = "block";
    frontCard.classList.remove("no-image");
  } else {
    previewImage.removeAttribute("src");
    previewImage.style.display = "none";
    imageFallback.style.display = "block";
    frontOverlay.style.display = "none";
    frontCard.classList.add("no-image");
  }

  document.querySelector("#preview-subtitle").hidden = !visibility.showSubtitle;
  backHeader.hidden = !visibility.showBackHeader;
  metaStrip.hidden = !visibility.showMetaStrip;
  metaPrep.hidden = !visibility.showMetaStrip || !visibility.showPrepTime;
  metaCook.hidden = !visibility.showMetaStrip || !visibility.showCookTime;
  metaServings.hidden = !visibility.showMetaStrip || !visibility.showServings;
  metaDifficulty.hidden = !visibility.showMetaStrip || !visibility.showDifficulty;
  const visibleMetaCount = [
    visibility.showPrepTime,
    visibility.showCookTime,
    visibility.showServings,
    visibility.showDifficulty
  ].filter(Boolean).length;
  metaStrip.hidden = !visibility.showMetaStrip || visibleMetaCount === 0;
  ingredientsBlock.hidden = !visibility.showIngredients;
  instructionsBlock.hidden = !visibility.showInstructions;
  notesBlock.hidden = !visibility.showNotes;

  const visibleColumnCount = [visibility.showIngredients, visibility.showInstructions].filter(Boolean).length;
  backColumns.hidden = visibleColumnCount === 0;
  backColumns.classList.toggle("single-column", visibleColumnCount === 1);

  syncIngredientColumns();
  syncImageStatus();
}

function setText(selector, value) {
  const element = document.querySelector(selector);
  element.textContent = value;
}

function renderList(selector, items, numbered, fallbackItems) {
  const list = document.querySelector(selector);
  list.innerHTML = "";
  const content = items.length ? items : fallbackItems;

  content.forEach((item, index) => {
    const listItem = listItemTemplate.content.firstElementChild.cloneNode(true);
    listItem.textContent = item;
    if (numbered && item === fallbackItems[0]) {
      listItem.value = index + 1;
    }
    list.appendChild(listItem);
  });
}

function syncImageStatus() {
  const t = translations[currentLanguage];
  imageStatus.textContent = recipe.image ? t.imageStatusEmbedded : t.imageStatusEmpty;
}

function syncIngredientColumns() {
  previewIngredients.classList.remove("content-list-two-column");

  if (ingredientsBlock.hidden || backColumns.hidden || recipe.ingredients.length < 2) {
    return;
  }

  const overflowsSingleColumn = ingredientsBlock.scrollHeight > ingredientsBlock.clientHeight + 1;

  if (overflowsSingleColumn) {
    previewIngredients.classList.add("content-list-two-column");
  }
}

function updateStorageStatus(state) {
  const t = translations[currentLanguage];
  const wasError = storageState !== "ready";
  storageState = state;
  storageStatus.classList.remove("is-error", "is-success");

  if (state === "ready") {
    storageStatus.textContent = wasError ? t.storageStatusRecovered : t.storageStatusReady;
    if (wasError) {
      storageStatus.classList.add("is-success");
    }
    return;
  }

  if (state === "quota-error") {
    storageStatus.textContent = t.storageErrorQuota;
  } else {
    storageStatus.textContent = t.storageErrorGeneric;
  }

  storageStatus.classList.add("is-error");
}

function isQuotaExceededError(error) {
  return error instanceof DOMException && (
    error.name === "QuotaExceededError" ||
    error.name === "NS_ERROR_DOM_QUOTA_REACHED" ||
    error.code === 22 ||
    error.code === 1014
  );
}

function syncDebugPrint() {
  document.body.classList.toggle("debug-print", Boolean(debugPrintInput?.checked));
}

function applyTranslations() {
  const t = translations[currentLanguage];
  document.documentElement.lang = currentLanguage;

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t[element.dataset.i18n];
  });

  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    element.innerHTML = t[element.dataset.i18nHtml];
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = t[element.dataset.i18nPlaceholder];
  });

  languageButtons.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.language === currentLanguage);
  });

  updateStorageStatus(storageState);
  renderRecipe();
}

function setLanguage(language) {
  currentLanguage = translations[language] ? language : "en";
  localStorage.setItem(LANGUAGE_KEY, currentLanguage);
  applyTranslations();
}

function downloadRecipe() {
  const blob = new Blob([JSON.stringify(recipe, null, 2)], { type: "application/json" });
  const recipeSlug = (recipe.title || "recipe-card")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${recipeSlug || "recipe-card"}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(link.href);
}

function resetRecipe() {
  recipe = structuredClone(defaultRecipe);
  persistRecipe();
  fillForm(recipe);
  renderRecipe();
}

async function handleImageUpload(file) {
  if (!file) {
    return;
  }

  const previousImage = recipe.image;
  recipe.image = await readFileAsDataUrl(file);

  if (!persistRecipe()) {
    recipe.image = previousImage;
    imageUploadInput.value = "";
  }

  renderRecipe();
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

async function handleImport(file) {
  if (!file) {
    return;
  }

  try {
    const text = await file.text();
    recipe = normalizeRecipe(JSON.parse(text));
    persistRecipe();
    fillForm(recipe);
    renderRecipe();
  } catch (error) {
    alert(translations[currentLanguage].importError);
    console.error(error);
  } finally {
    importInput.value = "";
  }
}

form.addEventListener("input", updateRecipe);

imageUploadInput.addEventListener("change", async (event) => {
  const [file] = event.target.files;
  await handleImageUpload(file);
});

removeImageButton.addEventListener("click", () => {
  recipe.image = "";
  persistRecipe();
  renderRecipe();
  imageUploadInput.value = "";
});

printButton.addEventListener("click", () => {
  updateRecipe();
  window.print();
});

exportButton.addEventListener("click", () => {
  updateRecipe();
  downloadRecipe();
});

newButton.addEventListener("click", resetRecipe);

debugPrintInput?.addEventListener("change", syncDebugPrint);

languageButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setLanguage(button.dataset.language);
  });
});

importInput.addEventListener("change", async (event) => {
  const [file] = event.target.files;
  await handleImport(file);
});

fillForm(recipe);
applyTranslations();
syncDebugPrint();
