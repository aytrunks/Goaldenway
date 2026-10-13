import React from 'react';
import {Composition} from 'remotion';
import {DealOfTheDay, DealProps} from './DealOfTheDay';
import {GuessThePrice, GuessProps} from './GuessThePrice';
import {FPS, HEIGHT, WIDTH} from './theme';

// Sample data. Swap these per video, or pass --props='{"item":"..."}' when rendering.
const deal: DealProps = {
  item: '14k Gold Cuban Chain',
  detail: '22 inch · 38 grams · like new',
  price: 1199,
  wasPrice: 1650,
  footer: 'In store now · Sunny Pawn',
};

const guess: GuessProps = {
  item: 'Rolex Datejust 36',
  price: 6450,
  footer: 'Sunny Pawn · Buy · Sell · Pawn',
};

export const Root: React.FC = () => (
  <>
    <Composition id="DealOfTheDay" component={DealOfTheDay} durationInFrames={8 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} defaultProps={deal} />
    <Composition id="GuessThePrice" component={GuessThePrice} durationInFrames={9 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} defaultProps={guess} />
  </>
);
