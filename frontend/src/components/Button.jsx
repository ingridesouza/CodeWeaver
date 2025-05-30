export default function Button({ children, ...props }) {
  return (
    <button
      className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded disabled:opacity-50"
      {...props}
    >
      {children}
    </button>
  );
}
