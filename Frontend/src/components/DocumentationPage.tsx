import React from 'react';
import { HandCoins, FileText, LineChart, Bot } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const DocumentationPage = ({ onExploreClick }) => {
  const navigate = useNavigate();

  const tabs = [
    {
      icon: <HandCoins size={48} />,
      title: "Personalized Financial Advisor",
      description: "This tab provides a platform for personalized financial consultation and strategic planning.",
      color: "text-[#a04ffc]",
    },
    {
      icon: <FileText size={48} />,
      title: "Customer Banking Queries & Automation",
      description: "This section is dedicated to addressing all customer banking inquiries and automating routine tasks.",
      color: "text-[#a04ffc]",
    },
    {
      icon: <LineChart size={48} />,
      title: "Financial Analytics & Investment Tools",
      description: "Here, users can access comprehensive financial analytics and a suite of advanced investment tools.",
      color: "text-[#a04ffc]",
    },
    {
      icon: <Bot size={48} />,
      title: "Agentic AI for Automated Stock Trader & Investor",
      description: "This tab empowers users with an agentic AI designed to autonomously manage stock trading and investment strategies.",
      color: "text-[#a04ffc]",
    },
  ];

  const handleGoBack = () => {
    // This line is changed to explicitly navigate to the root path
    navigate('/'); 
  };

  return (
    <div className="min-h-screen bg-black text-white relative p-4 sm:p-8 font-sans backdrop-filter backdrop-blur-3xl"
        style={{ 
          backgroundImage: 'radial-gradient(ellipse at 50% -20%, rgba(0, 0, 139, 0.3), transparent 80%)',
        }}>
      
      {/* Back button/logo */}
      <button 
        onClick={handleGoBack} 
        className="absolute top-4 left-12 flex items-center gap-2 text-[#00FF88] font-bold text-3xl hover:underline transition-colors"
      >
        <img src="/assets/Logo.png" alt="FINBUZZ.AI Logo" className="w-8 h-8" />
        FINBUZZ.AI
      </button>

      {/* Main Title - Split into two parts for different colors and with simple styling */}
      <motion.h1 
        className="text-3xl sm:text-5xl lg:text-6xl font-bold text-center mb-6 sm:mb-8 tracking-tight pt-16 md:pt-24"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <div className="flex items-center justify-center gap-4">
          
          <span className="text-[#00FF88]">FINBUZZ.AI</span> <span className="text-white">Agent Workflow Documentation</span>
        </div>
      </motion.h1>

      {/* Description - Increased size and made bold */}
      <motion.p 
        className="text-xl sm:text-2xl font-semibold text-center text-gray-300 max-w-3xl mx-auto mb-16"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        The Finbuzz.AI agent provides a comprehensive financial journey through a four-tab workflow. Users can select the tab that aligns with their specific needs to engage with the agent's specialized capabilities.
      </motion.p>

      {/* Grid for the 4 tabs */}
      <div className="w-full max-w-7xl mx-auto grid grid-cols-1 gap-8 sm:gap-12 lg:gap-16">
        {tabs.map((tab, index) => (
          <motion.div 
            key={index}
            className="bg-black/40 py-4 px-8 rounded-2xl border border-gray-700 transition-all duration-300 ease-in-out transform hover:scale-105 hover:shadow-[0_0_20px_rgba(160,79,252,0.5)]"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.5, delay: index * 0.2 + 0.3 }}
          >
            <div className="flex items-center gap-6">
              {/* Icon */}
              <div className={`mb-0 ${tab.color} drop-shadow-[0_0_10px_#a04ffc]`}>
                {tab.icon}
              </div>
              
              {/* Text Content */}
              <div>
                {/* Tab Number and Orange Subheading */}
                <h2 className="text-2xl font-semibold text-orange-500 mb-1 drop-shadow-[0_0_5px_#ff7e25]">
                  Tab {index + 1} : {tab.title}
                </h2>
                
                {/* Description */}
                <p className="text-gray-200 leading-relaxed text-base">
                  {tab.description}
                </p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Explore button */}
      <motion.div 
        className="flex justify-center mt-16 sm:mt-24 mb-4"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.5, delay: 1.1 }}
      >
        <button 
          onClick={onExploreClick}
          className="bg-orange-500 text-white px-14 py-5 rounded-xl text-xl font-bold transition-all duration-300 transform hover:scale-110 shadow-lg drop-shadow-[0_0_10px_#ff7e25] hover:drop-shadow-[0_0_25px_#ff7e25]">
          Explore All Tabs
        </button>
      </motion.div>
      
    </div>
  );
};

export default DocumentationPage;
