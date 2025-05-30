import { useState } from 'react';
import Button from '../components/Button';
import Input from '../components/Input';
import ProgressSteps from '../components/ProgressSteps';
import { generatePrompt } from '../services/api';

export default function HomePage({ onResult }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(0);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setStep(0);
    try {
      const data = await generatePrompt(prompt);
      onResult(data);
    } catch (err) {
      setError(err.message || 'Error generating');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-center">CodeWeaver</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="text"
          placeholder="Enter your prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          required
        />
        {error && <p className="text-red-500">{error}</p>}
        <div className="text-center">
          <Button type="submit" disabled={loading}>
            {loading ? 'Generating...' : 'Submit'}
          </Button>
        </div>
      </form>
      {loading && <ProgressSteps currentStep={step} />}
    </div>
  );
}
