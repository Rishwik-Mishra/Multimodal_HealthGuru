import { useState, useEffect, useMemo } from "react";
import { searchDish, logFood } from "../services/api";

interface Dish {
  id: number;
  name: string;
  calories_100g: number;
  protein_100g: number;
  carbs_100g: number;
  fat_100g: number;
  fiber_100g: number;
  sugar_100g: number;
  sat_fat_100g: number;
  sodium_mg_100g: number;
}

export default function ManualEntryCard({
  onLogged,
}: {
  onLogged: () => void;
}) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Dish[]>([]);
  const [selected, setSelected] = useState<Dish | null>(null);
  const [portion, setPortion] = useState(1);
  const [logging, setLogging] = useState(false);
  const [highlightIndex, setHighlightIndex] = useState(0);

  // 🔎 Debounced Search
  useEffect(() => {
    if (!query || query.length < 1) {
      setResults([]);
      return;
    }

    const delay = setTimeout(async () => {
      try {
        const data = await searchDish(query);
        if (Array.isArray(data)) {
          setResults(data);
          setHighlightIndex(0);
        } else {
          setResults([]);
        }
      } catch (err) {
        console.error(err);
        setResults([]);
      }
    }, 250);

    return () => clearTimeout(delay);
  }, [query]);

  // ⌨️ Keyboard Handling
  const handleKeyDown = async (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      setHighlightIndex((prev) =>
        prev < results.length - 1 ? prev + 1 : prev
      );
    }

    if (e.key === "ArrowUp") {
      setHighlightIndex((prev) => (prev > 0 ? prev - 1 : prev));
    }

    if (e.key === "Enter") {
      // If nothing selected → select highlighted
      if (!selected && results.length > 0) {
        const dish = results[highlightIndex];
        setSelected(dish);
        setQuery(dish.name);
        setResults([]);
        return;
      }

      // If already selected → log immediately
      if (selected) {
        await handleLog();
      }
    }
  };

  // 🧮 Macro Calculation
  const macros = useMemo(() => {
    if (!selected) return null;

    const factor = portion;

    return {
      calories: (selected.calories_100g * factor).toFixed(2),
      protein: (selected.protein_100g * factor).toFixed(2),
      carbs: (selected.carbs_100g * factor).toFixed(2),
      fat: (selected.fat_100g * factor).toFixed(2),
    };
  }, [selected, portion]);

  const handleLog = async () => {
    if (!selected) return;

    try {
      setLogging(true);

      await logFood({
        dish_id: selected.id,
        portion_count: portion,
        grams: 100 * portion,
      });

      onLogged();

      setSelected(null);
      setQuery("");
      setResults([]);
      setPortion(1);
    } catch (err) {
      console.error(err);
    } finally {
      setLogging(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-lg font-semibold mb-3">
        Manual Entry
      </h2>

      <input
        type="text"
        placeholder="Search food..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setSelected(null);
        }}
        onKeyDown={handleKeyDown}
        className="w-full border p-2 rounded mb-2"
      />

      {/* Suggestions */}
      {results.length > 0 && !selected && (
        <div className="border rounded mb-2 max-h-40 overflow-y-auto">
          {results.map((dish, index) => (
            <div
              key={dish.id}
              onClick={() => {
                setSelected(dish);
                setQuery(dish.name);
                setResults([]);
              }}
              className={`p-2 cursor-pointer ${
                index === highlightIndex
                  ? "bg-blue-100"
                  : "hover:bg-gray-100"
              }`}
            >
              {dish.name}
            </div>
          ))}
        </div>
      )}

      {selected && macros && (
        <>
          <div className="text-sm space-y-1 mb-3">
            <p>Calories: {macros.calories} kcal</p>
            <p>Protein: {macros.protein} g</p>
            <p>Carbs: {macros.carbs} g</p>
            <p>Fat: {macros.fat} g</p>
          </div>

          <label className="block text-sm mb-1">
            Portion: {portion}x (100g base)
          </label>

          <input
            type="range"
            min="0.5"
            max="3"
            step="0.5"
            value={portion}
            onChange={(e) => setPortion(Number(e.target.value))}
            className="w-full mb-3"
          />

          <button
            onClick={handleLog}
            disabled={logging}
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            {logging ? "Logging..." : "Log Food"}
          </button>
        </>
      )}
    </div>
  );
}