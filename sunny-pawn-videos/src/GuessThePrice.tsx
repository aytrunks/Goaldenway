import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Footer, ItemShot, Logo, Stage, StaggerText, SunRays, formatPrice} from './components';
import {body, colors, display} from './theme';

export type GuessProps = {
  item: string;
  price: number;
  image?: string;
  footer: string;
};

// Timeline (30fps): question 0–60, item 30, countdown 75–165, price roll 165–210, burst + CTA after.
const COUNT_START = 75;
const REVEAL = 165;

export const GuessThePrice: React.FC<GuessProps> = ({item, price, image, footer}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const counting = frame >= COUNT_START && frame < REVEAL;
  const countNumber = 3 - Math.floor((frame - COUNT_START) / 30);
  const tick = ((frame - COUNT_START) % 30) / 30;
  const ring = counting ? 1 - tick : 0;

  const roll = interpolate(frame, [REVEAL, REVEAL + 40], [0, price], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const revealed = frame >= REVEAL;
  const pop = spring({frame: frame - (REVEAL + 40), fps, config: {damping: 8}});
  const ctaIn = spring({frame: frame - (REVEAL + 55), fps, config: {damping: 14}});

  return (
    <Stage glowY={45}>
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 90}}>
        <Logo size={150} />
        <div style={{height: 20}} />
        <StaggerText text="Guess the price" size={130} color={colors.yellow} weight={700} />
        <div style={{marginTop: 20}}>
          <StaggerText text={item} size={64} delay={20} weight={300} />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', top: 20}}>
        <ItemShot image={image} size={600} delay={30} />
      </AbsoluteFill>

      <AbsoluteFill style={{alignItems: 'center', top: 1300}}>
        {counting ? (
          <div style={{position: 'relative', width: 260, height: 260}}>
            <svg width={260} height={260} style={{position: 'absolute', transform: 'rotate(-90deg)'}}>
              <circle cx={130} cy={130} r={115} stroke="rgba(255,255,255,0.15)" strokeWidth={10} fill="none" />
              <circle
                cx={130}
                cy={130}
                r={115}
                stroke={colors.orange}
                strokeWidth={10}
                fill="none"
                strokeDasharray={2 * Math.PI * 115}
                strokeDashoffset={2 * Math.PI * 115 * (1 - ring)}
                strokeLinecap="round"
              />
            </svg>
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontFamily: display,
                fontWeight: 700,
                fontSize: 150,
                color: colors.white,
                transform: `scale(${1.25 - tick * 0.25})`,
              }}
            >
              {countNumber}
            </div>
          </div>
        ) : null}

        {revealed ? (
          <div style={{position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{position: 'absolute', opacity: pop * 0.35}}>
              <SunRays size={480} delay={REVEAL + 40} count={20} />
            </div>
            <span
              style={{
                fontFamily: display,
                fontWeight: 700,
                fontSize: 200,
                color: colors.yellow,
                textShadow: `0 0 60px ${colors.orange}`,
                transform: `scale(${1 + pop * 0.12})`,
                position: 'relative',
              }}
            >
              {formatPrice(roll)}
            </span>
          </div>
        ) : null}

        <div
          style={{
            marginTop: 30,
            fontFamily: body,
            fontWeight: 600,
            fontSize: 44,
            color: colors.white,
            opacity: ctaIn,
            transform: `translateY(${(1 - ctaIn) * 30}px)`,
          }}
        >
          Did you guess right? Comment below
        </div>
      </AbsoluteFill>

      <Footer delay={REVEAL + 70} line={footer} />
    </Stage>
  );
};
