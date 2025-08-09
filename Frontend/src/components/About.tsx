import React from 'react';
import { Award, Users, Globe, Cpu, Handshake, Zap, Headset, Wrench, TrendingDown } from 'lucide-react';
import { motion } from 'framer-motion';

// The original component code is a functional component named 'About'
const About = () => {
  // A map to link string names to the Lucide-React components
  const iconMap = {
    Headset: Headset,
    Wrench: Wrench,
    TrendingDown: TrendingDown,
    Zap: Zap,
  };

  const stats = [
    {
      icon: "Headset",
      number: "24/7",
      label: "Customer Support",
      description: "Seamless 24/7 automated customer service with smooth escalation to human experts",
    },
    {
      icon: "Zap",
      number: "7+",
      label: "Agentic AI Frameworks",
      description: "A powerful, comprehensive AI agent for finance, unifying multiple frameworks."
    },
    {
      icon: "TrendingDown",
      number: "30%",
      label: "Operational Cost Reduction",
      description: "Reduce costs for financial institutions with automated processes and AI efficiency.",
    },
    {
      icon: "Wrench",
      number: "20+",
      label: "AI-Powered Tools",
      description: "AI-powered tools for generating automated insights and strategic recommendations.",
    }
  ];

  // Updated array to include image paths for each team member
  const teamMembers = [
    { name: "Pawan Pahune", role: "Head of AI Innovation & Team Leader", image: "/assets/pawan.png" },
    { name: "Varun Nikam", role: "Head of Product Strategist", image: "/assets/varun.png" },
    { name: "Himanshi Sonkusale", role: "Head of Frontend Architect", image: "/assets/himanshi.png" }
  ];

  return (
    <motion.section
      id="about"
      className="py-20 bg-gradient-to-b from-space-blue-950 to-deep-black relative overflow-hidden"
      initial={{ opacity: 0, x: -50 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* About Content */}
        <div className="text-center mb-16 transform hover:scale-105 transition-transform duration-700">
          <h2 className="text-4xl sm:text-4xl lg:text-5xl font-bold mb-6">
            <span className="text-white">About </span>
            <span className="text-[#00FF88] drop-shadow-[0_0_7px_#00FF88]">FINBUZZ.AI</span>
          </h2>
          <motion.div
            className="max-w-4xl mx-auto space-y-6"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <p className="text-xl text-text-secondary leading-relaxed hover:text-text-primary transition-colors duration-300">
              FINBUZZ.AI is a revolutionary AI-powered agent designed to be your comprehensive financial partner. It's a unified, intelligent platform that combines the roles of a professional financial advisor, investment manager, and personalized query assistant into a single solution. This innovative agent goes beyond simple advice, offering a robust suite of advanced tools and features to manage investments, provide expert guidance, and handle all your financial inquiries with precision. It's the one-stop solution for all your financial needs, empowering you with a sophisticated and trustworthy guide right at your fingertips.
            </p>
            <p className="text-lg text-text-muted leading-relaxed hover:text-text-secondary transition-colors duration-300">
              Our mission is to empower every individual with the tools and insights needed to make informed
              financial decisions, backed by cutting-edge machine learning algorithms and real-time market analysis.
            </p>
          </motion.div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {stats.map((stat, index) => {
            const IconComponent = iconMap[stat.icon];
            return (
              <motion.div
                key={index}
                className="text-center group transform hover:scale-110 transition-transform duration-500"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              >
                <div className="w-16 h-16 bg-gradient-to-r from-orange-500/30 to-red-600/30 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:from-orange-500/50 group-hover:to-red-600/50 transition-all duration-500 group-hover:scale-125 group-hover:rotate-12 shadow-orange group-hover:shadow-red">
                  {IconComponent && <IconComponent className="w-8 h-8 text-orange-400 group-hover:text-orange-300 transition-colors duration-300" />}
                </div>
                <div className="text-3xl font-bold text-text-primary mb-2 group-hover:text-orange-300 transition-colors duration-300">{stat.number}</div>
                <div className="text-lg font-semibold text-text-secondary mb-1 group-hover:text-text-primary transition-colors duration-300">{stat.label}</div>
                <div className="text-sm text-text-muted group-hover:text-text-subtle transition-colors duration-300">{stat.description}</div>
              </motion.div>
            );
          })}
        </div>

        {/* Team Section */}
        <motion.div
          className="bg-gradient-to-br from-space-blue-900/40 via-space-blue-950/60 to-deep-black/80 backdrop-blur-md rounded-2xl border border-orange-500/30 p-8 lg:p-12 transform hover:scale-105 transition-transform duration-700 hover:border-orange-400/50 shadow-glow-lg hover:shadow-glow-xl"
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.2 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          <motion.div
            className="text-center mb-8"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6, delay: 0.7 }}
          >
            <h3 className="text-2xl font-bold text-text-primary mb-4 hover:text-orange-300 transition-colors duration-300">The Minds Behind FINBUZZ.AI</h3>
            <p className="text-text-muted hover:text-text-secondary transition-colors duration-300">Combining financial knowledge with a drive for tech innovation.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {teamMembers.map((member, index) => (
              <motion.div
                key={index}
                className="text-center group transform hover:scale-110 transition-transform duration-500"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.2 }}
                transition={{ duration: 0.6, delay: 0.9 + index * 0.1 }}
              >
                {/* Replaced div with img tag using the provided image paths */}
                <img
                  src={member.image}
                  alt={member.name}
                  className={`w-24 h-24 object-cover rounded-full mx-auto mb-4 border border-charcoal-600/40 group-hover:border-orange-400/60 transition-all duration-500 group-hover:scale-125 shadow-glow-sm group-hover:shadow-orange`}
                />
                <h4 className="text-lg font-semibold text-text-primary group-hover:text-orange-300 transition-colors duration-300">{member.name}</h4>
                <p className="text-text-muted group-hover:text-text-secondary transition-colors duration-300">{member.role}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
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
    </motion.section>
  );
};

export default About;
