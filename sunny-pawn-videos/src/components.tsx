import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {body, colors, display, sunGradient} from './theme';

// Black stage with a slow orange glow, like the logo sitting on night sky.
export const Stage: React.FC<{children: React.ReactNode; glowY?: number}> = ({children, glowY = 45}) => {
  const frame = useCurrentFrame();
  const pulse = 0.85 + 0.15 * Math.sin(frame / 20);
  return (
    <AbsoluteFill style={{backgroundColor: colors.black, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 50% ${glowY}%, rgba(242,106,27,${0.35 * pulse}) 0%, rgba(242,106,27,0.08) 35%, transparent 60%)`,
        }}
      />
      {children}
    </AbsoluteFill>
  );
};

// Ring of triangular rays that grows in and turns slowly, echoing the logo's sun.
export const SunRays: React.FC<{size: number; delay?: number; count?: number; opacity?: number}> = ({
  size,
  delay = 0,
  count = 16,
  opacity = 1,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const grow = spring({frame: frame - delay, fps, config: {damping: 14}});
  const rotation = (frame - delay) * 0.25;
  const r = size / 2;
  return (
    <svg
      width={size}
      height={size}
      viewBox={`${-r} ${-r} ${size} ${size}`}
      style={{transform: `rotate(${rotation}deg) scale(${grow})`, opacity}}
    >
      <defs>
        <linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={colors.yellow} />
          <stop offset="100%" stopColor={colors.orange} />
        </linearGradient>
      </defs>
      {Array.from({length: count}).map((_, i) => {
        const inner = r * 0.62;
        const outer = r * (i % 2 === 0 ? 0.98 : 0.84);
        const half = (Math.PI / count) * 0.45;
        const a = (i / count) * Math.PI * 2;
        const pts = [
          [Math.cos(a - half) * inner, Math.sin(a - half) * inner],
          [Math.cos(a) * outer, Math.sin(a) * outer],
          [Math.cos(a + half) * inner, Math.sin(a + half) * inner],
        ]
          .map((p) => p.join(','))
          .join(' ');
        return <polygon key={i} points={pts} fill="url(#ray)" />;
      })}
    </svg>
  );
};

export const Logo: React.FC<{size: number; delay?: number}> = ({size, delay = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping: 12}});
  return <Img src={staticFile('logo.png')} style={{width: size, height: size, transform: `scale(${s})`}} />;
};

// Words drop in one at a time.
export const StaggerText: React.FC<{text: string; delay?: number; size: number; color?: string; weight?: number}> = ({
  text,
  delay = 0,
  size,
  color = colors.white,
  weight = 600,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: size * 0.25}}>
      {text.split(' ').map((word, i) => {
        const s = spring({frame: frame - delay - i * 4, fps, config: {damping: 15}});
        return (
          <span
            key={i}
            style={{
              fontFamily: display,
              fontWeight: weight,
              fontSize: size,
              lineHeight: 1.05,
              color,
              letterSpacing: size * 0.04,
              textTransform: 'uppercase',
              opacity: s,
              transform: `translateY(${(1 - s) * 60}px)`,
              display: 'inline-block',
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

// The product: the shop's photo if given, otherwise a glowing sun disc so the template still renders.
export const ItemShot: React.FC<{image?: string; size: number; delay?: number}> = ({image, size, delay = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping: 13, mass: 0.8}});
  const float = Math.sin((frame - delay) / 18) * 10;
  return (
    <div
      style={{
        width: size,
        height: size,
        transform: `translateY(${float}px) scale(${interpolate(s, [0, 1], [0.6, 1])})`,
        opacity: s,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      <div style={{position: 'absolute'}}>
        <SunRays size={size * 1.25} delay={delay} opacity={0.9} />
      </div>
      {image ? (
        <Img
          src={staticFile(image)}
          style={{
            width: size * 0.78,
            height: size * 0.78,
            objectFit: 'cover',
            borderRadius: '50%',
            border: `8px solid ${colors.yellow}`,
            boxShadow: `0 0 80px ${colors.orange}`,
            position: 'relative',
          }}
        />
      ) : (
        <div
          style={{
            width: size * 0.62,
            height: size * 0.62,
            borderRadius: '50%',
            background: sunGradient,
            boxShadow: `0 0 120px ${colors.orange}`,
            position: 'relative',
          }}
        />
      )}
    </div>
  );
};

export const Footer: React.FC<{delay: number; line: string}> = ({delay, line}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame - delay, [0, 15], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', bottom: 120, width: '100%', textAlign: 'center', opacity: o}}>
      <div style={{fontFamily: body, fontSize: 36, color: colors.muted, letterSpacing: 2}}>{line}</div>
    </div>
  );
};

export const formatPrice = (n: number) => `$${Math.round(n).toLocaleString('en-US')}`;
