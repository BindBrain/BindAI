import React from "react";

export default function FormDesigner({
  formDefinition,
  setFormDefinition,
  isConnected,
  handleFormSave,
  savingForm,
}) {
  if (!formDefinition) {
    return (
      <div className="empty-inspector">
        Loading form definition...
      </div>
    );
  }

  const updateField = (index, property, value) => {
    setFormDefinition((current) => {
      if (!current) return current;
      const fields = [...(current.fields || [])];
      fields[index] = { ...fields[index], [property]: value };
      return { ...current, fields };
    });
  };

  const removeField = (index) => {
    setFormDefinition((current) => ({
      ...current,
      fields: (current.fields || []).filter((_, i) => i !== index),
    }));
  };

  const addField = () => {
    setFormDefinition((current) => ({
      ...current,
      fields: [
        ...(current.fields || []),
        {
          id: `field-${Date.now()}`,
          type: "string",
          label: "New Field",
          name: null,
          description: null,
          required: false,
          default: null,
          placeholder: null,
          options: [],
          binding: null,
          validation: {},
        },
      ],
    }));
  };

  const updateOption = (fieldIndex, optionIndex, property, value) => {
    setFormDefinition((current) => {
      const fields = [...(current.fields || [])];
      const field = { ...(fields[fieldIndex] || {}) };
      const options = [...(field.options || [])];

      options[optionIndex] = {
        ...options[optionIndex],
        [property]: value,
      };

      fields[fieldIndex] = { ...field, options };
      return { ...current, fields };
    });
  };

  const removeOption = (fieldIndex, optionIndex) => {
    setFormDefinition((current) => {
      const fields = [...(current.fields || [])];
      const field = { ...(fields[fieldIndex] || {}) };

      fields[fieldIndex] = {
        ...field,
        options: (field.options || []).filter(
          (_, i) => i !== optionIndex,
        ),
      };

      return { ...current, fields };
    });
  };

  const addOption = (fieldIndex) => {
    setFormDefinition((current) => {
      const fields = [...(current.fields || [])];
      const field = { ...(fields[fieldIndex] || {}) };

      fields[fieldIndex] = {
        ...field,
        options: [
          ...(field.options || []),
          { value: "", label: "" },
        ],
      };

      return { ...current, fields };
    });
  };

  const updateAction = (index, property, value) => {
    setFormDefinition((current) => {
      const actions = [...(current.actions || [])];
      actions[index] = {
        ...actions[index],
        [property]: value,
      };
      return { ...current, actions };
    });
  };

  const removeAction = (index) => {
    setFormDefinition((current) => ({
      ...current,
      actions: (current.actions || []).filter((_, i) => i !== index),
    }));
  };

  const addAction = () => {
    setFormDefinition((current) => ({
      ...current,
      actions: [
        ...(current.actions || []),
        {
          id: `action-${Date.now()}`,
          label: "New Action",
          value: "new_action",
        },
      ],
    }));
  };

  const renderPreviewField = (field) => {
    if (field.type === "textarea") {
      return (
        <textarea
          rows={3}
          placeholder={field.placeholder || ""}
          disabled
        />
      );
    }

    if (field.type === "select") {
      return (
        <select disabled defaultValue="">
          <option value="">Select...</option>
          {(field.options || []).map((option) => (
            <option
              key={String(option.value)}
              value={String(option.value)}
            >
              {option.label || option.value}
            </option>
          ))}
        </select>
      );
    }

    if (field.type === "boolean") {
      return (
        <label className="inspector-checkbox">
          <span>{field.label || field.id}</span>
          <input type="checkbox" disabled />
        </label>
      );
    }

    return (
      <input
        type={
          field.type === "email"
            ? "email"
            : field.type === "number" || field.type === "integer"
              ? "number"
              : field.type === "date"
                ? "date"
                : "text"
        }
        placeholder={field.placeholder || ""}
        disabled
      />
    );
  };

  return (
    <div className="inspector-content">
      <div className="inspector-section-title">
        Form Designer
      </div>

      <div className="inspector-field">
        <label>Form ID</label>
        <input value={formDefinition.id || ""} readOnly />
      </div>

      <div className="inspector-field">
        <label>Name</label>
        <input
          value={formDefinition.name || ""}
          disabled={!isConnected}
          onChange={(event) =>
            setFormDefinition((current) => ({
              ...current,
              name: event.target.value,
            }))
          }
        />
      </div>

      <div className="inspector-field">
        <label>Description</label>
        <textarea
          rows={3}
          value={formDefinition.description || ""}
          disabled={!isConnected}
          onChange={(event) =>
            setFormDefinition((current) => ({
              ...current,
              description: event.target.value,
            }))
          }
        />
      </div>

      <div className="inspector-section-title">
        Fields
      </div>

      {(formDefinition.fields || []).length === 0 ? (
        <div className="empty-inspector">
          No fields yet. Add a field below.
        </div>
      ) : (
        (formDefinition.fields || []).map((field, index) => (
          <div
            key={field.id || index}
            style={{
              border: "1px solid #e2e5e9",
              borderRadius: "8px",
              padding: "12px",
              marginBottom: "12px",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "10px",
              }}
            >
              <strong>
                {field.label || field.id || "Field"}
              </strong>

              <button
                type="button"
                disabled={!isConnected}
                onClick={() => removeField(index)}
              >
                Remove
              </button>
            </div>

            <div className="inspector-field">
              <label>Field ID</label>
              <input
                value={field.id || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(index, "id", event.target.value)
                }
              />
            </div>

            <div className="inspector-field">
              <label>Label</label>
              <input
                value={field.label || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(index, "label", event.target.value)
                }
              />
            </div>

            <div className="inspector-field">
              <label>Type</label>
              <select
                value={field.type || "string"}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(index, "type", event.target.value)
                }
              >
                <option value="string">String</option>
                <option value="text">Text</option>
                <option value="textarea">Textarea</option>
                <option value="email">Email</option>
                <option value="number">Number</option>
                <option value="integer">Integer</option>
                <option value="boolean">Boolean</option>
                <option value="date">Date</option>
                <option value="select">Select</option>
              </select>
            </div>

            <div className="inspector-field">
              <label>Name</label>
              <input
                value={field.name || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(
                    index,
                    "name",
                    event.target.value || null,
                  )
                }
              />
            </div>

            <div className="inspector-field">
              <label>Description</label>
              <textarea
                rows={2}
                value={field.description || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(
                    index,
                    "description",
                    event.target.value || null,
                  )
                }
              />
            </div>

            <div className="inspector-field">
              <label>Placeholder</label>
              <input
                value={field.placeholder || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(
                    index,
                    "placeholder",
                    event.target.value || null,
                  )
                }
              />
            </div>

            <div className="inspector-checkbox">
              <span>Required</span>
              <input
                type="checkbox"
                checked={Boolean(field.required)}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(
                    index,
                    "required",
                    event.target.checked,
                  )
                }
              />
            </div>

            <div className="inspector-field">
              <label>Binding</label>
              <input
                value={field.binding || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateField(
                    index,
                    "binding",
                    event.target.value || null,
                  )
                }
              />
            </div>

            {field.type === "select" && (
              <>
                <div className="inspector-section-title">
                  Options
                </div>

                {(field.options || []).map(
                  (option, optionIndex) => (
                    <div
                      key={`${field.id}-option-${optionIndex}`}
                      style={{
                        display: "grid",
                        gridTemplateColumns: "1fr 1fr auto",
                        gap: "8px",
                        alignItems: "end",
                        marginBottom: "8px",
                      }}
                    >
                      <div className="inspector-field">
                        <label>Value</label>
                        <input
                          value={option.value ?? ""}
                          disabled={!isConnected}
                          onChange={(event) =>
                            updateOption(
                              index,
                              optionIndex,
                              "value",
                              event.target.value,
                            )
                          }
                        />
                      </div>

                      <div className="inspector-field">
                        <label>Label</label>
                        <input
                          value={option.label ?? ""}
                          disabled={!isConnected}
                          onChange={(event) =>
                            updateOption(
                              index,
                              optionIndex,
                              "label",
                              event.target.value,
                            )
                          }
                        />
                      </div>

                      <button
                        type="button"
                        disabled={!isConnected}
                        onClick={() =>
                          removeOption(index, optionIndex)
                        }
                      >
                        Remove
                      </button>
                    </div>
                  ),
                )}

                <button
                  type="button"
                  disabled={!isConnected}
                  onClick={() => addOption(index)}
                >
                  Add Option
                </button>
              </>
            )}
          </div>
        ))
      )}

      <button
        type="button"
        disabled={!isConnected}
        onClick={addField}
      >
        Add Field
      </button>

      <div className="inspector-section-title">
        Actions
      </div>

      {(formDefinition.actions || []).length === 0 ? (
        <div className="empty-inspector">
          No actions yet.
        </div>
      ) : (
        (formDefinition.actions || []).map((action, index) => (
          <div
            key={action.id || index}
            style={{
              border: "1px solid #e2e5e9",
              borderRadius: "8px",
              padding: "12px",
              marginBottom: "12px",
            }}
          >
            <div className="inspector-field">
              <label>Action ID</label>
              <input
                value={action.id || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateAction(index, "id", event.target.value)
                }
              />
            </div>

            <div className="inspector-field">
              <label>Label</label>
              <input
                value={action.label || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateAction(index, "label", event.target.value)
                }
              />
            </div>

            <div className="inspector-field">
              <label>Value</label>
              <input
                value={action.value || ""}
                disabled={!isConnected}
                onChange={(event) =>
                  updateAction(index, "value", event.target.value)
                }
              />
            </div>

            <button
              type="button"
              disabled={!isConnected}
              onClick={() => removeAction(index)}
            >
              Remove Action
            </button>
          </div>
        ))
      )}

      <button
        type="button"
        disabled={!isConnected}
        onClick={addAction}
      >
        Add Action
      </button>

      <div className="inspector-section-title">
        Form Preview
      </div>

      <div
        style={{
          border: "1px solid #e2e5e9",
          borderRadius: "8px",
          padding: "14px",
          background: "#ffffff",
        }}
      >
        <div
          style={{
            fontWeight: 600,
            marginBottom: "4px",
          }}
        >
          {formDefinition.name || "Untitled Form"}
        </div>

        {formDefinition.description && (
          <div
            style={{
              fontSize: "12px",
              color: "#68707a",
              marginBottom: "14px",
            }}
          >
            {formDefinition.description}
          </div>
        )}

        {(formDefinition.fields || []).length === 0 ? (
          <div className="empty-inspector">
            Add fields to preview the form.
          </div>
        ) : (
          (formDefinition.fields || []).map((field) => (
            <div
              key={field.id}
              className="inspector-field"
            >
              <label>
                {field.label || field.id}
                {field.required ? " *" : ""}
              </label>

              {renderPreviewField(field)}
            </div>
          ))
        )}

        {(formDefinition.actions || []).length > 0 && (
          <div
            style={{
              display: "flex",
              gap: "8px",
              marginTop: "12px",
              flexWrap: "wrap",
            }}
          >
            {(formDefinition.actions || []).map((action) => (
              <button
                key={action.id}
                type="button"
                disabled
              >
                {action.label || action.value}
              </button>
            ))}
          </div>
        )}
      </div>

      <button
        type="button"
        className="inspector-save-button"
        onClick={handleFormSave}
        disabled={!isConnected || savingForm}
      >
        {savingForm ? "Saving Form..." : "Save Form"}
      </button>
    </div>
  );
}
