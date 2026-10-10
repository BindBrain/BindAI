const API_BASE = "";

export function getApiKey() {
  return (
    window.localStorage.getItem(
      "bindai_api_key",
    ) || ""
  );
}

export function setApiKey(value) {
  window.localStorage.setItem(
    "bindai_api_key",
    value,
  );
}

export async function apiFetch(
  path,
  options = {},
  apiKeyOverride = null,
) {
  const headers = new Headers(
    options.headers || {},
  );

  const apiKey =
    apiKeyOverride !== null
      ? apiKeyOverride
      : getApiKey();

  if (apiKey) {
    headers.set(
      "Authorization",
      `Bearer ${apiKey}`,
    );
  }

  const response = await fetch(
    `${API_BASE}${path}`,
    {
      ...options,
      headers,
    },
  );

  if (!response.ok) {
    let detail = "";

    try {
      const body = await response.json();

      if (typeof body?.detail === "string") {
        detail = body.detail;
      } else if (body?.detail?.message) {
        detail = body.detail.message;
      }
    } catch {
      // Keep the generic HTTP error below.
    }

    throw new Error(
      detail ||
        `BindAI API request failed: ${response.status} ${response.statusText}`,
    );
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function getProjects() {
  return apiFetch(
    "/api/v1/studio/projects",
  );
}

export function validateApiKey(apiKey) {
  const value = String(apiKey || "").trim();

  if (!value) {
    return Promise.reject(
      new Error("API key is required."),
    );
  }

  return apiFetch(
    "/api/v1/studio/projects",
    {},
    value,
  );
}

export function createProject(name) {
  return apiFetch(
    "/api/v1/studio/projects",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    },
  );
}

export function getWorkflows(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows`,
  );
}

export function createWorkflow(
  projectId,
  name,
  id = null,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        ...(id ? { id } : {}),
      }),
    },
  );
}

export function getCapabilities() {
  return apiFetch(
    "/api/v1/studio/capabilities",
  );
}

export function getProviders() {
  return apiFetch(
    "/api/v1/studio/providers",
  );
}

export function getWorkflow(
  projectId,
  workflowId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}`,
  );
}

export function saveWorkflow(
  projectId,
  workflowId,
  definition,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(definition),
    },
  );
}

export function deleteWorkflow(
  projectId,
  workflowId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}`,
    {
      method: "DELETE",
    },
  );
}

export function validateWorkflow(
  projectId,
  workflowId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}/validate`,
    {
      method: "POST",
    },
  );
}

export function runWorkflow(
  projectId,
  workflowId,
  variables = {},
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}/run`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        variables,
      }),
    },
  );
}

export function resolveHumanTask(
  projectId,
  workflowId,
  instanceId,
  action,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/workflows/${encodeURIComponent(
      workflowId,
    )}/instances/${encodeURIComponent(
      instanceId,
    )}/human-task`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action,
      }),
    },
  );
}

export function getAgents(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/agents`,
  );
}

export function getAgent(
  projectId,
  agentId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/agents/${encodeURIComponent(
      agentId,
    )}`,
  );
}

export function saveAgent(
  projectId,
  agentId,
  definition,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/agents/${encodeURIComponent(
      agentId,
    )}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        agent: definition,
      }),
    },
  );
}

export function deleteAgent(
  projectId,
  agentId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/agents/${encodeURIComponent(
      agentId,
    )}`,
    {
      method: "DELETE",
    },
  );
}

export function createAgent(
  projectId,
  name,
  id = null,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/agents`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        ...(id ? { id } : {}),
      }),
    },
  );
}

export function getTools(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/tools`,
  );
}

export function getConnectionProviders() {
  return apiFetch(
    "/api/v1/studio/connection-providers",
  );
}
export function getConnections(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/connections`,
  );
}

export function createConnection(projectId, connection) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/connections`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(connection),
    },
  );
}
export function setConnectionCredential(projectId, name, credential) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/connections/${encodeURIComponent(name)}/credential`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        credential,
      }),
    },
  );
}
export function deleteConnection(projectId, name) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/connections/${encodeURIComponent(name)}`,
    {
      method: "DELETE",
    },
  );
}
export function getKnowledge(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/knowledge`,
  );
}

export function uploadKnowledge(
  projectId,
  file,
) {
  const formData = new FormData();

  formData.append(
    "file",
    file,
  );

  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/knowledge`,
    {
      method: "POST",
      body: formData,
    },
  );
}

export function getForms(projectId) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/forms`,
  );
}

export function createForm(
  projectId,
  name,
  id = null,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/forms`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        ...(id ? { id } : {}),
      }),
    },
  );
}

export function getForm(
  projectId,
  formId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/forms/${encodeURIComponent(
      formId,
    )}`,
  );
}

export function saveForm(
  projectId,
  formId,
  definition,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/forms/${encodeURIComponent(
      formId,
    )}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        definition,
      ),
    },
  );
}

export function deleteForm(
  projectId,
  formId,
) {
  return apiFetch(
    `/api/v1/studio/projects/${encodeURIComponent(
      projectId,
    )}/forms/${encodeURIComponent(
      formId,
    )}`,
    {
      method: "DELETE",
    },
  );
}
