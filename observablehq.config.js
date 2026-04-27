// Observable Framework config — nist-rfi-site
// Docs: https://observablehq.com/framework/config

export default {
  title: "NIST AI Agent Security RFI — Public Comment Analysis",
  pages: [
    {name: "The corpus", pages: [
      {name: "Who commented", path: "/who"},
      {name: "Topic-area engagement", path: "/topics"},
      {name: "Major themes", path: "/themes"},
    ]},
    {name: "Findings", pages: [
      {name: "Points of agreement", path: "/agreement"},
      {name: "The silences", path: "/silences"},
      {name: "Stakeholder patterns", path: "/stakeholders"},
      {name: "Notable submissions", path: "/notable"},
    ]},
    {name: "Explore", pages: [
      {name: "All 517 comments", path: "/explore/"},
      {name: "Cross-tab any two fields", path: "/explore/crosstab"},
    ]},
    {name: "Methods & data", pages: [
      {name: "Methodology", path: "/methods"},
      {name: "How this was built", path: "/how-built"},
    ]},
  ],
  head: `<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>§</text></svg>">
<link rel="stylesheet" href="./style.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+Pro:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">`,
  root: "src",
  theme: ["light", "dark", "wide"],
  header: "",
  footer: `<div>Williams, M. (2026). <em>Public Comments to NIST RFI on AI Agent Security.</em> Professor of the Practice, Vanderbilt Law School. Source data: <a href="https://www.regulations.gov/docket/NIST-2025-0035">NIST-2025-0035</a> on regulations.gov. Code/data: <a href="/methods">Methods</a>.</div>`,
  toc: true,
  pager: true,
  output: "dist",
  linkify: true,
  typographer: true,
  preserveIndex: false,
  preserveExtension: false,
};
