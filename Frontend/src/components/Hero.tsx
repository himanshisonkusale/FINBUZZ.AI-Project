import React, { useRef, useEffect, useState } from 'react';
import { TrendingUp, BarChart3, DollarSign, Brain, PieChart } from 'lucide-react';
import * as THREE from 'three';
import { motion } from 'framer-motion';

// Main Hero component for the landing page
const Hero = () => {
  // Ref for the THREE.js container element
  const mountRef = useRef(null);

  // State for the animated stock price
  const [stockPrice, setStockPrice] = useState(150.75);
  const [isPositive, setIsPositive] = useState(true);

  // Animate the stock price
  useEffect(() => {
    const priceInterval = setInterval(() => {
      // Generate a new price based on the current price
      const change = (Math.random() - 0.5) * 5; // Change between -2.5 and +2.5
      let newPrice = stockPrice + change;
      newPrice = Math.max(100, Math.min(200, newPrice)); // Keep price within a reasonable range

      // Update state
      setStockPrice(parseFloat(newPrice.toFixed(2)));
      setIsPositive(change >= 0);
    }, 1500);

    return () => clearInterval(priceInterval);
  }, [stockPrice]);

  // useEffect hook for the THREE.js setup
  useEffect(() => {
    // --- THREE.js Setup ---
    let scene, camera, renderer, grid;
    const currentMount = mountRef.current;

    const init = () => {
      // Scene
      scene = new THREE.Scene();
      scene.background = null; // Transparent background

      // Camera
      camera = new THREE.PerspectiveCamera(75, currentMount.clientWidth / currentMount.clientHeight, 0.1, 1000);
      camera.position.set(0, 5, 20); // Position the camera to look at the grid from a slight angle

      // Renderer
      renderer = new THREE.WebGLRenderer({ antialiasing: true, alpha: true });
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
      currentMount.appendChild(renderer.domElement);

      // Grid
      const size = 100;
      const divisions = 100;
      const colorCenterLine = new THREE.Color(0x00ff88);
      const colorGrid = new THREE.Color(0x007744);
      grid = new THREE.GridHelper(size, divisions, colorCenterLine, colorGrid);
      grid.material.opacity = 0.5;
      grid.material.transparent = true;
      grid.position.y = -5; // Lower the grid slightly
      scene.add(grid);

      // Animation Loop
      const animate = () => {
        requestAnimationFrame(animate);
        // Animate the grid for a dynamic effect
        if (grid) {
          // Increased the rotation speed as requested
          grid.rotation.z += 0.006; // Slightly increased speed from 0.005
          grid.rotation.x += 0.002; // Slightly increased speed from 0.0018
        }

        renderer.render(scene, camera);
      };

      // Handle window resize
      const onWindowResize = () => {
        camera.aspect = currentMount.clientWidth / currentMount.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
      };

      window.addEventListener('resize', onWindowResize);
      animate();

      return () => {
        window.removeEventListener('resize', onWindowResize);
        if (currentMount && renderer.domElement) {
          currentMount.removeChild(renderer.domElement);
        }
      };
    };

    if (currentMount) {
      init();
    }
  }, []);

  // Handler to open the specified URL
  const handleLaunchClick = () => {
    window.open('https://huggingface.co/spaces/Pawan2605/FINBUZZ.AI_CHAT_AGENT', '_blank');
  };

  const handleTradingAgentClick = () => {
    window.open('https://huggingface.co/spaces/Pawan2605/FINBUZZ.AI_TRADING_AGENT', '_blank');
  };

  return (
    <section id="home" className="pt-16 min-h-screen flex items-center relative overflow-hidden bg-deep-black">
      {/* 3D Animated Background */}
      <motion.div
        ref={mountRef}
        className="absolute inset-0 z-0"
        initial={{ opacity: 0, x: -50 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      ></motion.div>

      {/* Smooth transition to black at the top */}
      <div className="absolute top-0 left-0 w-full h-24 bg-gradient-to-b from-black to-transparent z-20"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-30">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Side - Text Content */}
          <motion.div
            className="space-y-8"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="space-y-4">
              <h1 className="text-7xl sm:text-5xl lg:text-6xl font-bold leading-tight animate-fadeInUp transition-colors duration-500">
                <span className="text-white">WELCOME</span>
                <span className="text-[#00FF88] drop-shadow-[0_0_6px_#00FF88]"> FINBUZZ.AI</span>
              </h1>
              <p className="text-xl text-white leading-relaxed animate-fadeInUp text-justify" style={{ animationDelay: '0.2s' }}>
                An AI-powered conversational agent serves as a sophisticated financial partner, expertly managing diverse customer inquiries. It provides personalized financial advisory services, executes complex operations, and offers predictive market analysis by monitoring global news and sentiment. For intricate issues, the agent ensures a seamless handoff to human experts, guaranteeing a superior customer experience.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row justify-center sm:justify-start items-center gap-4 animate-fadeInUp" style={{ animationDelay: '0.6s' }}>
              <button
                className="bg-gradient-to-r from-[#d8480a] to-[#f37c28] text-white px-8 py-3 rounded-xl text-lg font-bold transition-all duration-500 transform hover:scale-105 group relative overflow-hidden shadow-lg hover:shadow-2xl w-full sm:w-auto"
                onClick={handleLaunchClick}
              >
                <span className="relative z-10 group-hover:animate-pulse font-bold">FINBUZZ.AI Chat Agent</span>
                <div className="absolute inset-0 bg-[#ff4500]/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
              <button
                className="bg-gradient-to-r from-[#44c744] to-[#026f31] text-white px-8 py-3 rounded-xl text-lg font-bold transition-all duration-500 transform hover:scale-105 group relative overflow-hidden shadow-lg hover:shadow-2xl w-full sm:w-auto"
                onClick={handleTradingAgentClick}
              >
                <span className="relative z-10 group-hover:animate-pulse font-bold">FINBUZZ.AI Trading Agent</span>
                <div className="absolute inset-0 bg-[#2e8b57]/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>
            </div>
          </motion.div>
          {/* Right Side - New SVG-based animation area */}
          <motion.div
            className="relative hidden h-[450px] items-center justify-center lg:flex"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <div className="relative h-full w-full max-w-[500px]">
              {/* Main 3D Stock Analysis Chart */}
              {/* Changed position from top-1/2 left-1/2 to top-[45%] left-[55%] to move it up and right */}
              <div className="absolute top-[45%] left-[55%] h-[300px] w-[380px] -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-border bg-[#13131b]/50 p-6 shadow-[0_0_80px_-10px_rgba(0,255,136,0.25)] backdrop-blur-md">
                <div className="mb-4 text-center">
                  <h3 className="text-sm font-semibold text-white">AI Stock Analysis</h3>
                  <p className="text-xs text-green-400">Real-time Market Insights</p>
                </div>

                {/* Animated 3D Stock Chart */}
                <div className="relative h-[200px] overflow-hidden rounded-lg bg-black/30">
                  <svg width="100%" height="100%" viewBox="0 0 350 200" className="absolute inset-0">
                    {/* Define a gradient for the area fill */}
                    <defs>
                      <pattern id="grid" width="35" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 35 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="0.5" />
                      </pattern>
                      <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style={{ stopColor: '#00FF88', stopOpacity: 0.3 }} />
                        <stop offset="100%" style={{ stopColor: '#007744', stopOpacity: 0 }} />
                      </linearGradient>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#grid)" />

                    {/* Animated Area Fill under the profit line */}
                    <path
                      d="M 20 160 Q 70 140, 120 100 T 220 80 T 320 60 L 320 200 L 20 200 Z"
                      fill="url(#areaGradient)"
                      className="animate-pulse"
                      style={{ filter: 'drop-shadow(0px 0px 8px rgba(0,255,136,0.5))' }}
                    >
                      <animate
                        attributeName="d"
                        values="M 20 160 Q 70 140, 120 100 T 220 80 T 320 60 L 320 200 L 20 200 Z;
                                M 20 160 Q 70 120, 120 90 T 220 70 T 320 50 L 320 200 L 20 200 Z;
                                M 20 160 Q 70 140, 120 100 T 220 80 T 320 60 L 320 200 L 20 200 Z"
                        dur="3s"
                        repeatCount="indefinite"
                      />
                    </path>

                    {/* Animated Profit Line (Green) */}
                    <path
                      d="M 20 160 Q 70 140, 120 100 T 220 80 T 320 60"
                      stroke="#00ff88"
                      fill="none"
                      strokeWidth="3"
                      strokeLinecap="round"
                      className="animate-pulse"
                    >
                      <animate
                        attributeName="d"
                        values="M 20 160 Q 70 140, 120 100 T 220 80 T 320 60;
                                M 20 160 Q 70 120, 120 90 T 220 70 T 320 50;
                                M 20 160 Q 70 140, 120 100 T 220 80 T 320 60"
                        dur="3s"
                        repeatCount="indefinite"
                      />
                    </path>

                    {/* Animated Loss Line (Red) - now more jagged like a realistic loss line */}
                    <path
                      d="M 20 120 Q 80 180, 140 160 T 240 140 T 320 120"
                      stroke="#ff4d4d"
                      fill="none"
                      strokeWidth="2"
                      strokeLinecap="round"
                    >
                      <animate
                        attributeName="d"
                        values="M 20 120 Q 80 170, 140 150 T 240 130 T 320 110;
                                M 20 120 Q 80 180, 140 160 T 240 140 T 320 120"
                        dur="4s"
                        repeatCount="indefinite"
                      />
                    </path>

                    {/* Moving data points */}
                    <circle r="4" fill="#00ff88" className="animate-bounce">
                      <animateMotion dur="5s" repeatCount="indefinite">
                        <path d="M 20 160 Q 70 140, 120 100 T 220 80 T 320 60" />
                      </animateMotion>
                    </circle>

                    <circle r="3" fill="#ff4d4d">
                      <animateMotion dur="6s" repeatCount="indefinite">
                        <path d="M 20 120 Q 80 180, 140 160 T 240 140 T 320 120" />
                      </animateMotion>
                    </circle>
                  </svg>
                  {/* Stock Price and change indicator */}
                  <div className="absolute top-4 left-4 flex items-baseline space-x-2">
                    <span className="text-4xl font-bold text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.5)]">${stockPrice}</span>
                    <span className={`text-xl font-semibold transition-colors duration-500 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                      {isPositive ? '+' : ''}{(stockPrice - 150.75).toFixed(2)}
                    </span>
                  </div>

                  {/* Live data indicators */}
                  <div className="absolute bottom-2 left-2 text-xs">
                    <div className="flex items-center gap-2 text-green-400">
                      <div className="h-2 w-2 animate-pulse rounded-full bg-green-400"></div>
                      <span>Profit +24.5%</span>
                    </div>
                    <div className="flex items-center gap-2 text-red-400 mt-1">
                      <div className="h-2 w-2 animate-pulse rounded-full bg-red-400"></div>
                      <span>Loss -8.2%</span>
                    </div>
                  </div>
                </div>
              </div>
              {/* Floating Analysis Badges with Movement */}
              {/* Adjusted badge positions to move up and right with the main chart */}
              <div
                className="absolute top-[13%] left-[70%] animate-fade-in-up animate-bounce rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "200ms", animationDuration: "2s" }}
              >
                AI Forecasting
              </div>
              <div
                className="absolute top-[35%] left-[93%] animate-fade-in-up animate-pulse rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "400ms", animationDuration: "3s" }}
              >
                Risk Monitoring
              </div>
              <div
                className="absolute top-[60%] left-[90%] animate-fade-in-up animate-bounce rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "600ms", animationDuration: "2.5s" }}
              >
                Portfolio Analysis
              </div>
              <div
                className="absolute top-[65%] left-[0%] animate-fade-in-up animate-pulse rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "300ms", animationDuration: "3.5s" }}
              >
                Real-time Data
              </div>
              <div
                className="absolute top-[40%] left-[-10%] animate-fade-in-up animate-bounce rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "500ms", animationDuration: "2s" }}
              >
                Market Sentiment
              </div>
              <div
                className="absolute top-[85%] left-[10%] animate-fade-in-up animate-pulse rounded-lg border border-border bg-card-background/60 px-4 py-2 text-sm text-text-secondary backdrop-blur-sm"
                style={{ animationDelay: "700ms", animationDuration: "4s" }}
              >
                AI Insights
              </div>
              <div
                className="absolute bottom-[5%] right-[0%] flex animate-fade-in-up animate-bounce flex-col items-start rounded-lg border border-border bg-card-background/60 px-4 py-2 backdrop-blur-sm"
                style={{ animationDelay: "800ms", animationDuration: "3s" }}
              >
                <span className="text-xs text-text-secondary">
                  Live Performance</span>
                <span className="text-lg font-semibold text-neon-green-500">
                  +15.7%
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
      {/* Smooth transition to black at the bottom */}
      <div className="absolute bottom-0 left-0 w-full h-48 bg-gradient-to-t from-black to-transparent z-20"></div>
      {/* Custom CSS for animations */}
      <style jsx>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInRight {
          from {
            opacity: 0;
            transform: translateX(30px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease-out forwards;
          opacity: 0;
        }

        .animate-fadeInRight {
          animation: fadeInRight 0.8s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </section>
  );
};

export default Hero;
