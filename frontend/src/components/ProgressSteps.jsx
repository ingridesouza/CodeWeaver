export default function ProgressSteps({ currentStep = 0 }) {
  const steps = ['Prompt Enhancer', 'Scrum Master', 'Dev Agents', 'QA'];

  return (
    <ol className="flex items-center justify-center space-x-4 mt-4">
      {steps.map((step, index) => (
        <li key={step} className="flex items-center">
          <span className={`w-4 h-4 rounded-full mr-2 border-2 ${index <= currentStep ? 'bg-blue-500 border-blue-500' : 'border-gray-300'}`}></span>
          <span className="text-sm">{step}</span>
          {index < steps.length - 1 && <span className="mx-2 text-gray-400">→</span>}
        </li>
      ))}
    </ol>
  );
}
