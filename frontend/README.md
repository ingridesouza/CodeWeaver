# CodeWeaver Frontend

This directory contains the React based frontend for the CodeWeaver system.
It was bootstrapped manually for usage with **Vite** and **Tailwind CSS**.

## Development

1. Install dependencies (requires Node.js):
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. The app will be available at `http://localhost:3000`.

## Build

To create a production build run:

```bash
npm run build
```

The output will be placed in the `dist/` directory.

## Overview

- `src/` – application source code
  - `components/` – reusable UI components
  - `pages/` – route pages (`HomePage` and `ResultPage`)
  - `services/` – API wrapper using Axios

The app posts a prompt to `/api/generate/` and displays the resulting
`enhanced_prompt` or any additional returned data.
