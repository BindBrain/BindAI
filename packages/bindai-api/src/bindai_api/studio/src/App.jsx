import {
    workflowToReactFlow,
    reactFlowToWorkflow,
  } from "./workflow/workflowTransform";
import FormDesigner from "./components/FormDesigner";
import CreateProjectDialog from "./components/dialogs/CreateProjectDialog";
import WorkflowEditorHeader from "./components/WorkflowEditorHeader";
import CreateWorkflowDialog from "./components/dialogs/CreateWorkflowDialog";
import CreateAgentDialog from "./components/dialogs/CreateAgentDialog";
import CreateFormDialog from "./components/dialogs/CreateFormDialog";
import RunWorkflowDialog from "./components/dialogs/RunWorkflowDialog";
import BindAINode, {
    getNodeDescription,
  } from "./components/BindAINode";
import NodeIcon from "./components/NodeIcon";
import NodeConfigurationFields from "./components/NodeConfigurationFields";
import StudioSidebar from "./components/StudioSidebar";
import AgentDefinitionEditor from "./components/AgentDefinitionEditor";
import Modal from "./components/Modal";
import { useCallback, useEffect, useState } from "react";
import {
    getApiKey,
    setApiKey,
    validateApiKey,
    getProjects,
    createProject,
    getWorkflows,
    createWorkflow,
    getCapabilities,
    getProviders,
    getWorkflow,
    saveWorkflow,
    deleteWorkflow,
    validateWorkflow,
    runWorkflow,
    resolveHumanTask,
    getAgents,
    getTools,
    getKnowledge,
  getConnections,
  getConnectionProviders,
  createConnection,
  deleteConnection,
  setConnectionCredential,
    uploadKnowledge,
    getAgent,
    saveAgent,
    createAgent,
    getForms,
    createForm,
    getForm,
    saveForm,
    deleteAgent,
    deleteForm,
  } from "./api";
import {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  ReactFlow,
  addEdge,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";

const nodeTypes = {
  bindai: BindAINode,
};

const initialNodes = [
  {
    id: "start",
    type: "bindai",
    position: { x: 80, y: 180 },
    data: {
      label: "Start",
      type: "start",
      configuration: {},
    },
  },
  {
    id: "agent",
    type: "bindai",
    position: { x: 330, y: 180 },
    data: {
      label: "Agent",
      type: "agent",
      configuration: {},
    },
  },
  {
    id: "end",
    type: "bindai",
    position: { x: 620, y: 180 },
    data: {
      label: "End",
      type: "end",
      configuration: {},
    },
  },
];

const initialEdges = [
  {
    id: "start-agent",
    source: "start",
    target: "agent",
  },
  {
    id: "agent-end",
    source: "agent",
    target: "end",
  },
];

function getProjectId(project) {
  if (!project?.path) {
    return "";
  }

  return project.path.split(/[\\/]/).pop();
}

export default function App() {
  const [apiKey, setApiKeyValue] = useState("");
  const [isConnected, setIsConnected] = useState(false);

  const [projects, setProjects] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [providers, setProviders] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);

  const [workflows, setWorkflows] = useState([]);
  const [agents, setAgents] = useState([]);
  const [forms, setForms] = useState([]);
  const [tools, setTools] = useState([]);
  const [knowledge, setKnowledge] = useState([]);
  const [connections, setConnections] = useState([]);
  const [connectionProviders, setConnectionProviders] = useState([]);

  const [selectedForm, setSelectedForm] = useState(null);
  const [formDefinition, setFormDefinition] = useState(null);

  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [workflowDefinition, setWorkflowDefinition] = useState(null);
  const [editingWorkflowTitle, setEditingWorkflowTitle] = useState(false);
  const [workflowTitleDraft, setWorkflowTitleDraft] = useState("");
  const [savingWorkflowTitle, setSavingWorkflowTitle] = useState(false);
  const [deleteWorkflowTarget, setDeleteWorkflowTarget] = useState(null);
  const [deleteAgentTarget, setDeleteAgentTarget] = useState(null);
  const [deleteFormTarget, setDeleteFormTarget] = useState(null);
  const [deletingWorkflow, setDeletingWorkflow] = useState(false);
  const [deletingAgent, setDeletingAgent] = useState(false);
  const [deletingForm, setDeletingForm] = useState(false);

  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentDefinition, setAgentDefinition] = useState(null);

  const [apiError, setApiError] = useState("");

  const [showProjectDialog, setShowProjectDialog] = useState(false);
  const [showWorkflowDialog, setShowWorkflowDialog] = useState(false);
  const [showAgentDialog, setShowAgentDialog] = useState(false);
  const [showFormDialog, setShowFormDialog] = useState(false);
  const [showRunDialog, setShowRunDialog] = useState(false);

  const [newProjectName, setNewProjectName] = useState("");
  const [newWorkflowName, setNewWorkflowName] = useState("");
  const [newWorkflowId, setNewWorkflowId] = useState("");
  const [newAgentName, setNewAgentName] = useState("");
  const [newAgentId, setNewAgentId] = useState("");

  const [newFormName, setNewFormName] = useState("");
  const [newFormId, setNewFormId] = useState("");

  const [runVariables, setRunVariables] = useState(
    '{\n  "input": "Hello from BindAI Studio"\n}',
  );
  const [runResult, setRunResult] = useState(null);
  const [runError, setRunError] = useState("");
  const [runningWorkflow, setRunningWorkflow] = useState(false);
  const [resolvingHumanTask, setResolvingHumanTask] =
  useState(false);

  const [creatingProject, setCreatingProject] = useState(false);
  const [creatingWorkflow, setCreatingWorkflow] = useState(false);
  const [creatingAgent, setCreatingAgent] = useState(false);
  const [creatingForm, setCreatingForm] = useState(false);
  const [savingForm, setSavingForm] = useState(false);
  const [savingBeforeRun, setSavingBeforeRun] = useState(false);
  const [validatingWorkflow, setValidatingWorkflow] = useState(false);

  const [validationDiagnostics, setValidationDiagnostics] =
    useState([]);
  const [hasValidatedWorkflow, setHasValidatedWorkflow] =
    useState(false);

  const [nodes, setNodes, onNodesChange] =
    useNodesState([]);

  const [edges, setEdges, onEdgesChange] =
    useEdgesState([]);

  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);

  const loadProjects = useCallback(async () => {
    setApiError("");

    try {
        const [
          projectResult,
          capabilityResult,
          providerResult,
          connectionProviderResult,
        ] = await Promise.all([
          getProjects(),
          getCapabilities(),
          getProviders(),
          getConnectionProviders(),
        ]);
      setProjects(projectResult);
      setCapabilities(capabilityResult);
        setProviders(providerResult);
      setConnectionProviders(connectionProviderResult);

      return projectResult;
    } catch (error) {
      setApiError(error.message);
      return [];
    }
  }, []);

  /*
   * A stored key is never trusted merely because it exists in
   * localStorage. Revalidate it against the protected API on startup.
   */
  useEffect(() => {
    const storedApiKey = getApiKey();

    setApiKeyValue(storedApiKey);

    if (!storedApiKey) {
      setIsConnected(false);
      return;
    }

    validateApiKey(storedApiKey)
      .then(async () => {
        setIsConnected(true);
        await loadProjects();
      })
      .catch(() => {
        setIsConnected(false);
        setApiError(
          "API key is invalid. Studio remains locked.",
        );
      });
  }, [loadProjects]);

  const loadProjectContents = useCallback(async (project) => {
    if (!isConnected) {
      throw new Error(
        "Studio is locked. Enter a valid API key to continue.",
      );
    }

    const projectId = getProjectId(project);

    if (!projectId) {
      throw new Error(
        "Unable to determine the BindAI project ID.",
      );
    }

    const [
      workflowResult,
      agentResult,
      formResult,
      toolResult,
      knowledgeResult,
      connectionResult,
    ] = await Promise.all([
      getWorkflows(projectId),
      getAgents(projectId),
      getForms(projectId),
      getTools(projectId),
      getKnowledge(projectId),
      getConnections(projectId),
    ]);

    setWorkflows(workflowResult);
    setAgents(agentResult);
    setForms(formResult);
    setTools(toolResult);
    setKnowledge(knowledgeResult);
    setConnections(connectionResult);

    return {
        projectId,
        workflows: workflowResult,
        agents: agentResult,
        forms: formResult,
        tools: toolResult,
      };
  }, [isConnected]);

  const handleKnowledgeUpload = useCallback(
    async (file) => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject || !file) {
        return;
      }

      try {
        const projectId =
          getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        setApiError("");

        await uploadKnowledge(
          projectId,
          file,
        );

        const knowledgeResult =
          await getKnowledge(projectId);

          setKnowledge(knowledgeResult);
    setConnections(connectionResult);
      } catch (error) {
        setApiError(error.message);
      }
    },
    [
      isConnected,
      selectedProject,
    ],
  );

  useEffect(() => {
    const handleUploadEvent = (event) => {
      const file = event.detail?.file;

      if (!file) {
        return;
      }

      void handleKnowledgeUpload(file);
    };

    window.addEventListener(
      "bindai-studio-upload-knowledge",
      handleUploadEvent,
    );

    return () => {
      window.removeEventListener(
        "bindai-studio-upload-knowledge",
        handleUploadEvent,
      );
    };
  }, [handleKnowledgeUpload]);

  const handleProjectSelect = useCallback(
    async (project) => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      setApiError("");
      setSelectedProject(project);
      setSelectedWorkflow(null);
      setWorkflowDefinition(null);
      setWorkflows([]);
      setAgents([]);
      setForms([]);
    setConnections([]);
      setSelectedForm(null);
      setFormDefinition(null);
      setSelectedAgent(null);
      setAgentDefinition(null);
      setSelectedNode(null);
      setSelectedEdge(null);
      setRunResult(null);
      setRunError("");
      setValidationDiagnostics([]);
      setHasValidatedWorkflow(false);
      setNodes([]);
      setEdges([]);

      try {
        await loadProjectContents(project);
      } catch (error) {
        setApiError(error.message);
      }
    },
    [
      isConnected,
      loadProjectContents,
      setNodes,
      setEdges,
    ],
  );

  const handleWorkflowSelect = useCallback(
    async (workflow) => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject) {
        return;
      }

      setApiError("");
      setSelectedWorkflow(workflow);
      setSelectedNode(null);
      setSelectedEdge(null);
      setSelectedForm(null);
      setFormDefinition(null);
      setSelectedAgent(null);
      setAgentDefinition(null);
      setRunResult(null);
      setRunError("");
      setValidationDiagnostics([]);
      setHasValidatedWorkflow(false);

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const definition = await getWorkflow(
          projectId,
          workflow.id,
        );

        setWorkflowDefinition(definition);

        const flow = workflowToReactFlow(definition);

        setNodes(flow.nodes);
        setEdges(flow.edges);
      } catch (error) {
        setApiError(error.message);
      }
    },
    [
      isConnected,
      selectedProject,
      setNodes,
      setEdges,
    ],
  );

  const handleCreateProject = useCallback(
    async (event) => {
      event.preventDefault();

      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      const name = newProjectName.trim();

      if (!name) {
        setApiError("Project name is required.");
        return;
      }

      setCreatingProject(true);
      setApiError("");

      try {
        const result = await createProject(name);
        const refreshedProjects = await loadProjects();

        const createdProject =
          refreshedProjects.find(
            (project) => project.path === result.path,
          ) || {
            name: result.name,
            path: result.path,
            workflow_count: result.workflow_count || 0,
            agent_count: result.agent_count || 0,
          };

        setShowProjectDialog(false);
        setNewProjectName("");

        await handleProjectSelect(createdProject);
      } catch (error) {
        setApiError(error.message);
      } finally {
        setCreatingProject(false);
      }
    },
    [
      isConnected,
      newProjectName,
      loadProjects,
      handleProjectSelect,
    ],
  );

  const handleCreateWorkflow = useCallback(
    async (event) => {
      event.preventDefault();

      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject) {
        setApiError(
          "Select a project before creating a workflow.",
        );
        return;
      }

      const name = newWorkflowName.trim();
      const id = newWorkflowId.trim();

      if (!name) {
        setApiError("Workflow name is required.");
        return;
      }

      setCreatingWorkflow(true);
      setApiError("");

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const result = await createWorkflow(
          projectId,
          name,
          id || null,
        );

        const workflowResult = await getWorkflows(projectId);

        setWorkflows(workflowResult);

        const createdWorkflow =
          workflowResult.find(
            (workflow) =>
              workflow.id === result.workflow.workflow.id,
          ) || {
            id: result.workflow.workflow.id,
            name: result.workflow.workflow.name,
            path: result.path,
          };

        setShowWorkflowDialog(false);
        setNewWorkflowName("");
        setNewWorkflowId("");

        await handleWorkflowSelect(createdWorkflow);
      } catch (error) {
        setApiError(error.message);
      } finally {
        setCreatingWorkflow(false);
      }
    },
    [
      isConnected,
      selectedProject,
      newWorkflowName,
      newWorkflowId,
      handleWorkflowSelect,
    ],
  );

  const handleDeleteWorkflow = useCallback(
    async () => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject || !deleteWorkflowTarget) {
        return;
      }

      setDeletingWorkflow(true);
      setApiError("");

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        await deleteWorkflow(
          projectId,
          deleteWorkflowTarget.id,
        );

        const workflowResult = await getWorkflows(projectId);
        setWorkflows(workflowResult);

        if (
          selectedWorkflow?.id ===
          deleteWorkflowTarget.id
        ) {
          setSelectedWorkflow(null);
          setWorkflowDefinition(null);
          setNodes([]);
          setEdges([]);
        }

        setDeleteWorkflowTarget(null);
      } catch (error) {
        setApiError(error.message);
      } finally {
        setDeletingWorkflow(false);
      }
    },
    [
      isConnected,
      selectedProject,
      deleteWorkflowTarget,
      selectedWorkflow,
      setNodes,
      setEdges,
    ],
  );

    const handleDeleteAgent = useCallback(
    async () => {
        if (!isConnected) {
        setApiError(
            "Studio is locked. Enter a valid API key to continue.",
        );
        return;
        }

        if (!selectedProject || !deleteAgentTarget) {
        return;
        }

        setDeletingAgent(true);
        setApiError("");

        try {
        const projectId = getProjectId(
            selectedProject,
        );

        if (!projectId) {
            throw new Error(
            "Unable to determine the BindAI project ID.",
            );
        }

        await deleteAgent(
            projectId,
            deleteAgentTarget.id,
        );

        const refreshedAgents =
            await getAgents(projectId);

        setAgents(refreshedAgents);

        if (
            selectedAgent ===
            deleteAgentTarget.id
        ) {
            setSelectedAgent(null);
            setAgentDefinition(null);
        }

        if (
            selectedNode?.data?.type === "agent" &&
            selectedNode?.data?.configuration
            ?.agent === deleteAgentTarget.id
        ) {
            setSelectedNode(null);
        }

        setDeleteAgentTarget(null);
        setApiError("");
        } catch (error) {
        setApiError(error.message);
        } finally {
        setDeletingAgent(false);
        }
    },
    [
        isConnected,
        selectedProject,
        deleteAgentTarget,
        selectedAgent,
        selectedNode,
    ],
    );

    const handleDeleteForm = useCallback(
    async () => {
        if (!isConnected) {
        setApiError(
            "Studio is locked. Enter a valid API key to continue.",
        );
        return;
        }

        if (!selectedProject || !deleteFormTarget) {
        return;
        }

        setDeletingForm(true);
        setApiError("");

        try {
        const projectId = getProjectId(
            selectedProject,
        );

        if (!projectId) {
            throw new Error(
            "Unable to determine the BindAI project ID.",
            );
        }

        await deleteForm(
            projectId,
            deleteFormTarget.id,
        );

        const refreshedForms =
            await getForms(projectId);

        setForms(refreshedForms);

        if (
            selectedForm ===
            deleteFormTarget.id
        ) {
            setSelectedForm(null);
            setFormDefinition(null);
        }

        setDeleteFormTarget(null);
        setApiError("");
        } catch (error) {
        setApiError(error.message);
        } finally {
        setDeletingForm(false);
        }
    },
    [
        isConnected,
        selectedProject,
        deleteFormTarget,
        selectedForm,
    ],
    );

  const handleCreateAgent = useCallback(
    async (event) => {
      event.preventDefault();

      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject) {
        setApiError(
          "Select a project before creating an agent.",
        );
        return;
      }

      const name = newAgentName.trim();
      const id = newAgentId.trim();

      if (!name) {
        setApiError("Agent name is required.");
        return;
      }

      setCreatingAgent(true);
      setApiError("");

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const result = await createAgent(
          projectId,
          name,
          id || null,
        );

        const refreshedAgents = await getAgents(projectId);

        setAgents(refreshedAgents);

        setSelectedAgent(result.agent.id);
        setAgentDefinition(result.agent);

        setShowAgentDialog(false);
        setNewAgentName("");
        setNewAgentId("");

        setApiError("");
      } catch (error) {
        setApiError(error.message);
      } finally {
        setCreatingAgent(false);
      }
    },
    [
      isConnected,
      selectedProject,
      newAgentName,
      newAgentId,
    ],
  );

  const handleCreateForm = useCallback(
    async (event) => {
      event.preventDefault();

      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject) {
        setApiError(
          "Select a project before creating a form.",
        );
        return;
      }

      const name = newFormName.trim();
      const id = newFormId.trim();

      if (!name) {
        setApiError("Form name is required.");
        return;
      }

      setCreatingForm(true);
      setApiError("");

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const result = await createForm(
          projectId,
          name,
          id || null,
        );

        const refreshedForms = await getForms(projectId);

        setForms(refreshedForms);

        const createdForm =
          refreshedForms.find(
            (form) => form.id === result.form.form.id,
          ) || {
            id: result.form.form.id,
            name: result.form.form.name,
            path: result.path,
          };

        setSelectedForm(createdForm.id);
        setFormDefinition(result.form.form);

        setShowFormDialog(false);
        setNewFormName("");
        setNewFormId("");
        setSelectedNode(null);
        setSelectedEdge(null);
        setSelectedAgent(null);
        setAgentDefinition(null);
        setApiError("");
      } catch (error) {
        setApiError(error.message);
      } finally {
        setCreatingForm(false);
      }
    },
    [
      isConnected,
      selectedProject,
      newFormName,
      newFormId,
    ],
  );

  const handleFormSelect = useCallback(
    async (form) => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedProject) {
        return;
      }

      setApiError("");
      setSelectedForm(form.id);
      setSelectedNode(null);
      setSelectedEdge(null);
      setSelectedAgent(null);
      setAgentDefinition(null);

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const result = await getForm(
          projectId,
          form.id,
        );

        setFormDefinition(result.form.form);
      } catch (error) {
        setApiError(error.message);
      }
    },
    [isConnected, selectedProject],
  );

  const handleFormSave = useCallback(async () => {
    if (!isConnected) {
      setApiError(
        "Studio is locked. Enter a valid API key to continue.",
      );
      return;
    }

    if (
      !selectedProject ||
      !selectedForm ||
      !formDefinition
    ) {
      setApiError("Select a form before saving.");
      return;
    }

    setSavingForm(true);
    setApiError("");

    try {
      const projectId = getProjectId(selectedProject);

      if (!projectId) {
        throw new Error(
          "Unable to determine the BindAI project ID.",
        );
      }

      const result = await saveForm(
        projectId,
        selectedForm,
        {
          form: formDefinition,
        },
      );

      setFormDefinition(result.form.form);

      const refreshedForms = await getForms(projectId);
      setForms(refreshedForms);
      setApiError("");
    } catch (error) {
      setApiError(error.message);
    } finally {
      setSavingForm(false);
    }
  }, [
    isConnected,
    selectedProject,
    selectedForm,
    formDefinition,
  ]);

  const updateFormField = useCallback(
    (fieldId, property, value) => {
      setFormDefinition((current) => {
        if (!current) {
          return current;
        }

        return {
          ...current,
          fields: (current.fields || []).map((field) =>
            field.id === fieldId
              ? {
                  ...field,
                  [property]: value,
                }
              : field,
          ),
        };
      });
    },
    [],
  );

  const addFormField = useCallback(() => {
    setFormDefinition((current) => {
      if (!current) {
        return current;
      }

      const fields = current.fields || [];

      let fieldId = "field";
      let suffix = 2;

      while (
        fields.some((field) => field.id === fieldId)
      ) {
        fieldId = `field-${suffix}`;
        suffix += 1;
      }

      return {
        ...current,
        fields: [
          ...fields,
          {
            id: fieldId,
            type: "text",
            label: "New Field",
            required: false,
          },
        ],
      };
    });
  }, []);

  const removeFormField = useCallback((fieldId) => {
    setFormDefinition((current) => {
      if (!current) {
        return current;
      }

      return {
        ...current,
        fields: (current.fields || []).filter(
          (field) => field.id !== fieldId,
        ),
      };
    });
  }, []);

  const buildCurrentWorkflowDefinition = useCallback(() => {
    if (!workflowDefinition) {
      throw new Error(
        "Workflow definition is not loaded.",
      );
    }

    return reactFlowToWorkflow(
      workflowDefinition,
      nodes,
      edges,
    );
  }, [workflowDefinition, nodes, edges]);

  const handleWorkflowSave = useCallback(async () => {
    if (!isConnected) {
      setApiError(
        "Studio is locked. Enter a valid API key to continue.",
      );
      return null;
    }

    if (
      !selectedProject ||
      !selectedWorkflow ||
      !workflowDefinition
    ) {
      setApiError("Select a workflow before saving.");
      return null;
    }

    setApiError("");

    try {
      const projectId = getProjectId(selectedProject);

      if (!projectId) {
        throw new Error(
          "Unable to determine the BindAI project ID.",
        );
      }

      const definition = buildCurrentWorkflowDefinition();

      const result = await saveWorkflow(
        projectId,
        selectedWorkflow.id,
        definition,
      );

      setWorkflowDefinition(result.workflow);

      if (result.diagnostics?.length > 0) {
        setApiError(
          result.diagnostics
            .map((diagnostic) => diagnostic.message)
            .join(" "),
        );
      }

      return result;
    } catch (error) {
      setApiError(error.message);
      return null;
    }
  }, [
    isConnected,
    selectedProject,
    selectedWorkflow,
    workflowDefinition,
    buildCurrentWorkflowDefinition,
  ]);

  const handleValidateWorkflow = useCallback(async () => {
    if (!isConnected) {
      setApiError(
        "Studio is locked. Enter a valid API key to continue.",
      );
      return;
    }

    if (!selectedProject || !selectedWorkflow) {
      setApiError("Select a workflow before validating.");
      return;
    }

    const projectId = getProjectId(selectedProject);

    if (!projectId) {
      setApiError("Unable to determine the BindAI project ID.");
      return;
    }

    setValidatingWorkflow(true);
    setApiError("");
    setValidationDiagnostics([]);
    setHasValidatedWorkflow(false);

    try {
      /*
       * Validation operates on the canonical workflow definition saved
       * in the project. Save first so the backend validates exactly what
       * the project currently contains.
       */
      const saveResult = await handleWorkflowSave();

      if (!saveResult) {
        throw new Error(
          "Workflow could not be saved. Fix the workflow save error before validating.",
        );
      }

      const diagnostics = await validateWorkflow(
        projectId,
        selectedWorkflow.id,
      );

      setValidationDiagnostics(
        Array.isArray(diagnostics) ? diagnostics : [],
      );
      setHasValidatedWorkflow(true);
    } catch (error) {
      setApiError(error.message);
    } finally {
      setValidatingWorkflow(false);
    }
  }, [
    isConnected,
    selectedProject,
    selectedWorkflow,
    handleWorkflowSave,
  ]);

  const handleRunWorkflow = useCallback(async () => {
    if (!isConnected) {
      setRunError(
        "Studio is locked. Enter a valid API key to continue.",
      );
      return;
    }

    if (!selectedProject || !selectedWorkflow) {
      setRunError("Select a workflow before running.");
      return;
    }

    let variables = {};

    try {
      const parsed = JSON.parse(runVariables || "{}");

      if (
        parsed === null ||
        Array.isArray(parsed) ||
        typeof parsed !== "object"
      ) {
        throw new Error(
          "Run variables must be a JSON object.",
        );
      }

      variables = parsed;
    } catch (error) {
      setRunError(
        `Invalid run variables JSON: ${error.message}`,
      );
      return;
    }

    const projectId = getProjectId(selectedProject);

    if (!projectId) {
      setRunError(
        "Unable to determine the BindAI project ID.",
      );
      return;
    }

    setRunningWorkflow(true);
    setSavingBeforeRun(true);
    setRunError("");
    setRunResult(null);

    try {
      /*
       * Run always persists the current canvas first.
       *
       * This means Studio never executes an older workflow definition
       * while the user is looking at a newer unsaved graph.
       */
      const saveResult = await handleWorkflowSave();

      if (!saveResult) {
        throw new Error(
          "Workflow could not be saved. Fix the workflow save error before running.",
        );
      }

      setSavingBeforeRun(false);

      const result = await runWorkflow(
        projectId,
        selectedWorkflow.id,
        variables,
      );

      setRunResult(result);
      setRunError("");
    } catch (error) {
      setRunError(error.message);
    } finally {
      setSavingBeforeRun(false);
      setRunningWorkflow(false);
    }
  }, [
    isConnected,
    selectedProject,
    selectedWorkflow,
    runVariables,
    handleWorkflowSave,
  ]);

  const handleResolveHumanTask = useCallback(
    async (action) => {
      if (!isConnected) {
        setRunError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (
        !selectedProject ||
        !selectedWorkflow ||
        !runResult?.instance_id
      ) {
        setRunError(
          "No waiting workflow instance is available.",
        );
        return;
      }

      const projectId = getProjectId(selectedProject);

      if (!projectId) {
        setRunError(
          "Unable to determine the BindAI project ID.",
        );
        return;
      }

      setResolvingHumanTask(true);
      setRunError("");

      try {
        const result = await resolveHumanTask(
          projectId,
          selectedWorkflow.id,
          runResult.instance_id,
          action,
        );

        setRunResult(result);
        setRunError("");
      } catch (error) {
        setRunError(error.message);
      } finally {
        setResolvingHumanTask(false);
      }
    },
    [
      isConnected,
      selectedProject,
      selectedWorkflow,
      runResult,
    ],
  );

  const handleAgentSave = useCallback(async () => {
    if (!isConnected) {
      setApiError(
        "Studio is locked. Enter a valid API key to continue.",
      );
      return;
    }

    if (!selectedProject || !selectedAgent || !agentDefinition) {
      setApiError("Select an agent before saving.");
      return;
    }

    setApiError("");

    try {
      const projectId = getProjectId(selectedProject);

      if (!projectId) {
        throw new Error(
          "Unable to determine the BindAI project ID.",
        );
      }

      if (
        !agentDefinition.id ||
        agentDefinition.id !== selectedAgent
      ) {
        throw new Error(
          "Agent ID cannot be changed while editing a saved agent.",
        );
      }

      console.log(
        "SAVE AGENT DEFINITION",
        agentDefinition,
      );

      const result = await saveAgent(
        projectId,
        selectedAgent,
        agentDefinition,
      );

      setAgentDefinition(result.agent);

      const refreshedAgents = await getAgents(projectId);
      setAgents(refreshedAgents);

      setApiError("");
    } catch (error) {
      setApiError(error.message);
    }
  }, [
    isConnected,
    selectedProject,
    selectedAgent,
    agentDefinition,
  ]);

  const handleAgentSelect = useCallback(
    async (agent) => {
      if (!isConnected || !selectedProject) {
        return;
      }

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error("Selected project has no ID.");
        }

        const definition = await getAgent(
          projectId,
          agent.id,
        );

        setSelectedAgent(agent.id);
        setAgentDefinition(definition.agent);
        setSelectedEdge(null);
        setApiError("");

        if (selectedNode?.data?.type === "agent") {
            const updatedNode = {
              ...selectedNode,
              data: {
                ...selectedNode.data,
                configuration: {
                  ...(selectedNode.data?.configuration || {}),
                  agent: agent.id,
                },
              },
            };

            setSelectedNode(updatedNode);

            setNodes((currentNodes) =>
              currentNodes.map((node) =>
                node.id === selectedNode.id
                  ? updatedNode
                  : node,
              ),
            );
          }
      } catch (error) {
        setApiError(error.message);
      }
    },
    [
        isConnected,
        selectedNode,
        selectedProject,
        setNodes,
      ],
  );
  const handleAddNode = useCallback(
    (capability) => {
      if (!isConnected) {
        setApiError(
          "Studio is locked. Enter a valid API key to continue.",
        );
        return;
      }

      if (!selectedWorkflow) {
        setApiError(
          "Select a workflow before adding a node.",
        );
        return;
      }

      const baseId =
        capability.label
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-|-$/g, "") || "node";

      let nodeId = baseId;
      let suffix = 2;

      while (nodes.some((node) => node.id === nodeId)) {
        nodeId = `${baseId}-${suffix}`;
        suffix += 1;
      }

      const configuration = {};

      for (const field of capability.configuration || []) {
        if (
          field.default !== null &&
          field.default !== undefined
        ) {
          configuration[field.name] = field.default;
        }
      }

      const newNode = {
        id: nodeId,
        type: "bindai",
        position: {
          x: 160 + (nodes.length % 3) * 260,
          y: 120 + Math.floor(nodes.length / 3) * 160,
        },
        data: {
          label: capability.label,
          type: capability.type
            .replace(/Node$/, "")
            .toLowerCase(),
          configuration,
        },
      };

      setNodes((currentNodes) => [
        ...currentNodes,
        newNode,
      ]);

      setSelectedNode(newNode);
      setSelectedForm(null);
      setFormDefinition(null);
      setSelectedAgent(null);
      setAgentDefinition(null);
      setApiError("");
    },
    [
      isConnected,
      selectedWorkflow,
      nodes,
      setNodes,
    ],
  );

  const handleNodeConfigurationChange = useCallback(
    async (field, value) => {
      if (!isConnected) {
        return;
      }

      if (!selectedNode) {
        return;
      }

      setNodes((currentNodes) =>
        currentNodes.map((node) => {
          if (node.id !== selectedNode.id) {
            return node;
          }

          const updatedNode = {
            ...node,
            data: {
              ...node.data,
              configuration: {
                ...(node.data?.configuration || {}),
                ...(field === "tool"
                  ? {
                      tool: value,
                      parameter_mapping: {},
                    }
                  : {
                      [field]: value,
                    }),
              },
            },
          };

          setSelectedNode(updatedNode);

          return updatedNode;
        }),
      );

      if (
        field !== "agent" ||
        selectedNode.data?.type !== "agent"
      ) {
        return;
      }

      if (!selectedProject || !value) {
        setSelectedAgent(null);
        setAgentDefinition(null);
        return;
      }

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const definition = await getAgent(
          projectId,
          value,
        );

        setSelectedAgent(value);
        setAgentDefinition(definition.agent);
        setApiError("");
      } catch (error) {
        setSelectedAgent(value);
        setAgentDefinition(null);
        setApiError(error.message);
      }
    },
    [
      isConnected,
      selectedNode,
      selectedProject,
      setNodes,
    ],
  );

  const handleDeleteNode = useCallback(() => {
    if (!isConnected) {
      return;
    }

    if (!selectedNode) {
      return;
    }

    const nodeId = selectedNode.id;

    setNodes((currentNodes) =>
      currentNodes.filter((node) => node.id !== nodeId),
    );

    setEdges((currentEdges) =>
      currentEdges.filter(
        (edge) =>
          edge.source !== nodeId &&
          edge.target !== nodeId,
      ),
    );

    setSelectedNode(null);
    setSelectedEdge(null);
    setSelectedAgent(null);
    setAgentDefinition(null);
    setApiError("");
  }, [
    isConnected,
    selectedNode,
    setNodes,
    setEdges,
  ]);

  const handleDeleteEdge = useCallback(() => {
    if (!isConnected) {
      return;
    }

    if (!selectedEdge) {
      return;
    }

    const edgeId = selectedEdge.id;

    setEdges((currentEdges) =>
      currentEdges.filter((edge) => edge.id !== edgeId),
    );

    setSelectedEdge(null);
    setSelectedNode(null);
    setApiError("");
  }, [
    isConnected,
    selectedEdge,
    setEdges,
  ]);

  const handleApiKeySave = async () => {
    const value = apiKey.trim();

    if (!value) {
      setIsConnected(false);
      setApiError("API key is required.");
      return;
    }

    /*
     * Lock immediately while the supplied key is being checked.
     * This prevents an old valid session from remaining editable
     * while a new key is being tested.
     */
    setIsConnected(false);
    setApiError("");

    try {
      /*
       * validateApiKey() sends this exact key directly to the
       * protected API without first storing it.
       */
      await validateApiKey(value);

      /*
       * Only store the key after the server accepts it.
       */
      setApiKey(value);
      setIsConnected(true);

      await loadProjects();
    } catch (error) {
      setIsConnected(false);

      setShowProjectDialog(false);
      setShowWorkflowDialog(false);
      setShowAgentDialog(false);
      setShowRunDialog(false);

      setApiError(
        error.message === "Invalid or missing API key."
          ? "Invalid API key. Studio remains locked."
          : error.message,
      );
    }
  };

  const onConnect = useCallback(
    (connection) => {
      if (!isConnected) {
        return;
      }

      const sourceNode = nodes.find(
        (node) => node.id === connection.source,
      );

      const sourceType = String(
        sourceNode?.data?.type || "",
      ).toLowerCase();

      const sourceHandle =
        connection.sourceHandle || null;

      const branchTypes = new Set([
        "condition",
        "conditionnode",
        "decision",
        "decisionnode",
      ]);

      const loopTypes = new Set([
        "loop",
        "loopnode",
      ]);

      const humanTaskTypes = new Set([
        "humantask",
        "human_task",
        "humantasknode",
      ]);

      if (branchTypes.has(sourceType)) {
        if (!["true", "false"].includes(sourceHandle)) {
          setApiError(
            "Condition and Decision nodes require a true or false output.",
          );
          return;
        }
      }

      if (loopTypes.has(sourceType)) {
        if (!["body", "exit"].includes(sourceHandle)) {
          setApiError(
            "Loop nodes require a body or exit output.",
          );
          return;
        }
      }

      if (humanTaskTypes.has(sourceType)) {
        if (
          !["approved", "rejected"].includes(
            sourceHandle,
          )
        ) {
          setApiError(
            "Human Approval nodes require an approved or rejected output.",
          );
          return;
        }
      }

      if (
        sourceHandle &&
        nodes.some(
          (node) => node.id === connection.source,
        )
      ) {
        const duplicateBranch = edges.some(
          (edge) =>
            edge.source === connection.source &&
            edge.sourceHandle === sourceHandle,
        );

        if (duplicateBranch) {
          setApiError(
            `The '${sourceHandle}' branch is already connected.`,
          );
          return;
        }
      }

      const edge = {
        ...connection,
      };

      setEdges((currentEdges) =>
        addEdge(edge, currentEdges),
      );
      setApiError("");
    },
    [
      isConnected,
      nodes,
      edges,
      setEdges,
    ],
  );
  const onNodeClick = useCallback(
    async (_, node) => {
      if (!isConnected) {
        return;
      }

      setSelectedNode(node);
      setSelectedEdge(null);
      setSelectedForm(null);
      setFormDefinition(null);
      setSelectedAgent(null);
      setAgentDefinition(null);

      if (
        node.data?.type !== "agent" ||
        !selectedProject
      ) {
        return;
      }

      const agentId = node.data?.configuration?.agent;

      if (!agentId) {
        return;
      }

      try {
        const projectId = getProjectId(selectedProject);

        if (!projectId) {
          throw new Error(
            "Unable to determine the BindAI project ID.",
          );
        }

        const definition = await getAgent(
          projectId,
          agentId,
        );

        setSelectedAgent(agentId);
        setAgentDefinition(definition.agent);
        setApiError("");
      } catch (error) {
        setApiError(error.message);
      }
    },
    [isConnected, selectedProject],
  );

  const handleCanvasEdgeClick = useCallback(
    (event, edge) => {
      event.stopPropagation();
      setSelectedEdge(edge);
      setSelectedNode(null);
      setSelectedForm(null);
      setFormDefinition(null);
      setSelectedAgent(null);
      setAgentDefinition(null);
      setApiError("");
    },
    [],
  );

  const handleCanvasPaneClick = useCallback(() => {
    setSelectedNode(null);
    setSelectedForm(null);
    setFormDefinition(null);
    setSelectedEdge(null);
    setSelectedAgent(null);
    setAgentDefinition(null);
  }, []);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (!isConnected) {
        return;
      }

      if (
        event.key !== "Delete" &&
        event.key !== "Backspace"
      ) {
        return;
      }

      const target = event.target;

      if (
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        target instanceof HTMLSelectElement ||
        target?.isContentEditable
      ) {
        return;
      }

      if (selectedNode) {
        event.preventDefault();
        handleDeleteNode();
        return;
      }

      if (selectedEdge) {
        event.preventDefault();
        handleDeleteEdge();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener(
        "keydown",
        handleKeyDown,
      );
    };
  }, [
    isConnected,
    selectedNode,
    selectedEdge,
    handleDeleteNode,
    handleDeleteEdge,
  ]);

  return (
    <div className="studio">
      <header className="studio-header">
        <div className="brand">
          <strong>BindAI</strong>
          <span>Studio</span>
        </div>

        <div className="toolbar">
          <button
            onClick={handleWorkflowSave}
            disabled={
              !isConnected ||
              !selectedWorkflow ||
              runningWorkflow
            }
          >
            Save
          </button>

          <button
            onClick={handleValidateWorkflow}
            disabled={
              !isConnected ||
              !selectedWorkflow ||
              runningWorkflow ||
              validatingWorkflow
            }
          >
            {validatingWorkflow
              ? "Validating..."
              : "Validate"}
          </button>

          <button
            className="run-button"
            disabled={
              !isConnected ||
              !selectedWorkflow ||
              runningWorkflow
            }
            onClick={() => {
              setRunError("");
              setRunResult(null);
              setShowRunDialog(true);
            }}
          >
            {runningWorkflow ? "Running..." : "Run"}
          </button>
        </div>
      </header>

      <div className="studio-body">

        <StudioSidebar
        apiKey={apiKey}
        setApiKeyValue={setApiKeyValue}
        handleApiKeySave={handleApiKeySave}
        apiError={apiError}
        isConnected={isConnected}
        projects={projects}
        selectedProject={selectedProject}
        handleProjectSelect={handleProjectSelect}
        setShowProjectDialog={setShowProjectDialog}
        workflows={workflows}
        selectedWorkflow={selectedWorkflow}
        handleWorkflowSelect={handleWorkflowSelect}
        setShowWorkflowDialog={setShowWorkflowDialog}
        setDeleteWorkflowTarget={setDeleteWorkflowTarget}
        forms={forms}
        selectedForm={selectedForm}
        handleFormSelect={handleFormSelect}
        setDeleteFormTarget={setDeleteFormTarget}
        setNewFormName={setNewFormName}
        setNewFormId={setNewFormId}
        setShowFormDialog={setShowFormDialog}
        agents={agents}
        handleAgentSelect={handleAgentSelect}
        setDeleteAgentTarget={setDeleteAgentTarget}
        knowledge={knowledge}
        connections={connections}
        connectionProviders={connectionProviders}
        onCreateConnection={async (connection) => {
          const projectId = getProjectId(selectedProject);
          const result = await createConnection(projectId, connection);
          setConnections((current) => [...current, result]);
        }}
        onSetConnectionCredential={async (name, credential) => {
          const projectId = getProjectId(selectedProject);
          await setConnectionCredential(projectId, name, credential);
          setConnections((current) =>
            current.map((connection) =>
              connection.name === name
                ? { ...connection, configured: true }
                : connection,
            ),
          );
        }}
        onDeleteConnection={async (name) => {
          const projectId = getProjectId(selectedProject);
          await deleteConnection(projectId, name);
          setConnections((current) =>
            current.filter((connection) => connection.name !== name),
          );
        }}
        setNewAgentName={setNewAgentName}
        setNewAgentId={setNewAgentId}
        setShowAgentDialog={setShowAgentDialog}
        capabilities={capabilities}
        handleAddNode={handleAddNode}
        setApiError={setApiError}
        />

        <main className="editor">
          <WorkflowEditorHeader
  selectedWorkflow={selectedWorkflow}
  editingWorkflowTitle={editingWorkflowTitle}
  setEditingWorkflowTitle={setEditingWorkflowTitle}
  workflowTitleDraft={workflowTitleDraft}
  setWorkflowTitleDraft={setWorkflowTitleDraft}
  savingWorkflowTitle={savingWorkflowTitle}
  setSavingWorkflowTitle={setSavingWorkflowTitle}
  setApiError={setApiError}
  selectedProject={selectedProject}
  workflowDefinition={workflowDefinition}
  setSelectedWorkflow={setSelectedWorkflow}
  setWorkflowDefinition={setWorkflowDefinition}
  setWorkflows={setWorkflows}
  getProjectId={getProjectId}
  savingBeforeRun={savingBeforeRun}
  runningWorkflow={runningWorkflow}
  validatingWorkflow={validatingWorkflow}
/>
<div className="validation-panel">
              <div className="validation-panel-header">
                <strong>Validation Results</strong>

                <span>
                  {validationDiagnostics.length}{" "}
                  {validationDiagnostics.length === 1
                    ? "diagnostic"
                    : "diagnostics"}
                </span>
              </div>

              <div className="validation-diagnostics">
                {validationDiagnostics.map(
                  (diagnostic, index) => (
                    <div
                    className={`validation-diagnostic validation-${String(
                        diagnostic.severity || "error",
                    ).toLowerCase()}`}
                    key={`${diagnostic.code || "diagnostic"}-${index}`}
                    role={diagnostic.node_id ? "button" : undefined}
                    tabIndex={diagnostic.node_id ? 0 : undefined}
                    onClick={() => {
                        if (!diagnostic.node_id) {
                        return;
                        }

                        const node = nodes.find(
                        (item) => item.id === diagnostic.node_id,
                        );

                        if (!node) {
                        return;
                        }

                        setSelectedNode(node);
                        setSelectedEdge(null);
                        setSelectedForm(null);
                        setFormDefinition(null);
                        setSelectedAgent(null);
                        setAgentDefinition(null);
                    }}
                    onKeyDown={(event) => {
                        if (
                        !diagnostic.node_id ||
                        (event.key !== "Enter" &&
                            event.key !== " ")
                        ) {
                        return;
                        }

                        event.preventDefault();

                        const node = nodes.find(
                        (item) => item.id === diagnostic.node_id,
                        );

                        if (!node) {
                        return;
                        }

                        setSelectedNode(node);
                        setSelectedEdge(null);
                        setSelectedForm(null);
                        setFormDefinition(null);
                        setSelectedAgent(null);
                        setAgentDefinition(null);
                    }}
                    >
                      <div className="validation-diagnostic-severity">
                        {diagnostic.severity || "error"}
                      </div>

                      <div className="validation-diagnostic-content">
                        <strong>
                          {diagnostic.message ||
                            "Workflow validation issue."}
                        </strong>

                        {(diagnostic.node_id ||
                          diagnostic.path ||
                          diagnostic.code) && (
                          <div className="validation-diagnostic-meta">
                            {diagnostic.node_id && (
                              <span>
                                Node: {diagnostic.node_id}
                              </span>
                            )}

                            {diagnostic.path && (
                              <span>
                                Path: {diagnostic.path}
                              </span>
                            )}

                            {diagnostic.code && (
                              <span>
                                Code: {diagnostic.code}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ),
                )}
              </div>
            </div>


          {selectedWorkflow &&
            hasValidatedWorkflow &&
            !validatingWorkflow &&
            validationDiagnostics.length === 0 && (
              <div className="validation-success">
                Workflow validation passed.
              </div>
            )}

            <div className="canvas">
            {!selectedProject && (
                <div className="canvas-empty-state">
                <strong>Select or create a project</strong>
                <span>
                    Choose a project to start building a workflow.
                </span>
                </div>
            )}

            {selectedProject && !selectedWorkflow && (
                <div className="canvas-empty-state">
                <strong>Select or create a workflow</strong>
                <span>
                    Choose a workflow to open it in the editor.
                </span>
                </div>
            )}

            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                onNodesChange={
                isConnected ? onNodesChange : undefined
                }
                onEdgesChange={
                isConnected ? onEdgesChange : undefined
                }
                onConnect={
                isConnected ? onConnect : undefined
                }
                onNodeClick={
                isConnected ? onNodeClick : undefined
                }
                onEdgeClick={handleCanvasEdgeClick}
                onPaneClick={handleCanvasPaneClick}
                fitView
                colorMode="light"
            >
                <Background
                variant={BackgroundVariant.Dots}
                gap={20}
                size={1}
                />

                <Controls />
                <MiniMap />
            </ReactFlow>
            </div>
        </main>

<aside className="inspector">
  <div className="panel-heading">
    Inspector
  </div>

  {selectedNode && (
    <div className="inspector-danger-action">
      <button
        type="button"
        onClick={handleDeleteNode}
        disabled={!isConnected}
        title="Delete selected node and its connections"
      >
        <span className="delete-icon">
          <svg
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M4 7h16" />
            <path d="M10 11v6M14 11v6" />
            <path d="M6 7l1 13h10l1-13" />
            <path d="M9 7V4h6v3" />
          </svg>
        </span>
        Delete Node
      </button>
    </div>
  )}

  {selectedEdge && (
    <div className="inspector-danger-action">
      <button
        type="button"
        onClick={handleDeleteEdge}
        disabled={!isConnected}
        title="Delete selected connector"
      >
        <span className="delete-icon">
          <svg
            width="13"
            height="13"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M6 7h12" />
            <path d="M9 7V4h6v3" />
            <path d="m8 11 8 8M16 11l-8 8" />
          </svg>
        </span>
        Delete Connector
      </button>
    </div>
  )}

  {runResult && !showRunDialog && (
    <div className="inspector-content">
      <div className="inspector-section-title">
        Last Run
      </div>

      <pre
        style={{
          margin: 0,
          padding: "12px",
          borderRadius: "8px",
          background: "#f6f7f9",
          border: "1px solid #e2e5e9",
          overflow: "auto",
          maxHeight: "320px",
          fontSize: "12px",
          lineHeight: 1.5,
        }}
      >
        {JSON.stringify(runResult, null, 2)}
      </pre>
    </div>
  )}

  {/*
    ------------------------------------------------------------------------
    FORM DESIGNER
    ------------------------------------------------------------------------
    A selected Form is independent from selectedNode.

    This must NOT be nested inside the node inspector because a Form is a
    project resource, not a workflow node.
  */}
  {selectedForm ? (
              <FormDesigner
                formDefinition={formDefinition}
                setFormDefinition={setFormDefinition}
                isConnected={isConnected}
                handleFormSave={handleFormSave}
                savingForm={savingForm}
              />
            ) : selectedNode ? (
    <div className="inspector-content">
      {(() => {
        const nodeType =
          selectedNode.data?.type || "default";

        const capability = capabilities.find(
          (item) =>
            item.type
              ?.replace(/Node$/, "")
              .toLowerCase() === nodeType,
        );

        const configuration =
          selectedNode.data?.configuration || {};

          const renderField = (field) => (
            <NodeConfigurationFields
              key={field.name}
              field={field}
              nodeType={nodeType}
              selectedNode={selectedNode}
              tools={tools}
              agents={agents}
    workflows={workflows}
              forms={forms}
              isConnected={isConnected}
              handleNodeConfigurationChange={
                handleNodeConfigurationChange
              }
            />
          );

        return (
          <>
            <div className="inspector-field">
              <label>Node</label>

              <input
                value={
                  selectedNode.data?.label || ""
                }
                readOnly
              />
            </div>

            <div className="inspector-field">
              <label>Type</label>

              <input
                value={nodeType}
                readOnly
              />
            </div>

            <div className="inspector-field">
              <label>ID</label>

              <input
                value={selectedNode.id}
                readOnly
              />
            </div>

            {capability?.configuration?.length > 0 ? (
              <>
                <div className="inspector-section-title">
                  Configuration
                </div>

                {capability.configuration.map(
                  renderField,
                )}
              </>
            ) : (
              <div className="empty-inspector">
                This node has no configurable
                properties.
              </div>
            )}

            {(() => {
              const graphNodeType =
                String(selectedNode.data?.type || "").toLowerCase();

              const outgoingEdges = edges.filter(
                (edge) => edge.source === selectedNode.id,
              );

              const incomingEdges = edges.filter(
                (edge) => edge.target === selectedNode.id,
              );

              const getNodeLabel = (nodeId) => {
                const node = nodes.find(
                  (item) => item.id === nodeId,
                );

                return node?.data?.label || nodeId;
              };

              const branchTarget = (handle) =>
                outgoingEdges.find(
                  (edge) => edge.sourceHandle === handle,
                );

              const branchStatus = (handle) => {
                const edge = branchTarget(handle);

                return edge
                  ? getNodeLabel(edge.target)
                  : "Not connected";
              };

              const showBranchInspector =
                graphNodeType === "condition" ||
                graphNodeType === "conditionnode" ||
                graphNodeType === "decision" ||
                graphNodeType === "decisionnode" ||
                graphNodeType === "loop" ||
                graphNodeType === "loopnode";

              const showParallelInspector =
                graphNodeType === "parallel" ||
                graphNodeType === "parallelnode";

              const showJoinInspector =
                graphNodeType === "join" ||
                graphNodeType === "joinnode";

              if (
                !showBranchInspector &&
                !showParallelInspector &&
                !showJoinInspector
              ) {
                return null;
              }

              const branchDefinitions =
                graphNodeType === "loop" ||
                graphNodeType === "loopnode"
                  ? [
                      ["body", "Body"],
                      ["exit", "Exit"],
                    ]
                  : [
                      ["true", "True"],
                      ["false", "False"],
                    ];

              return (
                <>
                  <div className="inspector-section-title">
                    Connections
                  </div>

                  {showBranchInspector && (
                    <div className="inspector-connection-list">
                      {branchDefinitions.map(
                        ([handle, label]) => (
                          <div
                            className="inspector-connection-row"
                            key={handle}
                          >
                            <span>{label}</span>
                            <span>
                              {branchStatus(handle)}
                            </span>
                          </div>
                        ),
                      )}
                    </div>
                  )}

                  {showParallelInspector && (
                    <div className="inspector-connection-list">
                      <div className="inspector-connection-row">
                        <span>Outgoing branches</span>
                        <span>
                          {outgoingEdges.length}
                        </span>
                      </div>

                      {outgoingEdges.map((edge) => (
                        <div
                          className="inspector-connection-row"
                          key={edge.id}
                        >
                          <span>Branch</span>
                          <span>
                            {getNodeLabel(edge.target)}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {showJoinInspector && (
                    <div className="inspector-connection-list">
                      <div className="inspector-connection-row">
                        <span>Incoming branches</span>
                        <span>
                          {incomingEdges.length}
                        </span>
                      </div>

                      {incomingEdges.map((edge) => (
                        <div
                          className="inspector-connection-row"
                          key={edge.id}
                        >
                          <span>Branch</span>
                          <span>
                            {getNodeLabel(edge.source)}
                          </span>
                        </div>
                      ))}

                      <div className="inspector-connection-row">
                        <span>Expected</span>
                        <span>
                          {configuration.expected ??
                            "Not configured"}
                        </span>
                      </div>
                    </div>
                  )}
                </>
              );
            })()}

            {selectedNode.data?.type === "agent" && (
            <AgentDefinitionEditor
                agentDefinition={agentDefinition}
                setAgentDefinition={setAgentDefinition}
                isConnected={isConnected}
                handleAgentSave={handleAgentSave}
                providers={providers}
                knowledge={knowledge}
            />
            )}

          </>
        );
      })()}
    </div>
  ) : (
    !runResult && (
      <div className="empty-inspector">
        Select a node or form to inspect it.
      </div>
    )
  )}
</aside>
      </div>

      <CreateProjectDialog
  Modal={Modal}
  showProjectDialog={showProjectDialog}
  isConnected={isConnected}
  creatingProject={creatingProject}
  newProjectName={newProjectName}
  setShowProjectDialog={setShowProjectDialog}
  setNewProjectName={setNewProjectName}
  handleCreateProject={handleCreateProject}
/>

<CreateWorkflowDialog
  Modal={Modal}
  showWorkflowDialog={showWorkflowDialog}
  selectedProject={selectedProject}
  isConnected={isConnected}
  creatingWorkflow={creatingWorkflow}
  newWorkflowName={newWorkflowName}
  newWorkflowId={newWorkflowId}
  setShowWorkflowDialog={setShowWorkflowDialog}
  setNewWorkflowName={setNewWorkflowName}
  setNewWorkflowId={setNewWorkflowId}
  handleCreateWorkflow={handleCreateWorkflow}
/>

<CreateAgentDialog
  Modal={Modal}
  showAgentDialog={showAgentDialog}
  selectedProject={selectedProject}
  isConnected={isConnected}
  creatingAgent={creatingAgent}
  newAgentName={newAgentName}
  newAgentId={newAgentId}
  setShowAgentDialog={setShowAgentDialog}
  setNewAgentName={setNewAgentName}
  setNewAgentId={setNewAgentId}
  handleCreateAgent={handleCreateAgent}
/>

<CreateFormDialog
  Modal={Modal}
  showFormDialog={showFormDialog}
  selectedProject={selectedProject}
  isConnected={isConnected}
  creatingForm={creatingForm}
  newFormName={newFormName}
  newFormId={newFormId}
  setShowFormDialog={setShowFormDialog}
  setNewFormName={setNewFormName}
  setNewFormId={setNewFormId}
  handleCreateForm={handleCreateForm}
/>

<RunWorkflowDialog
  Modal={Modal}
  showRunDialog={showRunDialog}
  selectedProject={selectedProject}
  selectedWorkflow={selectedWorkflow}
  isConnected={isConnected}
  runningWorkflow={runningWorkflow}
  resolvingHumanTask={resolvingHumanTask}
  savingBeforeRun={savingBeforeRun}
  runVariables={runVariables}
  runError={runError}
  runResult={runResult}
  setShowRunDialog={setShowRunDialog}
  setRunVariables={setRunVariables}
  handleRunWorkflow={handleRunWorkflow}
  handleResolveHumanTask={handleResolveHumanTask}
/>
{deleteWorkflowTarget && (
  <Modal
    title="Delete workflow"
    onClose={() => {
      if (!deletingWorkflow) {
        setDeleteWorkflowTarget(null);
      }
    }}
  >
    <div className="studio-modal-form">
      <p>
        Delete "{deleteWorkflowTarget.name}"?
      </p>

      <p>
        This action cannot be undone.
      </p>
        {apiError && (
        <div className="studio-modal-error" role="alert">
            {apiError}
        </div>
        )}

      <div className="studio-modal-actions">
        <button
          type="button"
          disabled={deletingWorkflow}
          onClick={() =>
            setDeleteWorkflowTarget(null)
          }
        >
          Cancel
        </button>

        <button
          type="button"
          className="run-button"
          disabled={deletingWorkflow}
          onClick={handleDeleteWorkflow}
        >
          {deletingWorkflow
            ? "Deleting..."
            : "Delete"}
        </button>
      </div>
    </div>
  </Modal>
)}

{deleteAgentTarget && (
  <Modal
    title="Delete agent"
    onClose={() => {
      if (!deletingAgent) {
        setDeleteAgentTarget(null);
      }
    }}
  >
    <div className="studio-modal-form">
      <p>
        Delete "{deleteAgentTarget.name}"?
      </p>

      <p>
        This action cannot be undone.
      </p>

      <div className="studio-modal-actions">
        <button
          type="button"
          disabled={deletingAgent}
          onClick={() =>
            setDeleteAgentTarget(null)
          }
        >
          Cancel
        </button>

        <button
          type="button"
          className="run-button"
          disabled={deletingAgent}
          onClick={handleDeleteAgent}
        >
          {deletingAgent
            ? "Deleting..."
            : "Delete"}
        </button>
      </div>
    </div>
  </Modal>
)}

{deleteFormTarget && (
  <Modal
    title="Delete form"
    onClose={() => {
      if (!deletingForm) {
        setDeleteFormTarget(null);
      }
    }}
  >
    <div className="studio-modal-form">
      <p>
        Delete "{deleteFormTarget.name}"?
      </p>

      <p>
        This action cannot be undone.
      </p>

        {apiError && (
        <div className="studio-modal-error" role="alert">
            {apiError}
        </div>
        )}

      <div className="studio-modal-actions">
        <button
          type="button"
          disabled={deletingForm}
          onClick={() =>
            setDeleteFormTarget(null)
          }
        >
          Cancel
        </button>

        <button
          type="button"
          className="run-button"
          disabled={deletingForm}
          onClick={handleDeleteForm}
        >
          {deletingForm ? "Deleting..." : "Delete"}
        </button>
      </div>
    </div>
  </Modal>
)}
    </div>
  );
}
