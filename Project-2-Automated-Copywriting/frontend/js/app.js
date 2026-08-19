const API_URL = "http://127.0.0.1:8000/api/generate";
const BATCH_API_URL = "http://127.0.0.1:8000/api/generate-batch";
const productName = document.getElementById("productName");
const productDescription = document.getElementById("productDescription");
const platform = document.getElementById("platform");
const tone = document.getElementById("tone");

const temperature = document.getElementById("temperature");
const topP = document.getElementById("topP");
const temperatureValue = document.getElementById("temperatureValue");
const topPValue = document.getElementById("topPValue");

const generateBtn = document.getElementById("generateBtn");
const batchBtn = document.getElementById("batchBtn");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");

const errorMessage = document.getElementById("errorMessage");
const loading = document.getElementById("loading");
const emptyState = document.getElementById("emptyState");
const result = document.getElementById("result");

const outputMeta = document.getElementById("outputMeta");
const content = document.getElementById("content");
const batchResult = document.getElementById("batchResult");
const batchResults = document.getElementById("batchResults");

const subjectSection = document.getElementById("subjectSection");
const subject = document.getElementById("subject");

const hashtagsSection = document.getElementById("hashtagsSection");
const hashtags = document.getElementById("hashtags");

let generatedText = "";

temperature.addEventListener("input", () => {
    temperatureValue.textContent = temperature.value;
});

topP.addEventListener("input", () => {
    topPValue.textContent = topP.value;
});

function showError(message) {
    errorMessage.textContent = message;
}

function clearError() {
    errorMessage.textContent = "";
}

function setLoading(isLoading) {
    generateBtn.disabled = isLoading;
    batchBtn.disabled = isLoading;
    loading.classList.toggle("hidden", !isLoading);
}

function resetOutput() {
    result.classList.add("hidden");
    batchResult.classList.add("hidden");
    batchResults.innerHTML = "";
    emptyState.classList.remove("hidden");
    copyBtn.disabled = true;

    subjectSection.classList.add("hidden");
    hashtagsSection.classList.add("hidden");

    subject.textContent = "";
    content.textContent = "";
    hashtags.innerHTML = "";
    outputMeta.textContent = "Your AI-generated content will appear here.";

    generatedText = "";
}

function renderOutput(data) {
    const output = data.output;

    emptyState.classList.add("hidden");
    result.classList.remove("hidden");
    copyBtn.disabled = false;

    outputMeta.textContent = `${data.platform} � ${data.tone}`;

    if (data.platform === "Email") {
        subjectSection.classList.remove("hidden");
        subject.textContent = output.subject || "";

        generatedText =
            `Subject: ${output.subject || ""}\n\n${output.body || ""}`;

        content.textContent = output.body || "";
        hashtagsSection.classList.add("hidden");
    } else {
        subjectSection.classList.add("hidden");

        content.textContent = output.content || "";

        generatedText = output.content || "";

        if (Array.isArray(output.hashtags) && output.hashtags.length > 0) {
            hashtagsSection.classList.remove("hidden");

            hashtags.innerHTML = "";

            output.hashtags.forEach((tag) => {
                const span = document.createElement("span");
                span.className = "hashtag";
                span.textContent = tag;
                hashtags.appendChild(span);
            });

            generatedText +=
                "\n\n" + output.hashtags.join(" ");
        } else {
            hashtagsSection.classList.add("hidden");
        }
    }
}

async function generateCopy() {
    clearError();

    if (!productName.value.trim()) {
        showError("Please enter a product name.");
        productName.focus();
        return;
    }

    if (!productDescription.value.trim()) {
        showError("Please enter a product description.");
        productDescription.focus();
        return;
    }

    setLoading(true);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                product_name: productName.value.trim(),
                product_description: productDescription.value.trim(),
                platform: platform.value,
                tone: tone.value,
                temperature: Number(temperature.value),
                top_p: Number(topP.value)
            })
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = Array.isArray(data.detail)
                ? data.detail.map((item) => item.msg).join(", ")
                : data.detail || "Generation failed.";

            throw new Error(detail);
        }

        renderOutput(data);

    } catch (error) {
        resetOutput();

        if (error instanceof TypeError) {
            showError(
                "Unable to connect to the API. Make sure the FastAPI server is running."
            );
        } else {
            showError(error.message || "Something went wrong.");
        }
    } finally {
        setLoading(false);
    }
}

async function generateBatch() {
    clearError();

    if (!productName.value.trim()) {
        showError("Please enter a product name.");
        productName.focus();
        return;
    }

    if (!productDescription.value.trim()) {
        showError("Please enter a product description.");
        productDescription.focus();
        return;
    }

    setLoading(true);

    try {
        const platforms = ["Instagram", "LinkedIn", "Email"];

        const requests = platforms.map((selectedPlatform) => ({
            product_name: productName.value.trim(),
            product_description: productDescription.value.trim(),
            platform: selectedPlatform,
            tone: tone.value,
            temperature: Number(temperature.value),
            top_p: Number(topP.value)
        }));

        const response = await fetch(BATCH_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(requests)
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = Array.isArray(data.detail)
                ? data.detail.map((item) => item.msg).join(", ")
                : data.detail || "Batch generation failed.";

            throw new Error(detail);
        }

        emptyState.classList.add("hidden");
        result.classList.add("hidden");
        batchResult.classList.remove("hidden");

        batchResults.innerHTML = "";

        data.forEach((item) => {
            const card = document.createElement("div");
            card.className = "batch-card";

            const title = document.createElement("h3");
            title.textContent = item.platform;

            const toneText = document.createElement("p");
            toneText.className = "batch-tone";
            toneText.textContent = `Tone: ${item.tone}`;

            card.appendChild(title);
            card.appendChild(toneText);

            if (item.platform === "Email") {
                const subjectTitle = document.createElement("strong");
                subjectTitle.textContent = "Subject";

                const subjectText = document.createElement("p");
                subjectText.textContent = item.output.subject || "";

                const contentTitle = document.createElement("strong");
                contentTitle.textContent = "Body";

                const contentText = document.createElement("pre");
                contentText.textContent = item.output.body || "";

                card.appendChild(subjectTitle);
                card.appendChild(subjectText);
                card.appendChild(contentTitle);
                card.appendChild(contentText);

            } else {
                const contentTitle = document.createElement("strong");
                contentTitle.textContent = "Content";

                const contentText = document.createElement("pre");
                contentText.textContent = item.output.content || "";

                card.appendChild(contentTitle);
                card.appendChild(contentText);

                if (
                    Array.isArray(item.output.hashtags) &&
                    item.output.hashtags.length > 0
                ) {
                    const hashtagsTitle = document.createElement("strong");
                    hashtagsTitle.textContent = "Hashtags";

                    const hashtagsText = document.createElement("p");
                    hashtagsText.textContent =
                        item.output.hashtags.join(" ");

                    card.appendChild(hashtagsTitle);
                    card.appendChild(hashtagsText);
                }
            }

            batchResults.appendChild(card);
        });

    } catch (error) {
        resetOutput();

        if (error instanceof TypeError) {
            showError(
                "Unable to connect to the API. Make sure the FastAPI server is running."
            );
        } else {
            showError(error.message || "Batch generation failed.");
        }
    } finally {
        setLoading(false);
    }
}

async function copyOutput() {
    if (!generatedText) return;

    try {
        await navigator.clipboard.writeText(generatedText);

        const originalText = copyBtn.textContent;
        copyBtn.textContent = "Copied!";

        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 1500);

    } catch {
        showError("Unable to copy content.");
    }
}

function clearForm() {
    productName.value = "";
    productDescription.value = "";

    platform.value = "Instagram";
    tone.value = "Friendly";

    temperature.value = "0.7";
    topP.value = "0.9";

    temperatureValue.textContent = "0.7";
    topPValue.textContent = "0.9";

    clearError();
    resetOutput();
}

generateBtn.addEventListener("click", generateCopy);
batchBtn.addEventListener("click", generateBatch);
copyBtn.addEventListener("click", copyOutput);
clearBtn.addEventListener("click", clearForm);
