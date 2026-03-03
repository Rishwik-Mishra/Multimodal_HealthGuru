import { useState, useEffect, useMemo } from "react";
import UploadCard from "./components/UploadCard";
import ManualEntryCard from "./components/ManualEntryCard";
import {
  logFood,
  getDailySummary,
  getLogs,
} from "./services/api";
import Toast from "./components/Toast";

const DAILY_CALORIE_GOAL = 2000;

export default function App() {
  // ✅ Single source of truth for date (LOCAL TIME)
  const today = new Date().toLocaleDateString("en-CA");

  const [prediction, setPrediction] = useState<any>(null);
  const [portion, setPortion] = useState(1);
  const [logging, setLogging] = useState(false);
  const [summary, setSummary] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // -----------------------------
  // Fetch Summary + Logs
  // -----------------------------
  const refreshData = async () => {
    try {
      const summaryData = await getDailySummary(today);
      const logsData = await getLogs(today);

      setSummary(summaryData.summary);
      setLogs(logsData.logs);
    } catch (err) {
      console.error("Failed to refresh data", err);
    }
  };

  // ✅ Runs on mount
  useEffect(() => {
    refreshData();
  }, []);

  // -----------------------------
  // Macro Scaling (Optimized)
  // -----------------------------
  const macros = useMemo(() => {
    if (!prediction) return null;

    const factor = portion;

    return {
      calories: (prediction.macros.calories * factor).toFixed(2),
      protein: (prediction.macros.protein * factor).toFixed(2),
      carbs: (prediction.macros.carbs * factor).toFixed(2),
      fat: (prediction.macros.fat * factor).toFixed(2),
      fiber: (prediction.macros.fiber * factor).toFixed(2),
      sugar: (prediction.macros.sugar * factor).toFixed(2),
      sat_fat: (prediction.macros.sat_fat * factor).toFixed(2),
      sodium_mg: (prediction.macros.sodium_mg * factor).toFixed(2),
    };
  }, [prediction, portion]);

  // -----------------------------
  // Logging
  // -----------------------------
  const handleLog = async () => {
    if (!prediction) return;

    try {
      setLogging(true);

      await logFood({
        dish_id: prediction.dish_id,
        portion_count: portion,
        grams: prediction.grams_used * portion,
      });

      // ✅ Immediately refresh after logging
      await refreshData();

      setToastMessage("Food logged successfully!");
    } catch (err) {
      console.error(err);
      setToastMessage("Logging failed ❌");
    } finally {
      setLogging(false);
    }
  };

  // -----------------------------
  // Calorie Progress %
  // -----------------------------
  const calorieProgress = summary
    ? Math.min((summary.calories / DAILY_CALORIE_GOAL) * 100, 100)
    : 0;

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-5xl mx-auto p-4">
        <h1 className="text-3xl font-bold text-center mb-6">
          HealthGuru 🥗
        </h1>

        <div className="grid md:grid-cols-2 gap-6">
          {/* LEFT SIDE */}
          <div className="space-y-6">
            <ManualEntryCard onLogged={refreshData} />

            <UploadCard
              onPrediction={(data) => {
                setPrediction(data);
                setPortion(1);
              }}
            />

            {prediction && macros && (
              <div className="bg-white p-6 rounded-xl shadow">
                <h2 className="text-xl font-semibold capitalize mb-2">
                  {prediction.food_detected}
                </h2>

                <p className="text-sm text-gray-500 mb-4">
                  Confidence: {(prediction.confidence * 100).toFixed(2)}%
                </p>

                <div className="space-y-1 text-sm mb-4">
                  <p>Calories: {macros.calories} kcal</p>
                  <p>Protein: {macros.protein} g</p>
                  <p>Carbs: {macros.carbs} g</p>
                  <p>Fat: {macros.fat} g</p>
                  <p>Fiber: {macros.fiber} g</p>
                  <p>Sugar: {macros.sugar} g</p>
                  <p>Sat Fat: {macros.sat_fat} g</p>
                  <p>Sodium: {macros.sodium_mg} mg</p>
                </div>

                <div className="mb-4">
                  <label className="block text-sm font-medium mb-2">
                    Portion: {portion}x
                  </label>

                  <input
                    type="range"
                    min="0.5"
                    max="3"
                    step="0.5"
                    value={portion}
                    onChange={(e) =>
                      setPortion(Number(e.target.value))
                    }
                    className="w-full"
                  />
                </div>

                <button
                  onClick={handleLog}
                  disabled={logging}
                  className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
                >
                  {logging ? "Logging..." : "Log Food"}
                </button>
              </div>
            )}
          </div>

          {/* RIGHT SIDE */}
          <div className="space-y-6">
            {/* DAILY SUMMARY */}
            <div className="bg-white p-6 rounded-xl shadow">
              <h2 className="text-xl font-semibold mb-3">
                Today's Summary
              </h2>

              {summary ? (
                <>
                  <p className="mb-2 font-medium">
                    Calories: {summary.calories.toFixed(2)} kcal
                  </p>

                  <div className="w-full bg-gray-300 rounded-full h-5 mb-2 overflow-hidden">
                    <div
                      className="bg-blue-600 h-5 transition-all duration-700"
                      style={{ width: `${calorieProgress}%` }}
                    />
                  </div>

                  <p className="text-xs text-gray-500 mb-4">
                    Goal: {DAILY_CALORIE_GOAL} kcal
                  </p>

                  <p>Protein: {summary.protein.toFixed(2)} g</p>
                  <p>Carbs: {summary.carbs.toFixed(2)} g</p>
                  <p>Fat: {summary.fat.toFixed(2)} g</p>
                </>
              ) : (
                <p>No data yet.</p>
              )}
            </div>

            {/* LOGGED ITEMS */}
            <div className="bg-white p-6 rounded-xl shadow">
              <h2 className="text-xl font-semibold mb-3">
                Logged Items
              </h2>

              {logs.length === 0 && <p>No logs today.</p>}

              {logs.map((log) => (
                <div
                  key={log.log_id}
                  className="border-b py-2 text-sm"
                >
                  <p className="font-medium">
                    {log.food_name}
                  </p>
                  <p>{log.calories.toFixed(2)} kcal</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {toastMessage && (
        <Toast
          message={toastMessage}
          onClose={() => setToastMessage(null)}
        />
      )}
    </div>
  );
}