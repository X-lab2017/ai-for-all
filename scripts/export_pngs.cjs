// Run with the installed sharp package available on NODE_PATH.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('sharp');
(async () => {
  const root = path.resolve(__dirname, '..');
  const names = ['inclusion-views', 'goal-path', 'dual-forces', 'evaluation-core', 'twin-flywheels'];
  for (const name of names) for (const lang of ['zh','en']) {
    const source = path.join(root, 'site/assets/diagrams', `${name}-${lang}.svg`);
    await sharp(source, {density:144}).png().toFile(source.replace('.svg','.png'));
  }
  await sharp(path.join(root,'site/assets/social-preview.svg')).png().toFile(path.join(root,'site/assets/social-preview.png'));
  console.log('Exported 10 diagram PNGs and the social card.');
})().catch(error => {console.error(error); process.exit(1);});
