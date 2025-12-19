// src/lib/api.ts
// Small helper for talking to your Django backend endpoints.
// Uses same-origin credentials and X-CSRFToken for POSTs.

export async function getCsrfToken(): Promise<string> {
  const res = await fetch("/posts/api/csrf/", { credentials: "same-origin" });
  if (!res.ok) throw new Error("Failed to get CSRF token");
  const data = await res.json();
  return data.csrfToken;
}

async function postJson(url: string, body: any) {
  // get CSRF token (this also ensures the csrftoken cookie is set)
  const token = await getCsrfToken();
  const res = await fetch(url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": token,
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) {
    // surface server error message if present
    throw new Error(data?.error || JSON.stringify(data));
  }
  return data;
}

export const auth = {
  login: async (email: string, password: string) =>
    await postJson("/posts/api/login/", { email, password }),

  signup: async (email: string, username: string, password: string) =>
    await postJson("/posts/api/signup/", { email, username, password }),

  logout: async () => await postJson("/posts/api/logout/", {}),
};

export const postsApi = {
  list: async () => {
    const res = await fetch("/posts/api/posts/", { credentials: "same-origin" });
    if (!res.ok) throw new Error("Failed to fetch posts");
    return await res.json(); // { posts: [...] }
  },

  create: async (header: string, body: string) =>
    await postJson("/posts/api/posts/create", { header, body }),

  edit: async (id: number | string, header: string, body: string) =>
    await postJson(`/posts/api/posts/${id}/edit`, { header, body }),

  delete: async (id: number | string) => await postJson(`/posts/api/posts/${id}/delete`, {}),

  // simple helper: fetch all posts and find by id (we didn't add a single-post endpoint)
  getById: async (id: number | string) => {
    const data = await postsApi.list();
    const found = data.posts.find((p: any) => String(p.id) === String(id));
    if (!found) throw new Error("Post not found");
    return found;
  },
};
