import assert from "node:assert/strict";
import { readFile, readdir, stat } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const skillRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

async function read(relativePath) {
  return readFile(path.join(skillRoot, relativePath), "utf8");
}

test("skill routes dynamic theme work through an executable settling gate", async () => {
  const skill = await read("SKILL.md");
  const stability = await read("references/dynamic-ui-stability.md");

  assert.match(skill, /change_class: <static-visual \/ structural-theme \/ dynamic-runtime>/u);
  assert.match(skill, /make every enhancement idempotent/u);
  assert.match(skill, /smallest stable container/u);
  assert.match(skill, /300 ms and 600 ms checkpoints/u);
  assert.match(skill, /exactly one additional\s+enhancement/u);
  assert.match(stability, /minimal synthetic page/u);
  assert.match(stability, /initial600\)\.toBe\(initial300\)/u);
  assert.match(stability, /mutation300\)\.toBe\(initial600 \+ 1\)/u);
  assert.match(stability, /mutation600\)\.toBe\(mutation300\)/u);
  assert.match(stability, /page\.goto\("about:blank"\)/u);
  assert.match(stability, /Section replacement or teardown/u);
});

test("skill retains exact mutation scope without requiring redundant confirmation", async () => {
  const skill = await read("SKILL.md");
  const standard = await read("references/shopify-theme-delivery-standard.md");
  const handoff = await read("references/acceptance-and-handoff.md");

  assert.match(skill, /A draft-theme write is still a Shopify mutation/u);
  assert.match(skill, /current explicit user request[\s\S]*operation, target, and intended effect/u);
  assert.match(skill, /do not ask for equivalent confirmation again/u);
  assert.match(standard, /Draft acceptance does not authorize publication/u);
  assert.match(standard, /existing explicit publish request suffices/u);
  assert.match(skill, /Ask again only when the target, scope, material effect, credential boundary,/u);
  assert.match(skill, /belong to Shopify Admin\/data operations/u);
  assert.match(skill, /Split mixed requests into separate/u);
  assert.match(handoff, /publish_state: not-published/u);
  assert.match(handoff, /dynamic_stability:/u);
  assert.match(handoff, /not-applicable-live-file-patch/u);
  assert.doesNotMatch(standard, /Publish only after separate explicit\s+approval/u);
});

test("local completion and remote reads do not inherit write-release gates", async () => {
  const skill = await read("SKILL.md");
  const standard = await read("references/shopify-theme-delivery-standard.md");
  const handoff = await read("references/acceptance-and-handoff.md");

  assert.match(skill, /For source-only work, remote-only fields may be `not-applicable`/u);
  assert.match(skill, /read access does not\s+require write or publish authorization/u);
  assert.match(skill, /Local source work ends after the applicable local checks/u);
  assert.match(standard, /Isolated copy\/styling\s+does not require full browser acceptance/u);
  assert.match(standard, /Keep dynamic settling proof/u);
  assert.match(handoff, /Dynamic-runtime local work still needs the isolated settling proof/u);
  assert.doesNotMatch(skill, /Before any\s+remote read or write, every target and approval field must be known/u);
});

test("project route and affected verification do not force a broader write mode", async () => {
  const skill = await read("SKILL.md");
  const standard = await read("references/shopify-theme-delivery-standard.md");

  assert.match(skill, /including a narrower valid route/u);
  assert.match(skill, /Verification depth and remote write mode are separate decisions/u);
  assert.match(skill, /Dynamic runtime risk does\s+not by itself require a new draft or role transition/u);
  assert.match(standard, /Never replace an unsupported guarded path with a raw writer/u);
  assert.match(skill, /A narrow fix may list unrelated surfaces as `excluded`/u);
  assert.match(skill, /Broader verification\s+does not expand the allowed file manifest or remote effect/u);
  assert.match(skill, /unrelated mainline commits/u);
});

test("propagation and uncertain writes require observation or reconciliation", async () => {
  const skill = await read("SKILL.md");
  const standard = await read("references/shopify-theme-delivery-standard.md");
  const handoff = await read("references/acceptance-and-handoff.md");

  assert.match(skill, /Propagation delay alone does not authorize another write, publication, new\s+candidate, or automatic rollback/u);
  assert.match(skill, /Reconcile uncertain writes from receipts and\s+target readback/u);
  assert.match(standard, /conflict-safe rollback only for a verified failure/u);
  assert.match(handoff, /prior public bytes during bounded propagation permit only read-only observation/u);
});

test("instruction references resolve inside a portable self-contained package", async () => {
  const instructionPaths = ["SKILL.md", ...(await readdir(path.join(skillRoot, "references")))
    .filter((name) => name.endsWith(".md")).map((name) => `references/${name}`)];

  for (const relativePath of instructionPaths) {
    const text = await read(relativePath);
    assert.doesNotMatch(text, /\/(?:Users|home)\/[^/\s]+\/|\.agents\/skills\/|\.codex\/skills\//u,
      relativePath);
    for (const match of text.matchAll(/`(references\/[^`]+\.md)`/gu)) {
      assert.equal((await stat(path.join(skillRoot, match[1]))).isFile(), true, match[1]);
    }
  }
  const skill = await read("SKILL.md");
  assert.match(skill, /project-neutral rules are extracted without store IDs/u);
});
