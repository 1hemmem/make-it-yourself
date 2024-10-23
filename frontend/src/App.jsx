import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./Navbar";
import { Test } from "./Test";
import { Build } from "./Build";
import { Home } from "./Home";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Default route that redirects to the home page */}
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/build" element={<Build />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </Router>
  );
};

export default App;