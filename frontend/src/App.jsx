import { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultPage from './pages/ResultPage';

export default function App() {
  
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleResult = (data) => {
    setResult(data);
    navigate('/result');
  };

  return (
    <Routes>
      <Route path="/" element={<HomePage onResult={handleResult} />} />
      <Route path="/result" element={<ResultPage result={result} />} />
    </Routes>
  );
}
