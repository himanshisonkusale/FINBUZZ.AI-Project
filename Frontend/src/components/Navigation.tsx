import React, { useState } from 'react';
import { Menu, X, ChevronDown, Globe } from 'lucide-react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLangOpen, setIsLangOpen] = useState(false);
  const navigate = useNavigate(); // Initialize the hook

  const handleGetStartedClick = () => {
    navigate('/documentation'); // Navigate to the documentation page
  };

  return (
    <nav className="fixed top-0 w-full z-50 bg-gradient-to-b from-blackto-black backdrop-blur-lg border-b border-slate-950/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and App Name */}
          <div className="flex-shrink-0 flex items-center gap-2">
            <img src="/assets/Logo.png" alt="FINBUZZ.AI Logo" className="w-8 h-8" />
            <h1 className="text-3xl font-bold text-[#00FF88] hover:animate-pulse-glow transition-all duration-300">
              FINBUZZ.AI
            </h1>
          </div>

          {/* Desktop Menu and CTA - Combined into one container */}
          <div className="hidden md:flex ml-auto items-center space-x-6">
            <a href="#features" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 hover:shadow-electric-blue">Features</a>
            <a href="#how-it-works" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 hover:shadow-electric-blue">How FINBUZZ.AI Works</a>
            <a href="#about" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 hover:shadow-electric-blue">About</a>
            {/* The desktop button now has the same styling as the mobile button */}
            <button 
              onClick={handleGetStartedClick} // Add onClick handler
              className="bg-gradient-to-r from-[#e45619] to-[#dd6c1c] text-text-primary px-6 py-2 rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-neon-green">
              Get Started
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-deep-black/95 backdrop-blur-md border-t border-electric-blue-900/30 shadow-glow-sm">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <a href="#features" className="block px-3 py-2 text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300">Features</a>
            <a href="#how-it-works" className="block px-3 py-2 text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300">How It Works</a>
            <a href="#about" className="block px-3 py-2 text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300">About</a>
            <div className="px-3 py-2">
              {/* The mobile button retains its original styling */}
              <button 
                onClick={handleGetStartedClick} // Add onClick handler
                className="w-full bg-gradient-to-r from-[#4c2ffc] to-[#a04ffc] text-text-primary px-6 py-2 rounded-2xl transition-all duration-300 shadow-neon-green">
                Get Started
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;
