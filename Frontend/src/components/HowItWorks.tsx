"use client"

import React from 'react';
import { UserPlus, Brain, TrendingUp, Target, Cloud, Database, BarChart2, Lightbulb } from 'lucide-react';
import { motion, useAnimation } from 'framer-motion';

// Define custom CSS variables and keyframes for the theme
const customStyles = `
  :root {
    --neon-green: #00ff88;
    --neon-purple: #8b5cf6;
    --glow-blue: #3b82f6;
    --background: #0d0d0d;
    --container-background: #1a1a1a;
  }
  
  body {
    background-color: var(--background);
    color: white;
    font-family: 'Inter', sans-serif;
  }
  
  /* Keyframe for a pulsing border glow effect */
  @keyframes border-pulse-orange {
    0%, 100% { box-shadow: 0 0 5px #f97316, inset 0 0 5px #f97316; }
    50% { box-shadow: 0 0 15px #f97316, inset 0 0 15px #f97316; }
  }
  
  @keyframes border-pulse-purple {
    0%, 100% { box-shadow: 0 0 5px #a855f7, inset 0 0 5px #a855f7; }
    50% { box-shadow: 0 0 15px #a855f7, inset 0 0 15px #a855f7; }
  }
  
  /* Animation styles for the original component */
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
  
  @keyframes fadeInLeft {
    from {
      opacity: 0;
      transform: translateX(-30px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
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
  
  .animate-fadeInLeft {
    animation: fadeInLeft 0.8s ease-out forwards;
    opacity: 0;
  }
  
  .animate-fadeInRight {
    animation: fadeInRight 0.8s ease-out forwards;
    opacity: 0;
  }
`;

const HowItWorks = () => {
  // We'll use the existing steps array for both the left-side text and the right-side visualization.
  const steps = [
    {
      number: "01",
      icon: UserPlus,
      title: "Get Started",
      description: "Click the Get Started button to begin your journey. Our step-by-step guide will walk you through our tools and show you how to leverage our agent's full capabilities."
    },
    {
      number: "02",
      icon: Brain,
      title: "Click FINBUZZ.AI Chat / Trading Agent",
      description: "Instantly access the conversational or trading agent by selecting the \"FINBUZZ.AI Chat / Trading Agent\" button."
    },
    {
      number: "03",
      icon: TrendingUp,
      title: "Integrate Your Data",
      description: "Securely upload your financial data in formats like JSON, PDF, or TXT for personalized analysis and insights."
    },
    {
      number: "04",
      icon: Target,
      title: "Gain Actionable Insights",
      description: "Utilize a suite of tools to address various needs, from handling routine customer queries to conducting in-depth financial analysis and receiving personalized advice."
    }
  ];

  const rotatingItems = [
    { icon: UserPlus, title: "Get Started", color: "text-orange-300" },
    { icon: Cloud, title: "Upload Data", color: "text-orange-300" },
    { icon: BarChart2, title: "Analyze", color: "text-orange-300" },
    { icon: Lightbulb, title: "Insights", color: "text-orange-300" },
  ];

  return (
    <>
      <style>{customStyles}</style>
      <section id="how-it-works" className="py-20 bg-gradient-to-b from-deep-black to-space-blue-950 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            {/* Left Side - Steps */}
            <motion.div
              className="space-y-8 animate-fadeInLeft"
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.8 }}
            >
              <div className="text-center lg:text-left transform hover:scale-105 transition-transform duration-700">
                <motion.h2
                  className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{ duration: 0.6 }}
                >
                  <span className="text-white">How </span>
                  <span className="text-[#00FF88] drop-shadow-[0_0_7px_#00FF88]">FINBUZZ.AI</span>
                  <span className="text-white"> Works</span>
                </motion.h2>

                <motion.p
                  className="text-xl text-text-muted animate-fadeInUp hover:text-text-secondary transition-colors duration-300"
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.2 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  Initiate Your AI Financial Transformation in Four Simple Stages.
                </motion.p>
              </div>

              <div className="space-y-10">
                {steps.map((step, index) => (
                  <motion.div
                    key={index}
                    className="flex space-x-6 group animate-fadeInUp transform hover:scale-105 transition-transform duration-500"
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.2 }}
                    transition={{ duration: 0.6, delay: index * 0.2 + 0.4 }}
                  >
                    <div className="flex-shrink-0">
                      <div className="w-16 h-16 bg-gradient-to-r from-orange-500/30 to-red-600/30 rounded-full flex items-center justify-center border border-orange-500/40 group-hover:border-orange-400/70 transition-all duration-500 group-hover:scale-110 group-hover:rotate-12 shadow-orange group-hover:shadow-red">
                        <step.icon className="w-8 h-8 text-orange-400 group-hover:text-orange-300 transition-colors duration-300" />
                      </div>
                    </div>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center space-x-3">
                        <span className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-500 bg-clip-text text-transparent group-hover:scale-110">
                          {step.number}
                        </span>
                        <h3 className="text-2xl font-semibold text-text-primary group-hover:text-orange-300 transition-colors duration-300">{step.title}</h3>
                      </div>
                      <p className="text-text-muted leading-relaxed group-hover:text-text-secondary transition-colors duration-300">{step.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
            
            {/* Right Side - Interactive Visualization (updated) */}
            <motion.div
              className="relative h-96 flex items-center justify-center lg:ml-12 animate-fadeInRight"
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md rounded-3xl border border-orange-500/30 transform hover:scale-105 transition-transform duration-700 hover:border-orange-400/50 shadow-glow-lg hover:shadow-glow-xl" />
              
              {/* Central AI Core */}
              <motion.div
                className="relative z-10 w-32 h-32 bg-charcoal-900/80 rounded-full flex items-center justify-center border border-orange-400/60 backdrop-blur-sm shadow-orange"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 3, ease: "easeInOut", repeat: Infinity }}
              >
                <Brain className="w-16 h-16 text-orange-400 animate-pulse-glow" />
                <div className="absolute w-24 h-24 border border-dashed border-orange-600/30 rounded-full animate-spin-slow" />
              </motion.div>
              
              {/* Top 3 boxes - aligned horizontally */}
              <motion.div
                className="absolute w-32 h-16"
                style={{ top: '10%', left: '10%', transform: 'translate(-50%, -50%)' }}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <UserPlus className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Get Started
                  </div>
                </div>
              </motion.div>
              <motion.div
                className="absolute w-32 h-16"
                style={{ top: '10%', left: '40%', transform: 'translate(-50%, -50%)' }}
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <Lightbulb className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Launch Agent
                  </div>
                </div>
              </motion.div>
              <motion.div
                className="absolute w-32 h-16"
                style={{ top: '10%', left: '70%', transform: 'translate(-50%, -50%)' }}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.6, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <Database className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Integrate Data
                  </div>
                </div>
              </motion.div>
              
              {/* Bottom 3 boxes - aligned horizontally */}
              <motion.div
                className="absolute w-32 h-16"
                style={{ bottom: '10%', left: '10%', transform: 'translate(-50%, 50%)' }}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 2.0, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <TrendingUp className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Gain Insights
                  </div>
                </div>
              </motion.div>
              <motion.div
                className="absolute w-32 h-16"
                style={{ bottom: '10%', left: '40%', transform: 'translate(-50%, 50%)' }}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2.4, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <Target className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Invest smartly
                  </div>
                </div>
              </motion.div>
              <motion.div
                className="absolute w-32 h-16"
                style={{ bottom: '10%', left: '70%', transform: 'translate(-50%, 50%)' }}
                initial={{ opacity: 0, x: 50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 2.8, duration: 0.6 }}
              >
                <div className="bg-gray-800/70 p-2 rounded-lg shadow-lg border border-gray-600/50 hover:scale-110 transition-transform duration-300">
                  <div className="text-xs text-center text-orange-300">
                    <Cloud className="w-6 h-6 mx-auto mb-1 text-orange-300" />
                    Connect Data
                  </div>
                </div>
              </motion.div>
              
            </motion.div>
          </div>
        </div>
      </section>
    </>
  );
};

export default HowItWorks;
