import "./App.css";
import ComparisonsHistory from "./components/Comparisons/ComparisonsHistory";
import FilesUpload from "./components/FilesUpload/FilesUpload";
import React from "react";

const App = () => {
  return (
    <>
      <div className="main">
        <ComparisonsHistory />
        <FilesUpload />
      </div>
    </>
  );
};

export default App;
