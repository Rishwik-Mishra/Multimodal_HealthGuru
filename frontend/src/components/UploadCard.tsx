import { useState } from "react";
import { predictFood } from "../services/api";

interface Props {
  onPrediction: (data: any) => void;
}

export default function UploadCard({ onPrediction }: Props) {
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    if (!e.target.files) return;

    const file = e.target.files[0];
    setLoading(true);

    try {
      const result = await predictFood(file);
      onPrediction(result);
    } catch (error) {
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow">
      <h2 className="text-xl font-semibold mb-4">Upload Food</h2>

      <input
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileChange}
        className="block w-full mb-4"
      />

      {loading && (
        <p className="text-blue-500 font-medium">
          Analyzing image...
        </p>
      )}
    </div>
  );
}