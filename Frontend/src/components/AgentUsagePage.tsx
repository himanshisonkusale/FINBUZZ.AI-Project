import React from 'react';
import { motion } from 'framer-motion';
import { HandCoins, FileText, LineChart, Bot } from 'lucide-react';

const AgentUsagePage = ({ onGoBack }) => {
  // Common styles for the tab header boxes
  const tabBoxStyle = "bg-black/40 p-6 rounded-2xl border border-gray-700 transition-all duration-300 ease-in-out transform hover:scale-105 hover:shadow-[0_0_20px_rgba(160,79,252,0.5)] flex items-center gap-6 mb-12";
  
  // Common icon styling
  const iconStyle = "text-[#a04ffc] drop-shadow-[0_0_10px_#a04ffc]";

  // Style for the steps
  const stepBoxStyle = "bg-white/5 backdrop-blur-sm p-6 rounded-xl border border-gray-700 shadow-lg mb-8";
  
  // Base style for images to prevent cropping and maintain aspect ratio
  const imageStyle = "rounded-lg shadow-lg object-contain w-full h-full";
  
  // New style for the image containers to enforce equal sizing
  const imageContainerStyle = "flex items-center justify-center overflow-hidden";
  
  // Handler to open the specified URL
  const handleLaunchClick = () => {
    window.open('https://huggingface.co/spaces/Pawan2605/FINBUZZ', '_blank');
  };

  return (
    <div className="min-h-screen bg-black text-white relative p-4 sm:p-8 font-sans backdrop-filter backdrop-blur-3xl"
        style={{ 
          backgroundImage: 'radial-gradient(ellipse at 50% -20%, rgba(0, 0, 139, 0.3), transparent 80%)',
        }}>

      {/* Back button, renamed to FINBUZZ.AI */}
      <button 
        onClick={onGoBack} 
        className="absolute top-4 left-12 flex items-center gap-2 text-[#00FF88] font-bold text-3xl hover:underline transition-colors"
      >
        <img src="/assets/Logo.png" alt="FINBUZZ.AI Logo" className="w-8 h-8" />
        FINBUZZ.AI
      </button>

      {/* Main Heading moved up */}
      <motion.h1
        className="text-3xl sm:text-5xl lg:text-6xl font-bold text-center mb-6 sm:mb-8 tracking-tight pt-10 md:pt-16"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <span className="text-[#00FF88]">FINBUZZ.AI Agent</span> <span className="text-white">Usage Guide</span>
      </motion.h1>

      {/* Tab 1 Section with new box styling and icon */}
      <motion.div
        className="max-w-6xl mx-auto my-20"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <div className={tabBoxStyle}>
          <HandCoins size={48} className={iconStyle} />
          <h2 className="text-3xl font-bold text-orange-500 mb-0">
            Tab 1 - Using Financial Advisor Agent
          </h2>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-semibold text-xl">Step 1:</span> Navigate to Tab 1 to access the Financial Advisor agent. The agent supports both text-based chat and voice interactions. To activate the automated voice chat feature, simply check the 'Voice Chat Mode' box. This setting is turned off by default for faster performance and computation. As shown in the image below
          </p>
        </div>
        <div className="flex justify-center mb-12">
          <div className={`${imageContainerStyle} w-3/5 h-64`}>
            <img src="/assets/Tab1image1.png" alt="Placeholder image for Step 1" className={imageStyle} />
          </div>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-semibold text-xl">Step 2:</span> Upload a file with your financial data (e.g., .txt, .json, or .pdf). You can also use the provided Submit.json file. Once the file is ready, click the "Process file" button. As shown in the image below
          </p>
        </div>
        <div className="flex justify-center mb-12">
          <div className={`${imageContainerStyle} w-4/5 h-64`}>
            <img src="/assets/Tab1image2.png" alt="Placeholder image for Step 2" className={imageStyle} />
          </div>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-semibold text-xl">Step 3:</span> To initiate a conversation with the agent, you can either type a greeting or, when using the voice option, you must first click the record button to capture your voice and then the process voice button to convert it to a message for the agent. The agent will then present a list of its capabilities, allowing you to instruct it to perform a specific task using one of the available tools. For example: As shown in the image below
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className={`${imageContainerStyle} h-80`}>
            <img src="/assets/Tab1image3.png" alt="Placeholder example 1" className={imageStyle} />
          </div>
          <div className={`${imageContainerStyle} h-80`}>
            <img src="/assets/Tab1image4.png" alt="Placeholder example 2" className={imageStyle} />
          </div>
          <div className={`${imageContainerStyle} h-80`}>
            <img src="/assets/Tab1image5.png" alt="Placeholder example 3" className={imageStyle} />
          </div>
        </div>
      </motion.div>

      {/* Tab 2 Section with new box styling and icon */}
      <motion.div
        className="max-w-6xl mx-auto my-20"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        <div className={tabBoxStyle}>
          <FileText size={48} className={iconStyle} />
          <h2 className="text-3xl font-bold text-orange-500 mb-0">
            Tab 2 - Customer Queries and Automation Agent
          </h2>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-semibold text-xl">Step 1:</span> Navigate to Tab 2 to access the Customer Queries and Automation Agent. The agent supports both text-based chat and voice interactions. To activate the automated voice chat feature, simply check the 'Voice Chat Mode' box. This setting is turned off by default for faster performance and computation.
          </p>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-semibold text-xl">Step 2:</span> Upload a file with your financial data (e.g., .txt, .json, or .pdf). You can also use the provided Submit.json file. Once the file is ready, click the "Process file" button.
          </p>
        </div>

        <div className={stepBoxStyle}>
          <p className="font-semibold text-xl">
            Step 3: Activating the Agents
          </p>
          <p className="mt-4 text-lg">
            Begin by asking the agent what services it can provide. It will then list its capabilities. You can then select a service and initiate an automated workflow. The Customer Queries and Automation agent offers several features to try:
          </p>
          <ul className="list-disc list-inside space-y-2 mt-4 text-lg">
            <li>
              <span className="font-bold">Financial Literacy Agent:</span> This agent can define and explain any terms related to the banking sector that you need to understand.
            </li>
            <li>
              <span className="font-bold">Fraud Detection Agent:</span> This agent can access recent transaction data from its secure database. You can instruct it to "load fraud transactions," which will then give you the option to report them to the bank's servers and generate a copy of an official report (FIR). The agent will automate the entire process; you only need to confirm.
            </li>
          </ul>
        </div>
        
        <p className="mb-4 font-bold text-lg">Full automation example:</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className={`${imageContainerStyle} h-64`}>
              <img
                src={`/assets/Tab2image${i + 1}.png`}
                alt={`Tab 2 example ${i + 1}`}
                className={imageStyle}
              />
            </div>
          ))}
        </div>
        <div className="flex justify-center mb-12">
          <div className={`${imageContainerStyle} h-64`}>
            <img src="/assets/Tab2image7.png" alt="Automation example 7" className={imageStyle} />
          </div>
        </div>
        
        <div className={stepBoxStyle}>
          <p className="text-lg">
            <span className="font-bold">Crisis Mode:</span> In a crisis or serious emergency, you can activate this mode by simply typing "crisis." The agent is trained to recognize the urgency and will immediately present critical options like reporting fraud, a medical emergency, or theft, allowing you to proceed with the necessary automation. For security reasons, the full workflow is not shown, but the agent ensures that the information is securely and urgently sent to the cyber police department. Similarly, other agents are available for tasks such as scheduling meetings, understanding new bank schemes, and more. Check images for clarification .
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <div className={`${imageContainerStyle} h-64`}>
            <img src="/assets/Tab2image8.png" alt="Placeholder image for agent" className={imageStyle} />
          </div>
          <div className={`${imageContainerStyle} h-64`}>
            <img src="/assets/Tab2image9.png" alt="Placeholder image for agent" className={imageStyle} />
          </div>
        </div>
      </motion.div>

      {/* Tab 3 Section with new box styling and icon */}
      <motion.div
        className="max-w-6xl mx-auto my-20"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.5, delay: 0.7 }}
      >
        <div className={tabBoxStyle}>
          <LineChart size={48} className={iconStyle} />
          <h2 className="text-3xl font-bold text-orange-500 mb-0">
            Tab 3 - Financial Analytics and Investment Tools
          </h2>
        </div>
        <div className={stepBoxStyle}>
          <p className="text-lg">
            While the full suite of tools within the Financial Analytics and Investment Tools tab is still in development, you can see the implementation of two of the most useful and widely-used tools, including the <span className="font-bold">Stock Sentiment Analysis and Forecasting Tool</span>, in the image below.
          </p>
        </div>
        <div className="mb-12">
          <div className="flex justify-center gap-6 mb-6">
            <div className={`${imageContainerStyle} h-80`}>
              <img
                src="/assets/Tab3image1.png"
                alt="Tab 3 image 1"
                className={imageStyle}
              />
            </div>
            <div className={`${imageContainerStyle} h-80`}>
              <img
                src="/assets/Tab3image2.png"
                alt="Tab 3 image 2"
                className={imageStyle}
              />
            </div>
          </div>
          <div className="flex justify-center">
            <div className={`${imageContainerStyle} h-80`}>
              <img
                src="/assets/Tab3image3.png"
                alt="Tab 3 image 3"
                className={imageStyle}
              />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Tab 4 Section with new box styling and icon */}
      <motion.div
        className="max-w-6xl mx-auto my-20"
        initial={{ opacity: 0, y: 50 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.2 }}
        transition={{ duration: 0.5, delay: 0.9 }}
      >
        <div className={tabBoxStyle}>
          <Bot size={48} className={iconStyle} />
          <h2 className="text-3xl font-bold text-orange-500 mb-0">
            Tab 4 - Automated Stock Trading & Investing Agent
          </h2>
        </div>
        <div className={stepBoxStyle}>
          <p className="text-lg">
            As this is a prototype, the AI automated stock trading agent is currently in development and will be launching soon.
          </p>
        </div>
      </motion.div>

      {/* New button to launch FINBUZZ.AI */}
      <div className="flex justify-center mt-12 mb-12">
        <button
          className="bg-gradient-to-r from-[#e45619] to-[#dd6c1c] text-white px-16 py-5 rounded-2xl text-2xl font-bold transition-all duration-500 transform hover:scale-110 group relative overflow-hidden shadow-lg hover:shadow-2xl"
          onClick={handleLaunchClick}
        >
          <span className="relative z-10 group-hover:animate-pulse font-bold">LAUNCH FINBUZZ.AI</span>
          <div className="absolute inset-0 bg-[#dd6c1c]/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </button>
      </div>

      {/* Footer bar */}
      <footer className="bg-black/50 text-white text-center py-4 mt-12 rounded-lg">
        <p className="text-sm">© 2025 FinBuzz.AI. All rights reserved. | Empowering your financial journey.</p>
      </footer>

    </div>
  );
};

export default AgentUsagePage;
