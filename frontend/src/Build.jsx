import { useState } from "react";
import "./Build.css";

export const Build = () => {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [description, setDescription] = useState("");
  const [selectedBase, setSelectedBase] = useState("");
  const [selectedEmbedding, setSelectedEmbedding] = useState("");
  const [temperature, setTemperature] = useState(0.5);
  const [topP, setTopP] = useState(0.9);
  const [topK, setTopK] = useState(40);

  const basemodels = [
    "llama3.2",
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

  // const handleSubmit = async (event) => {
  //   event.preventDefault(); // Prevent the default form submission

  //   // Create an object with all the parameters
  //   const formData = {
  //     pdfFiles: pdfFiles.map((file) => file.name), // Collect just the file names
  //     description,
  //     selectedBase,
  //     selectedEmbedding,
  //     temperature: parseFloat(temperature),
  //     top_p: parseFloat(topP),
  //     top_k: parseInt(topK, 10),
  //   };

  //   // Send the data to the server
  //   try {
  //     const response = await fetch("http://localhost:8000/submit/", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify(formData),
  //     });

  //     if (response.ok) {
  //       const responseData = await response.json();
  //       console.log("Success:", responseData);
  //     } else {
  //       console.error("Error:", response.statusText);
  //     }
  //   } catch (error) {
  //     console.error("Network error:", error);
  //   }
  // };
  // const handleSubmit = async (event) => {
  //   event.preventDefault(); // Prevent the default form submission

  //   // Create a new FormData object
  //   const formData = new FormData();

  //   // Append PDF files to FormData
  //   pdfFiles.forEach((file) => {
  //     formData.append("pdfFiles", file); // Use "pdfFiles" as the field name for the files
  //   });

  //   // Append other form data
  //   formData.append("description", description);
  //   formData.append("selectedBase", selectedBase);
  //   formData.append("selectedEmbedding", selectedEmbedding);
  //   formData.append("temperature", parseFloat(temperature));
  //   formData.append("top_p", parseFloat(topP));
  //   formData.append("top_k", parseInt(topK, 10));

  //   // Send the data to the server
  //   try {
  //     const response = await fetch("http://localhost:8000/submit/", {
  //       mode:'no-cors',
  //       method: "POST",
  //       body: formData,
  //     });

  //     if (response.ok) {
  //       const responseData = await response.json();
  //       console.log("Success:", responseData);
  //     } else {
  //       console.error("Error:", response.statusText);
  //     }
  //   } catch (error) {
  //     console.error("Network error:", error);
  //   }
  // };
  // When using FormData, do not use 'application/json' headers.
  const handleSubmit = async (event) => {
    event.preventDefault();

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
    }
  };

  return (
    <div>
      <h1>Upload PDFs and Provide Document Info</h1>
      <form onSubmit={handleSubmit}>
        {/* PDF Upload Section */}
        <div className="form-section">
          <label htmlFor="pdf-upload">Upload PDFs:</label>
          <br />
          <input
            type="file"
            id="pdf-upload"
            multiple
            accept=".pdf"
            onChange={handlePdfUpload}
            required
          />
          <ul>
            {pdfFiles.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>

        {/* Document Description Section */}
        <div className="form-section">
          <label htmlFor="description">Document Description:</label>
          <br />
          <textarea
            id="description"
            value={description}
            onChange={handleDescriptionChange}
            placeholder="Enter document description, based on this description the model will detect if the user question is relevant or not and make a decision to either answer or apologies"
            required
          />
        </div>

        {/* Base Model Selection Section */}
        <div className="form-section">
          <label htmlFor="base-dropdown">Select a base model:</label>
          <br />
          <select
            id="base-dropdown"
            value={selectedBase}
            onChange={handleBaseChange}
            required
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
          <label htmlFor="embedding-dropdown">Select an embedding model:</label>
          <br />
          <select
            id="embedding-dropdown"
            value={selectedEmbedding}
            onChange={handleEmbeddingChange}
            required
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
          <label htmlFor="temperature-slider">Temperature: {temperature}</label>
          <br />
          <input
            type="range"
            id="temperature-slider"
            min="0"
            max="1"
            step="0.01"
            value={temperature}
            onChange={handleTemperatureChange}
          />
        </div>

        {/* Top-p Slider */}
        <div className="form-section">
          <label htmlFor="top-p-slider">Top-p: {topP}</label>
          <br />
          <input
            type="range"
            id="top-p-slider"
            min="0"
            max="1"
            step="0.01"
            value={topP}
            onChange={handleTopPChange}
          />
        </div>

        {/* Top-k Number Input */}
        <div className="form-section">
          <label htmlFor="top-k-input">Top-k: {topK}</label>
          <br />
          <input
            type="number"
            id="top-k-input"
            value={topK}
            onChange={handleTopKChange}
          />
        </div>

        {/* Submit Button */}
        <div className="form-section">
          <button type="submit">Build</button>
        </div>
      </form>
    </div>
  );
};