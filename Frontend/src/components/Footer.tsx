import React from 'react';
import { Twitter, Linkedin, Github, Mail, Phone, MapPin, Instagram } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <motion.footer
      className="bg-deep-black border-t border-electric-blue-900/40 relative overflow-hidden shadow-glow-sm"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.8, delay: 0.2 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 animate-fadeInUp">
          
          {/* Company Info */}
          <div className="col-span-1 md:col-span-2 transform hover:scale-105 transition-transform duration-500">
            <h3 className="text-2xl font-bold text-[#00FF88] mb-4">
              FINBUZZ.AI
            </h3>
            <p className="text-text-muted mb-6 leading-relaxed hover:text-text-secondary transition-colors duration-300">
              The revolutionary financial platform powered by advanced AI.<br />
              making your financial journey effortless and intuitive.
            </p>
          </div>

          {/* Quick Links */}
          <div className="transform hover:scale-105 transition-transform duration-500 animate-fadeInUp" style={{ animationDelay: '0.4s' }}>
            <h4 className="text-lg font-semibold text-text-primary mb-4 hover:text-electric-blue-300 transition-colors duration-300">Quick Links</h4>
            <ul className="space-y-2 animate-fadeInUp" style={{ animationDelay: '0.6s' }}>
              <li>
                <Link to="/features" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 transform hover:translate-x-2">
                  Features
                </Link>
              </li>
              <li>
                <Link to="/how-to-use" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 transform hover:translate-x-2">
                  FINBUZZ.AI Workflow
                </Link>
              </li>
              <li>
                <Link to="/documentation" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 transform hover:translate-x-2">
                  Documentation
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-text-muted hover:text-text-primary hover:text-electric-blue-400 transition-all duration-300 transform hover:translate-x-2">
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div className="transform hover:scale-105 transition-transform duration-500 animate-fadeInUp" style={{ animationDelay: '0.8s' }}>
            <h4 className="text-lg font-semibold text-text-primary mb-4 hover:text-electric-blue-300 transition-colors duration-300">Contact</h4>
            <div className="space-y-3 animate-fadeInUp" style={{ animationDelay: '1s' }}>
              {/* Email link can also be updated if needed */}
            </div>
            {/* Social Media Icons */}
            <div className="flex space-x-4 animate-fadeInUp mt-4" style={{ animationDelay: '1.2s' }}>
              {[
                { icon: Instagram, href: "https://www.instagram.com/finbuzz.ai", label: "Instagram" },
                { icon: Linkedin, href: "https://www.linkedin.com/in/finbuzz-ai", label: "LinkedIn" },
                { icon: Github, href: "https://github.com/github/FINBUZZ.AI", label: "GitHub" },
                { 
                  icon: Mail, 
                  href: "https://mail.google.com/mail/?view=cm&fs=1&to=customercarefinbuzz@gmail.com&su=Inquiry%20from%20FINBUZZ.AI%20Website", 
                  label: "Email",
                  target: "_blank", 
                  rel: "noopener noreferrer" 
                }
              ].map(({ icon: Icon, href, label, target, rel }) => (
                <a
                  key={label}
                  href={href}
                  target={target}
                  rel={rel}
                  className="w-10 h-10 bg-charcoal-900 border border-electric-blue-500/40 rounded-full flex items-center justify-center text-text-muted hover:text-text-primary hover:bg-electric-blue-600 transition-all duration-500 transform hover:scale-125 hover:rotate-12 shadow-glow-sm hover:shadow-electric-blue"
                  aria-label={label}
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-electric-blue-900/40 mt-8 pt-8 flex flex-col md:flex-row justify-center items-center animate-fadeInUp" style={{ animationDelay: '1.4s' }}>
          <div className="text-text-muted text-sm mb-4 md:mb-0 hover:text-text-secondary transition-colors duration-300">
            © 2025 FinBuzz.AI. All rights reserved. | Empowering your financial journey.
          </div>
        </div>
      </div>
      
      {/* Animation styles */}
      <style jsx>{`
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
        
        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease-out forwards;
          opacity: 0;
        }
      `}</style>
    </motion.footer>
  );
};

export default Footer;
