export default function Modal({
	title,
	children,
	onClose,
  }) {
	return (
	  <div
		className="studio-modal-backdrop"
		onMouseDown={onClose}
	  >
		<div
		  className="studio-modal"
		  onMouseDown={(event) =>
			event.stopPropagation()
		  }
		>
		  <div className="studio-modal-header">
			<strong>{title}</strong>

			<button
			  type="button"
			  className="studio-modal-close"
			  onClick={onClose}
			  aria-label="Close"
			>
			  ×
			</button>
		  </div>

		  {children}
		</div>
	  </div>
	);
  }
