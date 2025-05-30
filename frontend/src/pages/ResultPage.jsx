import Button from '../components/Button';
import { Link } from 'react-router-dom';

export default function ResultPage({ result }) {
  if (!result) {
    return (
      <div className="max-w-xl mx-auto p-4 text-center">
        <p>No result yet.</p>
        <Link to="/">
          <Button className="mt-4">Back</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h2 className="text-xl font-bold text-center">Result</h2>
      <pre className="whitespace-pre-wrap p-4 bg-gray-100 rounded">
        {result.enhanced_prompt || JSON.stringify(result, null, 2)}
      </pre>
      {result.zip_path && (
        <a
          href={result.zip_path}
          className="underline text-blue-600"
          download
        >
          Download Files
        </a>
      )}
      <div className="text-center">
        <Link to="/">
          <Button>New Prompt</Button>
        </Link>
      </div>
    </div>
  );
}
