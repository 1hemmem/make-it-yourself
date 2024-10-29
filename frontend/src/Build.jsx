import { useState } from "react";
import "./Styles/Build.css";

export const Build = () => {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [description, setDescription] = useState("");
  const [selectedBase, setSelectedBase] = useState("");
  const [selectedEmbedding, setSelectedEmbedding] = useState("");
  const [temperature, setTemperature] = useState(0.5);
  const [topP, setTopP] = useState(0.9);
  const [topK, setTopK] = useState(40);
  const [loading, setLoading] = useState(false); // State to track loading

  const basemodels = [
    "llama3.2:3b",
    "llama3.1",
    "gemma2",
    "qwen2.5",
    "phi3.5",
    "nemotron-mini",
  ];

  const embeddingmodels = [
    "nvidia/NV-Embed-v2",
    "BAAI/bge-en-icl",
    "dunzhang/stella_en_1.5B_v5",
    "sentence-transformers/all-MiniLM-L6-v2",
    "Salesforce/SFR-Embedding-2_R",
    "Alibaba-NLP/gte-Qwen2-7B-instruct",
  ];

  const handlePdfUpload = (event) => {
    const files = Array.from(event.target.files);
    setPdfFiles((prevFiles) => [...prevFiles, ...files]);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleBaseChange = (event) => {
    setSelectedBase(event.target.value);
  };

  const handleEmbeddingChange = (event) => {
    setSelectedEmbedding(event.target.value);
  };

  const handleTemperatureChange = (event) => {
    setTemperature(event.target.value);
  };

  const handleTopPChange = (event) => {
    setTopP(event.target.value);
  };

  const handleTopKChange = (event) => {
    setTopK(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true); // Set loading to true when starting the submission

    // Create a new FormData object
    const formData = new FormData();

    // Append files to the FormData
    pdfFiles.forEach((file) => {
      formData.append("pdfFiles", file);
    });

    // Append other form data (as strings)
    formData.append("description", description);
    formData.append("selectedBase", selectedBase);
    formData.append("selectedEmbedding", selectedEmbedding);
    formData.append("temperature", temperature.toString()); // Convert to string
    formData.append("top_p", topP.toString());
    formData.append("top_k", topK.toString());

    try {
      const response = await fetch("http://localhost:8000/submit/", {
        mode: "no-cors",
        method: "POST",
        body: formData, // No content-type here; browser handles it automatically
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log("Success:", responseData);
      } else {
        console.error("Error:", response.statusText);
      }
    } catch (error) {
      console.error("Network error:", error);
    } finally {
      setLoading(false); // Reset loading to false once submission is complete
    }
  };

  return (
    <div className="build-container">
      <br /><br /><br />
      <h1 className="build-title">Upload PDFs and Provide Document Info</h1>
      <form onSubmit={handleSubmit} className="build-form">
        {/* PDF Upload Section */}
        <div className="form-section">
          <label htmlFor="pdf-upload" className="form-label">
            Upload PDFs:
          </label>
          <br />
          <input
            type="file"
            id="pdf-upload"
            multiple
            accept=".pdf"
            onChange={handlePdfUpload}
            required
            disabled={loading} // Disable during loading
            className="form-input"
          />
          <ul className="file-list">
            {pdfFiles.map((file, index) => (
              <li key={index} className="file-item">
                {file.name}
              </li>
            ))}
          </ul>
        </div>

        {/* Document Description Section */}
        <div className="form-section">
          <label htmlFor="description" className="form-label">
            Document Description:
          </label>
          <br />
          <textarea
            id="description"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Enter document description, based on this description the model will detect if the user question is relevant or not and make a decision to either answer or apologize"
            required
            disabled={loading} // Disable during loading
            className="form-textarea"
          />
        </div>

        {/* Base Model Selection Section */}
        <div className="form-section">
          <label htmlFor="base-dropdown" className="form-label">
            Select a base model:
          </label>
          <br />
          <select
            id="base-dropdown"
            value={selectedBase}
            onChange={handleBaseChange}
            required
            disabled={loading} // Disable during loading
            className="form-select"
          >
            <option value="" disabled>
              Choose a base model
            </option>
            {basemodels.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        {/* Embedding Model Selection Section */}
        <div className="form-section">
          <label htmlFor="embedding-dropdown" className="form-label">
            Select an embedding model:
          </label>
          <br />
          <select
            id="embedding-dropdown"
            value={selectedEmbedding}
            onChange={handleEmbeddingChange}
            required
            disabled={loading} // Disable during loading
            className="form-select"
          >
            <option value="" disabled>
              Choose an embedding model
            </option>
            {embeddingmodels.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </select>
        </div>

        {/* Temperature Slider */}
        <div className="form-section">
          <label htmlFor="temperature-slider" className="form-label">
            Temperature: {temperature}
          </label>
          <br />
          <input
            type="range"
            id="temperature-slider"
            min="0"
            max="1"
            step="0.01"
            value={temperature}
            onChange={handleTemperatureChange}
            disabled={loading} // Disable during loading
            className="form-slider"
          />
        </div>

        {/* Top-p Slider */}
        <div className="form-section">
          <label htmlFor="top-p-slider" className="form-label">
            Top-p: {topP}
          </label>
          <br />
          <input
            type="range"
            id="top-p-slider"
            min="0"
            max="1"
            step="0.01"
            value={topP}
            onChange={handleTopPChange}
            disabled={loading} // Disable during loading
            className="form-slider"
          />
        </div>

        {/* Top-k Number Input */}
        <div className="form-section">
          <label htmlFor="top-k-input" className="form-label">
            Top-k: {topK}
          </label>
          <br />
          <input
            type="number"
            id="top-k-input"
            value={topK}
            onChange={handleTopKChange}
            disabled={loading} // Disable during loading
            className="form-input"
          />
        </div>

        {/* Loading Animation */}
        {loading && (
          <div className="loading-spinner">
            <div className="lds-ring">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="form-section">
          <button type="submit" disabled={loading} className="form-button">
            {loading ? "Building..." : "Build"}
          </button>
        </div>
      </form>
    </div>
  );
};
