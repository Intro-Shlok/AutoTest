import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const snapshotsDir = path.join(__dirname, '..', 'snapshots');
const snapshots = fs.existsSync(snapshotsDir)
  ? fs.readdirSync(snapshotsDir).sort()
  : [];

const manifest = {
  version: '1.0.0',
  generated: new Date().toISOString(),
  snapshots,
  api_endpoints: {
    commands: '/api/v1/commands.json',
    registry: '/api/v1/registry.json',
    by_domain: '/api/v1/by-domain.json',
    by_capability: '/api/v1/by-capability.json',
    by_workflow: '/api/v1/by-workflow.json',
    semantic_chunks: '/api/v1/semantic-chunks.json',
    embeddings: '/api/v1/embeddings.jsonl',
  },
  llms: {
    llms_txt: '/llms.txt',
    llms_full_txt: '/llms-full.txt',
  },
};

const distPath = path.join(__dirname, '..', 'dist');
fs.writeFileSync(
  path.join(distPath, 'manifest.json'),
  JSON.stringify(manifest, null, 2)
);

console.log('Retrieval manifest generated');