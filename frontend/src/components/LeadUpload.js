import { useState } from "react";
import api from "../api/axios";
import "./LeadUpload.css"; // Ensure this is imported
import Navbar from "./Navbar";
import Footer from "./Footer";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudArrowUp, faFileCsv, faCheckCircle, faExclamationCircle } from '@fortawesome/free-solid-svg-icons';

function LeadUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    if (!selectedFile.name.endsWith(".csv")) {
      setMessage("Please upload a valid CSV file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first.");
      return;
    }

    setIsUploading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("/leads/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Leads uploaded successfully.");
      setFile(null);
    } catch (err) {
      setMessage(err.response?.data?.message || "Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="leadupload-wrapper"> {/* Uses background from Dashboard.css */}
      <Navbar />
      <div className="upload-content-area">
        <div className="upload-card stat-card"> {/* Inherits glass styles */}
          <div className="upload-header">
            <FontAwesomeIcon icon={faCloudArrowUp} className="upload-icon-main" />
            <h1 className="gradient-text">Import Your Leads</h1>
            <p className="stat-label">Choose a CSV file to enrich your lead database with AI.</p>
          </div>

          <div className={`upload-drop-zone ${file ? 'active' : ''}`}>
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              disabled={isUploading}
              id="csv-upload"
              className="hidden-input"
            />
            <label htmlFor="csv-upload" className="upload-label">
              {file ? (
                <div className="file-info">
                  <FontAwesomeIcon icon={faFileCsv} size="2x" color="#8b5cf6" />
                  <span>{file.name}</span>
                </div>
              ) : (
                "Click to browse or drag & drop CSV"
              )}
            </label>
          </div>

          <button
            onClick={handleUpload}
            disabled={isUploading || !file}
            className={`upload-action-btn ${!file || isUploading ? 'disabled' : ''}`}
          >
            {isUploading ? "Uploading..." : "Upload & Enrich Leads"}
          </button>

          {message && (
            <div className={`status-box ${message.includes("successfully") ? "success" : "error"}`}>
              <FontAwesomeIcon icon={message.includes("successfully") ? faCheckCircle : faExclamationCircle} />
              <span>{message}</span>
            </div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default LeadUpload;