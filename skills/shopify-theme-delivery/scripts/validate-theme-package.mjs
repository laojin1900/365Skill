#!/usr/bin/env node

import { access, readFile, readdir } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

function stripJsonComments(source) {
  let result = "";
  let inString = false;
  let escaped = false;

  for (let index = 0; index < source.length; index += 1) {
    const character = source[index];
    const next = source[index + 1];

    if (inString) {
      result += character;
      if (escaped) escaped = false;
      else if (character === "\\") escaped = true;
      else if (character === '"') inString = false;
      continue;
    }
    if (character === '"') {
      inString = true;
      result += character;
      continue;
    }
    if (character === "/" && next === "/") {
      index += 2;
      while (index < source.length && source[index] !== "\n") index += 1;
      if (index < source.length) result += "\n";
      continue;
    }
    if (character === "/" && next === "*") {
      index += 2;
      while (index < source.length && !(source[index] === "*" && source[index + 1] === "/")) {
        if (source[index] === "\n") result += "\n";
        index += 1;
      }
      index += 1;
      continue;
    }
    result += character;
  }

  return result;
}

function stripTrailingCommas(source) {
  let result = "";
  let inString = false;
  let escaped = false;

  for (let index = 0; index < source.length; index += 1) {
    const character = source[index];
    if (inString) {
      result += character;
      if (escaped) escaped = false;
      else if (character === "\\") escaped = true;
      else if (character === '"') inString = false;
      continue;
    }
    if (character === '"') {
      inString = true;
      result += character;
      continue;
    }
    if (character === ",") {
      let cursor = index + 1;
      while (/\s/.test(source[cursor] || "")) cursor += 1;
      if (source[cursor] === "}" || source[cursor] === "]") continue;
    }
    result += character;
  }

  return result;
}

function normalizeJsonc(source) {
  return stripTrailingCommas(stripJsonComments(source.replace(/^\uFEFF/, "")));
}

function parseJson(source, label, errors) {
  try {
    return JSON.parse(normalizeJsonc(source));
  } catch (error) {
    errors.push(`${label}: invalid JSON (${error instanceof Error ? error.message : "parse failed"})`);
    return null;
  }
}

async function directoryExists(directory) {
  try {
    await access(directory);
    return true;
  } catch {
    return false;
  }
}

async function listFiles(directory, predicate) {
  if (!(await directoryExists(directory))) return [];

  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...await listFiles(absolute, predicate));
    } else if (entry.isFile() && predicate(absolute)) {
      files.push(absolute);
    }
  }

  return files.sort();
}

function normalizeRelativePath(value) {
  return value.replaceAll("\\", "/").replace(/^\.\//, "");
}

function isAppSectionType(type) {
  return type.startsWith("shopify://apps/");
}

function validateComposition({ data, label, sectionTypes, errors }) {
  if (!data || typeof data !== "object" || Array.isArray(data)) {
    errors.push(`${label}: root must be an object`);
    return;
  }
  if (!data.sections || typeof data.sections !== "object" || Array.isArray(data.sections)) {
    errors.push(`${label}: sections must be an object`);
    return;
  }
  if (!Array.isArray(data.order)) {
    errors.push(`${label}: order must be an array`);
    return;
  }

  const seen = new Set();
  for (const id of data.order) {
    if (typeof id !== "string" || !id) {
      errors.push(`${label}: order entries must be non-empty strings`);
      continue;
    }
    if (seen.has(id)) errors.push(`${label}: duplicate order id '${id}'`);
    seen.add(id);
    if (!Object.hasOwn(data.sections, id)) {
      errors.push(`${label}: order id '${id}' is missing from sections`);
    }
  }

  for (const [id, section] of Object.entries(data.sections)) {
    if (!section || typeof section !== "object" || Array.isArray(section)) {
      errors.push(`${label}: section '${id}' must be an object`);
      continue;
    }
    if (typeof section.type !== "string" || !section.type) {
      errors.push(`${label}: section '${id}' has no type`);
      continue;
    }
    if (!isAppSectionType(section.type) && !sectionTypes.has(section.type)) {
      errors.push(`${label}: section '${id}' references missing sections/${section.type}.liquid`);
    }
  }
}

function extractSchemaBlocks(source) {
  return [...source.matchAll(/{%\s*schema\s*%}([\s\S]*?){%\s*endschema\s*%}/g)];
}

export async function validateThemePackage({
  themeRoot,
  changedFiles = [],
  allowSettingsData = false,
} = {}) {
  const root = path.resolve(themeRoot || ".");
  const errors = [];
  const warnings = [];
  const templatesDirectory = path.join(root, "templates");
  const sectionsDirectory = path.join(root, "sections");

  for (const [name, directory] of [["templates", templatesDirectory], ["sections", sectionsDirectory]]) {
    if (!(await directoryExists(directory))) errors.push(`missing required ${name}/ directory`);
  }

  const [templateFiles, sectionFiles, sectionGroupFiles, configJsonFiles, localeJsonFiles] = await Promise.all([
    listFiles(templatesDirectory, (file) => file.endsWith(".json")),
    listFiles(sectionsDirectory, (file) => file.endsWith(".liquid")),
    listFiles(sectionsDirectory, (file) => file.endsWith(".json")),
    listFiles(path.join(root, "config"), (file) => file.endsWith(".json")),
    listFiles(path.join(root, "locales"), (file) => file.endsWith(".json")),
  ]);
  const sectionTypes = new Set(sectionFiles.map((file) => path.basename(file, ".liquid")));
  let schemaCount = 0;

  for (const file of [...templateFiles, ...sectionGroupFiles]) {
    const label = normalizeRelativePath(path.relative(root, file));
    const data = parseJson(await readFile(file, "utf8"), label, errors);
    if (data) validateComposition({ data, label, sectionTypes, errors });
  }

  for (const file of [...configJsonFiles, ...localeJsonFiles]) {
    const label = normalizeRelativePath(path.relative(root, file));
    parseJson(await readFile(file, "utf8"), label, errors);
  }

  for (const file of sectionFiles) {
    const label = normalizeRelativePath(path.relative(root, file));
    const blocks = extractSchemaBlocks(await readFile(file, "utf8"));
    if (blocks.length > 1) errors.push(`${label}: contains more than one schema block`);
    if (blocks.length === 1) {
      schemaCount += 1;
      parseJson(blocks[0][1], `${label} schema`, errors);
    }
  }

  for (const rawFile of changedFiles) {
    const file = normalizeRelativePath(String(rawFile).trim());
    if (!file) continue;
    if (path.isAbsolute(file) || file === ".." || file.startsWith("../") || file.includes("/../")) {
      errors.push(`changed file escapes theme root: ${rawFile}`);
      continue;
    }
    if (file === "config/settings_data.json" && !allowSettingsData) {
      errors.push("config/settings_data.json is protected; pass --allow-settings-data only after explicit approval");
    }
    if (!(await directoryExists(path.join(root, file)))) {
      errors.push(`changed file does not exist: ${file}`);
    }
  }

  if (changedFiles.length === 0) {
    warnings.push("no changed-file manifest supplied; settings_data.json change protection was not evaluated");
  }

  return {
    ok: errors.length === 0,
    root,
    counts: {
      templates: templateFiles.length,
      sections: sectionFiles.length,
      sectionGroups: sectionGroupFiles.length,
      schemas: schemaCount,
      jsonFiles: templateFiles.length + sectionGroupFiles.length + configJsonFiles.length + localeJsonFiles.length,
    },
    errors,
    warnings,
  };
}

function usage() {
  return `Usage: validate-theme-package.mjs --theme PATH [options]\n\nOptions:\n  --changed-file PATH       Repeat for each changed theme-relative file\n  --changed-files FILE      Read newline-delimited changed files\n  --allow-settings-data     Permit config/settings_data.json in the manifest\n  --json                    Print JSON output\n  --help                    Show this help\n`;
}

async function parseCliArguments(argv) {
  const options = { changedFiles: [], allowSettingsData: false, json: false, themeRoot: "" };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--theme") options.themeRoot = argv[++index] || "";
    else if (argument === "--changed-file") options.changedFiles.push(argv[++index] || "");
    else if (argument === "--changed-files") {
      const manifestPath = argv[++index];
      if (!manifestPath) throw new Error("--changed-files requires a file path");
      const manifest = await readFile(manifestPath, "utf8");
      options.changedFiles.push(...manifest.split(/\r?\n/).filter(Boolean));
    } else if (argument === "--allow-settings-data") options.allowSettingsData = true;
    else if (argument === "--json") options.json = true;
    else if (argument === "--help") options.help = true;
    else throw new Error(`unknown option: ${argument}`);
  }

  if (!options.help && !options.themeRoot) throw new Error("--theme is required");
  return options;
}

async function main() {
  try {
    const options = await parseCliArguments(process.argv.slice(2));
    if (options.help) {
      process.stdout.write(usage());
      return;
    }
    const result = await validateThemePackage(options);
    if (options.json) {
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    } else {
      process.stdout.write(`Shopify theme package: ${result.ok ? "PASS" : "FAIL"}\n`);
      process.stdout.write(`templates=${result.counts.templates} sections=${result.counts.sections} schemas=${result.counts.schemas}\n`);
      for (const warning of result.warnings) process.stdout.write(`WARN ${warning}\n`);
      for (const error of result.errors) process.stderr.write(`ERROR ${error}\n`);
    }
    if (!result.ok) process.exitCode = 1;
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : "validation failed"}\n`);
    process.exitCode = 1;
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  await main();
}
