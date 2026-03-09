const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function parseResponse<T>(response: Response, method: string, path: string): Promise<T> {
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${method} ${path} failed: ${response.status} ${detail}`);
  }
  return (await response.json()) as T;
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, { credentials: "include" });
  return parseResponse<T>(response, "GET", path);
}

export async function apiPost<T>(path: string, payload: object): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<T>(response, "POST", path);
}

export async function apiUpload<T>(
  path: string,
  options: {
    fields?: Record<string, string>;
    file: File;
    fileField?: string;
  },
): Promise<T> {
  const formData = new FormData();
  formData.set(options.fileField ?? "file", options.file);
  Object.entries(options.fields ?? {}).forEach(([key, value]) => {
    formData.set(key, value);
  });
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });
  return parseResponse<T>(response, "POST", path);
}
