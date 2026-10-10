export default function NodeIcon({ type, size = 14 }) {
	const common = {
	  width: size,
	  height: size,
	  viewBox: "0 0 24 24",
	  fill: "none",
	  stroke: "currentColor",
	  strokeWidth: 1.8,
	  strokeLinecap: "round",
	  strokeLinejoin: "round",
	  "aria-hidden": true,
	};

	switch (String(type || "").toLowerCase()) {
	  case "start":
		return (
		  <svg {...common}>
			<circle cx="12" cy="12" r="8" />
			<path d="M10 8.5 16 12l-6 3.5Z" />
		  </svg>
		);

	  case "end":
		return (
		  <svg {...common}>
			<circle cx="12" cy="12" r="8" />
			<rect x="9" y="9" width="6" height="6" rx="1" />
		  </svg>
		);

	  case "agent":
		return (
		  <svg {...common}>
			<rect x="5" y="6" width="14" height="12" rx="3" />
			<path d="M9 11h.01M15 11h.01" />
			<path d="M9 14h6" />
			<path d="M12 3v3M8 3v2M16 3v2" />
		  </svg>
		);

	  case "tool":
		return (
		  <svg {...common}>
			<path d="m14.5 6.5 3-3a4 4 0 0 1-5.2 5.2l-7 7a2.1 2.1 0 1 0 3 3l7-7a4 4 0 0 1 5.2-5.2l-3 3" />
		  </svg>
		);

	  case "condition":
		return (
		  <svg {...common}>
			<path d="m12 3 8 9-8 9-8-9Z" />
			<path d="M9.5 12h5" />
		  </svg>
		);

	  case "decision":
		return (
		  <svg {...common}>
			<path d="m12 3 8 9-8 9-8-9Z" />
			<path d="M9 12h6M12 9v6" />
		  </svg>
		);

	  case "parallel":
		return (
		  <svg {...common}>
			<path d="M6 5h5v5H6zM13 14h5v5h-5z" />
			<path d="M11 7h2a3 3 0 0 1 3 3v4" />
			<path d="M13 17h-2a3 3 0 0 1-3-3v-4" />
		  </svg>
		);

	  case "join":
		return (
		  <svg {...common}>
			<path d="M6 5v5c0 2 2 3 6 3s6-1 6-3V5" />
			<path d="M6 19v-5c0-2 2-3 6-3s6 1 6 3v5" />
		  </svg>
		);

	  case "loop":
		return (
		  <svg {...common}>
			<path d="M17 7a7 7 0 1 0 1.5 7" />
			<path d="M17 3v4h-4" />
		  </svg>
		);

	  case "humantask":
	  case "human":
		return (
		  <svg {...common}>
			<circle cx="12" cy="8" r="3" />
			<path d="M6 20c.8-3.2 2.8-5 6-5s5.2 1.8 6 5" />
		  </svg>
		);

	  case "subworkflow":
		return (
		  <svg {...common}>
			<rect x="4" y="5" width="16" height="14" rx="2" />
			<path d="M8 9h8M8 13h5M8 17h3" />
		  </svg>
		);

	  default:
		return (
		  <svg {...common}>
			<rect x="5" y="5" width="14" height="14" rx="3" />
			<path d="M9 12h6M12 9v6" />
		  </svg>
		);
	}
  }
