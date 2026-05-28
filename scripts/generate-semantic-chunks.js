import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const commandsPath = path.join(__dirname, '..', 'public', 'api', 'v1', 'commands.json');
const commands = JSON.parse(fs.readFileSync(commandsPath, 'utf-8'));

const chunks = commands.map(cmd => {
  const ns = cmd.namespace || '';
  return {
    id: cmd.id || '',
    namespace: ns,
    domain: ns.includes(':') ? ns.split(':')[0] : 'unknown',
    name: cmd.name || '',
    tokens_est: 200 + Math.floor((cmd.description || '').length / 4),
  };
});

const output = { total_chunks: chunks.length, chunks };

const distApiPath = path.join(__dirname, '..', 'dist', 'api', 'v1');
fs.mkdirSync(distApiPath, { recursive: true });

fs.writeFileSync(
  path.join(distApiPath, 'semantic-chunks.json'),
  JSON.stringify(output, null, 2)
);

console.log(`Semantic manifest: ${chunks.length} chunks`);