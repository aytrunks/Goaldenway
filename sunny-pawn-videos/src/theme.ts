import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Brand colours sampled from the Sunny Pawn logo.
export const colors = {
  black: '#050505',
  yellow: '#FFC61A',
  orange: '#F26A1B',
  white: '#FFFFFF',
  muted: 'rgba(255,255,255,0.6)',
};

export const sunGradient = `linear-gradient(180deg, ${colors.yellow} 0%, ${colors.orange} 100%)`;

// Fonts are bundled in public/fonts so renders work offline.
export const display = 'Oswald';
export const body = 'Inter';
for (const weight of ['300', '600', '700']) {
  loadFont({family: display, url: staticFile(`fonts/oswald-latin-${weight}-normal.woff2`), weight});
}
for (const weight of ['400', '600']) {
  loadFont({family: body, url: staticFile(`fonts/inter-latin-${weight}-normal.woff2`), weight});
}

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;
