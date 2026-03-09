import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const changesetDir = path.join(root, ".changeset");
const files = fs
  .readdirSync(changesetDir)
  .filter((file) => file.endsWith(".md"))
  .sort();

const summaries = files.map((file) => {
  const raw = fs.readFileSync(path.join(changesetDir, file), "utf8");
  const [frontmatter = "", ...bodyParts] = raw.split("---").slice(1);
  const releases = frontmatter
    .trim()
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.replace(/\"/g, "").split(":").map((item) => item.trim()))
    .map(([pkg, bump]) => ({ pkg, bump }));

  return {
    file,
    releases,
    summary: bodyParts.join("---").trim()
  };
});

const output = {
  generatedAt: new Date().toISOString(),
  count: summaries.length,
  changesets: summaries
};

fs.writeFileSync(path.join(changesetDir, "status.json"), JSON.stringify(output, null, 2));
console.log(JSON.stringify(output, null, 2));
