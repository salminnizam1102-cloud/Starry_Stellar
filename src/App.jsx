import React, { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame, useLoader, useThree } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// Import local texture files from src/textures/
import sunImg from './textures/sun.jpg';
import earthImg from './textures/earth.jpg';
import earthNightImg from './textures/earth_night.jpg';
import earthCloudsImg from './textures/earth_clouds.jpg';
import moonImg from './textures/moon.jpg';
import marsImg from './textures/mars.jpg';

const SUN_POSITION = new THREE.Vector3(-200, 20, 40);

const CELESTIAL_DATA = {
  sun: {
    title: "Sun",
    type: "G-Type Main-Sequence Star",
    desc: "The blazing nuclear heart of our system. Its relentless solar wind and gravitational anchor hold the remnants of human ambition in a perpetual cosmic dance.",
    hasEquipment: false,
  },
  earth: {
    title: "Earth",
    type: "Terrestrial Biosphere",
    desc: "The birthplace of humanity. From this blue sanctuary, humanity reached outward into the void, leaving behind steel footprints and silent mechanical ghosts across the cosmos.",
    hasEquipment: false,
  },
  moon: {
    title: "Moon",
    type: "Desolate Satellite",
    desc: "Earth's companion in the dark. The surface is littered with the monumental hardware of early space exploration—silent testaments to humanity's first leaps.",
    equipment: "Abandoned Assets: Apollo 11 Descent Stage, retroreflectors, and discarded descent modules.",
    hasEquipment: true,
  },
  mars: {
    title: "Mars",
    type: "Arid Desert World",
    desc: "The red dust world. A graveyard of robotic pioneers that mapped its canyons, sampled its soil, and eventually fell silent beneath iron-oxide skies.",
    equipment: "Abandoned Assets: Viking landers, static science platforms, and disabled rover chassis.",
    hasEquipment: true,
  }
};

// --- CAMERA CONTROLLER FOR ZOOM EFFECT ---
function CameraController({ targetPosition, controlsRef }) {
  const { camera } = useThree();

  React.useEffect(() => {
    if (!targetPosition) {
      // Zoom out to overview
      gsap.to(camera.position, {
        x: 0,
        y: 3.5,
        z: 16,
        duration: 1.8,
        ease: 'power3.inOut',
        onUpdate: () => camera.lookAt(0, 0, 0)
      });
      if (controlsRef.current) {
        gsap.to(controlsRef.current.target, { x: 0, y: 0, z: 0, duration: 1.8, ease: 'power3.inOut' });
      }
      return;
    }

    // Zoom in on Moon or Mars
    gsap.to(camera.position, {
      x: targetPosition.x,
      y: targetPosition.y + 0.5,
      z: targetPosition.z + 1.8,
      duration: 1.8,
      ease: 'power3.inOut',
      onUpdate: () => camera.lookAt(targetPosition)
    });

    if (controlsRef.current) {
      gsap.to(controlsRef.current.target, {
        x: targetPosition.x,
        y: targetPosition.y,
        z: targetPosition.z,
        duration: 1.8,
        ease: 'power3.inOut',
      });
    }
  }, [targetPosition, camera, controlsRef]);

  return null;
}

// --- TWINKLING STARS ---
function TwinklingStars() {
  const starsRef = useRef();

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    if (starsRef.current) {
      starsRef.current.rotation.y = t * 0.015;
      starsRef.current.scale.setScalar(1 + Math.sin(t * 1.5) * 0.015);
    }
  });

  return (
    <group ref={starsRef}>
      <Stars radius={250} depth={80} count={6000} factor={4} saturation={0.5} fade />
    </group>
  );
}

// --- DAY/NIGHT EARTH ---
function DayNightEarth({ dayTexture, nightTexture, cloudsTexture, position, onHover, onUnhover }) {
  const earthRef = useRef();
  const cloudsRef = useRef();

  const earthShader = useMemo(() => ({
    uniforms: {
      dayMap: { value: dayTexture },
      nightMap: { value: nightTexture },
      sunDirection: { value: SUN_POSITION.clone().normalize() },
    },
    vertexShader: `
      varying vec2 vUv;
      varying vec3 vWorldNormal;
      void main() {
        vUv = uv;
        vWorldNormal = normalize(mat3(modelMatrix) * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D dayMap;
      uniform sampler2D nightMap;
      uniform vec3 sunDirection;
      varying vec2 vUv;
      varying vec3 vWorldNormal;

      void main() {
        vec3 dayColor = texture2D(dayMap, vUv).rgb;
        vec3 nightColor = texture2D(nightMap, vUv).rgb;
        float intensity = dot(normalize(vWorldNormal), sunDirection);
        float dayMix = smoothstep(-0.15, 0.25, intensity);
        vec3 litDay = dayColor * (max(intensity, 0.0) * 1.3 + 0.15);
        vec3 litNight = nightColor * 1.4;
        vec3 finalColor = mix(litNight, litDay, dayMix);
        gl_FragColor = vec4(finalColor, 1.0);
      }
    `
  }), [dayTexture, nightTexture]);

  useFrame(() => {
    if (earthRef.current) earthRef.current.rotation.y += 0.001;
    if (cloudsRef.current) cloudsRef.current.rotation.y += 0.0013;
  });

  return (
    <group 
      position={position}
      onPointerOver={(e) => { e.stopPropagation(); onHover('earth'); }}
      onPointerOut={(e) => { e.stopPropagation(); onUnhover(); }}
    >
      <mesh ref={earthRef}>
        <sphereGeometry args={[2, 64, 64]} />
        <shaderMaterial attach="material" args={[earthShader]} />
      </mesh>
      <mesh ref={cloudsRef}>
        <sphereGeometry args={[2.03, 64, 64]} />
        <meshStandardMaterial map={cloudsTexture} transparent={true} opacity={0.45} depthWrite={false} />
      </mesh>
    </group>
  );
}

// --- SOLAR SYSTEM & PLANET ROUTING ---
function SolarSystem({ onSelectPlanet, onHover, onUnhover, moonGroupRef, isZoomed }) {
  const moonRef = useRef();
  const marsRef = useRef();
  const sunRef = useRef();

  const [sunTexture, earthTexture, earthNightTexture, earthCloudsTexture, moonTexture, marsTexture] = useLoader(
    THREE.TextureLoader,
    [sunImg, earthImg, earthNightImg, earthCloudsImg, moonImg, marsImg]
  );

  const EARTH_X = -6.5;

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    // Freeze orbital revolution if zoomed in
    const moonOrbitT = isZoomed ? 0 : t * 0.15;

    if (moonGroupRef.current && !isZoomed) {
      moonGroupRef.current.position.x = EARTH_X + Math.cos(moonOrbitT) * 3.4;
      moonGroupRef.current.position.z = Math.sin(moonOrbitT) * 3.4;
    }

    // Always maintain slow self-rotation
    if (marsRef.current) marsRef.current.rotation.y += 0.0008;
    if (sunRef.current) sunRef.current.rotation.y += 0.0005;
    if (moonRef.current) moonRef.current.rotation.y += 0.0003;
  });

  return (
    <group>
      {/* SUN */}
      <group 
        position={SUN_POSITION}
        onPointerOver={(e) => { e.stopPropagation(); onHover('sun'); }}
        onPointerOut={(e) => { e.stopPropagation(); onUnhover(); }}
      >
        <mesh ref={sunRef}>
          <sphereGeometry args={[20, 48, 48]} />
          <meshBasicMaterial map={sunTexture} />
        </mesh>
        <mesh>
          <sphereGeometry args={[22.5, 32, 32]} />
          <meshBasicMaterial color="#ff6a00" transparent opacity={0.22} blending={THREE.AdditiveBlending} />
        </mesh>
      </group>

      {/* EARTH */}
      <DayNightEarth
        dayTexture={earthTexture}
        nightTexture={earthNightTexture}
        cloudsTexture={earthCloudsTexture}
        position={[EARTH_X, 0, 0]}
        onHover={onHover}
        onUnhover={onUnhover}
      />

      {/* MOON */}
      <group
        ref={moonGroupRef}
        position={[EARTH_X + 3.4, 0, 0]}
        onPointerOver={(e) => { e.stopPropagation(); onHover('moon'); }}
        onPointerOut={(e) => { e.stopPropagation(); onUnhover(); }}
        onClick={(e) => {
          e.stopPropagation();
          onSelectPlanet('moon', moonGroupRef);
        }}
      >
        <mesh ref={moonRef}>
          <sphereGeometry args={[0.55, 48, 48]} />
          <meshStandardMaterial
            map={moonTexture}
            bumpMap={moonTexture}
            bumpScale={0.03}
            roughness={0.85}
          />
        </mesh>
      </group>

      {/* MARS */}
      <mesh
        ref={marsRef}
        position={[7.5, 0, 0]}
        onPointerOver={(e) => { e.stopPropagation(); onHover('mars'); }}
        onPointerOut={(e) => { e.stopPropagation(); onUnhover(); }}
        onClick={(e) => {
          e.stopPropagation();
          onSelectPlanet('mars', marsRef);
        }}
      >
        <sphereGeometry args={[1.5, 48, 48]} />
        <meshStandardMaterial
          map={marsTexture}
          bumpMap={marsTexture}
          bumpScale={0.03}
          roughness={0.8}
        />
      </mesh>
    </group>
  );
}

// --- MAIN APP COMPONENT ---
export default function App() {
  const [hoveredBody, setHoveredBody] = useState(null);
  const [targetPosition, setTargetPosition] = useState(null);
  const [activePhase, setActivePhase] = useState(null); // 'phase-3-moon' or 'phase-4-mars'
  const [showPhasePanel, setShowPhasePanel] = useState(false);
  const [videoModalSubject, setVideoModalSubject] = useState(null);

  const controlsRef = useRef();
  const moonGroupRef = useRef();

  const handleSelectPlanet = (planetName, refObj) => {
    if (planetName === 'moon' && moonGroupRef.current) {
      const pos = new THREE.Vector3();
      moonGroupRef.current.getWorldPosition(pos);
      setTargetPosition(pos);
      setActivePhase('phase-3-moon');
      // Delay opening panel until camera zoom completes (1.8 seconds)
      setTimeout(() => setShowPhasePanel(true), 1800);
    } else if (planetName === 'mars' && refObj.current) {
      const pos = new THREE.Vector3();
      refObj.current.getWorldPosition(pos);
      setTargetPosition(pos);
      setActivePhase('phase-4-mars');
      setTimeout(() => setShowPhasePanel(true), 1800);
    }
  };

  const handleReturnToOrbit = () => {
    setShowPhasePanel(false);
    setActivePhase(null);
    setTargetPosition(null);
  };

  const activeData = hoveredBody ? CELESTIAL_DATA[hoveredBody] : null;

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000', margin: 0, overflow: 'hidden', position: 'relative' }}>
      
      {/* LEFT HOVER SIDEBAR (Hidden when zoomed into Phase Panel) */}
      {!showPhasePanel && (
        <div style={{
          position: 'absolute',
          top: '30px',
          left: '30px',
          width: '360px',
          zIndex: 20,
          background: 'rgba(5, 10, 20, 0.08)',
          backdropFilter: 'blur(4px)',
          border: '1px solid rgba(255, 255, 255, 0.06)',
          boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.2)',
          borderRadius: '12px',
          padding: '24px',
          color: '#f8fafc',
          fontFamily: 'system-ui, -apple-system, sans-serif',
          pointerEvents: 'none',
          transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)', paddingBottom: '10px' }}>
            <span style={{ fontSize: '0.75rem', letterSpacing: '2px', color: '#38bdf8', fontWeight: 700 }}>
              // SECTOR ANALYSIS
            </span>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: hoveredBody ? '#38bdf8' : '#64748b', boxShadow: hoveredBody ? '0 0 10px #38bdf8' : 'none' }}></span>
          </div>

          {!hoveredBody ? (
            <div>
              <h1 style={{ 
                margin: 0, 
                fontSize: '2.2rem', 
                fontWeight: 800, 
                letterSpacing: '1px', 
                color: '#ffffff',
              }}>
                Ghosts of Space
              </h1>
              <p style={{ margin: '12px 0 0 0', fontSize: '0.9rem', color: '#94a3b8', lineHeight: '1.5' }}>
                Hover over celestial bodies to inspect coordinates, historical logs, and discarded cosmic artifacts.
              </p>
            </div>
          ) : (
            <div style={{ animation: 'fadeIn 0.3s ease' }}>
              <div style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '4px' }}>
                {activeData.type}
              </div>
              <h2 style={{ margin: '0 0 12px 0', fontSize: '1.8rem', fontWeight: 700, color: '#ffffff', letterSpacing: '0.5px' }}>
                {activeData.title}
              </h2>
              <p style={{ margin: '0 0 16px 0', fontSize: '0.88rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                {activeData.desc}
              </p>

              {activeData.hasEquipment && (
                <div style={{ 
                  background: 'rgba(239, 68, 68, 0.1)', 
                  borderLeft: '3px solid #ef4444', 
                  padding: '10px 12px', 
                  borderRadius: '0 6px 6px 0',
                  marginBottom: '14px'
                }}>
                  <p style={{ margin: 0, fontSize: '0.82rem', color: '#fca5a5', lineHeight: '1.4', fontWeight: 500 }}>
                    {activeData.equipment}
                  </p>
                </div>
              )}

              {(hoveredBody === 'moon' || hoveredBody === 'mars') && (
                <div style={{ 
                  fontSize: '0.75rem', 
                  color: '#38bdf8', 
                  textTransform: 'uppercase', 
                  letterSpacing: '1.5px', 
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}>
                  <span>▶</span> Click to zoom & explore
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* --- PHASE 3 & 4 TRANSLUCENT GLOWING WINDOW PANEL --- */}
      {showPhasePanel && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',

          width: '85vw',
          maxWidth: '1100px',
          height: '65vh',

          zIndex: 30,

          // More transparent glass effect
          background: 'rgba(5, 12, 28, 0.48)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',

          // Glowing cyan border
          border: '1.5px solid rgba(56, 189, 248, 0.85)',
          boxShadow: '0 0 35px rgba(56, 189, 248, 0.25)',

          borderRadius: '16px',
          padding: '30px',
          color: '#ffffff',
          fontFamily: 'system-ui, -apple-system, sans-serif',

          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',

          animation: 'fadeIn 0.5s ease',

        }}>
          {/* Top Bar with Return Button */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(56, 189, 248, 0.2)', paddingBottom: '15px' }}>
            <span style={{ fontSize: '0.85rem', letterSpacing: '2px', color: '#38bdf8', fontWeight: 700, textTransform: 'uppercase' }}>
              // {activePhase === 'phase-3-moon' ? 'LUNAR ARCHIVE' : 'MARTIAN ARCHIVE'}
            </span>
            <button 
              onClick={handleReturnToOrbit}
              style={{
                background: 'rgba(56, 189, 248, 0.1)',
                border: '1px solid #38bdf8',
                color: '#38bdf8',
                padding: '8px 16px',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 600,
                fontSize: '0.85rem',
                transition: 'all 0.2s',
              }}
              onMouseEnter={(e) => e.target.style.background = 'rgba(56, 189, 248, 0.25)'}
              onMouseLeave={(e) => e.target.style.background = 'rgba(56, 189, 248, 0.1)'}
            >
              ← Return to Solar System
            </button>
          </div>

          {/* Split Screen Content Layout */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', flex: 1, margin: '20px 0' }}>
            
            {/* --- MOON PANEL (PHASE 3) --- */}
            {activePhase === 'phase-3-moon' && (
              <>
                {/* Left Side: Apollo 11 */}
                <div 
                  onClick={() => setVideoModalSubject('Apollo 11')}
                  style={{
                    background: 'rgba(15, 23, 42, 0.30)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    padding: '20px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    transition: 'border-color 0.2s',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = '#38bdf8'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'}
                >
                  <div>
                    <h2 style={{ margin: '0 0 10px 0', fontSize: '1.5rem', color: '#38bdf8' }}>Apollo 11</h2>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                      We are going to know its story—the monumental descent that left humankind's first engineered artifacts on a foreign world.
                    </p>
                  </div>
                  {/* Photo Slot Placeholder */}
                  <div style={{ 
                    width: '100%', 
                    height: '140px', 
                    background: 'rgba(0,0,0,0.4)', 
                    border: '1px dashed rgba(56, 189, 248, 0.4)',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#94a3b8',
                    fontSize: '0.85rem'
                  }}>
                    [ Photo Placeholder: Apollo 11 Landing Site ]
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#38bdf8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px' }}>
                    ▶ Click to learn more about the mission
                  </div>
                </div>

                {/* Right Side: Blank for future addition */}
                <div style={{
                  background: 'rgba(15, 23, 42, 0,22)',
                  border: '1px dashed rgba(255, 255, 255, 0.1)',
                  borderRadius: '12px',
                  padding: '20px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#64748b',
                  fontSize: '0.9rem',
                  fontStyle: 'italic'
                }}>
                  [ Reserved for Future Expansion ]
                </div>
              </>
            )}

            {/* --- MARS PANEL (PHASE 4) --- */}
            {activePhase === 'phase-4-mars' && (
              <>
                {/* Left Side: Spirit Rover */}
                <div 
                  onClick={() => setVideoModalSubject('Spirit and Opportunity Rovers')}
                  style={{
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    padding: '20px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = '#38bdf8'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'}
                >
                  <div>
                    <h2 style={{ margin: '0 0 10px 0', fontSize: '1.5rem', color: '#f97316' }}>Spirit and Opportunity Rovers</h2>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                      Twin robotic explorers that traversed the Martian surface, uncovering evidence of past water activity and leaving behind their silent, rusting frames.
                    </p>
                  </div>
                  <div style={{ 
                    width: '100%', 
                    height: '130px', 
                    background: 'rgba(0,0,0,0.4)', 
                    border: '1px dashed rgba(249, 115, 22, 0.4)',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#94a3b8',
                    fontSize: '0.85rem'
                  }}>
                    [ Photo Placeholder: Spirit Rover ]
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#f97316', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px' }}>
                    ▶ Click to learn more about the mission
                  </div>
                </div>

                {/* Right Side: Sojourner */}
                <div 
                  onClick={() => setVideoModalSubject('Sojourner Rover')}
                  style={{
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '12px',
                    padding: '20px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = '#38bdf8'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.1)'}
                >
                  <div>
                    <h2 style={{ margin: '0 0 10px 0', fontSize: '1.5rem', color: '#f97316' }}>Sojourner Rover</h2>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.5' }}>
                      The first successful rover on Mars, paving the way for future exploration and leaving behind a legacy of scientific discovery in the Martian dust.
                    </p>
                  </div>
                  <div style={{ 
                    width: '100%', 
                    height: '130px', 
                    background: 'rgba(0,0,0,0.4)', 
                    border: '1px dashed rgba(249, 115, 22, 0.4)',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#94a3b8',
                    fontSize: '0.85rem'
                  }}>
                    [ Photo Placeholder: sojouner Rover ]
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#f97316', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px' }}>
                    ▶ Click to learn more about the mission
                  </div>
                </div>
              </>
            )}

          </div>

          <div style={{ fontSize: '0.75rem', color: '#64748b', textAlign: 'center' }}>
            NASA Space Apps Challenge — "Abandoned but not Forgotten" Telemetry Active
          </div>
        </div>
      )}

      {/* --- SUB-MODAL FOR FUTURE ANIMATED VIDEO INTEGRATION --- */}
      {videoModalSubject && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          zIndex: 40,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <div style={{
            background: '#0a0f1d',
            border: '1px solid #38bdf8',
            borderRadius: '12px',
            padding: '30px',
            width: '450px',
            textAlign: 'center',
            boxShadow: '0 0 40px rgba(56, 189, 248, 0.3)',
            color: '#fff',
            fontFamily: 'system-ui, sans-serif'
          }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#38bdf8' }}>Video Feed: {videoModalSubject}</h3>
            <p style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '20px' }}>
              Animated video asset placeholder ready for integration. Hook your custom player or React component here later!
            </p>
            <button 
              onClick={() => setVideoModalSubject(null)}
              style={{
                background: '#38bdf8',
                border: 'none',
                color: '#000',
                padding: '10px 20px',
                borderRadius: '6px',
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              Close Window
            </button>
          </div>
        </div>
      )}

      {/* 3D CANVAS */}
      <Canvas camera={{ position: [0, 3.5, 16], fov: 60 }}>
        <directionalLight position={SUN_POSITION} intensity={3.5} color="#fff6e0" />
        <ambientLight intensity={0.15} />

        <TwinklingStars />

        <React.Suspense fallback={null}>
          <SolarSystem 
            onSelectPlanet={handleSelectPlanet} 
            onHover={(body) => setHoveredBody(body)}
            onUnhover={() => setHoveredBody(null)}
            moonGroupRef={moonGroupRef}
            isZoomed={showPhasePanel}
          />
        </React.Suspense>

        <CameraController targetPosition={targetPosition} controlsRef={controlsRef} />
        <OrbitControls ref={controlsRef} enablePan={true} enableZoom={true} maxDistance={40} minDistance={2} />
      </Canvas>
    </div>
  );
}