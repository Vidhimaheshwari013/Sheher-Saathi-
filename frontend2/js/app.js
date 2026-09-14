const API_URL = "http://127.0.0.1:8000";

// Get the report input and button
const reportInput = document.querySelector("input");
const reportButtons = document.querySelectorAll("button");

// Find the AI File Report button
let reportButton = null;

reportButtons.forEach((button) => {
    if (button.innerText.includes("AI File Report")) {
        reportButton = button;
    }
});

if (reportButton) {
    reportButton.addEventListener("click", submitComplaint);
}

async function submitComplaint() {
    const complaintText = reportInput?.value.trim();

    if (!complaintText) {
        alert("Please describe the civic issue first.");
        return;
    }

    reportButton.disabled = true;
    reportButton.innerText = "Submitting...";

    try {
        // 1. Create complaint
        const complaintResponse = await fetch(
            `${API_URL}/complaints`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    raw_text: complaintText
                })
            }
        );

        if (!complaintResponse.ok) {
            throw new Error("Could not submit complaint.");
        }

        const complaintData = await complaintResponse.json();

        console.log("Complaint created:", complaintData);

        // 2. Analyze complaint
        const analysisResponse = await fetch(
            `${API_URL}/complaints/analyze`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    raw_text: complaintText
                })
            }
        );

        if (!analysisResponse.ok) {
            throw new Error("Complaint submitted, but analysis failed.");
        }

        const analysisData = await analysisResponse.json();

        console.log("AI analysis:", analysisData);

        // Save data for the report page
        localStorage.setItem(
            "latestComplaint",
            JSON.stringify(complaintData)
        );

        localStorage.setItem(
            "latestAnalysis",
            JSON.stringify(analysisData)
        );

        // Go to report page
        window.location.href = "report.html";

    } catch (error) {
        console.error(error);
        alert(error.message);
    }

    reportButton.disabled = false;
    reportButton.innerText = "AI File Report";
}