import next from "eslint-config-next";

const config = [
  ...next,
  {
    ignores: [".next/**", "node_modules/**", "public/**", "figures/.venv/**"],
  },
];

export default config;
