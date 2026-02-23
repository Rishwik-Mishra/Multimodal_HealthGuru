const BASE_URL = "http://127.0.0.1:8000";

// -----------------------------
// PREDICT
// -----------------------------
export async function predictFood(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  return response.json();
}

// -----------------------------
// SUMMARY (DATE REQUIRED)
// -----------------------------
export async function getDailySummary(date: string) {
  const response = await fetch(
    `${BASE_URL}/daily-summary?query_date=${date}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch summary");
  }

  return response.json();
}

// -----------------------------
// LOGS (DATE REQUIRED)
// -----------------------------
export async function getLogs(date: string) {
  const response = await fetch(
    `${BASE_URL}/logs?query_date=${date}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch logs");
  }

  return response.json();
}

// -----------------------------
// LOG FOOD
// -----------------------------
export async function logFood(data: {
  dish_id: number;
  portion_count: number;
  grams: number;
}) {
  const response = await fetch(`${BASE_URL}/log-food`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Logging failed");
  }

  return response.json();
}