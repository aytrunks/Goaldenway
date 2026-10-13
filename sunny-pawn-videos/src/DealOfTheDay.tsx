import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Footer, ItemShot, Logo, Stage, StaggerText, formatPrice} from './components';
import {body, colors, display} from './theme';

export type DealProps = {
  item: string;
  detail: string;
  price: number;
  wasPrice?: number;
  image?: string;
  footer: string;
};

export const DealOfTheDay: React.FC<DealProps> = ({item, detail, price, wasPrice, image, footer}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const priceIn = spring({frame: frame - 120, fps, config: {damping: 9, mass: 0.7}});
  const strike = interpolate(frame, [105, 120], [0, 100], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const wasIn = interpolate(frame, [90, 102], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <Stage glowY={48}>
      <AbsoluteFill style={{alignItems: 'center', paddingTop: 110}}>
        <Logo size={190} />
        <div style={{marginTop: 30}}>
          <StaggerText text="Deal of the day" size={120} delay={10} color={colors.yellow} weight={700} />
        </div>
      </AbsoluteFill>

      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', top: 40}}>
        <ItemShot image={image} size={620} delay={35} />
      </AbsoluteFill>

      <AbsoluteFill style={{alignItems: 'center', top: 1250, padding: '0 80px'}}>
        <StaggerText text={item} size={86} delay={60} />
        <div
          style={{
            fontFamily: body,
            fontSize: 40,
            color: colors.muted,
            marginTop: 14,
            opacity: interpolate(frame, [75, 90], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          }}
        >
          {detail}
        </div>

        <div style={{display: 'flex', alignItems: 'center', gap: 40, marginTop: 40}}>
          {wasPrice ? (
            <div style={{position: 'relative', opacity: wasIn * 0.7}}>
              <span style={{fontFamily: display, fontSize: 80, color: colors.white, fontWeight: 300}}>
                {formatPrice(wasPrice)}
              </span>
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  top: '52%',
                  height: 7,
                  width: `${strike}%`,
                  background: colors.orange,
                  transform: 'rotate(-8deg)',
                }}
              />
            </div>
          ) : null}
          <span
            style={{
              fontFamily: display,
              fontWeight: 700,
              fontSize: 170,
              color: colors.yellow,
              textShadow: `0 0 50px ${colors.orange}`,
              transform: `scale(${priceIn})`,
              display: 'inline-block',
            }}
          >
            {formatPrice(price)}
          </span>
        </div>
      </AbsoluteFill>

      <Footer delay={150} line={footer} />
    </Stage>
  );
};
